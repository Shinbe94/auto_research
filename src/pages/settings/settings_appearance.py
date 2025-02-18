import time
from typing import List

from src.pages.base import BasePlaywright, BaseSelenium
from playwright.sync_api import Locator, expect, sync_playwright

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from src.pages.constant import LocatorJSPath, CocCocText
from src.utilities import os_utils, file_utils
from tests import setting

lang = setting.coccoc_language


class SettingsAppearance(BasePlaywright):
    @property
    def warning_close_multiple_tabs(self) -> Locator:
        return self.page.locator(
            "#basicPage settings-appearance-page #pages settings-toggle-button.hr"
        )

    @property
    def toggle_btn_warning_close_multiple_tabs(self) -> Locator:
        return self.page.locator(
            '#basicPage settings-appearance-page #pages settings-toggle-button.hr #outerRow cr-toggle[id="control"]'
        )

    # Interaction methods
    def open_page(self):
        self.page.goto("coccoc://settings/appearance")

    def get_toggle_status(self, locator: Locator) -> str:
        return self.get_attribute_value_by_locator(locator, "aria-pressed")

    def turn_of_warning_when_closing_multiple_tabs(self):
        self.open_page()
        if (
            self.get_toggle_status(self.toggle_btn_warning_close_multiple_tabs)
            != "false"
        ):
            self.toggle_btn_warning_close_multiple_tabs.click()


class SettingsAppearanceSel(BaseSelenium):
    # locators
    BTN_OPEN_CHROME_THEME_STORE = f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("#themeRow cr-link-row").shadowRoot.querySelector("#icon")'
    BTN_RESTORE_DEFAULT = (
        f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("#useDefault")'
    )
    TEXT_THEME_NAME = f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("#themeRow cr-link-row").shadowRoot.querySelector("#subLabel")'

    TOGGLE_SHOW_HOME_BTN = f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("settings-toggle-button[label=\'{CocCocText.SHOW_HOME_BTN}\']").shadowRoot.querySelector("#control")'
    RATIO_NEWTAB_PAGE = f"{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector(\"controlled-radio-button[label='{CocCocText.HOME_NEWTAB_PAGE}']\")"
    ENTER_CUSTOM_WEB_ADDRESS = f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("#customHomePage").shadowRoot.querySelector("#input").shadowRoot.querySelector("#input")'

    TOGGLE_SHOW_BOOKMARK_BAR = f'{LocatorJSPath.SETTINGS_APPEAREANCE}.shadowRoot.querySelector("settings-toggle-button[label=\'{CocCocText.SHOW_BOOKMARK_BAR}\']").shadowRoot.querySelector("#control")'

    # interaction methods
    def open_setting_appearance(self):
        self.open_page(url="coccoc://settings/appearance")

    def get_warning_close_multiple_tabs_ele(
        self, is_need_open_setting_appearance_page=False
    ):
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        for ele in self.get_shadow_elements(
            LocatorJSPath.SETTINGS_APPEAREANCE_TOGGLE_ALL
        ):
            if (
                ele.get_attribute("label")
                == CocCocText.WARN_YOU_WHEN_CLOSING_MULTIPLE_TABS
            ):
                return ele

    def get_toggle_status_of_warning_close_multiple_tabs_ele(
        self, is_need_open_setting_appearance_page=True
    ) -> str:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        return (
            "true"
            if self.get_warning_close_multiple_tabs_ele().get_attribute("checked")
            else "false"
        )

    def toggle_on_warning_close_multiple_tabs(self):
        if self.get_toggle_status_of_warning_close_multiple_tabs_ele() != "true":
            self.get_warning_close_multiple_tabs_ele().click()
            assert self.get_toggle_status_of_warning_close_multiple_tabs_ele() == "true"

    def toggle_off_warning_close_multiple_tabs(self):
        if self.get_toggle_status_of_warning_close_multiple_tabs_ele() != "false":
            self.get_warning_close_multiple_tabs_ele().click()
            assert (
                self.get_toggle_status_of_warning_close_multiple_tabs_ele() == "false"
            )

    def open_chrome_web_store_themes(
        self, is_need_open_setting_appearance_page=True
    ) -> None:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        self.click_shadow_element(self.BTN_OPEN_CHROME_THEME_STORE)
        self.wait_for_title(title_text="Chrome Web Store - Themes")

    def restore_default_theme(self, is_need_open_setting_appearance_page=True) -> None:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        if self.is_shadow_element_appeared(self.BTN_RESTORE_DEFAULT, timeout=4):
            self.click_shadow_element(self.BTN_RESTORE_DEFAULT)
            assert self.get_theme_name() == CocCocText.OPEN_CHROME_STORE_TEXT
            time.sleep(5)

    def get_theme_name(self, is_need_open_setting_appearance_page=True) -> str:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        return self.get_text_shadow_element(self.TEXT_THEME_NAME)

    def get_status_toggle_show_home_button(
        self, is_need_open_setting_appearance_page=False
    ) -> str:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_SHOW_HOME_BTN, attribute_name="aria-pressed"
        )

    def toggle_on_show_home_button(self, is_need_open_setting_appearance_page=True):
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        if self.get_status_toggle_show_home_button() != "true":
            self.click_shadow_element(self.TOGGLE_SHOW_HOME_BTN)
            assert self.get_status_toggle_show_home_button() == "true"

    def toggle_off_show_home_button(self, is_need_open_setting_appearance_page=True):
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        if self.get_status_toggle_show_home_button() != "false":
            self.click_shadow_element(self.TOGGLE_SHOW_HOME_BTN)
            assert self.get_status_toggle_show_home_button() == "false"

    def enter_custom_web_address(self, url: str) -> None:
        self.toggle_on_show_home_button()
        self.fill_texts_shadow_element(
            self.ENTER_CUSTOM_WEB_ADDRESS, url, is_press_enter=True
        )

    def clear_custom_web_address(self) -> None:
        self.toggle_on_show_home_button()
        self.clear_text_of_shadow_element(self.ENTER_CUSTOM_WEB_ADDRESS)
        self.click_shadow_element(self.RATIO_NEWTAB_PAGE)

    def get_status_toggle_show_bookmark_bar(
        self, is_need_open_setting_appearance_page=False
    ) -> str:
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_SHOW_BOOKMARK_BAR, attribute_name="aria-pressed"
        )

    def toggle_on_show_bookmark_bar(self, is_need_open_setting_appearance_page=True):
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        if self.get_status_toggle_show_bookmark_bar() != "true":
            self.click_shadow_element(self.TOGGLE_SHOW_BOOKMARK_BAR)
            assert self.get_status_toggle_show_bookmark_bar() == "true"

    def toggle_off_show_bookmark_bar(self, is_need_open_setting_appearance_page=True):
        if is_need_open_setting_appearance_page:
            self.open_setting_appearance()
        if self.get_status_toggle_show_bookmark_bar() != "false":
            self.click_shadow_element(self.TOGGLE_SHOW_BOOKMARK_BAR)
            assert self.get_status_toggle_show_bookmark_bar() == "false"
