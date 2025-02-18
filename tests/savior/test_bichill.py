import time

from src.pages.savior.bichill_page import BichillPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestBichill(SaviorBaseTest):
    def test_Bichill(self):
        self.bichill_page = BichillPage(self)
        file_name = None
        try:
            data = self.bichill_page.open_bichill("https://bichill.net/phim-bo")
            self.bichill_page.click_btn_download()
            file_name = self.bichill_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert data[0] == file_utils.get_media_duration(file_name)
            assert data[1] == file_utils.get_extension_of_file(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(1)
