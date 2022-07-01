import paddlehub as hub
import cv2
import numpy as np
from PIL import Image
import pycapt


def handle_img(img, threshold=160, save_path='code_binary.jpg'):
    gray = Image.open(img).convert('L')

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img = gray.point(table, '1')
    img.save(save_path)


module_name = "chinese_ocr_db_crnn_server"
ocr_model = hub.Module(name=module_name)

def test1():
    handle_img('code.jpg', threshold=200)

    img = cv2.imread('code_binary.jpg')

    res = ocr_model.recognize_text(images=[img])
    print(res)

def test2():
    # img = Image.open('./img/frcc0.png')
    # img = pycapt.two_value(img, Threshold=100)

    # handle_img('code2.png', threshold=200, save_path='code_binary2.jpg')

    img = cv2.imread('code2.png')

    res = ocr_model.recognize_text(images=[img])
    print(res)

test2()