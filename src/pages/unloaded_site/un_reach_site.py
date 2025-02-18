from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from src.pages.constant import AWADL
from tests import setting

lang = setting.coccoc_language


class UnReachSite(BaseAppium):
    """
    this class is for checking some sites are unnable to load
    Args:
        BaseAppium (_type_): _description_
    """

    # Locators
    if lang == "en":
        BTN_RETRY_WITH_TOR = (By.NAME, "Retry with Tor")
    else:
        BTN_RETRY_WITH_TOR = (By.NAME, "Thử lại với Tor")
    if lang == "en":
        THIS_SITE_CANT_BE_REACHED = (By.NAME, "This site can't be reached")
    else:
        THIS_SITE_CANT_BE_REACHED = (By.NAME, "Không thể truy cập trang web này")

    if lang == "en":
        THERE_IS_TYPO = (By.NAME, "Check if there is a typo in ")
    else:
        THERE_IS_TYPO = (By.NAME, "Kiểm tra xem có lỗi chính tả trong ")

    RELOAD_BTN = (AWADL.AUTOMATION_ID, "reload-button")

    # Interaction methods

    def click_btn_retry_with_tor(self):
        wait = WebDriverWait(self.wad, 120)
        element = wait.until(EC.presence_of_element_located(self.BTN_RETRY_WITH_TOR))
        element.click()

    def is_retry_with_tor_btn_show(self, timeout=setting.timeout_for_tor):
        """
        Wait for the "Retry with Tor" button shown
        Args:
            timeout (int, optional): _description_. Defaults to setting.time_out_for_tor.
        """
        assert self.is_element_appeared(self.BTN_RETRY_WITH_TOR, timeout=timeout)

    def check_this_site_cant_be_reached(self):
        assert self.is_element_appeared(self.THIS_SITE_CANT_BE_REACHED)

    def check_there_is_a_type_in(self):
        assert self.is_element_appeared(self.THERE_IS_TYPO)

    @staticmethod
    def check_new_tor_window_opened(window_name: str):
        assert open_browser.is_coccoc_tor_window_appeared(title=window_name)
