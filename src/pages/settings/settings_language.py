from selenium.webdriver.common.by import By
from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.constant import CocCocText, LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class SettingsLanguageSel(BaseSelenium):
    # Locators
    OPTION_USE_GOOLE_TRANSLATE = f'{LocatorJSPath.SETTINGS_LANGUAGE_TRANSLATE}.shadowRoot.querySelector("#offerTranslateOtherLanguages")'
    TOGGLE_USE_GOOLE_TRANSLATE = f'{LocatorJSPath.SETTINGS_LANGUAGE_TRANSLATE}.shadowRoot.querySelector("#offerTranslateOtherLanguages").shadowRoot.querySelector("#control")'

    # Interaction methods

    def open_settings_language(self) -> None:
        self.open_page("coccoc://settings/languages")

    def get_toggle_status_of_use_google_translate(self) -> str:
        return self.get_attribute_value_of_shadow_element(
            self.TOGGLE_USE_GOOLE_TRANSLATE, "aria-pressed"
        )

    def toggle_on_use_google_translate(self) -> None:
        self.open_settings_language()
        if self.get_toggle_status_of_use_google_translate() != "true":
            # print("Clicking to ON")
            self.click_shadow_element(self.OPTION_USE_GOOLE_TRANSLATE)
            # assert self.get_toggle_status_of_use_google_translate() == "true"
            self.wait_for_attribute_update_value_shadow_element(
                self.TOGGLE_USE_GOOLE_TRANSLATE, "aria-pressed", "true"
            )

    def toggle_off_use_google_translate(self) -> None:
        self.open_settings_language()
        if self.get_toggle_status_of_use_google_translate() != "false":
            # print("Clicking to OFF")
            self.click_shadow_element(self.OPTION_USE_GOOLE_TRANSLATE)
            # assert self.get_toggle_status_of_use_google_translate() == "false"
            self.wait_for_attribute_update_value_shadow_element(
                self.TOGGLE_USE_GOOLE_TRANSLATE, "aria-pressed", "false"
            )
