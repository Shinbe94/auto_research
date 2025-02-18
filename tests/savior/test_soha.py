import time

from src.pages.savior.soha_page import SohaPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestSoha(SaviorBaseTest):
    def test_soha(self):
        self.soha_page = SohaPage(self)
        file_name = None
        try:
            data = self.soha_page.open_soha("https://soha.vn/video.htm")
            self.soha_page.click_btn_download()
            file_name = self.soha_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(1)
