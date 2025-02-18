import time

import pywinauto.win32defines
from pywinauto import Application
from selenium.webdriver.common.by import By
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage
from src.pages.coccoc_common import open_browser


class PhimplayPage(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, '#main-contents div[class="halim_box"] > article:nth-child(1)')
    PLAY_VIDEO = (By.CSS_SELECTOR, 'div[class="halim-watch-box"] a')
    VIDEO_AREA = (By.CSS_SELECTOR, '#player')
    VIDEO_AREA_TEXT = 'video[class="jw-video jw-reset"]'
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-display jw-button-color jw-reset"]')
    VIDEO_PAUSE_PLAY_BTN = (By.CSS_SELECTOR, 'div[aria-label="Play"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')
    IFRAME_FIRST = (By.CSS_SELECTOR, '#ajax-player iframe')
    IFRAME_SECOND = (By.CSS_SELECTOR, 'body > iframe')

    def open_phimplay(self, url):
        self.get_url(url)
        self.click(self.FIRST_VIDEO)
        self.click(self.PLAY_VIDEO)
        # Switch to Iframe
        self.switch_to_frame(self.IFRAME_FIRST)
        self.switch_to_frame(self.IFRAME_SECOND)
        self.click(self.VIDEO_PLAY_BTN)
        time.sleep(5)
        video_duration = self.get_video_duration()
        title = self.get_page_title()
        # Hover on video by pywinauto
        coccoc = open_browser.connect_to_opened_coccoc(title=title)
        coccoc.child_window(title="Video Player", auto_id="player", control_type="Window").drag_mouse_input(absolute=False)
        self.hover_on_element(self.VIDEO_AREA)
        self.leave_frame()
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
        print(video_duration)
        return video_duration