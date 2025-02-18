import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class GamevuiPage(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, 'body > div:nth-child(3)  ul > li:nth-child(1)')
    VIDEO_AREA = (By.CSS_SELECTOR, '#evideo video')
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.XPATH, '//*[@id="evideo"]/div[5]/div[4]/div')
    SKIP_ADS = (By.CSS_SELECTOR, 'div[class="videoAdUiSkipButtonExperimentalText"]')

    def open_gamevui(self, url):
        self.get_url(url)
        # time.sleep(4)
        self.click(self.FIRST_VIDEO)
        self.click(self.VIDEO_PLAY_BTN)
        time.sleep(1)
        self.click(self.VIDEO_AREA)
        time.sleep(2)
        self.click(self.VIDEO_AREA)
        video_duration = self.get_video_duration()
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        time.sleep(1)
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()
        return video_duration

    def get_video_duration(self):
        # Video duration of Vietbao has format is: "Độ dài 4:28"
        # We need to format them, before returning
        timing_duration = self.get_value_of_element_attribute(self.VIDEO_DURATION, 'innerText')
        timing_duration = string_number_utils.substring_after(timing_duration, 'Độ dài ')
        # To format the value before returning
        video_duration = string_number_utils.format_timing_duration(timing_duration)
        return video_duration
