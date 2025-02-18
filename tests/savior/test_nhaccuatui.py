import time

from src.pages.savior.nhaccuatui_page import NhaccuatuiPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import file_utils, os_utils, media_utils


class TestNhaccuatui(SaviorBaseTest):
    def test_download_mp3(self):
        self.nhaccuatui_page = NhaccuatuiPage(self)
        file_name = None
        try:
            self.nhaccuatui_page.open_nhaccuatui_mp3(
                "https://www.nhaccuatui.com/bai-hat/bai-hat-moi.html"
            )
            mp3_duration_from_site = self.nhaccuatui_page.get_mp3_duration()
            self.nhaccuatui_page.click_btn_download()
            file_name = self.nhaccuatui_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert mp3_duration_from_site == media_utils.get_media_duration(file_name)
            assert "audio" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)

    def test_download_video(self):
        self.nhaccuatui_page = NhaccuatuiPage(self)
        file_name = None
        try:
            self.nhaccuatui_page.open_nhaccuatui(
                "https://www.nhaccuatui.com/video.html"
            )
            media_duration_from_site = self.nhaccuatui_page.get_video_duration()
            self.nhaccuatui_page.click_btn_download()
            file_name = self.nhaccuatui_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == media_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
