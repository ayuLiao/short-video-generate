import json
import os
import requests

root_path = os.path.abspath(os.path.dirname(__file__))

DIRPATH = r"C:\Users\admin\workplace\short-video-generate\BaiduImageSpider\搞笑聊天 对话"


def ocr_img_file(img_path):
    headers = {
        'accept': 'application/json',
    }
    files = {
        'img': open(img_path, 'rb')
    }

    response = requests.post('http://127.0.0.1:8889/ocr/img/', headers=headers, files=files)
    return response.json()

def main():
    dirname = os.path.split(DIRPATH)[-1]
    json_dir_path = os.path.join(root_path, 'ocr_result', dirname)
    if not os.path.exists(json_dir_path):
        os.makedirs(json_dir_path)

    for img_name in os.listdir(DIRPATH):
        img_path = os.path.join(DIRPATH, img_name)
        ocr_result_json = ocr_img_file(img_path)
        ocr_name = img_name.split('.')[0] + '.json'
        save_path = os.path.join(json_dir_path, ocr_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(ocr_result_json, ensure_ascii=False, indent=4))
        print(f'OCR Done! Path: {save_path}')
        

main()