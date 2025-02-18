from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from appium.webdriver import WebElement

from tests import setting


class DownloadBar(BaseAppium):
    lang = setting.coccoc_language
    # Locators
    if lang == "en":
        DOWNLOAD_BAR = (By.NAME, "Downloads bar")
    else:
        DOWNLOAD_BAR = (By.NAME, "Thanh tệp đã tải xuống")
    if lang == "en":
        BTN_SHOW_ALL = (By.NAME, "Show all")
    else:
        BTN_SHOW_ALL = (By.NAME, "Hiển thị tất cả")

    if lang == "en":
        BTN_CLOSE_DOWNLOAD_BAR = (
            By.XPATH,
            r'/Pane[@ClassName="#32769"][@Name="Desktop 1"]/Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Downloads - Cốc Cốc"]/Pane/Pane/Pane/Group[@Name="Downloads bar"]/Button[@Name="Close"]',
        )
    else:
        BTN_CLOSE_DOWNLOAD_BAR = (By.NAME, "Đóng")
    ALL_ELE = (
        By.XPATH,
        r'/Pane[@ClassName="#32769"][@Name="Desktop 1"]/Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Downloads - Cốc Cốc"]/Pane/Pane/Pane/Group[@Name="Downloads bar"]/',
    )

    # Interaction methods
    def is_download_bar_shown(self):
        assert self.get_element(self.DOWNLOAD_BAR)

    def click_btn_show_all(self):
        self.click_element(self.BTN_SHOW_ALL)

    def click_close_download_bar(self):
        self.click_element(self.BTN_CLOSE_DOWNLOAD_BAR)

    def print_ele(self):
        eles = self.get_elements(self.ALL_ELE)
        for ele in eles:
            print(ele)
