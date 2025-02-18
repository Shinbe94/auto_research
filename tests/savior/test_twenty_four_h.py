import os
import time

from tests.savior.savior_base_test import SaviorBaseTest
from src.pages.savior.twenty_four_h_page import TwentyFourHPage
from src.utilities import os_utils, file_utils, media_utils


class Test24HCom(SaviorBaseTest):
    def test_24h(self):
        self.twenty_four_h = TwentyFourHPage(self)
        file_name = None
        try:
            self.twenty_four_h.open_24h("https://www.24h.com.vn/tong-hop-video.html")
            media_duration_from_site = self.twenty_four_h.get_video_duration()
            self.twenty_four_h.click_btn_download()
            file_name = self.twenty_four_h.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
