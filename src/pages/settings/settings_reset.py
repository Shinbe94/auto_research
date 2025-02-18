from time import sleep

from src.pages.base import BaseSelenium
from src.pages.constant import LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class SettingsResetSel(BaseSelenium):
    # Locators:
    RESTORE_SETTING = (
        f'{LocatorJSPath.SETTINGS_RESET_PAGE}.shadowRoot.querySelector("#resetProfile")'
    )
    BTN_RESET_SETTING = (
        f'{LocatorJSPath.SETTINGS_RESET_PAGE_DIALOG}.shadowRoot.querySelector("#reset")'
    )

    # Interaction methods
    def open_settings_reset_page(self):
        self.open_page(url="coccoc://settings/reset")

    def click_restore_settings(self) -> None:
        self.click_shadow_element(self.RESTORE_SETTING)

    def reset_settings(self, is_open_reset_settings_page=True) -> None:
        if is_open_reset_settings_page:
            self.open_settings_reset_page()
        self.click_restore_settings()
        self.click_shadow_element(self.BTN_RESET_SETTING)
