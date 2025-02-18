import time

from selenium.webdriver.common.by import By

from src.pages.coccoc_common import open_browser
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class DongphymtvPage(SaviorBasePage):
    FIRST_VIDEO = (By.CSS_SELECTOR, 'div[class="flex-wrap-movielist"] a:nth-child(1)')
    FIRST_CHAPTER = (By.CSS_SELECTOR, 'div[class="movie-rate"]:nth-child(3) a[class="movie-eps-item "]:nth-child(1)')
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[class="jw-video jw-reset"]')
    VIDEO_AREA_TEXT = 'video[class="jw-video jw-reset"]'
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-display jw-button-color jw-reset"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')
    IFRAME = (By.CSS_SELECTOR, '#playerLoaded > iframe')

    def open_dongphymtv(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.FIRST_VIDEO)
        self.click(self.FIRST_CHAPTER)
        time.sleep(3)
        self.switch_to_frame(self.IFRAME)
        self.click(self.VIDEO_PLAY_BTN)

        # self.hover_on_element_by_query_selector(self.VIDEO_AREA_TEXT)

        title = self.get_page_title()
        coccoc = open_browser.connect_to_opened_coccoc(title=title)
        # coccoc = open_browser.connect_to_opened_coccoc(title=title).print_control_identifiers()
        coccoc.child_window(title="Trình phát video", auto_id="video", control_type="Window").drag_mouse_input()

        video_duration = self.get_video_duration()

        self.leave_frame()
        self.wait_for_prefetch_savior_dock()
        self.is_quality_loaded()
        self.show_savior_dock()
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