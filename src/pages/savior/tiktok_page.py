import time

from src.utilities import string_number_utils
from selenium.webdriver.common.by import By
from src.pages.savior.savior_base_page import SaviorBasePage


class TiktokPage(SaviorBasePage):
    VIDEO_AREA = (By.XPATH, '//*[@id="app"]//div[2]/div[1]/div[1]//div[1][@data-e2e="feed-video"]')
    BTN_CLOSE_CAPTCHA = (By.CSS_SELECTOR, 'a[id="verify-bar-close"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]')

    def open_tiktok(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.VIDEO_AREA)
        time.sleep(4)
        self.click(self.BTN_CLOSE_CAPTCHA)
        # self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()

    def get_video_duration(self):
        # Format from tiktok is as eg: 00:01/00:59
        timing = self.get_media_duration_from_site(self.VIDEO_DURATION, is_need_format=False)
        # Format for duration for tiktok
        duration = string_number_utils.substring_after(timing, '/')
        if len(duration) == 5:
            duration = '00:' + duration
        return duration

