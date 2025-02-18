import time

from pywinauto import Application

from tests import setting
from src.pages.coccoc_common import open_browser
from src.pages.savior.vnexpress_page import VnexpressPage
from tests.savior.savior_base_test import SaviorBaseTest
from src.utilities import os_utils, file_utils, media_utils


class TestVnexpress(SaviorBaseTest):
    def test_vnexpress(self):
        self.vnexpress_page = VnexpressPage(self)
        file_name = None
        try:
            self.vnexpress_page.open_vnexpress("https://video.vnexpress.net/")
            media_duration_from_site = self.vnexpress_page.get_video_duration()
            self.vnexpress_page.click_btn_download()
            file_name = self.vnexpress_page.wait_for_downloads(
                rf"C:\Users\{os_utils.get_username()}\Downloads"
            )
            assert media_duration_from_site == media_utils.get_media_duration(file_name)
            assert "video" == media_utils.check_media_type(file_name)
        finally:
            if file_name is not None:
                file_utils.remove_a_file(file_name)
        time.sleep(3)


class TestOmni:
    def test_vnexpress_omnibox(self):
        coccoc = open_browser.open_and_connect_coccoc_by_selenium()
        driver = coccoc[0]
        window = coccoc[1]
        driver.get("https://video.vnexpress.net/")
        text = driver.title

        coccoc_title = text + " - Cốc Cốc"
        # window[coccoc_title].close()
        # print(text)
        # window[f'{text} - Cốc Cốc'].print_control_identifiers()
        time.sleep(8)
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=coccoc_title,
            timeout=setting.timeout_pywinauto,
        )
        app[coccoc_title].child_window(
            title_re="Download video, audio", control_type=50000
        ).click()
        app[coccoc_title].child_window(
            class_name="Chrome_WidgetWin_1", control_type=50033, found_index=0
        ).print_control_identifiers()
        app[coccoc_title].child_window(
            class_name="Chrome_WidgetWin_1", control_type=50033, found_index=0
        ).child_window(
            title="Download has failed to start. Try with different format or quality.",
            control_type="Text",
        ).click()

        # window[coccoc_title].print_control_identifiers()
