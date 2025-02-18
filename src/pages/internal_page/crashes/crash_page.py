import time

from src.pages.base import BaseAppium
from tests import setting
from selenium.webdriver.common.by import By


class CrashPage(BaseAppium):
    lang = setting.coccoc_language
    # Locators
    RELOAD_BTN = (By.NAME, "Reload")
    ADDRESS_AND_SEARCH_BAR = (By.NAME, "Address and search bar")

    # Interaction methods

    def open_crash_page(self):
        self.fill_texts(
            self.ADDRESS_AND_SEARCH_BAR, "coccoc://crash ", is_press_enter=True
        )
        time.sleep(1)

    def click_reload_btn(self):
        self.click_element(self.RELOAD_BTN)
        time.sleep(1)
