import time

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser, interactions
from tests import setting

lang = setting.coccoc_language


class IncognitoTorPage(BasePlaywright):
    @property
    def tor_connection_status(self) -> Locator:
        return self.page.locator("#tor-connection-status-description")

    @property
    def cookies_toggle(self) -> Locator:
        return self.page.locator("#cookie-controls-toggle")

    # Interaction methods

    def get_tor_connection_status(self) -> str:
        return self.tor_connection_status.text_content()

    def open_tor_credit_page(self) -> None:
        self.page.goto("coccoc://credits/")

    def open_any_page(self, url) -> None:
        self.wait_for_connected()
        self.page.goto(url, timeout=setting.timeout_for_tor_loadpage_playwright)

    def wait_for_connecting(self, timeout=10, language=setting.coccoc_language):
        is_connecting = False
        interval_delay = 0.01
        total_delay = 0
        if "en" in language:
            verify_text: str = "Connecting to Tor"
        else:
            verify_text: str = "Đang kết nối với Tor"
        while total_delay < timeout:
            try:
                if verify_text in self.get_tor_connection_status():
                    is_connecting = True
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        return is_connecting

    def wait_for_connected(
        self, timeout=setting.timeout, language=setting.coccoc_language
    ) -> bool:
        is_connected = False
        interval_delay = 0.1
        total_delay = 0
        if "en" in language:
            verify_text: str = "Connected to Tor successfully"
        else:
            verify_text: str = "Kết nối với Tor thành công"
        while total_delay < timeout:
            try:
                if verify_text in self.get_tor_connection_status():
                    is_connected = True
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        return is_connected

    def wait_for_connection_is_failed(
        self, timeout=setting.timeout, language=setting.coccoc_language
    ) -> bool:
        """
        trying to wait for the connection is failed
        Args:
            timeout:
            language:
        Returns:
        """
        is_connecting_failed = True
        interval_delay = 2
        total_delay = 0
        if "en" in language:
            verify_text: str = "Disconnected to Tor"
        else:
            verify_text: str = "Đã ngắt kết nối với Tor"
        while total_delay < timeout:
            try:
                if verify_text != self.get_tor_connection_status():
                    is_connecting_failed = False  # Mean connecting is OK
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        # After the timeout, the connection is still failing
        return is_connecting_failed

    def get_cookies_toggle_status(self) -> str:
        """Get toggle status on or off

        Returns:
            str: _description_
        """
        return self.cookies_toggle.get_attribute("aria-pressed")

    def is_cookies_toggle_enable(self) -> bool:
        """Check whether this option is diabled or enabled

        Returns:
            bool: True -> enabled and vice versa
        """
        if self.cookies_toggle.get_attribute("aria-disabled") == "false":
            return True
        else:
            return False

    def toggle_on_block_cookies_from_3rd(self) -> None:
        if self.get_cookies_toggle_status() != "true":
            self.cookies_toggle.click()
        assert self.get_cookies_toggle_status() == "true"

    def toggle_off_block_cookies_from_3rd(self) -> None:
        if self.get_cookies_toggle_status() != "false":
            self.cookies_toggle.click()
        assert self.get_cookies_toggle_status() == "false"


"""OUTSIDE the class"""

js_path_toggle = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-privacy-page").shadowRoot.querySelector("#pages settings-subpage settings-toggle-button").shadowRoot.querySelector("#outerRow #control")'


def get_tor_setting_status(driver) -> str:
    return interactions.get_attribute_value_by_js_path(
        driver, js_path_toggle, "aria-pressed"
    )


def turn_off_tor_from_setting(driver=None, is_closed=True):
    if driver is None:
        coccoc_instance = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
        )
        driver = coccoc_instance[0]
        window = coccoc_instance[1]
        try:
            driver.get("coccoc://settings/torOptions")
            if get_tor_setting_status(driver) != "false":
                interactions.click_shadow_element(driver, js_path=js_path_toggle)
                assert get_tor_setting_status(driver) == "false"
        finally:
            if is_closed:
                driver.quit()
                window.window().set_focus().close()
    else:
        driver.get("coccoc://settings/torOptions")
        if get_tor_setting_status(driver) != "false":
            interactions.click_shadow_element(driver, js_path=js_path_toggle)
            assert get_tor_setting_status(driver) == "false"


def turn_on_tor_from_setting(driver=None, is_closed=True):
    if driver is None:
        coccoc_instance = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
        )
        driver = coccoc_instance[0]
        window = coccoc_instance[1]
        try:
            driver.get("coccoc://settings/torOptions")
            if get_tor_setting_status(driver) != "true":
                interactions.click_shadow_element(driver, js_path=js_path_toggle)
                assert get_tor_setting_status(driver) == "true"
        finally:
            if is_closed:
                driver.quit()
                window.window().set_focus().close()
    else:
        driver.get("coccoc://settings/torOptions")
        if get_tor_setting_status(driver) != "true":
            interactions.click_shadow_element(driver, js_path=js_path_toggle)
            assert get_tor_setting_status(driver) == "true"
