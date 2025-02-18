import time

from src.pages.savior.zingnew_page import ZingnewsPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestZingnews(SaviorBaseTest):
    def test_zingnews(self):
        self.zingnews_page = ZingnewsPage(self)
        file_name = None
        try:
            self.zingnews_page.open_zingnews("https://zingnews.vn/video")
            media_duration_from_site = self.zingnews_page.get_video_duration()
            self.zingnews_page.click_btn_download()
            file_name = self.zingnews_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
