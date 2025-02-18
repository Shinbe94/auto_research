import time

from appium.webdriver.webelement import WebElement as AppiumElement
from pywinauto import Application
from pywinauto.keyboard import send_keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from src.pages.constant import AWADL, CocCocTitles
from tests import setting

lang = setting.coccoc_language


class Topbar(BaseAppium):
    # Locators
    if "en" in lang:
        NEW_TAB_TITLE_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="New Tab - Cốc Cốc"]/Pane/Pane/Pane/Pane/Tab/Pane/Pane',
        )
    else:
        NEW_TAB_TITLE_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Thẻ mới - Cốc Cốc"]/Pane/Pane/Pane/Pane/Tab/Pane/Pane',
        )
    if "en" in lang:
        BTN_NEW_TAB = (By.NAME, "New Tab")
    else:
        BTN_NEW_TAB = (By.NAME, "Thẻ mới")

    if "en" in lang:
        BTN_NEW_TAB_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Tab/Button[@Name="New Tab"]',
        )
    else:
        BTN_NEW_TAB_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Tab/Button[@Name="Thẻ mới"]',
        )
    if "en" in lang:
        BTN_CLOSE = (By.NAME, "Close")
    else:
        BTN_CLOSE = (By.NAME, "Đóng")
    if "en" in lang:
        BTN_CLOSE_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]//Button[@Name="Close"]',
        )
    else:
        BTN_CLOSE_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]//Button[@Name="Đóng"]',
        )

    if "en" in lang:
        BTN_YES = (By.NAME, "Yes")
    else:
        BTN_YES = (By.NAME, "Có")
    if "en" in lang:
        BTN_YES_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]/Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Yes"]',
        )
    else:
        BTN_YES_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]/Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Có"]',
        )

    # Interaction Methods
    def check_new_tab_opening(self) -> None:
        """
        To the new tab is opening
        """
        assert self.is_element_appeared(self.NEW_TAB_TITLE_XPATH)

    def check_no_new_tab_opening(self) -> None:
        """
        To Check the new tab is not opening
        """
        assert self.is_element_disappeared(self.NEW_TAB_TITLE_XPATH)

    def click_new_tab_title(self) -> None:
        self.click_element(self.NEW_TAB_TITLE_XPATH)

    def click_yes_btn(self) -> None:
        if self.is_element_appeared(self.BTN_YES_XPATH, timeout=2):
            self.click_element(self.BTN_YES_XPATH)

    def click_btn_minimize_window(self, window_name: str) -> None:
        locator = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{window_name}"]//Button[@Name="Minimize"]',
        )
        self.click_element(locator)

    def check_newtab_by_title(self, title: str) -> bool:
        NEW_TAB_BY_TITLE_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{title}"]/Pane/Pane/Pane/Pane/Tab/Pane/Pane',
        )
        assert self.is_element_appeared(NEW_TAB_BY_TITLE_XPATH)

    def get_close_btn_locator(
        self, window_title: str = CocCocTitles.NEW_TAB_TITLE
    ) -> tuple:
        if "en" in lang:
            return (
                By.XPATH,
                f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{window_title}"]//Button[@Name="Close"]',
            )
        else:
            return (
                By.XPATH,
                f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{window_title}"]//Button[@Name="Đóng"]',
            )

    def click_close_btn(
        self, window_title: str = CocCocTitles.NEW_TAB_TITLE, is_close_completed=False
    ) -> None:
        # self.click_element(self.BTN_CLOSE)
        self.click_element(self.get_close_btn_locator(window_title=window_title))
        if is_close_completed:
            if self.is_element_appeared(self.BTN_YES_XPATH, timeout=2):
                self.click_element(self.BTN_YES_XPATH)

    def switch_tab_by_its_name(self, tab_title: str) -> None:
        TAB_TITLE = (By.NAME, f"{tab_title}")
        # self.move_to_element(TAB_TITLE)
        self.click_element(TAB_TITLE)
