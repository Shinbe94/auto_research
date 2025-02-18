import time

from src.pages.savior.vtvgo_page import VtvgoPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import file_utils, os_utils, media_utils


class TestVtvgo(SaviorBaseTest):
    def test_download_video(self):
        self.vtvgo_page = VtvgoPage(self)
        file_name = None
        try:
            self.vtvgo_page.open_vtvgo("https://vtvgo.vn/tin-tuc.html")
            media_duration_from_site = self.vtvgo_page.get_video_duration()
            self.vtvgo_page.click_btn_download()
            file_name = self.vtvgo_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
