import os
import time

from tests.savior.savior_base_test import SaviorBaseTest
from src.pages.savior.tiktok_page import TiktokPage
from src.utilities import os_utils, file_utils, media_utils


class TestTiktok(SaviorBaseTest):
    def test_tiktok(self):
        self.tiktok_page = TiktokPage(self)
        file_name: str = ""
        try:
            self.tiktok_page.open_tiktok("https://www.tiktok.com/")
            media_duration_from_site = self.tiktok_page.get_video_duration()
            self.tiktok_page.click_btn_download()
            file_name = self.tiktok_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == media_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            os.remove(file_name)
        time.sleep(3)
