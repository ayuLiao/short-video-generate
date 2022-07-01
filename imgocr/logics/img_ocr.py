import os
import gc
import cv2
import time
import numpy as np
from PIL import Image
import paddlehub as hub

from utils import get_session
from logger import logger
from configs.configs import images_path

OCR_MODEL_USER_TIMES = 0
OCRModel = None


def get_ocr_model():
    """手动GC，控制model使用内存"""

    global OCR_MODEL_USER_TIMES
    global OCRModel
    module_name = "chinese_ocr_db_crnn_server"
    # 使用10次，就释放模型
    if OCR_MODEL_USER_TIMES < 10:
        if not OCRModel:
            OCRModel = hub.Module(name=module_name)
        OCR_MODEL_USER_TIMES += 1
    else:
        del OCRModel
        gc.collect()
        OCRModel = hub.Module(name=module_name)
        OCR_MODEL_USER_TIMES = 0
    return OCRModel


def save_img(img_name, content):
    img_path = os.path.join(images_path, img_name)
    with open(img_path, 'wb') as f:
        f.write(content)


def download_img(url):
    """下载远程图片"""

    session = get_session()
    img = None
    for i in range(3):
        img = session.get(url)
        if img.status_code == 200:
            break
    if not img:
        logger.error(f"远程图片下载失败, url: {url}")
        return None
    img_name = url.split('/')[-1]
    save_img(img_name, img.content)
    return img_name


def binary_img(images: list):
    """二值化图像元素"""
    imgs = []
    for img in images:
        # img = cv2.imread(images)
        # 灰度图
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 输入灰度图，输出二值图
        ret, binary = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)
        # 取反
        binary = cv2.bitwise_not(binary)
        imgs.append(binary)
    return imgs


def handle_img(img_name, threshold=160, save_name='code_binary.jpg'):
    img_path = os.path.join(images_path, img_name)
    gray = Image.open(img_path).convert('L')

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img = gray.point(table, '1')
    path = os.path.join(images_path, save_name)
    img.save(path)
    return save_name


def ocr_img(images: list, remote=False):
    """
    识别多张图片，如果remote=True，则下载远程图片，如果remote=False，则直接将图片对象传入
    :param images: 图片列表
    :param remote: 释放远程
    :return:
    """
    try:
        result = []
        for i in range(0, len(images), 5):
            _img_paths = images[i: 1 + 5]
            ocr_model = get_ocr_model()
            img_paths = []
            if remote:
                for url in _img_paths:
                    img_name = download_img(url)
                    if not img_name:
                        continue
                    img_paths.append(img_name)
            else:
                for img in images:
                    img_name = str(int(time.time())) + '.jpg'
                    save_img(img_name, img)
                    img_paths.append(img_name)
            imgs = []
            for img in img_paths:
                img_name = handle_img(img)
                img = cv2.imread(os.path.join(images_path, img_name))
                imgs.append(img)
            result.extend(ocr_model.recognize_text(images=imgs))


            # if remote:
            #     imgs = []
            #     for url in _img_paths:
            #         img = download_img(url)
            #         if img:
            #             img = cv2.imdecode(np.fromstring(img.content, np.uint8), 1)
            #             imgs.append(img)
            # else:
            #     imgs = [cv2.imdecode(np.fromstring(img, np.uint8), 1) for img in images]
            # imgs = binary_img(imgs)
            # result.extend(ocr_model.recognize_text(images=imgs))
        return result
    except Exception as e:
        logger.error(f"OCR Model处理失败, error: {e}", exc_info=True)
        return []
