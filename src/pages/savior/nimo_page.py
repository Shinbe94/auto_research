import time

from selenium.webdriver.common.by import By

from src.pages.savior.savior_base_page import SaviorBasePage


class NimoPage(SaviorBasePage):
    VIDEO_AREA = (By.CSS_SELECTOR, '#nimo-player')
    VIDEO_NIMO_PLAY_BTN = (By.CSS_SELECTOR, 'span[class="autoplay-alert__play"]')
    NIMO_ENTER_ROOM = (By.CSS_SELECTOR, 'a[class="enter-room-hover"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="vjs-duration-display"]')

    def open_nimo(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.VIDEO_NIMO_PLAY_BTN)
        self.click(self.NIMO_ENTER_ROOM)
        time.sleep(4)
        # self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()