import os
import time

from src.pages.savior.dailymotion_page import DailymotionPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestDailymotion(SaviorBaseTest):
    def test_dailymotion(self):
        self.dailymotion_page = DailymotionPage(self)
        file_name = None
        try:
            data = self.dailymotion_page.open_dailymotion(
                "https://www.dailymotion.com/vn"
            )
            file_name = self.dailymotion_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
