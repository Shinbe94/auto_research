from src.pages.base import BaseSelenium
from tests import setting
from selenium.webdriver.common.by import By

lang = setting.coccoc_language


class CocCocURLSel(BaseSelenium):
    # Locators
    LIST_URL_COCCOC = (By.CSS_SELECTOR, "ul li a")
    LIST_DEBUG_URL_COCCOC = (By.CSS_SELECTOR, "ul li")

    # interaction methods:
    def open_coccoc_url(self):
        self.open_page(url="coccoc://coccoc-urls/")

    def check_cococ_scheme_correct(self) -> None:
        self.open_coccoc_url()
        for ele in self.get_elements(self.LIST_URL_COCCOC):
            assert "coccoc://" in ele.text
            assert "chrome://" not in ele.text
        for ele in self.get_elements(self.LIST_DEBUG_URL_COCCOC):
            assert "coccoc://" in ele.text
            assert "chrome://" not in ele.text
