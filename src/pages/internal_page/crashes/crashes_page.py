import time

from selenium.webdriver.common.by import By

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright, BaseSelenium
from src.utilities import os_utils, file_utils
from tests import setting

lang = setting.coccoc_language


class CrashesPage(BasePlaywright):
    @property
    def btn_try_now(self) -> Locator:
        return self.page.locator('button[class="onboarding-btn"]')

    @property
    def text_crashes(self) -> Locator:
        return self.page.locator('//h1[text()="Crashes"]')

    # Interaction methods

    def open_page_crashes_page(self):
        self.page.goto("coccoc://crashes/")
        time.sleep(2)

    def check_no_provide_additional_details_show(self):
        self.open_page_crashes_page()
        if lang == "en":
            try:
                element = self.page.get_by_text("Show 1develop23123er details")
                print(element)
            except Exception as e:
                print(e)
            # expect(self.page.get_by_text('Provide additional details'))
        else:
            expect(
                self.page.get_by_text("Cung cấp chi tiết bổ sung")
            ).not_to_be_visible()


class CrashesPageSel(BaseSelenium):
    # Locators
    TEXT_CRASHES = (By.XPATH, '//h1[text()="Crashes"]')

    # Interaction methods
    def open_crashes_page(self) -> None:
        self.open_page(url="coccoc://crashes/")

    def double_click_text_crashes(self) -> None:
        self.open_crashes_page()
        self.double_click_element(self.TEXT_CRASHES)


# Open a coccoc then reload repeatedly and wait for the metrics sent
def wait_for_crash_report_is_sent(timeout=3700) -> bool:
    max_delay = timeout
    interval_delay = 10
    total_delay = 0
    metrics_json = (
        rf"C:\Users\{os_utils.get_username()}\Documents\crash_report_log.json"
    )
    while total_delay < max_delay:
        try:
            if file_utils.check_file_is_exists(metrics_json):
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if file_utils.check_file_is_exists(metrics_json):
        return True
    else:
        print(rf"Time out after {timeout} seconds of waiting for the metrics sent")
        return False
