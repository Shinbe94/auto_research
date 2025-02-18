import time

from src.pages.savior.savior_base_page import SaviorBasePage
from selenium.webdriver.common.by import By


class TwentyFourHPage(SaviorBasePage):

    VIDEO_24H = (By.CSS_SELECTOR, 'video[class="vjs-tech"]')
    VIDEO_24H_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="vjs-duration-display"]')

    def open_24h(self, url):
        self.get_url(url)
        self.click(self.VIDEO_24H_PLAY_BTN)
        time.sleep(3)
        self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_24H)
        self.wait_for_prefetch_savior_dock()
        self.click_preferred_quality_dropdown()
        time.sleep(1)
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)


