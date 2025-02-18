import time

from selenium.webdriver.common.by import By

from src.pages.savior.savior_base_page import SaviorBasePage


class MotphimtvPage(SaviorBasePage):

    FIRST_FILM = (By.CSS_SELECTOR, 'div[id="page-info"] ul li:nth-child(1) a img')
    BTN_XEMPHIM = (By.CSS_SELECTOR, 'div[id="page-info"] ul[class="buttons two-button"] li:nth-child(2)')
    IFRAME = (By.CSS_SELECTOR, 'div[id="player"] iframe')
    VIDEO_AREA = (By.CSS_SELECTOR, 'div[id="player"] video')
    VIDEO_AREA_TEXT = '#player > div.jw-wrapper.jw-reset > div.jw-media.jw-reset > video'
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'div[class="jw-icon jw-icon-inline jw-text jw-reset jw-text-duration"]')

    # This site having an iframe
    def open_motphimtv(self, url):
        self.get_url(url)
        time.sleep(3)
        # Playing a film
        self.click(self.FIRST_FILM)
        self.click(self.BTN_XEMPHIM)

        # Switch to an iframe, then interaction with element inside the frame
        # Video and its duration ... are inside the frame
        self.switch_to_frame(self.IFRAME)
        self.click(self.VIDEO_AREA)
        media_duration = self.get_media_duration_from_site(self.VIDEO_DURATION)
        time.sleep(4)
        self.hover_on_element_by_query_selector(self.VIDEO_AREA_TEXT)
        # Leave the frame
        self.leave_frame()

        # Continue the rest
        self.wait_for_prefetch_savior_dock()
        # self.show_savior_dock()
        self.click_preferred_quality_dropdown()
        time.sleep(1)
        self.select_random_media_quality_js_path()
        return media_duration

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)