from flask import request, jsonify
from flask_restplus import abort, Resource
from apis import *

from logics import img_ocr


class ImgOCROne(Resource):

    @staticmethod
    @api.doc(params={'url': '图片URL', 'img': '图片数据流-请使用requests files传递'})
    def post():
        img_url = get_params('url')
        img = get_files('img')
        result = []
        if img_url:
            result = img_ocr.ocr_img(images=[img_url, ], remote=True)
        elif img:
            img = img.stream.read()
            result = img_ocr.ocr_img(images=[img, ], remote=False)
        else:
            abort(code=400, message="url与img必须传一个")

        data = []
        for res in result:
            data.append(res['data'])

        response = {
            'code': 0,
            'message': 'success',
            'data': data
        }

        return jsonify(response)


ns = api.namespace("ocr", description="OCR相关操作")
ns.add_resource(ImgOCROne, "/img/")
