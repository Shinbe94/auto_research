import time

from src.pages.savior.savior_base_page import SaviorBasePage
from selenium.webdriver.common.by import By


class TuyenSinh247(SaviorBasePage):
    VIDEO_247 = (By.CSS_SELECTOR, 'video[class="vjs-tech"]')
    VIDEO_24H_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.XPATH, '//*[@id="movie_player"]/div[27]//span[@class="ytp-time-current"]')
    VIDEO_DURATION = (By.XPATH, '//*[@id="movie_player"]/div[27]//span[@class="ytp-time-duration"]')

    def open_tuyen_sinh_247(self, url):
        self.get_url(url)
        self.wait_for_page_loaded_completely()
        # self.click(self.VIDEO_24H_PLAY_BTN)
        time.sleep(3)
        self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_247)
        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()
