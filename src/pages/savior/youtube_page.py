import logging
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from src.pages.base import BaseAppium
from src.pages.savior.savior_base_page import SaviorBasePage
from src.pages.savior.youtube import wait_for_prefetch_savior
from src.pages.toolbar.toolbar import Toolbar


class YoutubePage(SaviorBasePage):
    VIDEO_YOUTUBE = (By.XPATH, '//*[@id="movie_player"]/div[1]/video')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="ytp-time-current"]')

    def open_youtube_url(self, url):
        self.get_url(url)
        time.sleep(3)
        self.wait_for_the_video_is_playing_by_state()
        self.hover_on_element(self.VIDEO_YOUTUBE)
        self.show_savior_dock()
        self.click_preferred_quality_dropdown()
        time.sleep(3)
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()

    def wait_for_the_video_is_playing_by_state(self):
        max_delay = 30
        interval_delay = 0.5
        total_delay = 0
        is_not_playing = True
        while is_not_playing:
            try:
                state = self.driver.execute_script(
                    "return document.getElementById('movie_player').getPlayerState()"
                )
                print("the state is " + str(state))
                if str(state) == "1":
                    is_not_playing = False
                    print("The video is playing ...")
                    time.sleep(3)
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    is_not_playing = False
                    print("Timeout when wait for the video is playing")
                    break
            except:
                logging.error("Video couldn't be loaded")

        # if not is_not_playing:

    def wait_for_the_video_is_playing2(self):
        is_not_playing = True
        current_time_sec = 0
        CURRENT_TIME_YOUTUBE = (By.CLASS_NAME, "ytp-time-current")
        while is_not_playing:
            self.hover_on_element(self.VIDEO_YOUTUBE)
            # length_str = self.driver.find_element_by_class_name("ytp-time-duration").text
            while self.get_ele(CURRENT_TIME_YOUTUBE).text is None:
                self.hover_on_element(self.VIDEO_YOUTUBE)
                current_time_str = self.get_ele(CURRENT_TIME_YOUTUBE).text
                second = int(current_time_str[-1:])
                if second >= 1:
                    is_not_playing = False
                    break
                print("current time sec is: " + str(second) + " seconds")
            break
        # return current_time_sec


class YoutubeAppium(Toolbar):
    """
    Interact with element of Youtube using appium
    https://www.youtube.com/

    Args:
        BaseAppium (_type_): _description_
    """

    # locator
    # MOVIE_PLAYER = (
    #     By.XPATH,
    #     '//Group[@Name="YouTube Video Player"][@AutomationId="movie_player"]/Group/Group',
    # )
    MOVIE_PLAYER = (By.NAME, "YouTube Video Player")
    BTN_DOWNLOAD = (By.XPATH, '//Hyperlink[@Name="DOWNLOAD"]')
    # BTN_DOWNLOAD = (By.NAME, "DOWNLOAD")

    # Interaction methods

    def open_youtube_url(self, url) -> None:
        self.make_search_value(search_str=url, is_press_enter=True, sleep_n_seconds=1)

    def hover_mouse_on_movie_player(self) -> None:
        self.move_to_element(self.MOVIE_PLAYER)
        self.click_and_hold(self.MOVIE_PLAYER)

    def click_btn_download(self) -> None:
        self.double_click_element(self.BTN_DOWNLOAD)
