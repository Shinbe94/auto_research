import time
from typing import List
from selenium.webdriver.common.by import By
from src.pages.base import BaseAppium, BasePlaywright
from playwright.sync_api import Locator, expect, sync_playwright

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from tests import setting

lang = setting.coccoc_language


class SettingsCookies(BasePlaywright):
    """This class is for settings cookies based on playwright

    Args:
        BasePlaywright (_type_): _description_

    Returns:
        _type_: _description_
    """

    @property
    def list_site_allow_cookies(self) -> List[Locator]:
        return self.page.locator(
            '#allowExceptionsList span[class="url-directionality"]'
        ).all()

    @property
    def allow_exception_list_part(self) -> Locator:
        return self.page.locator("#allowExceptionsList")

    # Interaction methods
    def open_page_setting_cookies(self):
        self.page.goto("coccoc://settings/cookies", timeout=60000)

    def get_list_site_allowed_cookies(self) -> list:
        """
        To return the list allowed cookies
        Returns: empty list if no, list if have
        """
        self.open_page_setting_cookies()
        self.allow_exception_list_part.scroll_into_view_if_needed()
        list_sites = []
        if len(self.list_site_allow_cookies) > 0:
            for element in self.list_site_allow_cookies:
                list_sites.append(element.text_content())
            # print(list_sites)
            return list_sites
        else:
            return list_sites


class SettingsCookiesAppium(BaseAppium):
    """This class is for settings cookies base on appium + winappdriver

    Args:
        BaseAppium (_type_): _description_
    """

    # Locator:
    if "en" in lang:
        RATIO_ALLOW_ALL_COOKIES = (By.NAME, "Allow all cookies")
    else:
        RATIO_ALLOW_ALL_COOKIES = (By.NAME, "Cho phép tất cả cookie")

    if "en" in lang:
        RATIO_BLOCK_3RD_COOLKIES_IN_INCOGNITO = (
            By.NAME,
            "Block third-party cookies in Incognito",
        )
    else:
        RATIO_BLOCK_3RD_COOLKIES_IN_INCOGNITO = (
            By.NAME,
            "Chặn các cookie của bên thứ ba trong chế độ Ẩn danh",
        )

    if "en" in lang:
        RATIO_BLOCK_3RD_COOKIES = (By.NAME, "Block third-party cookies")
    else:
        RATIO_BLOCK_3RD_COOKIES = (By.NAME, "Chặn cookie của bên thứ ba")

    if "en" in lang:
        RATIO_BLOCK_ALL_COOKIES = (By.NAME, "Block all cookies (not recommended)")
    else:
        RATIO_BLOCK_ALL_COOKIES = (By.NAME, "Chặn tất cả cookie (không khuyến nghị)")

    # Interaction methods
    def tick_ratio_allow_all_cookies(self) -> None:
        self.click_element(self.RATIO_ALLOW_ALL_COOKIES)

    def tick_ratio_block_3rd_cookies_in_incognito(self) -> None:
        self.click_element(self.RATIO_BLOCK_3RD_COOLKIES_IN_INCOGNITO)

    def tick_ratio_block_3rd_cookies(self) -> None:
        self.click_element(self.RATIO_BLOCK_3RD_COOKIES)

    def tick_ratio_block_all_cookies(self) -> None:
        self.click_element(self.RATIO_BLOCK_ALL_COOKIES)
