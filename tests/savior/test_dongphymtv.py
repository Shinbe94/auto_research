import os
import time

from src.pages.savior.dongphymtv_page import DongphymtvPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestDongphymtv(SaviorBaseTest):
    def test_dongphymtv(self):
        self.dongphymtv_page = DongphymtvPage(self)
        file_name = None
        try:
            data = self.dongphymtv_page.open_dongphymtv(
                "https://dongphymtv.com/phim-bo"
            )
            file_name = self.dongphymtv_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
