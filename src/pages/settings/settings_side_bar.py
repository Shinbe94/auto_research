import time

from src.pages.base import BasePlaywright
from playwright.sync_api import Locator, expect, sync_playwright

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from tests import setting

lang = setting.coccoc_language


class SettingsSidebar(BasePlaywright):
    @property
    def sidebar_title(self) -> Locator:
        if lang == "en":
            return self.page.get_by_role("heading", name="Sidebar")
        else:
            return self.page.get_by_role("heading", name="Thanh bên")

    @property
    def sidebar_toggle(self) -> Locator:
        if lang == "en":
            return self.page.get_by_role("button", name="Show Sidebar")
        else:
            return self.page.get_by_role("button", name="Hiển thị thanh bên")

    @property
    def settings_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Settings")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cài đặt")
                .locator("#control")
            )

    @property
    def settings_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Settings")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cài đặt")
                .locator("#labelWrapper")
            )

    @property
    def history_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="History")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Lịch sử")
                .locator("#control")
            )

    @property
    def history_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="History")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Lịch sử")
                .locator("#labelWrapper")
            )

    @property
    def reading_list_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Reading List")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Danh sách đọc")
                .locator("#control")
            )

    @property
    def reading_list_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Reading List")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Danh sách đọc")
                .locator("#labelWrapper")
            )

    @property
    def coccoc_points_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Points")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Points")
                .locator("#control")
            )

    @property
    def coccoc_points_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Points")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Points")
                .locator("#labelWrapper")
            )

    @property
    def facebook_messenger_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Facebook Messenger")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Facebook Messenger")
                .locator("#control")
            )

    @property
    def facebook_messenger_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Facebook Messenger")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Facebook Messenger")
                .locator("#labelWrapper")
            )

    @property
    def telegram_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Telegram")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Telegram")
                .locator("#control")
            )

    @property
    def telegram_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Telegram")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Telegram")
                .locator("#labelWrapper")
            )

    @property
    def skype_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="History")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Lịch sử")
                .locator("#control")
            )

    @property
    def skype_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Skype")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Skype")
                .locator("#labelWrapper")
            )

    @property
    def zalo_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Skype")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Skype")
                .locator("#control")
            )

    @property
    def zalo_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Zalo")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Zalo")
                .locator("#labelWrapper")
            )

    @property
    def coccoc_games_checkbox(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Games")
                .locator("#control")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Games")
                .locator("#control")
            )

    @property
    def coccoc_games_label(self) -> Locator:
        if lang == "en":
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Games")
                .locator("#labelWrapper")
            )
        else:
            return (
                self.page.locator("settings-checkbox-toggle")
                .filter(has_text="Cốc Cốc Games")
                .locator("#labelWrapper")
            )

    @property
    def ratio_sidebar_on_the_right(self) -> Locator:
        if lang == "en":
            return self.page.get_by_role("radio", name="Show sidebar on the right")
        else:
            return self.page.get_by_role("radio", name="Hiển thị thanh bên ở bên phải")

    @property
    def ratio_sidebar_on_the_left(self) -> Locator:
        if lang == "en":
            return self.page.get_by_role("radio", name="Show sidebar on the left")
        else:
            return self.page.get_by_role("radio", name="Hiển thị thanh bên ở bên trái")

    def check_sidebar_ui(self):
        expect(self.sidebar_title).to_be_visible()
        expect(self.sidebar_toggle).to_be_visible()
        expect(self.settings_label).to_be_visible()
        expect(self.settings_checkbox).to_be_visible()
        expect(self.history_label).to_be_visible()
        expect(self.history_checkbox).to_be_visible()
        expect(self.reading_list_label).to_be_visible()
        expect(self.reading_list_checkbox).to_be_visible()
        expect(self.coccoc_points_label).to_be_visible()
        expect(self.coccoc_points_checkbox).to_be_visible()
        expect(self.facebook_messenger_label).to_be_visible()
        expect(self.facebook_messenger_checkbox).to_be_visible()
        expect(self.telegram_label).to_be_visible()
        expect(self.telegram_checkbox).to_be_visible()
        expect(self.skype_label).to_be_visible()
        expect(self.skype_checkbox).to_be_visible()
        expect(self.zalo_label).to_be_visible()
        expect(self.zalo_checkbox).to_be_visible()
        expect(self.coccoc_games_label).to_be_visible()
        expect(self.coccoc_games_checkbox).to_be_visible()
        expect(self.ratio_sidebar_on_the_right).to_be_visible()
        expect(self.ratio_sidebar_on_the_left).to_be_visible()

    # Interaction methods
    def open_page(self):
        self.page.goto("coccoc://settings/sidebar")
        self.check_sidebar_ui()
        time.sleep(1)

    def get_current_sidebar_toggle_status(self) -> str:
        """Get toggle status of sidebar from its settings"""
        status = "OFF"
        if self.sidebar_toggle.get_attribute("aria-pressed") == "true":
            status = "ON"
        return status

    def on_off_sidebar(self, toggle_to: str):
        """Show/Hide sidebar via UI"""
        current_status = self.get_current_sidebar_toggle_status()
        if toggle_to in ("ON", "OFF") and toggle_to == current_status:
            pass
        elif toggle_to in ("ON", "OFF") and toggle_to != current_status:
            self.sidebar_toggle.click()
            assert toggle_to == self.get_current_sidebar_toggle_status()
        else:
            print(rf"Toggle status: {toggle_to} is not correct")

    def get_sidebar_status(self) -> str:
        """To get status of sidebar using api"""
        if self.page.evaluate("ntp.apiHandle.newTabPage.isSidebarShown") is True:
            return "ON"
        else:
            return "OFF"

    def show_sidebar(self, is_need_to_open_new_tab=False):
        """To show sidebar using api"""
        if is_need_to_open_new_tab:
            self.page.goto("https://coccoc.com/webhp?espv=2&ie=UTF-8&l=en-US")
        self.page.evaluate("ntp.apiHandle.newTabPage.showSidebar(true)")

    def hide_sidebar(self, is_need_to_open_new_tab=False):
        """To hide sidebar using api"""
        if is_need_to_open_new_tab:
            self.page.goto("https://coccoc.com/webhp?espv=2&ie=UTF-8&l=en-US")
        self.page.evaluate("ntp.apiHandle.newTabPage.showSidebar(false)")


def get_sidebar_status() -> bool:
    driver = open_browser.open_coccoc_by_selenium()
    # Open new tab
    driver.execute_script(
        'window.open("https://coccoc.com/webhp?espv=2&ie=UTF-8&l=en-US", "_blank");'
    )
    # Get last window name
    window_name = driver.window_handles[-1]
    # Switch to last window name
    driver.switch_to.window(window_name)
    time.sleep(1)
    try:
        sidebar_status = driver.execute_script(
            "return ntp.apiHandle.newTabPage.isSidebarShown"
        )
    finally:
        driver.quit()
    return sidebar_status
