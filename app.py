from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf

IMG_WIDTH, IMG_HEIGHT = 299, 299

app = Flask(__name__)

# Load the model and other necessary imports
model = tf.keras.models.load_model('Xception.h5')  # Use the relative path if the model is in the same directory

# Function to preprocess the frame for prediction
def preprocess_frame(frame, img_width, img_height):
    resized_frame = cv2.resize(frame, (img_width, img_height))
    preprocessed_frame = np.expand_dims(resized_frame, axis=0)
    preprocessed_frame = preprocessed_frame / 255.0
    return preprocessed_frame

@app.route('/process_recorded_video', methods=['POST'])
def process_recorded_video():
    try:
        # Get the video file from the form data
        recorded_video = request.files['recorded_video']

        # Convert the video file data to OpenCV format
        video_data = np.frombuffer(recorded_video.read(), dtype=np.uint8)  # Use np.frombuffer to convert bytes to array
        cap = cv2.VideoCapture()
        cap.open(video_data)  # Open the video from the array data

        # Variables to keep track of correct, partially correct, and incorrect frames
        total_frames = 0
        correct_frames = 0
        partially_correct_frames = 0
        incorrect_frames = 0

        # Process the video frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Preprocess and predict
            preprocessed_frame = preprocess_frame(frame, IMG_WIDTH, IMG_HEIGHT)
            predictions = model.predict(preprocessed_frame)
            predicted_class = np.argmax(predictions, axis=1)[0]  # Get the predicted class for the frame

            # Update counters based on the predicted class
            total_frames += 1
            if predicted_class == 0:  # Correct class index
                correct_frames += 1
            elif predicted_class == 3:  # Partially Correct class index
                partially_correct_frames += 1
            elif predicted_class == 1:  # Incorrect class index
                incorrect_frames += 1

        # Calculate scores and return response
        step = 100 / total_frames
        score1 = step * correct_frames
        score2 = step / 2 * partially_correct_frames
        total_score = score1 + score2

        # Close the video capture
        cap.release()

        return jsonify({
            "total_frames": total_frames,
            "correct_frames": correct_frames,
            "partially_correct_frames": partially_correct_frames,
            "incorrect_frames": incorrect_frames,
            "total_score": total_score
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
