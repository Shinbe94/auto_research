import time

from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By

from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.coccoc_common import open_browser, interactions
from tests import setting

lang = setting.coccoc_language


class SettingsTorOptions(BasePlaywright):
    """Setting Tor option by playwright

    Args:
        BasePlaywright (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Locators
    @property
    def incognito_with_tor(self) -> Locator:
        return self.page.locator(
            "settings-subpage[route-path='/torOptions'] settings-toggle-button:nth-child(1) #control"
        )

    @property
    def automatically_redirect_dot_onion_sites(self) -> Locator:
        return self.page.locator(
            "settings-subpage[route-path='/torOptions'] settings-toggle-button:nth-child(2) #control"
        )

    # Interaction methods

    def open_page(self):
        self.page.goto("coccoc://settings/torOptions")

    def get_incognito_with_tor_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.incognito_with_tor, "aria-pressed"
        )

    def get_automatically_redirect_dot_onion_sites_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.automatically_redirect_dot_onion_sites, "aria-pressed"
        )

    def turn_on_incognito_with_tor(self, is_need_to_access_tor_setting=True) -> None:
        if is_need_to_access_tor_setting:
            self.open_page()
        if self.get_incognito_with_tor_status() != "true":
            self.incognito_with_tor.click()
            assert self.get_incognito_with_tor_status() == "true"

    def turn_off_incognito_with_tor(self, is_need_to_access_tor_setting=True) -> None:
        if is_need_to_access_tor_setting:
            self.open_page()
        if self.get_incognito_with_tor_status() != "false":
            self.incognito_with_tor.click()
            assert self.get_incognito_with_tor_status() == "false"

    def turn_on_automatically_redirect_dot_onion_sites(
        self, is_need_to_access_tor_setting=True
    ) -> None:
        if is_need_to_access_tor_setting:
            self.open_page()
        if self.get_automatically_redirect_dot_onion_sites_status() != "true":
            self.automatically_redirect_dot_onion_sites.click()
            assert self.get_automatically_redirect_dot_onion_sites_status() == "true"

    def turn_off_automatically_redirect_dot_onion_sites(
        self, is_need_to_access_tor_setting=True
    ) -> None:
        if is_need_to_access_tor_setting:
            self.open_page()
        if self.get_automatically_redirect_dot_onion_sites_status() != "false":
            self.automatically_redirect_dot_onion_sites.click()
            assert self.get_automatically_redirect_dot_onion_sites_status() == "false"


class SettingsTorOptionsSel(BaseSelenium):
    """Setting Tor option by selenium

    Args:
        BaseSelenium (_type_): _description_
    """

    # Locators
    INCOGNITO_WITH_TOR = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-privacy-page").shadowRoot.querySelector("#pages settings-subpage settings-toggle-button:nth-child(1)").shadowRoot.querySelector("#control")'

    AUTOMATICALLY_REDIRECT_DOT_ONION_SITES = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage settings-privacy-page").shadowRoot.querySelector("#pages settings-subpage settings-toggle-button:nth-child(2)").shadowRoot.querySelector("#control")'
    # Interaction methods

    def open_setting_tor_options(self):
        self.open_page(url="coccoc://settings/torOptions")

    def get_incognito_with_tor_status(self) -> str:
        return self.get_attribute_value_of_shadow_element(
            self.INCOGNITO_WITH_TOR, "aria-pressed"
        )

    def get_automatically_redirect_dot_onion_sites_status(self) -> str:
        return self.get_attribute_value_of_shadow_element(
            self.AUTOMATICALLY_REDIRECT_DOT_ONION_SITES, "aria-pressed"
        )

    def turn_on_incognito_with_tor(self) -> None:
        self.open_setting_tor_options()
        if self.get_incognito_with_tor_status() != "true":
            self.click_shadow_element(self.INCOGNITO_WITH_TOR)
            assert self.get_incognito_with_tor_status() == "true"

    def turn_off_incognito_with_tor(self) -> None:
        self.open_setting_tor_options()
        if self.get_incognito_with_tor_status() != "false":
            self.click_shadow_element(self.INCOGNITO_WITH_TOR)
            assert self.get_incognito_with_tor_status() == "false"

    def turn_on_automatically_redirect_dot_onion_sites(self) -> None:
        self.open_setting_tor_options()
        if self.get_automatically_redirect_dot_onion_sites_status() != "true":
            self.click_shadow_element(self.AUTOMATICALLY_REDIRECT_DOT_ONION_SITES)
            assert self.get_automatically_redirect_dot_onion_sites_status() == "true"

    def turn_off_automatically_redirect_dot_onion_sites(self) -> None:
        self.open_setting_tor_options()
        if self.get_automatically_redirect_dot_onion_sites_status() != "false":
            self.click_shadow_element(self.AUTOMATICALLY_REDIRECT_DOT_ONION_SITES)
            assert self.get_automatically_redirect_dot_onion_sites_status() == "false"
