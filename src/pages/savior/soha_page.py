import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class SohaPage(SaviorBasePage):
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[class="vjs-tech"]')
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'div[class="SohaPlayer-loading-vid-icon"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="customSkin-duration"]')

    def open_soha(self, url):
        self.get_url(url)
        self.click(self.VIDEO_PLAY_BTN)
        time.sleep(3)
        self.hover_on_element(self.VIDEO_AREA)
        video_duration = self.get_video_duration()
        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        media_quality_selected = self.select_random_media_quality_js_path()
        # Return media duration and its extension
        return video_duration, media_quality_selected

    def get_video_duration(self):
        self.hover_on_element(self.VIDEO_AREA)
        return self.get_media_duration_from_site(self.VIDEO_DURATION)