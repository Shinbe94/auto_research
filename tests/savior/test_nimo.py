import time

from src.pages.savior.nimo_page import NimoPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils


class TestNimo(SaviorBaseTest):
    def test_nimo(self):
        self.nimo_page = NimoPage(self)
        file_name = None
        try:
            self.nimo_page.open_nimo("https://zingnews.vn/video")
            self.nimo_page.click_btn_download()
            file_name = self.nimo_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
