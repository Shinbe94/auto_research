from src.pages.base import BasePlaywright
from src.pages.coccoc_common import interactions
from playwright.sync_api import Locator, expect, sync_playwright
from typing import List

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from tests import setting

lang = setting.coccoc_language


TOGGLE_SAVIOR_ON_OFF = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#viewManager > extensions-detail-view").shadowRoot.querySelector("#enableToggle")'


def get_savior_toggle_status(driver):
    toggle_status = interactions.get_attribute_value_by_js_path(
        driver, TOGGLE_SAVIOR_ON_OFF, "aria-pressed"
    )
    if toggle_status == "true":
        return "ON"
    else:
        return "OFF"


def toggle_savior(driver, toggle_status):
    current_toggle_status = get_savior_toggle_status(driver)
    if (toggle_status in ("ON", "OFF")) and (toggle_status == current_toggle_status):
        pass
    elif (toggle_status in ("ON", "OFF")) and (toggle_status != current_toggle_status):
        interactions.get_shadow_element3(driver, TOGGLE_SAVIOR_ON_OFF).click()
    else:
        print("toggle_status must be ON or OFF")


class SaviorExtensionDetailPage(BasePlaywright):
    @property
    def list_site_allow_cookies(self) -> List[Locator]:
        return self.page.locator(
            '#allowExceptionsList span[class="url-directionality"]'
        ).all()

    @property
    def savior_detail_btn(self) -> Locator:
        return self.page.locator("#jdfkmiabjpfjacifcmihfdjhpnjpiick #detailsButton")

    @property
    def allow_incognito_btn(self) -> Locator:
        return self.page.locator('extensions-toggle-row[id="allow-incognito"]')

    @property
    def allow_incognito_toggle(self) -> Locator:
        return self.page.locator(
            'extensions-toggle-row[id="allow-incognito"] #crToggle'
        )

    # Interaction methods
    def open_detail_savior(self) -> None:
        self.page.goto("coccoc://extensions/?id=jdfkmiabjpfjacifcmihfdjhpnjpiick")

    def get_allow_incognito_toggle_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.allow_incognito_toggle, "aria-pressed"
        )

    def turn_on_allow_in_incognito(self) -> None:
        self.open_detail_savior()
        if self.get_allow_incognito_toggle_status() != "true":
            self.allow_incognito_btn.click()

    def turn_off_allow_in_incognito(self) -> None:
        self.open_detail_savior()
        if self.get_allow_incognito_toggle_status() != "false":
            self.allow_incognito_btn.click()
