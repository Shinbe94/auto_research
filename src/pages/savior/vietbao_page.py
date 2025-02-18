import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class VietbaoPage(SaviorBasePage):

    IFRAME = (By.CSS_SELECTOR, '#tubiaFrame')
    VIDEO_AREA = (By.CSS_SELECTOR, '#mainPlayerWrap video[id="mainPlayer_html5_api"]')
    VIDEO_VIETBAO_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[aria-label="Progress Bar"]')
    SKIP_ADS = (By.CSS_SELECTOR, 'div[class="videoAdUiSkipButtonExperimentalText"]')

    def open_vietbao(self, url):
        self.get_url(url)
        time.sleep(4)
        self.click(self.VIDEO_VIETBAO_PLAY_BTN)
        video_duration = self.get_video_duration()
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        time.sleep(1)
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()
        return video_duration

    def get_video_duration(self):
        # Video duration of Vietbao has format is: aria-valuetext="0:04 of 1:57"
        # We need to format them, before returning
        timing_bar = self.get_value_of_element_attribute(self.VIDEO_DURATION, 'aria-valuetext')
        timing_bar_duration = string_number_utils.substring_after(timing_bar, 'of ')
        video_duration = string_number_utils.format_timing_duration(timing_bar_duration)
        # return self.get_media_duration_from_site(self.VIDEO_DURATION)
        return video_duration