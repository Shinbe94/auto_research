import time

from selenium.webdriver.common.by import By

from src.pages.base import BasePlaywright, BaseSelenium
from playwright.sync_api import Locator, expect, sync_playwright

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser, interactions
from src.pages.constant import CocCocSettingTitle
from tests import setting

lang = setting.coccoc_language


class FlagsPage(BasePlaywright):
    @property
    def btn_reset_all(self) -> Locator:
        return self.page.locator("#experiment-reset-all")

    @property
    def btn_relaunch(self) -> Locator:
        return self.page.locator("#experiment-restart-button")

    # Interaction methods
    def open_page(self):
        self.page.goto("coccoc://flags/")

    def select_option(self, css_flag_id: str, option: str):
        assert option in ["Default", "Enable", "Disable"]

        self.page.locator(css_flag_id).scroll_into_view_if_needed()
        self.page.locator(
            rf'{css_flag_id} div[class="flex experiment-actions"]'
        ).click()
        self.page.locator(
            rf'{css_flag_id} select[class="experiment-select"] option'
        ).select_option(option)
        # self.page.get_by_role("combobox", name=flag_id).select_option(option)

    def click_btn_relaunch(self):
        self.btn_relaunch.click()
        self.accept_dialog()

    def click_btn_reset_all(self):
        self.btn_reset_all.click()

    def change_status_flag(self, css_flag_id: str, option: str):
        self.open_page()
        self.select_option(css_flag_id, option)
        self.click_btn_relaunch()


"""Outside of class"""


def change_flag_status(flag_id: str, status: str):
    drop_down = (By.CSS_SELECTOR, rf"#{flag_id} select.experiment-select")
    relaunch_btn = (By.CSS_SELECTOR, "#experiment-restart-button")
    driver = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    try:
        driver.get("coccoc://flags/")
        interactions.scroll_to_element(driver, drop_down)
        interactions.scroll_up_down(driver, y=-150)
        interactions.click_element(driver, drop_down)
        interactions.select_by_visible_text(driver, drop_down, status)
        if (
            interactions.get_attribute_value_by_element(
                interactions.get_element(driver, relaunch_btn), "tabindex"
            )
            == "9"
        ):
            interactions.click_element(driver, relaunch_btn)
        # driver.find_element(*element_flag_name)
    finally:
        driver.quit()
        open_browser.close_coccoc_by_window_title(title=CocCocSettingTitle.COCCOC_FLAGS)


class FlagsPageSel(BaseSelenium):
    # locator
    if "en" in lang:
        SEARCH_NO_RESULTS_TEXT = (By.XPATH, '//div[text()="No search results found"]')
    else:
        SEARCH_NO_RESULTS_TEXT = (
            By.XPATH,
            '//div[text()="Không tìm thấy kết quả tìm kiếm nào"]',
        )

    NO_FLAGS_SEARCH_MATCH = (
        By.XPATH,
        '//div[text()="No matching experiments" and @class="no-match"]',
    )

    def get_dropdown(self, flag_id: str) -> tuple:
        return (By.CSS_SELECTOR, f"#{flag_id} select.experiment-select")

    def get_locator_flag_status(self, flag_id: str) -> tuple:
        return (
            By.CSS_SELECTOR,
            f"#{flag_id} div.flex.experiment-actions > div > select",
        )

    RELAUNCH_BTN = (By.CSS_SELECTOR, "#experiment-restart-button")
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[id="search"]')
    COCCOC_AI_JSPATH = r'document.querySelector("#coccoc-sidebar-ai > flags-experiment").shadowRoot.querySelector("#coccoc-sidebar-ai div.flex.experiment-actions > select")'
    COCCOC_AI_JSPATH_DEFAULT = r'document.querySelector("#coccoc-sidebar-ai > flags-experiment").shadowRoot.querySelector("#coccoc-sidebar-ai div.flex.experiment-actions > select option:nth-child(1)")'
    COCCOC_AI_JSPATH_ENABLE = r'document.querySelector("#coccoc-sidebar-ai > flags-experiment").shadowRoot.querySelector("#coccoc-sidebar-ai div.flex.experiment-actions > select option:nth-child(2)")'
    COCCOC_AI_JSPATH_DISABLE = r'document.querySelector("#coccoc-sidebar-ai > flags-experiment").shadowRoot.querySelector("#coccoc-sidebar-ai div.flex.experiment-actions > select option:nth-child(3)")'

    # Interaction methods

    def open_flags_page(self, url="coccoc://flags/"):
        self.open_page(url=url)

    def change_flag_status(self, flag_id: str, status: str) -> None:
        self.open_flags_page(url=f"coccoc://flags/#{flag_id}")
        if self.get_status_flag(flag_id) != status:
            # self.click_element(self.get_dropdown(flag_id))
            # self.select_by_visible_text(
            #     by_locator=self.get_dropdown(flag_id), text=status
            # )
            self.click_shadow_element(self.COCCOC_AI_JSPATH)
            if status == "Default":
                self.click_shadow_element(self.COCCOC_AI_JSPATH_DEFAULT)
            elif status == "Enabled":
                self.click_shadow_element(self.COCCOC_AI_JSPATH_ENABLE)
            elif status == "Disabled":
                self.click_shadow_element(self.COCCOC_AI_JSPATH_DISABLE)
            else:
                raise ValueError(f"{status} is not valid")
                # if (
                #     self.get_element_attribute_by_its_name_and_locator(
                #         self.RELAUNCH_BTN, "tabindex"
                #     )
                #     == "9"
                # ):
            # self.click_element(self.RELAUNCH_BTN)

    def get_status_flag(self, flag_id: str, is_need_to_open_page=True) -> str:
        if is_need_to_open_page:
            self.open_flags_page(url=f"coccoc://flags/#{flag_id}")
        # return self.get_element_attribute_by_its_name_and_locator(
        #     self.get_locator_flag_status(flag_id), "value"
        # )
        return self.get_attribute_value_of_shadow_element(
            js_path=self.COCCOC_AI_JSPATH,
            attribute_name="value",
        )

    def make_search_at_flags_page(self, search_str: str):
        self.open_flags_page()
        self.fill_texts(self.SEARCH_INPUT, search_str, is_press_enter=True)
        return self

    def verify_search_no_results(self) -> None:
        assert self.is_element_appeared(self.NO_FLAGS_SEARCH_MATCH)
