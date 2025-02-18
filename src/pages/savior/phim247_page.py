import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class Phim247Page(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, '#content div[class="list-vod row category-tabs-item"] > div:nth-child(1)')
    PLAY_VIDEO = (By.CSS_SELECTOR, 'button[id="btnPlay"]')
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[class="jw-video jw-reset"]')
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    VIDEO_PAUSE_PLAY_BTN = (By.CSS_SELECTOR, 'div[aria-label="Play"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')
    VIDEO_SELECTOR_TEXT = '#rmpPlayer'

    def open_phim247(self, url):
        self.get_url(url)
        self.click(self.FIRST_VIDEO)
        self.click(self.PLAY_VIDEO)
        time.sleep(1)
        # self.click(self.VIDEO_PAUSE_PLAY_BTN)
        # self.hover_on_element_by_query_selector(self.VIDEO_SELECTOR_TEXT)
        self.hover_on_element(self.VIDEO_AREA)
        video_duration = self.get_video_duration()
        self.wait_for_prefetch_savior_dock()
        # self.show_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        media_quality_selected = self.select_random_media_quality_js_path()
        # Return media duration and its extension
        return video_duration, media_quality_selected

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)