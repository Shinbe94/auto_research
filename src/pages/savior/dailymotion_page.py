import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class DailymotionPage(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, '#daily_picks > div > div.col.xsmall-12.medium-8 > div > div:nth-child(2) div[class^="VideoCard__videoTitle"]')
    VIDEO_AREA = (By.CSS_SELECTOR, 'div #player')
    VIDEO_AREA_TEXT = 'div #player'
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'div[class="SohaPlayer-loading-vid-icon"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="np_TimerContent-duration"]')
    IFRAME = (By.CSS_SELECTOR, '#player-body')

    def open_dailymotion(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.FIRST_VIDEO)
        # self.click(self.VIDEO_PLAY_BTN)
        time.sleep(3)
        self.switch_to_frame(self.IFRAME)
        # self.hover_on_element(self.VIDEO_AREA)
        # self.hover_on_element_by_query_selector(self.VIDEO_AREA_TEXT)
        video_duration = self.get_video_duration()
        self.leave_frame()
        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        media_quality_selected = self.select_random_media_quality_js_path()
        self.click_btn_download()
        # Return media duration and its extension
        return video_duration, media_quality_selected

    def get_video_duration(self):
        # return self.get_media_duration_from_site(self.VIDEO_DURATION)
        # Video duration of animehay is under pseudo element (::before, ::after), we should use 'text' method
        timing_duration = self.get_element(self.VIDEO_DURATION).text
        # print(timing_duration)
        # To format the value before returning
        video_duration = string_number_utils.format_timing_duration(timing_duration)
        # print(video_duration)
        return video_duration