from flask import render_template, redirect, url_for, request, session
from flask_babel import refresh
from time import time
from os import urandom
from server.babel import get_locale, get_languages


class Website:
    def __init__(self,bp,url_prefix) -> None:
        self.bp = bp
        self.url_prefix = url_prefix
        self.routes = {
            '/':{
                'function':lambda:redirect(url_for('._index')),
                'methods':['GET','POST']
            },
            '/home':{
                'function':self._index,
                'methods':['GET','POST']
            },
            '/practice':{
                'function':self._practice,
                'methods':['GET','POST']
            },
            '/test':{
                'function':self._test,
                'methods':['GET','POST']
            },
            '/change-language': {
                'function': self.change_language,
                'methods': ['POST']
            },
            '/get-locale': {
                'function': self.get_locale,
                'methods': ['GET']
            },
            '/get-languages': {
                'function': self.get_languages,
                'methods': ['GET']
            }
        }

    def _practice(self):
        return render_template('practice.html', chat_id=f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}', url_prefix=self.url_prefix)

    def _index(self):
        return render_template('index.html', chat_id=f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}', url_prefix=self.url_prefix)

    def _test(self):
        return render_template('test.html')
    def change_language(self):
        data = request.get_json()
        session['language'] = data.get('language')
        refresh()
        return '', 204

    def get_locale(self):
        return get_locale()
    
    def get_languages(self):  
        return get_languages()