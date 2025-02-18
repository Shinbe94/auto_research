import os
import time

from tests.savior.savior_base_test import SaviorBaseTest
from src.pages.savior.kenh14_page import Kenh14Page
from src.utilities import os_utils, file_utils, media_utils


class TestKenh14(SaviorBaseTest):
    def test_kenh14(self):
        self.kenh14_page = Kenh14Page(self)
        file_name = None
        try:
            self.kenh14_page.open_kenh14("https://video.kenh14.vn/")
            media_duration_from_site = self.kenh14_page.get_video_duration()
            self.kenh14_page.click_btn_download()
            file_name = self.kenh14_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
