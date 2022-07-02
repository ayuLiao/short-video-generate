import os
import json
import random
import time
from base64 import b64decode
import cv2
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# ocr 目录路径
ocr_dir_path = r'C:\Users\admin\workplace\short-video-generate\BaiduImageSpider\ocr_result\funny_chat'
# 清理后的ocr结果
clean_ocr_dir_path = r'C:\Users\admin\workplace\short-video-generate\gen_video\clean_ocr'
# 生成聊天图片的目录
gen_image_dir_path = r'C:\Users\admin\workplace\short-video-generate\gen_video\wechat_images'
# 生成视频的目录
gen_video_dir_path = r'C:\Users\admin\workplace\short-video-generate\gen_video\wechat_videos'
gen_video_dir_path2 = r'C:\Users\admin\workplace\short-video-generate\gen_video\wechat_videos2'
# 提取音频的目录
sound_dir_path = r'C:\Users\admin\workplace\short-video-generate\gen_video\video_sounds'

def get_browser():
    url = 'http://127.0.0.1:5000/'
    root_path = os.path.abspath(os.path.dirname(__file__))
    chrome_driver_path = os.path.join(root_path, 'chromedriver.exe')
    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.get(url)
    return browser


def create_dirs(dir_paths):
    for dir_path in dir_paths:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


def get_ocr_json(ocr_path):
    for ocr_file_name in os.listdir(ocr_path):
        ocr_file_path = os.path.join(ocr_path, ocr_file_name)

        with open(ocr_file_path, 'r', encoding='utf-8') as f:
            ocr_json = f.read()

        ocr_json = json.loads(ocr_json)
        ocr_data_list = ocr_json.get('data', [])

        if ocr_data_list:
            ocr_data_list = ocr_data_list[0]
        last_text_box_first_position = 0
        sentences = []

        for ocr_item in ocr_data_list:
            text_box_position = ocr_item.get('text_box_position', [])
            text = ocr_item.get('text', '')

            if not text:
                continue

            if not text_box_position:
                continue

            text_box_first_position_x = text_box_position[0][0]
            text_box_first_position_y = text_box_position[0][1]

            # 很可能是聊天标题
            if text_box_first_position_y < 30:
                continue

            # y轴距离相差小，同一句话
            if last_text_box_first_position and abs(last_text_box_first_position - text_box_first_position_y) < 50:
                item = sentences[-1]
                item['text'] += text
            else:
                if text_box_first_position_x < 150:
                    sentences.append({
                        'postion': 'left',
                        'text': text
                    })
                else:
                    sentences.append({
                        'postion': 'right',
                        'text': text
                    })

            last_text_box_first_position = text_box_first_position_y

        sentences_str = json.dumps(sentences, ensure_ascii=False, indent=4)
        with open(os.path.join(clean_ocr_dir_path, ocr_file_name), 'w', encoding='utf-8') as f:
            f.write(sentences_str)


def wait_element_xpath(browser, xpath, wait_time=15):
    try:
        WebDriverWait(browser, wait_time, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f'[wait_element_css] 等待超时, error: {e}')
        raise


def gen_wechat_image(browser):
    for ocr_file_name in os.listdir(clean_ocr_dir_path):
        ocr_file_path = os.path.join(clean_ocr_dir_path, ocr_file_name)
        with open(ocr_file_path, 'r', encoding='utf-8') as f:
            ocr_json = f.read()
        ocr_json_list = json.loads(ocr_json)
        print(ocr_file_path)
        print(ocr_json)
        ocr_file_gen_image_save_dir_path = os.path.join(gen_image_dir_path, ocr_file_name.split('.')[0])
        if not os.path.exists(ocr_file_gen_image_save_dir_path):
            os.makedirs(ocr_file_gen_image_save_dir_path)

        i = 1
        # 清空对话
        time.sleep(0.2)
        # 需要在Chrome可视窗口中
        # clean_chat_input_button = browser.find_element(by=By.XPATH, value='//*[@id="w2"]/div/div[3]/input[2]')
        # ActionChains(browser).click(clean_chat_input_button).perform()

        # 不可行
        # clear_button_xpath = '//*[@id="w2"]/div/div[3]/input[2]'
        # wait_element_xpath(browser, clear_button_xpath)
        # browser.find_element(by=By.XPATH, value=clear_button_xpath).click()

        browser.execute_script("arguments[0].click();",
                               browser.find_element(by=By.XPATH, value='//*[@id="w2"]/div/div[3]/input[2]'))
        for ocr_item in ocr_json_list:


            postion = ocr_item.get('postion')
            text = ocr_item.get('text')
            if not text:
                continue
            if postion == 'right':
                textarea_xpath = '//*[@id="w2"]/div/div[2]/div[1]/div[2]/p[2]/textarea'
                add_text_button_xpath = '//*[@id="w2"]/div/div[2]/div[1]/div[3]/a'
            else:
                textarea_xpath = '//*[@id="w2"]/div/div[2]/div[2]/div[2]/p[2]/textarea'
                add_text_button_xpath = '//*[@id="w2"]/div/div[2]/div[2]/div[3]/a'
            # 添加聊天文字
            time.sleep(0.2)
            text_element = browser.find_element(by=By.XPATH, value=textarea_xpath)
            text_element.clear()
            text_element.send_keys(text)
            # 点击添加对话
            browser.execute_script("arguments[0].click();",
                                   browser.find_element(by=By.XPATH, value=add_text_button_xpath))
            time.sleep(0.2)
            browser.execute_script("arguments[0].click();",
                                   browser.find_element(by=By.XPATH, value='//*[@id="save"]'))
            time.sleep(1)
            base64_img_str = browser.find_element(by=By.XPATH, value='/html/body/div[2]/img').get_attribute('src')
            img_str = base64_img_str.split(",")[-1]  # 删除前面的 “data:image/jpeg;base64,”
            img_str = img_str.replace("%0A", '\n')  # 将"%0A"替换为换行符
            img_data = b64decode(img_str)  # b64decode 解码
            img_path = os.path.join(ocr_file_gen_image_save_dir_path, str(i) + '.jpeg')
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print('img_path: ', img_path)
            # 点击 返回继续修改
            browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/a').click()
            i += 1
        browser.refresh()


def gen_video_from_image():

    for img_dir in os.listdir(gen_image_dir_path):
        video_path = os.path.join(gen_video_dir_path, f'{img_dir}.avi')
        image_folder = os.path.join(gen_image_dir_path, img_dir)
        images = [img for img in os.listdir(image_folder) if img.endswith(".jpeg")]
        if not images:
            continue
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_path, 0, 1, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()
        print(f'{video_path} 生成成功！')


def get_sound_from_video():
    video_has_sound_path = r'C:\Users\admin\workplace\short-video-generate\TikTokDownload\Download\post\情感聊天'
    for video_name in os.listdir(video_has_sound_path):
        sound_name = video_name.split('.')[0]
        video_path = os.path.join(video_has_sound_path, video_name)
        audio_clip = AudioFileClip(video_path)
        sound_path = os.path.join(sound_dir_path, sound_name + '.wav')
        audio_clip.write_audiofile(sound_path)
        print(f'{sound_path} 提取成功')


def add_sound_to_video():
    sound_paths = []
    for sound_name in os.listdir(sound_dir_path):
        sound_path = os.path.join(sound_dir_path, sound_name)
        sound_paths.append(sound_path)

    sound_path = random.choice(sound_paths)
    for video_name in os.listdir(gen_video_dir_path):
        video_path = os.path.join(gen_video_dir_path, video_name)
        video = VideoFileClip(video_path)
        video_time = video.duration
        audio = AudioFileClip(sound_path)
        audio_video_time = audio.duration
        if audio_video_time > video_time:
            # 切割出目标视频长度的音频
            audio = audio.subclip(0, video_time)
        new_video = video.set_audio(audio)
        save_path = os.path.join(gen_video_dir_path2, f"{video_name.split('.')[0]}-sound.mp4")
        new_video.write_videofile(save_path, threads=8)
        video.close()
        audio.close()
        new_video.close()
        print(f'{save_path} 生成成功')

if __name__ == '__main__':
    create_dirs([gen_image_dir_path, gen_video_dir_path, clean_ocr_dir_path, sound_dir_path, gen_video_dir_path2])
    # get_ocr_json(ocr_dir_path)
    # browser = get_browser()
    # gen_wechat_image(browser)
    # gen_video_from_image()
    # get_sound_from_video()
    # add_sound_to_video()
    add_sound_to_video()