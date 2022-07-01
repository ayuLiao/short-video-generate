import requests
import os


root_path = os.path.abspath(os.path.dirname(__file__))
face_dir_path = os.path.join(root_path, 'statics', 'images', 'face')

for i in range(60):
    k = str(10000 + i + 1)
    file_name = k + '.jpg'
    url = f'https://www.goodsunlc.com/status/screenshots/images/face/{file_name}'
    r = requests.get(url)
    with open(os.path.join(face_dir_path, file_name), 'wb') as f:
        f.write(r.content)

print('done!')