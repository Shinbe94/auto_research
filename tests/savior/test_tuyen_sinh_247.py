# import os
# import time

# from tests.savior.savior_base_test import SaviorBaseTest
# from src.pages.savior.tuyen_sinh_247_page import TuyenSinh247
# from src.utilities import os_utils
# from selenium.webdriver.common.by import By


# class TestTuyenSinh247(SaviorBaseTest):
#     def test_tuyen_sinh_247(self):
#         self.test_tuyen_sinh_247 = TuyenSinh247(self)
#         self.test_tuyen_sinh_247.open_tuyen_sinh_247(
#             "https://tuyensinh247.com/gioi-thieu-r3.html"
#         )
#         self.test_tuyen_sinh_247.click_btn_download()
#         file_name = self.twenty_four_h.wait_for_downloads(
#             rf"C:\Users\{os_utils.get_username()}\Downloads"
#         )
#         os.remove(file_name)

#     def test_tuyen_sinh_2472(self):
#         self.test_tuyen_sinh_247 = TuyenSinh247(self.driver)
#         self.test_tuyen_sinh_247.get_url("https://video.vnexpress.net/")
#         js = """
#             div = document.createElement('div');
#             div.id = 'output';
#             document.body.append(div);
#         """
#         video_state_js = """
#             const media = document.getElementById('vne_vod_html5_api');
#             const output = document.getElementById('output');

#             media.addEventListener("playing", () => {
#               output.innerHTML = "Playing event triggered";
#             });

#             media.addEventListener("pause", () => {
#               output.innerHTML = "Pause event triggered";

#             });

#             media.addEventListener("seeking", () => {
#               output.innerHTML = "Seeking event triggered";
#             });

#             media.addEventListener("volumechange", () => {
#               output.innerHTML = "Volumechange event triggered";
#             });
#         """

#         self.test_tuyen_sinh_247.execute_js(js)
#         self.test_tuyen_sinh_247.execute_js(video_state_js)
#         VIDEO_VNEXPRESS_PLAY_BTN = (
#             By.CSS_SELECTOR,
#             'button[class="vjs-big-play-button"]',
#         )
#         self.test_tuyen_sinh_247.click(VIDEO_VNEXPRESS_PLAY_BTN)
#         time.sleep(2)
#         self.test_tuyen_sinh_247.click(VIDEO_VNEXPRESS_PLAY_BTN)
#         self.test_tuyen_sinh_247.click(VIDEO_VNEXPRESS_PLAY_BTN)
#         is_not_playing = True
#         video_status_ele = (By.ID, "output")
#         max_delay = 5
#         interval_delay = 0.5
#         total_delay = 0
#         while is_not_playing:
#             try:
#                 if (
#                     self.driver.find_element(*video_status_ele).get_attribute(
#                         "innerText"
#                     )
#                     == "Playing event triggered"
#                 ):
#                     is_not_playing = False
#                     print("The video is playing")
#                     break
#                 time.sleep(interval_delay)
#                 total_delay += interval_delay
#                 if total_delay > max_delay:
#                     is_not_playing = False
#                     print("Timeout for the video is playing")
#                     break
#             finally:
#                 print("Error")
#         time.sleep(4)
