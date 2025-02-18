from src.pages.base import BaseSelenium
from tests import setting
from selenium.webdriver.common.by import By

lang = setting.coccoc_language


class CocCocAppsPageSel(BaseSelenium):
    # Locators
    CC_LOGO = (By.CSS_SELECTOR, 'img[src="chrome://theme/IDR_PRODUCT_LOGO_32"]')
    CHROME_WEB_STORE_LOGO = (
        By.CSS_SELECTOR,
        'div[id="ahfgeienlihckogmohjhadlkjgocpleb"] img[src="chrome://extension-icon/ahfgeienlihckogmohjhadlkjgocpleb/128/1"]',
    )
    CHROME_APP_LAUNCHER_LOGO = (
        By.CSS_SELECTOR,
        'a[href="https://chrome.google.com/webstore?hl=en-US&utm_source=chrome-ntp-launcher"]',
    )

    # interaction methods:
    def open_coccoc_apps(self):
        self.open_page(url="coccoc://apps/")

    def check_logo_displayed_correctly(self):
        self.open_coccoc_apps()
        assert self.is_element_appeared(self.CC_LOGO)
        assert self.is_element_appeared(self.CHROME_WEB_STORE_LOGO)
        assert self.is_element_appeared(self.CHROME_APP_LAUNCHER_LOGO)
        return self

    def check_links_work_well(self):
        self.open_coccoc_apps()
        self.click_element(self.CHROME_WEB_STORE_LOGO)
        assert (
            self.get_current_url()
            == "https://chrome.google.com/webstore/category/extensions?utm_source=chrome-ntp-icon"
        )
        self.open_coccoc_apps()
        self.click_element(self.CHROME_APP_LAUNCHER_LOGO)
        assert (
            self.get_current_url()
            == "https://chrome.google.com/webstore/category/extensions?hl=en-US&utm_source=chrome-ntp-launcher"
        )
