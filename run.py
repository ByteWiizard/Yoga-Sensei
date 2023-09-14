import secrets
from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel
from json import load
from flask import Flask
import cv2
import numpy as np
import tensorflow as tf


if __name__ == '__main__':

    config = load(open('config.json','r'))
    site_config = config['site_config']
    url_prefix = config.pop('url_prefix')

    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    create_babel(app)

    site = Website(bp,url_prefix)
    for route in site.routes:
        bp.add_url_rule(
            route,
            view_func = site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    



    app.register_blueprint(bp,url_prefix=url_prefix)

    print(f"Running on {site_config['port']}{url_prefix}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")