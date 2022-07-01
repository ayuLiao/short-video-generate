import requests


def test_ocr_img_file():
    headers = {
        'accept': 'application/json',
    }
    files = {
        'img': open('code.jpg', 'rb')
    }

    response = requests.post('http://127.0.0.1:8889/ocr/img/', headers=headers, files=files)
    print(response.json())


def test_ocr_img_url():
    headers = {"Content-type": "application/json"}

    img_url = 'https://files.mdnice.com/user/4437/e2c791e3-a3d5-4d5b-9fb3-d6fe4a0d15d9.png'
    r = requests.post(url='http://127.0.0.1:8889/ocr/img/', headers=headers, json={'url': img_url})

    print(r.json())


test_ocr_img_url()
test_ocr_img_file()
