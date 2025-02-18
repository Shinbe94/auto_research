import time

from pywinauto import Application

from src.pages.base import BaseAppium
from selenium.webdriver.common.by import By
from appium.webdriver.webelement import WebElement as AppiumElement

from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles
from tests import setting

lang = setting.coccoc_language


class BookmarkBar(BaseAppium):
    # Locators

    if "en" in lang:
        EDIT_BOOKMARK_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit bookmark"]',
        )
    else:
        EDIT_BOOKMARK_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa dấu trang"]',
        )

    if "en" in lang:
        BOOKMARK_ADDED_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Bookmark added"]',
        )
    else:
        BOOKMARK_ADDED_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Đã thêm dấu trang"]',
        )

    if "en" in lang:
        EDIT_BOOKMARK_DIALOG_BTN_CLOSE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit bookmark"]//Button[@Name="Close"]',
        )
    else:
        EDIT_BOOKMARK_DIALOG_BTN_CLOSE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa dấu trang"]//Button[@Name="Đóng"]',
        )

    if "en" in lang:
        BOOKMARK_BAR = (By.XPATH, '//ToolBar[@Name="Bookmarks"]')
    else:
        BOOKMARK_BAR = (By.XPATH, '//ToolBar[@Name="Dấu trang"]')

    # Interaction methods
    def check_bookmark_exist(self, name: str):
        xpath_locator = (
            By.XPATH,
            rf'//ToolBar[@Name="Bookmarks"]/Button[@Name="{name}"]',
        )
        assert self.get_element(xpath_locator)

    def check_bookmark_is_not_exist(self, name: str):
        xpath_locator = (
            By.XPATH,
            rf'//ToolBar[@Name="Bookmarks"]/Button[@Name="{name}"]',
        )
        assert self.is_element_disappeared(xpath_locator)

    def check_bookmar_bar_shown(self) -> None:
        assert self.is_element_appeared(self.BOOKMARK_BAR)

    def check_bookmar_bar_hidden(self) -> None:
        assert self.is_element_disappeared(self.BOOKMARK_BAR)
