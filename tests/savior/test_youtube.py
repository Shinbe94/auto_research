import os

from tests.savior.savior_base_test import SaviorBaseTest
from src.pages.savior.youtube_page import YoutubePage
from src.utilities import os_utils


class TestYoutube(SaviorBaseTest):
    def test_download_youtube(self):
        self.youtube_page = YoutubePage(self)
        self.youtube_page.open_youtube_url(
            "https://www.youtube.com/watch?v=Vq25ZJwZJzU"
        )
        self.youtube_page.click_btn_download()
        file_name = self.youtube_page.wait_for_downloads(
            rf"C:\Users\{os_utils.get_username()}\Downloads"
        )
        os.remove(file_name)

    def test_download_youtube2(self):
        self.youtube_page = YoutubePage(self)
        self.youtube_page.open_youtube_url(
            "https://www.youtube.com/watch?v=Vq25ZJwZJzU"
        )

    def test_download_youtube3(self):
        self.youtube_page = YoutubePage(self)
        self.youtube_page.open_youtube_url(
            "https://www.youtube.com/watch?v=m-7YVLOgvag"
        )
