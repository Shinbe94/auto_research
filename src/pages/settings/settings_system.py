from time import sleep

from src.pages.base import BaseSelenium
from src.pages.constant import LocatorJSPath, CocCocText
from tests import setting

lang = setting.coccoc_language


class SettingsSystemSel(BaseSelenium):
    # Locators
    BTN_OPEN_PROXY = f'{LocatorJSPath.SETTINGS_SYSTEM_PAGE}.shadowRoot.querySelector("#proxy > cr-icon-button")'
    TOGGLE_RUN_IN_BG = f'{LocatorJSPath.SETTINGS_SYSTEM_PAGE}.shadowRoot.querySelector("settings-toggle-button[label=\'{CocCocText.RUNNING_IN_BG_AFTER_CLOSING}\']").shadowRoot.querySelector("#control")'

    # Interaction methods
    def open_settings_system(self) -> None:
        self.open_page(url="coccoc://settings/system")

    def get_status_toggle_running_bg(self, is_need_open_setting_system=False) -> str:
        if is_need_open_setting_system:
            self.open_settings_system()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_RUN_IN_BG, attribute_name="aria-pressed"
        )

    def toggle_on_show_bookmark_bar(self, is_need_open_setting_system=True):
        if is_need_open_setting_system:
            self.open_settings_system()
        if self.get_status_toggle_running_bg() != "true":
            self.click_shadow_element(self.TOGGLE_SHOW_BOOKMARK_BAR)
            assert self.get_status_toggle_running_bg() == "true"

    def toggle_off_show_bookmark_bar(self, is_need_open_setting_system=True):
        if is_need_open_setting_system:
            self.open_settings_system()
        if self.get_status_toggle_running_bg() != "false":
            self.click_shadow_element(self.TOGGLE_SHOW_BOOKMARK_BAR)
            assert self.get_status_toggle_running_bg() == "false"

    def open_computer_setting_proxy(self, is_need_open_setting_system=True) -> None:
        if is_need_open_setting_system:
            self.open_settings_system()
        self.click_shadow_element(self.BTN_OPEN_PROXY)
