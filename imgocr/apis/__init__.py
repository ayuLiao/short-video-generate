from flask import Flask, request
from flask_restplus import Api


def create_app():
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False

    api = Api(
        app,
        version='1.0.0',
        title='IMGOCR apis',
        description='img ocr apis',
        authorizations={
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Token'
            }
        },
        security='apikey',
        ui=True,
        validate=True)

    return app, api


def get_params(key):
    if request.json:
        return request.json.get(key)
    return None


def get_files(key):
    if request.files:
        return request.files.get(key)
    return None


app, api = create_app()

from .img_ocr import *
