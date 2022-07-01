import os
import shutil


root_path = os.path.abspath(os.path.dirname(__file__))

face_dir_path = os.path.join(root_path, 'statics', 'images', 'face')
new_face_dir_path = os.path.join(root_path, 'statics', 'images', 'new_face')
if not os.path.exists(new_face_dir_path):
    os.makedirs(new_face_dir_path)

i = 1
for face_file_name in os.listdir(face_dir_path):
    face_file_path = os.path.join(face_dir_path, face_file_name)
    k = str(10000 + i)
    new_face_file_name = k + '.jpg'
    new_face_file_path = os.path.join(new_face_dir_path, new_face_file_name)
    if face_file_name.split('.')[0] != k:
        os.rename(face_file_path, new_face_file_path)
    else:
        shutil.move(face_file_path, new_face_file_path)
    i += 1

print('clean done!')
