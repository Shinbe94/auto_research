import os
import time

from src.pages.savior.vietbao_page import VietbaoPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestVietbao(SaviorBaseTest):
    def test_vietbao(self):
        self.vietbao_page = VietbaoPage(self)
        file_name = None
        try:
            media_duration_from_site = self.vietbao_page.open_vietbao(
                "https://vietbao.vn/video"
            )
            # media_duration_from_site = self.vietbao_page.get_video_duration()
            self.vietbao_page.click_btn_download()
            file_name = self.vietbao_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
