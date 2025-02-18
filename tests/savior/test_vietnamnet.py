import time

from src.pages.savior.vietnamnet_page import VietnamnetPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import file_utils, os_utils, media_utils


class TestVietnamnet(SaviorBaseTest):
    def test_download_video(self):
        self.vietnamnet_page = VietnamnetPage(self)
        file_name = None
        try:
            self.vietnamnet_page.open_vietnamnet("https://vietnamnet.vn/video")
            media_duration_from_site = self.vietnamnet_page.get_video_duration()
            self.vietnamnet_page.click_btn_download()
            file_name = self.vietnamnet_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
