import time

from src.pages.savior.animehay_page import AnimehayPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestAnimehay(SaviorBaseTest):
    def test_animehay(self):
        self.animehay_page = AnimehayPage(self)
        file_name = None
        try:
            data = self.animehay_page.open_animehay("https://animehay.club/")
            self.animehay_page.click_btn_download()
            file_name = self.animehay_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(1)
