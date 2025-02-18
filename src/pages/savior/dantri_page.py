import time

from selenium.webdriver.common.by import By
from src.pages.savior.savior_base_page import SaviorBasePage


class DantriPage(SaviorBasePage):
    VIDEO_AREA = (By.CSS_SELECTOR, 'div[data-module="video-player"]')
    VIDEO_VNEXPRESS_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="vjs-duration-display"]')

    def open_dantri(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.VIDEO_AREA)
        time.sleep(4)
        # self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)