import time

from src.pages.savior.phimplay_page import PhimplayPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestPhimplay(SaviorBaseTest):
    def test_phimplay(self):
        self.phimplay_page = PhimplayPage(self)
        file_name = None
        try:
            data = self.phimplay_page.open_phimplay("https://phimplay.com/phim-le/")
            self.phimplay_page.click_btn_download()
            file_name = self.phimplay_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(1)
