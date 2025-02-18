import json
import logging
import os, subprocess
import shlex
from os import startfile

import cv2
import time

from pywinauto import Application
from selenium.webdriver.common.action_chains import ActionChains

from playwright.sync_api import sync_playwright
from selenium.webdriver.common.by import By

from src.utilities import os_utils
from src.pages.coccoc_common import open_browser

DOWNLOAD_BTN = 'document.querySelector("html > div").shadowRoot.querySelector("#download-main").click()'


def download_youtube():
    # LOGGER.info("Get Default download folder...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=f'C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe',
            # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Profile 1',
            user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default',
            headless=False,
        )
        # context = browser.new_context(ignore_https_errors=True)
        page = browser.new_page()
        page.goto('https://www.youtube.com/watch?v=w9r4nSBXKcw')
        page.hover('//*[@id="movie_player"]/div[1]/video')
        time.sleep(30)


def download_youtube2():
    # LOGGER.info("Get Default download folder...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                    executable_path=f'C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe')

        # context = browser.new_context(ignore_https_errors=True)
        page = browser.new_page()
        page.goto('https://www.youtube.com/watch?v=w9r4nSBXKcw')
        time.sleep(30)


def open_side_bar_setting():
    # LOGGER.info("Get Default download folder...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=f'C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe',
            # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Profile 1',
            user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default',
            headless=False
        )

        # browser = p.chromium.launch(
        #     executable_path=f'C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe',
        #     # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Profile 1',
        #     # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default',
        #     headless=False
        # )
        # context = browser.new_context(ignore_https_errors=True)
        page = browser.new_page()
        page.goto('coccoc://settings')
        page.click('a[href="/sidebar"]')
        page.click('settings-toggle-button[label="Show Sidebar"]')
        page.click('settings-toggle-button[label="Show Sidebar"]')
        page.click('cr-checkbox[aria-label="History"]')
        # time.sleep(30)
        browser.close()


def download_youtube3():
    # LOGGER.info("Get Default download folder...")
    # coccoc = Application(backend='uia').start(setting.coccoc_binary_64bit_debug,
    #                                  timeout=setting.time_out_pywinauto)
    # time.sleep(3)
    # driver = open_browser.connect_to_coccoc_by_selenium()
    driver = open_browser.open_coccoc_by_selenium()
    driver.get('https://www.youtube.com/watch?v=Vq25ZJwZJzU')
    time.sleep(3)
    VIDEO = driver.find_element(By.XPATH, '//*[@id="movie_player"]/div[1]/video')
    action = ActionChains(driver)
    action.move_to_element(VIDEO)
    action.perform()

    wait_for_prefetch_savior(driver)
    driver.execute_script(
        "document.querySelector('html > div').shadowRoot.querySelector('.overlay').classList.remove('hidden')")

    driver.execute_script('document.querySelector("html > div").shadowRoot.querySelector("#download-main").click()')
    file_name = wait_for_downloads(rf'C:\Users\{os_utils.get_username()}\Downloads')
    text = driver.title
    # print(text)
    driver.quit()

    # coccoc[f'{text} - Cốc Cốc'].close()
    startfile(file_name)
    time.sleep(10)
    play_media = Application(backend='uia').connect(title='Movies & TV', class_name='ApplicationFrameWindow',
                                                    control_type=50032)
    play_media['Movies & TV'].close()
    os.remove(file_name)


def download_24h_com():
    # LOGGER.info("Get Default download folder...")
    # coccoc = Application(backend='uia').start(setting.coccoc_binary_64bit_debug,
    #                                  timeout=setting.time_out_pywinauto)
    time.sleep(3)
    # driver = open_browser.connect_to_coccoc_by_selenium()
    driver = open_browser.open_coccoc_by_selenium()
    driver.get(
        'https://www.24h.com.vn/media-24h/suc-manh-to-hop-phao-ten-lua-phong-khong-tren-chien-ham-cua-nga-c762a1351204.html')
    time.sleep(3)
    VIDEO = driver.find_element(By.CSS_SELECTOR, 'video[class="vjs-tech"]')
    action = ActionChains(driver)
    action.move_to_element(VIDEO)
    action.perform()

    wait_for_prefetch_savior(driver)
    driver.execute_script(
        "document.querySelector('html > div').shadowRoot.querySelector('.overlay').classList.remove('hidden')")

    driver.execute_script('document.querySelector("html > div").shadowRoot.querySelector("#download-main").click()')
    file_name = wait_for_downloads(rf'C:\Users\{os_utils.get_username()}\Downloads')
    text = driver.title
    # print(text)
    driver.quit()
    # print(has_audio(file_name))
    # coccoc[f'{text} - Cốc Cốc'].close()
    startfile(file_name)
    time.sleep(10)
    play_media = Application(backend='uia').connect(title='Movies & TV', class_name='ApplicationFrameWindow',
                                                    control_type=50032)
    play_media['Movies & TV'].close()
    os.remove(file_name)


def test_playmedia():
    play_media('C:\\Users\\taynq\\Downloads\\a.mp4')


def play_media(filename_with_path):
    startfile(filename_with_path)
    # time.sleep(6)
    media_playing = Application(backend='uia').connect(title='Movies & TV', class_name='ApplicationFrameWindow',
                                                       control_type=50032)
    media_playing_window = media_playing['Movies & TV']
    slider_bar = media_playing['Movies & TV'].child_window(auto_id="ProgressSlider",
                                                           control_type="Slider").wrapper_object()
    slider_bar.drag_mouse_input()
    print(slider_bar.iface_range_value.CurrentValue)
    print(slider_bar.iface_range_value.CurrentMinimum)
    print(slider_bar.iface_range_value.CurrentMaximum)
    slider = media_playing_window.child_window(auto_id="ProgressSlider", control_type="Slider").window_text()
    current_position = slider[24:32]
    print(current_position)
    duration = slider[45:53]
    print(duration)

    # slider_2 = media_playing['Movies & TV'].child_window(auto_id="ProgressSlider", control_type="Slider").set_edit_text('Seek. Current position: 00:00:30 . Duration: 00:04:06 .')
    # slider_2.click_input(button='left')

    media_playing['Movies & TV'].close()
    return media_playing_window, current_position, duration


def seek_media(filename_with_path):
    data = play_media(filename_with_path)
    # slide_to_position = data[0]['Movies & TV'].child_window(title=f"Seek. Current position: 00:00:30 . Duration: 00:04:06 .", auto_id="ProgressSlider", control_type="Slider")
    # data[0].print_control_identifiers()
    # .set_edit_text(f"Seek. Current position: 00:00:30 . Duration: 00:04:06 .")
    # slide_1.click_input(button='left')
    # slide_to_position.click_input(button='left')


def test_seek():
    seek_media('C:\\Users\\taynq\\Downloads\\a.mp4')


class TestDownload:

    def test_youtube(self):
        download_youtube3()

    def test_24h(self):
        download_24h_com()


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("coccoc://downloads"):
        driver.get("coccoc://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


def wait_for_downloads(download_path):
    max_delay = 600
    interval_delay = 0.5
    total_delay = 0
    file = ''
    done = False
    while not done and total_delay < max_delay:
        files = [f for f in os.listdir(download_path) if f.endswith('.crdownload')]
        if not files and len(file) > 1:
            done = True
        if files:
            file = files[0]
        time.sleep(interval_delay)
        total_delay += interval_delay
    if not done:
        logging.error("File(s) couldn't be downloaded")
    print(download_path + '\\' + file.replace(".crdownload", ""))
    return download_path + '\\' + file.replace(".crdownload", "")


def wait_for_prefetch_savior(driver):
    max_delay = 300
    interval_delay = 0.5
    total_delay = 0
    is_done = False
    while is_done or total_delay > max_delay:
        btn_download = driver.execute_script(
            'document.querySelector("html > div").shadowRoot.querySelector("#preferred-select")')
        print('Savior dock:  ' + str(btn_download))
        if btn_download is not None:
            is_done = True
            print('got button at: ' + str(total_delay))
            break
        time.sleep(interval_delay)
        total_delay += interval_delay
    if not is_done:
        logging.error("File(s) couldn't be loaded")
    # return download_path + '/' + file.replace(".crdownload", "")


def has_audio(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=nb_streams", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return int(result.stdout) - 1


def test_audio():
    # has_audio(filename=r'C:\Users\taynq\Downloads\Sức mạnh tổ hợp pháo - tên lửa phòng không trên chiến hạm của Nga-Media.mp4')
    # has_audio_streams('C:\\Users\\taynq\\Downloads\\file.mp4')
    findVideoMetada('C:\\Users\\taynq\\Downloads\\file.mp4')
    # clip_has_audio()


def has_audio_streams(file_path):
    command = ['ffprobe', '-show_streams',
               '-print_format', 'json', file_path]
    output = subprocess.check_output(command, shell=True)
    parsed = json.loads(output)
    streams = parsed['streams']
    audio_streams = list(filter((lambda x: x['codec_type'] == 'audio'), streams))
    return len(audio_streams) > 0


def findVideoMetada(pathToInputVideo):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args, shell=True).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    # prints all the metadata available:
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ffprobeOutput)

    # for example, find height and width
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']

    print(height, width)
    return height, width


# def clip_has_audio():
#     p = ffmpeg.probe('in.mp4', select_streams='a')
#
#     # If p['streams'] is not empty, clip has an audio stream
#     if p['streams']:
#         print('Video clip has audio!')

def test_media_info():
    getMediaInfo('C:\\Users\\taynq\\Downloads\\a.mp4')


# ===============================
def getMediaInfo(mediafile):
    cmd = "mediainfo --Output=JSON %s" % (mediafile)
    # proc = subprocess.Popen(cmd, shell=True,
    #     stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # stdout, stderr = proc.communicate()
    stdout = subprocess.check_output(cmd, shell=True).decode('utf-8')
    data = json.loads(stdout)
    print(data)
    return data


# ===============================
def getDuration(mediafile):
    data = getMediaInfo(mediafile)
    duration = float(data['media']['track'][0]['Duration'])
    return duration


def test_open():
    get_playback_duration('C:\\Users\\taynq\\Downloads\\a.mp4')


def get_playback_duration(video_filepath, method='cv2'):  # pragma: no cover
    """
    Get video playback duration in seconds and fps
    "This epic classic car collection centres on co.webm"
    :param video_filepath: str, path to video file
    :param method: str, method cv2 or default ffprobe
    """
    if method == 'cv2':  # Use opencv-python
        video = cv2.VideoCapture(video_filepath)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        duration_seconds = frame_count / fps if fps else 0

        minutes = int(duration_seconds / 60)
        seconds = duration_seconds % 60
        print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

    else:  # ffprobe
        result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{video_filepath}"', shell=True).decode()
        fields = json.loads(result)['streams'][0]
        duration_seconds = fields['tags'].get('DURATION')
        fps = eval(fields.get('r_frame_rate'))
    return duration_seconds, fps
