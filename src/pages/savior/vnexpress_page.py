import time
from selenium.webdriver.common.by import By

from src.pages.savior.savior_base_page import SaviorBasePage


class VnexpressPage(SaviorBasePage):
    VIDEO_AREA = (By.CSS_SELECTOR, 'div[id="block_video_html5"]')
    VIDEO_VNEXPRESS_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
    CURRENT_PLAYING_TIME = (By.CSS_SELECTOR, 'span[class="vjs-current-time-display"]')
    VIDEO_DURATION = (By.CSS_SELECTOR, 'span[class="vjs-duration-display"]')

    def open_vnexpress(self, url):
        self.get_url(url)
        time.sleep(3)
        self.click(self.VIDEO_AREA)
        time.sleep(4)
        self.wait_for_the_video_is_playing(self.CURRENT_PLAYING_TIME)
        self.hover_on_element(self.VIDEO_AREA)
        self.wait_for_prefetch_savior_dock()
        # self.show_savior_dock()
        self.click_preferred_quality_dropdown()
        time.sleep(3)
        # self.select_media_quality_js_path()
        self.select_random_media_quality_js_path()

    def get_video_duration(self):
        return self.get_media_duration_from_site(self.VIDEO_DURATION)

    def is_video_playing(self):
        js = """
                    div = document.createElement('div');
                    div.id = 'output';
                    document.body.append(div);
                """
        video_state_js = """
                    const media = document.getElementById('vne_vod_html5_api');
                    const output = document.getElementById('output');

                    media.addEventListener("playing", () => {
                      output.innerHTML = "Playing event triggered";
                    });

                    media.addEventListener("pause", () => {
                      output.innerHTML = "Pause event triggered";

                    });

                    media.addEventListener("seeking", () => {
                      output.innerHTML = "Seeking event triggered";
                    });

                    media.addEventListener("volumechange", () => {
                      output.innerHTML = "Volumechange event triggered";
                    });
                """
        self.execute_js(js)
        self.execute_js(video_state_js)
        VIDEO_VNEXPRESS_PLAY_BTN = (By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]')
        self.click(VIDEO_VNEXPRESS_PLAY_BTN)
        time.sleep(3)
        self.click(VIDEO_VNEXPRESS_PLAY_BTN)
        self.click(VIDEO_VNEXPRESS_PLAY_BTN)
        is_not_playing = True
        video_status_ele = (By.ID, 'output')

        max_delay = 30
        interval_delay = 0.5
        total_delay = 0

        while is_not_playing:
            try:
                if self.driver.find_element(*video_status_ele).get_attribute('innerText') == 'Playing event triggered':
                    is_not_playing = False
                    print('The video is playing')
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    is_not_playing = False
                    print('Timeout for the video playing')
                    break
            finally:
                print('The video is not playing')
