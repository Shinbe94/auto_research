from time import sleep
from src.pages.base import BaseSelenium
from selenium.webdriver.common.by import By


class IncognitoPageSel(BaseSelenium):
    pass
    """Incognito FE by selenium

    Args:
        BaseSelenium (_type_): _description_
    """

    # Locators
    COOKIES_TOGGLE = (By.ID, "cookie-controls-toggle")
    COOKIES_SETTINGS_BTN_JS_PATH = 'document.querySelector("#cookie-controls-tooltip-icon").shadowRoot.querySelector("#indicator")'

    # Interaction methods

    def get_cookies_toggle_status(self) -> str:
        """Get toggle status on or off

        Returns:
            str: _description_
        """
        return self.get_element_attribute_by_its_name_and_locator(
            self.COOKIES_TOGGLE, "aria-pressed"
        )

    def is_cookies_toggle_enable(self) -> bool:
        """Check whether this option is diabled or enabled

        Returns:
            bool: True -> enabled and vice versa
        """
        if (
            self.get_element_attribute_by_its_name_and_locator(
                self.COOKIES_TOGGLE, "aria-disabled"
            )
            == "false"
        ):
            return True
        else:
            return False

    def click_cookies_settings_btn(self) -> None:
        self.click_shadow_element(self.COOKIES_SETTINGS_BTN_JS_PATH)
        sleep(2)

    def toggle_on_block_cookies_from_3rd(self) -> None:
        if self.get_cookies_toggle_status() != "true":
            self.click_element(self.COOKIES_TOGGLE)
        assert self.get_cookies_toggle_status() == "true"

    def toggle_off_block_cookies_from_3rd(self) -> None:
        if self.get_cookies_toggle_status() != "false":
            self.click_element(self.COOKIES_TOGGLE)
        assert self.get_cookies_toggle_status() == "false"
