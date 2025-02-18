import time

from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By

from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.coccoc_common import open_browser, interactions
from src.pages.constant import LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class SettingsAdblock(BasePlaywright):
    """Setting Adblock by playwright

    Args:
        BasePlaywright (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Locators
    @property
    def toggle_enable_adblock(self) -> Locator:
        if "en" in lang:
            return self.page.locator('cr-toggle[aria-label="Enable adblock"]')
        else:
            return self.page.locator('cr-toggle[aria-label="Bật chặn quảng cáo"]')

    @property
    def toggle_allow_acceptable_ads(self) -> Locator:
        if "en" in lang:
            return self.page.locator('cr-toggle[aria-label="Allow acceptable ads"]')
        else:
            return self.page.locator(
                'cr-toggle[aria-label="Cho phép quảng cáo chấp nhận được"]'
            )

    # Interaction methods

    def open_page(self):
        self.page.goto("coccoc://settings/adblock")

    def get_toggle_enable_adblock_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.toggle_enable_adblock, "aria-pressed"
        )

    def get_toggle_allow_acceptable_ads_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.toggle_allow_acceptable_ads, "aria-pressed"
        )

    def turn_on_toggle_enable_adblock_status(
        self, is_need_to_open_adblock_setting=True
    ) -> None:
        if is_need_to_open_adblock_setting:
            self.open_page()
        if self.get_toggle_enable_adblock_status() != "true":
            self.toggle_enable_adblock.click()
            assert self.get_toggle_enable_adblock_status() == "true"

    def turn_off_toggle_enable_adblock_status(
        self, is_need_to_open_adblock_setting=True
    ) -> None:
        if is_need_to_open_adblock_setting:
            self.open_page()
        if self.get_toggle_enable_adblock_status() != "false":
            self.toggle_enable_adblock.click()
            assert self.get_toggle_enable_adblock_status() == "false"

    def turn_on_toggle_allow_acceptable_ads_status(
        self, is_need_to_open_adblock_setting=True
    ) -> None:
        if is_need_to_open_adblock_setting:
            self.open_page()
        if self.get_toggle_allow_acceptable_ads_status() != "true":
            self.toggle_enable_adblock.click()
            assert self.get_toggle_allow_acceptable_ads_status() == "true"

    def turn_off_toggle_allow_acceptable_ads_status(
        self, is_need_to_open_adblock_setting=True
    ) -> None:
        if is_need_to_open_adblock_setting:
            self.open_page()
        if self.get_toggle_allow_acceptable_ads_status() != "false":
            self.toggle_enable_adblock.click()
            assert self.get_toggle_allow_acceptable_ads_status() == "false"


class SettingsAdblockSel(BaseSelenium):
    # Locators
    TITLE_ABLOCK_SECTION = (
        f'{LocatorJSPath.SETTINGS_ADSBLOCK_SECTION}.shadowRoot.querySelector("#title")'
    )
    ENABLE_ADBLOCK = f"{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector(\"adblock-toggle-button[data-qa='adblock-toogle']\")"
    ENABLE_ADBLOCK_TOGGLE = f'{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector("adblock-toggle-button[data-qa=\'adblock-toogle\']").shadowRoot.querySelector("#control")'
    ALLOW_ACEPTABLE_ADS = f"{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector(\"adblock-toggle-button[data-qa='aa-toogle']\")"
    ALLOW_ACEPTABLE_ADS_TOGGLE = f'{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector("adblock-toggle-button[data-qa=\'aa-toogle\']").shadowRoot.querySelector("#control")'
    MENU_BLOCKING_MODE = f'{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector("adblock-dropdown-menu").shadowRoot.querySelector("#dropdownMenu")'
    OPTION_STANDARD = f'{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector("adblock-dropdown-menu").shadowRoot.querySelector("#dropdownMenu option[value=\'0\']")'
    OPTION_STRICT = f'{LocatorJSPath.SETTINGS_ADSBLOCK_PAGE}.shadowRoot.querySelector("adblock-dropdown-menu").shadowRoot.querySelector("#dropdownMenu option[value=\'1\']")'
    BTN_REMOVE_WHITE_LIST = f'{LocatorJSPath.SETTINGS_ADSBLOCK_WHITE_LIST}.shadowRoot.querySelector("#delete")'
    WHITE_LIST_ENTRY = f'{LocatorJSPath.SETTINGS_ADSBLOCK_WHITE_LIST}.shadowRoot.querySelectorAll("adblock-white-list-entry")'

    # Interaction methods
    def open_setting_adblock_page(self) -> None:
        self.open_page("coccoc://settings/adblock")

    def get_toggle_adblock_status(self, is_need_open_setting_adblock_page=True) -> str:
        if is_need_open_setting_adblock_page:
            self.open_setting_adblock_page()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.ENABLE_ADBLOCK_TOGGLE, attribute_name="aria-pressed"
        )

    def check_toggle_adblock_status_is_on_at_default(self) -> None:
        assert self.get_toggle_adblock_status() == "true"

    def toggle_on_adblock(self) -> None:
        if self.get_toggle_adblock_status() != "true":
            self.click_shadow_element(self.ENABLE_ADBLOCK_TOGGLE)
            assert self.get_toggle_adblock_status() == "true"

    def toggle_off_adblock(self) -> None:
        if self.get_toggle_adblock_status() != "false":
            self.click_shadow_element(self.ENABLE_ADBLOCK_TOGGLE)
            assert self.get_toggle_adblock_status() == "false"

    def get_toggle_allow_acceptable_ads(
        self, is_need_open_setting_adblock_page=True
    ) -> str:
        if is_need_open_setting_adblock_page:
            self.open_setting_adblock_page()
        self.get_attribute_value_of_shadow_element(
            js_path=self.ALLOW_ACEPTABLE_ADS_TOGGLE, attribute_name="aria-pressed"
        )

    def toggle_on_allow_acceptable_ads(self) -> None:
        if self.get_toggle_allow_acceptable_ads() != "true":
            self.click_shadow_element(self.ALLOW_ACEPTABLE_ADS_TOGGLE)
            assert self.get_toggle_allow_acceptable_ads() == "true"

    def toggle_off_allow_acceptable_ads(self) -> None:
        if self.get_toggle_allow_acceptable_ads() != "false":
            self.click_shadow_element(self.ALLOW_ACEPTABLE_ADS_TOGGLE)
            assert self.get_toggle_allow_acceptable_ads() == "false"

    def click_dropdown_menu(self) -> None:
        self.open_setting_adblock_page()
        self.click_shadow_element(self.MENU_BLOCKING_MODE)

    def select_standard_mode(self) -> None:
        self.click_dropdown_menu()
        self.click_shadow_element(self.OPTION_STANDARD)

    def select_strict_mode(self) -> None:
        self.click_dropdown_menu()
        self.click_shadow_element(self.OPTION_STRICT)

    def verify_adblock_default_ui(self) -> None:
        if "en" in lang:
            assert (
                self.get_text_shadow_element(js_path=self.TITLE_ABLOCK_SECTION)
                == "Adblock"
            )
        else:
            assert (
                self.get_text_shadow_element(js_path=self.TITLE_ABLOCK_SECTION)
                == "Chặn quảng cáo"
            )
        if "en" in lang:
            assert (
                self.get_attribute_value_of_shadow_element(
                    self.ENABLE_ADBLOCK, "sub-label"
                )
                == "Adblock helps to protect personal data and surf the web faster."
            )
        else:
            assert (
                self.get_attribute_value_of_shadow_element(
                    self.ENABLE_ADBLOCK, "sub-label"
                )
                == "Chặn quảng cáo giúp bảo vệ thông tin cá nhân và duyệt web nhanh hơn."
            )

        if "en" in lang:
            assert (
                self.get_attribute_value_of_shadow_element(
                    self.ALLOW_ACEPTABLE_ADS, "sub-label"
                )
                == "Acceptable ads are not annoying and do not interfere with the content you are viewing."
            )
        else:
            assert (
                self.get_attribute_value_of_shadow_element(
                    self.ALLOW_ACEPTABLE_ADS, "sub-label"
                )
                == "Quảng cáo chấp nhận được không làm phiền và không cản trở nội dung bạn đang xem."
            )

    def get_total_white_sites(self) -> int:
        self.open_setting_adblock_page()
        return self.get_count_shadow_elements(js_path=self.WHITE_LIST_ENTRY)

    def get_list_white_list(self) -> list:
        list_sites = []
        total_sites = self.get_total_white_sites()
        if total_sites > 0:
            for i in range(total_sites):
                js_path = f'{LocatorJSPath.SETTINGS_ADSBLOCK_WHITE_LIST}.shadowRoot.querySelector("#frb{i}").shadowRoot.querySelector("div.start.text-elide")'
                list_sites.append(self.get_text_shadow_element(js_path=js_path))
        return list_sites

    def remove_all_white_sites(self) -> None:
        total_sites = self.get_total_white_sites()
        if total_sites > 0:
            for _ in range(total_sites):
                js_path = f'{LocatorJSPath.SETTINGS_ADSBLOCK_WHITE_LIST}.shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#button")'
                self.click_shadow_element(js_path)
                self.click_shadow_element(self.BTN_REMOVE_WHITE_LIST)
