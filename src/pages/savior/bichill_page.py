import time

from selenium.webdriver.common.by import By

from src.pages.coccoc_common import open_browser
from src.utilities import string_number_utils
from src.pages.savior.savior_base_page import SaviorBasePage


class BichillPage(SaviorBasePage):

    FIRST_VIDEO = (By.CSS_SELECTOR, '#all-items > div:nth-child(1)')
    XEMPHIM_BTN = (By.CSS_SELECTOR, 'div[class="movie-thumb position-relative"] a')
    IFRAME = (By.CSS_SELECTOR, '#playerLoaded > iframe')
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[class="jw-video jw-reset"]')
    VIDEO_PLAY_BTN = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-display jw-button-color jw-reset"]')
    VIDEO_BAR = (By.CSS_SELECTOR, 'div[class="jw-reset jw-button-container"]')
    VIDEO_PAUSE_PLAY_BTN = (By.CSS_SELECTOR, 'div[aria-label="Play"]')
    VIDEO_10_SECONDS_BACK = (By.CSS_SELECTOR, '#rmpPlayer > div.jw-controls.jw-reset > div.jw-controlbar.jw-reset > div.jw-reset.jw-button-container > div.jw-icon.jw-icon-inline.jw-button-color.jw-reset.jw-icon-rewind')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')
    VIDEO_SELECTOR_TEXT = 'video[class="jw-video jw-reset"]'

    def open_bichill(self, url):
        self.get_url(url)
        self.click(self.FIRST_VIDEO)
        self.click(self.XEMPHIM_BTN)
        time.sleep(1)

        self.switch_to_frame(self.IFRAME)
        # self.hover_on_element(self.VIDEO_PLAY_BTN)
        self.click(self.VIDEO_PLAY_BTN)
        time.sleep(1)

        self.hover_mouse_center('video[class="jw-video jw-reset"]')
        self.hover_on_element_by_query_selector(self.VIDEO_SELECTOR_TEXT)

        title = self.get_page_title()
        coccoc = open_browser.connect_to_opened_coccoc(title=title)
        coccoc.child_window(title="Trình phát video", auto_id="video", control_type="Window").drag_mouse_input()
        video_duration = self.get_video_duration()
        time.sleep(3)
        # Leaving the iframe
        self.leave_frame()

        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()
        self.is_quality_loaded()
        self.show_savior_dock()
        self.click_preferred_quality_dropdown()
        media_quality_selected = self.select_random_media_quality_js_path()
        # Return media duration and its extension
        return video_duration, media_quality_selected

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)