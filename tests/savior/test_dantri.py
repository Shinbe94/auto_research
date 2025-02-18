import time

from tests.savior.savior_base_test import SaviorBaseTest
from src.pages.savior.dantri_page import DantriPage
from src.utilities import os_utils, file_utils, media_utils


class TestDantri(SaviorBaseTest):
    def test_dantri(self):
        self.dantri_page = DantriPage(self)
        file_name = None
        try:
            self.dantri_page.open_dantri("https://dantri.com.vn/video-page.htm")
            media_duration_from_site = self.dantri_page.get_video_duration()
            self.dantri_page.click_btn_download()

            file_name = self.dantri_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
