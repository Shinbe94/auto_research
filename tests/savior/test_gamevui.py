import os
import time

from src.pages.savior.gamevui_page import GamevuiPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestGamevui(SaviorBaseTest):
    def test_gamevui(self):
        self.gamevui_page = GamevuiPage(self)
        file_name = None
        try:
            media_duration_from_site = self.gamevui_page.open_gamevui(
                "https://gamevui.vn/video"
            )
            # media_duration_from_site = self.vietbao_page
            # .get_video_duration()
            self.gamevui_page.click_btn_download()
            file_name = self.gamevui_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
