import time

from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class AnimehayPage(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, 'div[class="movies-list ah-frame-bg"] > div:nth-child(1)')
    PLAY_VIDEO = (By.CSS_SELECTOR, 'div[class="flex flex-wrap flex-1"] > a:nth-child(1)')
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[class="jw-video jw-reset"]')
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    VIDEO_PAUSE_PLAY_BTN = (By.CSS_SELECTOR, 'div[aria-label="Play"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')
    OK_POPUP_BTN = (By.CSS_SELECTOR, 'div[class="swal2-actions"] button:nth-child(2)')

    def open_animehay(self, url):
        self.get_url(url)
        self.click(self.FIRST_VIDEO)
        self.click(self.PLAY_VIDEO)
        video_duration = self.get_video_duration()
        time.sleep(2)
        if self.is_element_exist(self.OK_POPUP_BTN, timeout=2):
            self.click(self.OK_POPUP_BTN)
            time.sleep(1)
        else:
            pass
        self.hover_on_element(self.VIDEO_AREA)

        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()
        self.click_preferred_quality_dropdown()
        media_quality_selected = self.select_random_media_quality_js_path()
        # Return media duration and its extension
        return video_duration, media_quality_selected

    def get_video_duration(self):
        # return self.get_media_duration_from_site(self.VIDEO_DURATION)
        # Video duration of animehay is under pseudo element (::before, ::after), we should use 'text' method
        timing_duration = self.get_element(self.VIDEO_DURATION).text
        # To format the value before returning
        video_duration = string_number_utils.format_timing_duration(timing_duration)
        return video_duration