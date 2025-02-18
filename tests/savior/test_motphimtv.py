import time

from src.pages.savior.motphimtv_page import MotphimtvPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import file_utils, os_utils, media_utils


class TestMotphimtv(SaviorBaseTest):
    def test_motphimtv(self):
        self.motphimtv_page = MotphimtvPage(self)
        file_name = None
        try:
            media_duration_from_site = self.motphimtv_page.open_motphimtv(
                "https://motphimtv.tv/phim-bo/"
            )
            # media_duration_from_site = self.motphimtv_page.get_video_duration()
            self.motphimtv_page.click_btn_download()
            file_name = self.motphimtv_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == file_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)
