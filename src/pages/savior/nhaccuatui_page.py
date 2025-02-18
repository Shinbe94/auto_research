import time

from selenium.webdriver.common.by import By

from src.pages.savior.savior_base_page import SaviorBasePage


class NhaccuatuiPage(SaviorBasePage):

    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')

    FIRST_VIDEO = (By.CSS_SELECTOR, 'div[class="box-left"] >div:nth-child(2) ul li:nth-child(1)')
    VIDEO_AREA = (By.CSS_SELECTOR, '#coverImagenctPlayer')
    VIDEO_DURATION = (By.CSS_SELECTOR, '#utTotalTimenctPlayer')

    FIRST_MP3 = (By.CSS_SELECTOR, 'div[class="list_music listGenre"] ul li:nth-child(1) img')
    MP3_AREA = (By.CSS_SELECTOR, '#mainScreenflashPlayer')
    MP3_DURATION = (By.CSS_SELECTOR, '#utTotalTimeflashPlayer')

    def open_nhaccuatui(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.FIRST_VIDEO)
        time.sleep(4)
        # self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.click_preferred_quality_dropdown()
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()

    def open_nhaccuatui_mp3(self, url):
        self.get_url(url, is_wait_for_loaded=False)
        time.sleep(3)
        self.click(self.FIRST_MP3)
        time.sleep(2)
        self.hover_on_element(self.MP3_AREA)
        self.wait_for_prefetch_savior_dock()
        self.click_preferred_quality_dropdown()
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()

    def get_mp3_duration(self):
        return self.get_media_duration_from_site(self.MP3_DURATION)

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)