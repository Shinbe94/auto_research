from time import sleep

from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium, BasePlaywright, BaseSelenium
from tests import setting

lang = setting.coccoc_language


class TaskManagerAppium(BaseAppium):
    """This class is for manage the Coccoc Task manager

    Args:
        BaseAppium (_type_): _description_
    """

    # Locator:
    if "en" in lang:
        TORRENT_PROCESS = (By.NAME, "Torrent Process")
    else:
        TORRENT_PROCESS = (By.NAME, "Tiến trình Torrent")

    if "en" in lang:
        END_PROCESS = (By.NAME, "End process")
    else:
        END_PROCESS = (By.NAME, "Kết thúc quá trình")

    # Interaction methods
    def click_cancel_btn(self) -> None:
        self.click_element(self.BTN_CANCEL)

    def end_torrent_process(self) -> None:
        self.click_element(self.TORRENT_PROCESS)
        sleep(5)
        self.click_element(self.END_PROCESS)
