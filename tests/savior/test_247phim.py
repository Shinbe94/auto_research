import time

from src.pages.savior.phim247_page import Phim247Page
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestPhunuvagiadinh(SaviorBaseTest):
    def test_phunuvagiadinh(self):
        self.phim247_page = Phim247Page(self)
        file_name = None
        try:
            data = self.phim247_page.open_phim247(
                "https://247phim.com/phim/khong-the-bo-lo?xem-them=1"
            )
            self.phim247_page.click_btn_download()
            file_name = self.phim247_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(1)
