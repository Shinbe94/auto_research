import time

from selenium.webdriver.common.by import By

from src.pages.savior.savior_base_page import SaviorBasePage


class VtvgoPage(SaviorBasePage):

    FIRST_VIDEO = (By.CSS_SELECTOR, 'div[class="swiper-slide news-slide-content-item swiper-slide-active"')
    VIDEO_AREA = (By.CSS_SELECTOR, 'video[id="flowplayer_html5_api"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="vjs-duration-display"]')

    FIRST_MP3 = (By.CSS_SELECTOR, 'div[class="list_music listGenre"] ul li:nth-child(1) img')
    MP3_AREA = (By.CSS_SELECTOR, '#mainScreenflashPlayer')
    MP3_DURATION = (By.CSS_SELECTOR, '#utTotalTimeflashPlayer')

    def open_vtvgo(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.FIRST_VIDEO)
        time.sleep(4)
        # self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        self.show_savior_dock()

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)