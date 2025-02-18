from time import sleep
from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By
from pywinauto import Application

from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.constant import CocCocSettingTitle, LocatorJSPath
from src.pages.settings.settings_home import SettingsHomeSel
from src.utilities import os_utils, file_utils
from src.pages.coccoc_common import open_browser, interactions
from tests import setting

lang = setting.coccoc_language


class SettingsDownloads(BasePlaywright):
    """Setting Downloads by playwright

    Args:
        BasePlaywright (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Locators
    @property
    def btn_change(self) -> Locator:
        return self.page.locator("#changeDownloadsPath")

    @property
    def default_download_path(self) -> Locator:
        return self.page.locator("#defaultDownloadPath")

    @property
    def toggle_ask_where_to_save(self) -> Locator:
        if "en" in lang:
            return self.page.locator(
                'cr-toggle[aria-label="Ask where to save each file before downloading"]'
            )
        else:
            return self.page.locator(
                'cr-toggle[aria-label="Hỏi vị trí lưu từng tệp trước khi tải về"]'
            )

    @property
    def toggle_enable_torrent_client(self) -> Locator:
        if "en" in lang:
            return self.page.locator('cr-toggle[aria-label="Enable torrent client"]')
        else:
            return self.page.locator('cr-toggle[aria-label="Chức năng torrent"]')

    @property
    def toggle_use_UPnP_and_NAT_PMP_port_forwarding(self) -> Locator:
        if "en" in lang:
            return self.page.locator(
                'cr-toggle[aria-label="Use UPnP and NAT-PMP port forwarding"]'
            )
        else:
            return self.page.locator('cr-toggle[aria-label="Sử dụng UPnP và NAT-PMP"]')

    @property
    def toggle_automatically_stop_seeding_completed_torrents(self) -> Locator:
        if "en" in lang:
            return self.page.locator(
                'cr-toggle[aria-label="Automatically stop seeding completed torrents"]'
            )
        else:
            return self.page.locator(
                'cr-toggle[aria-label="Tự động ngừng seed những torrent đã hoàn thành"]'
            )

    # Interaction methods

    def open_page(self):
        self.page.goto("coccoc://settings/downloads")

    def get_toggle_ask_where_to_save_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.toggle_ask_where_to_save, "aria-pressed"
        )

    def get_toggle_enable_torrent_client_status(self) -> str:
        return self.get_attribute_value_by_locator(
            self.toggle_enable_torrent_client, "aria-pressed"
        )

    def turn_on_toggle_ask_where_to_save(
        self, is_need_to_open_downloads_setting=True
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_page()
        if self.get_toggle_ask_where_to_save_status() != "true":
            self.toggle_ask_where_to_save.click()
            assert self.get_toggle_ask_where_to_save_status() == "true"

    def turn_off_toggle_ask_where_to_save(
        self, is_need_to_open_downloads_setting=True
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_page()
        if self.get_toggle_ask_where_to_save_status() != "false":
            self.toggle_ask_where_to_save.click()
            assert self.get_toggle_ask_where_to_save_status() == "false"

    def turn_on_toggle_enable_torrent_client(
        self, is_need_to_open_downloads_setting=True
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_page()
        if self.get_toggle_enable_torrent_client_status() != "true":
            self.toggle_enable_torrent_client.click()
            assert self.get_toggle_enable_torrent_client_status() == "true"

    def turn_off_toggle_enable_torrent_client(
        self, is_need_to_open_downloads_setting=True
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_page()
        if self.get_toggle_enable_torrent_client_status() != "false":
            self.toggle_enable_torrent_client.click()
            assert self.get_toggle_enable_torrent_client_status() == "false"

    def get_current_saving_folder(self) -> str:
        return self.default_download_path.text_content()


class SettingsDownloadsSel(SettingsHomeSel):
    # Locators
    if "en" in lang:
        TOGGLE_ASK_WHERE_TO_SAVE = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Ask where to save each file before downloading\"]").shadowRoot.querySelector("cr-toggle")'
    else:
        TOGGLE_ASK_WHERE_TO_SAVE = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Hỏi vị trí lưu từng tệp trước khi tải về\"]").shadowRoot.querySelector("cr-toggle")'

    if "en" in lang:
        TOGGLE_ENABLE_TORRENT_CLIENT = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Enable torrent client\"]").shadowRoot.querySelector("cr-toggle")'
    else:
        TOGGLE_ENABLE_TORRENT_CLIENT = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Chức năng torrent\"]").shadowRoot.querySelector("cr-toggle")'

    DEFAULT_DOWNLOAD_PATH = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("#defaultDownloadPath")'
    BTN_CHANGE_DOWNLOAD_PATH = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("#changeDownloadsPath")'

    TORRENT_MAX_NUMBER_CONNECTION_PER_CLIENT = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(13) > cr-input").shadowRoot.querySelector("#input")'
    TORRENT_MAX_NUMBER_CONNECTION_PER_ITEM = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(14) > cr-input").shadowRoot.querySelector("#input")'
    TORRENT_PEERS_LISTENING_PORT = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(15) > cr-input").shadowRoot.querySelector("#input")'
    TORRENT_MAX_ACTIVE_DOWNLOAD = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(16) > cr-input").shadowRoot.querySelector("#input")'
    TORRENT_MAX_ACTIVE_SEEDING = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(17) > cr-input").shadowRoot.querySelector("#input")'
    TORRENT_MAX_ACTIVE_SEEDING_ALL = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("div:nth-child(17) > cr-input").shadowRoot.querySelectorAll("#input")'
    if "en" in lang:
        TOGGLE_Use_UPnP_and_NAT_PMP_port_forwarding = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Use UPnP and NAT-PMP port forwarding\"]").shadowRoot.querySelector("cr-toggle")'
    else:
        TOGGLE_Use_UPnP_and_NAT_PMP_port_forwarding = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Sử dụng UPnP và NAT-PMP\"]").shadowRoot.querySelector("cr-toggle")'

    if "en" in lang:
        TORRENT_AUTOMATICALLY_STOP_SEEDING_COMPLETED_TORRENTS = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Automatically stop seeding completed torrents\"]").shadowRoot.querySelector("cr-toggle")'
    else:
        TORRENT_AUTOMATICALLY_STOP_SEEDING_COMPLETED_TORRENTS = rf'{LocatorJSPath.SETTINGS_DOWNLOAD_PRE}.shadowRoot.querySelector("settings-toggle-button[label=\"Tự động ngừng seed những torrent đã hoàn thành\"]").shadowRoot.querySelector("cr-toggle")'

    # Interaction methods
    def open_settings_download(self):
        self.open_page("coccoc://settings/downloads")

    def get_toggle_ask_where_to_save_status(
        self, is_need_to_open_downloads_setting=False
    ) -> str:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_ASK_WHERE_TO_SAVE, attribute_name="aria-pressed"
        )

    def check_default_toggle_ask_where_to_save_status_is_off(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        assert (
            self.get_attribute_value_of_shadow_element(
                js_path=self.TOGGLE_ASK_WHERE_TO_SAVE, attribute_name="aria-pressed"
            )
            == "false"
        )

    def turn_on_toggle_ask_where_to_save(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_toggle_ask_where_to_save_status() != "true":
            self.click_shadow_element(js_path=self.TOGGLE_ASK_WHERE_TO_SAVE)
            assert self.get_toggle_ask_where_to_save_status() == "true"

    def turn_off_toggle_ask_where_to_save(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_toggle_ask_where_to_save_status() != "false":
            self.click_shadow_element(js_path=self.TOGGLE_ASK_WHERE_TO_SAVE)
            assert self.get_toggle_ask_where_to_save_status() == "false"

    def get_download_path(self, is_need_to_open_downloads_setting=False) -> str:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        return self.get_text_shadow_element(js_path=self.DEFAULT_DOWNLOAD_PATH)

    def change_download_path(
        self,
        change_to_where: str = rf"C:\Users\{os_utils.get_username()}\Downloads",
        is_need_to_open_downloads_setting=True,
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.click_shadow_element(js_path=self.BTN_CHANGE_DOWNLOAD_PATH)
        window_dialog: Application = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=CocCocSettingTitle.SETTINGS_DOWNLOADS_TITLE,
            timeout=setting.timeout_pywinauto,
        )
        # window_dialog.window().print_control_identifiers(filename="all.txt")
        assert (
            window_dialog.window()
            .child_window(
                title=CocCocSettingTitle.SETTINGS_DOWNLOADS_PATH_DIALOG_TITLE,
                control_type="Window",
            )
            .exists(timeout=setting.timeout_pywinauto)
        )
        window_dialog.window().child_window(
            title="Folder:", auto_id="1152", control_type="Edit"
        ).click_input()
        window_dialog.window().child_window(
            title="Folder:", auto_id="1152", control_type="Edit"
        ).type_keys(change_to_where, with_spaces=True)

        window_dialog.window().child_window(
            title="Select Folder", auto_id="1", control_type="Button"
        ).click_input()
        sleep(1)
        assert self.get_download_path() == change_to_where

    def get_max_number_connection_per_client(
        self, is_need_to_open_setting_download=False
    ) -> int:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return int(
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_NUMBER_CONNECTION_PER_CLIENT, "value"
            )
        )

    def get_max_number_connection_per_item(
        self, is_need_to_open_setting_download=False
    ) -> int:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return int(
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_NUMBER_CONNECTION_PER_ITEM, "value"
            )
        )

    def get_peers_listening_port(self, is_need_to_open_setting_download=False) -> int:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return int(
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_PEERS_LISTENING_PORT, "value"
            )
        )

    def get_max_active_download(self, is_need_to_open_setting_download=False) -> int:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return int(
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_ACTIVE_DOWNLOAD, "value"
            )
        )

    def get_max_active_seeding(self, is_need_to_open_setting_download=False) -> int:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return int(
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_ACTIVE_SEEDING, "value"
            )
        )

    def get_toggle_enable_torrent_client_status(
        self, is_need_to_open_setting_download=False
    ) -> str:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_ENABLE_TORRENT_CLIENT, attribute_name="aria-pressed"
        )

    def get_use_upnp_and_nat_pmp_port_forwarding_status(
        self, is_need_to_open_setting_download=False
    ) -> str:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TOGGLE_Use_UPnP_and_NAT_PMP_port_forwarding,
            attribute_name="aria-pressed",
        )

    def get_automatically_stop_seeding_completed_torrents_status(
        self, is_need_to_open_setting_download=False
    ) -> str:
        if is_need_to_open_setting_download:
            self.open_settings_download()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.TORRENT_AUTOMATICALLY_STOP_SEEDING_COMPLETED_TORRENTS,
            attribute_name="aria-pressed",
        )

    def verify_default_value(self) -> None:
        self.open_settings_download()
        assert (
            self.get_download_path(is_need_to_open_downloads_setting=False)
            == rf"C:\Users\{os_utils.get_username()}\Downloads"
        )
        assert self.get_toggle_ask_where_to_save_status() == "false"
        assert self.get_toggle_enable_torrent_client_status() == "true"
        assert self.get_max_number_connection_per_client() == 1000
        assert self.get_max_number_connection_per_item() == 100
        assert self.get_peers_listening_port() == 3800
        assert self.get_max_active_download() == 5
        assert self.get_max_active_seeding() == 5
        assert self.get_use_upnp_and_nat_pmp_port_forwarding_status() == "false"
        assert (
            self.get_automatically_stop_seeding_completed_torrents_status() == "false"
        )

    def verify_search_no_duplication(self):
        """
        Verify for bug: PF-3907
        By checking one search term and then check no duplication part
        """
        self.enter_value_to_search(search_text="Max active seeding")
        assert (
            self.get_count_shadow_elements(js_path=self.TORRENT_MAX_ACTIVE_SEEDING_ALL)
            == 1
        )

    def turn_on_toggle_use_upnp_and_nat_pmp_port_forwarding(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_use_upnp_and_nat_pmp_port_forwarding_status() != "true":
            self.click_shadow_element(
                js_path=self.TOGGLE_Use_UPnP_and_NAT_PMP_port_forwarding
            )
            assert self.get_use_upnp_and_nat_pmp_port_forwarding_status() == "true"

    def turn_off_toggle_use_upnp_and_nat_pmp_port_forwarding(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_use_upnp_and_nat_pmp_port_forwarding_status() != "false":
            self.click_shadow_element(
                js_path=self.TOGGLE_Use_UPnP_and_NAT_PMP_port_forwarding
            )
            assert self.get_use_upnp_and_nat_pmp_port_forwarding_status() == "false"

    def turn_on_toggle_automatically_stop_seeding_completed_torrents(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_automatically_stop_seeding_completed_torrents_status() != "true":
            self.click_shadow_element(
                js_path=self.TORRENT_AUTOMATICALLY_STOP_SEEDING_COMPLETED_TORRENTS
            )
            assert (
                self.get_automatically_stop_seeding_completed_torrents_status()
                == "true"
            )

    def turn_off_toggle_automatically_stop_seeding_completed_torrents(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_automatically_stop_seeding_completed_torrents_status() != "false":
            self.click_shadow_element(
                js_path=self.TORRENT_AUTOMATICALLY_STOP_SEEDING_COMPLETED_TORRENTS
            )
            assert (
                self.get_automatically_stop_seeding_completed_torrents_status()
                == "false"
            )

    def set_value_for_max_number_of_connections_per_client(
        self, max_number: int = 1000, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.fill_texts_shadow_element(
            js_path=self.TORRENT_MAX_NUMBER_CONNECTION_PER_CLIENT,
            text=str(max_number),
            is_press_enter=True,
        )

    def set_value_for_max_number_of_connections_per_item(
        self, max_number: int = 100, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.fill_texts_shadow_element(
            js_path=self.TORRENT_MAX_NUMBER_CONNECTION_PER_ITEM,
            text=str(max_number),
            is_press_enter=True,
        )

    def set_value_for_peers_listening_port(
        self, port_number: int = 3800, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.fill_texts_shadow_element(
            js_path=self.TORRENT_PEERS_LISTENING_PORT,
            text=str(port_number),
            is_press_enter=True,
        )

    def set_value_for_max_active_download(
        self, max_number: int = 5, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.fill_texts_shadow_element(
            js_path=self.TORRENT_MAX_ACTIVE_DOWNLOAD,
            text=str(max_number),
            is_press_enter=True,
        )

    def set_value_for_max_active_seeding(
        self, max_number: int = 5, is_need_to_open_downloads_setting=False
    ) -> None:
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        self.fill_texts_shadow_element(
            js_path=self.TORRENT_MAX_ACTIVE_SEEDING,
            text=str(max_number),
            is_press_enter=True,
        )

    def turn_on_toggle_enable_torrent_client(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        """Turn ON torrent feature

        Args:
            is_need_to_open_downloads_setting (bool, optional): _description_. Defaults to False.
        """
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_toggle_enable_torrent_client_status() != "true":
            self.click_shadow_element(js_path=self.TOGGLE_ENABLE_TORRENT_CLIENT)
            assert self.get_toggle_enable_torrent_client_status() == "true"

    def turn_off_toggle_enable_torrent_client(
        self, is_need_to_open_downloads_setting=False
    ) -> None:
        """Turn OFF torrent feature

        Args:
            is_need_to_open_downloads_setting (bool, optional): _description_. Defaults to False.
        """
        if is_need_to_open_downloads_setting:
            self.open_settings_download()
        if self.get_toggle_enable_torrent_client_status() != "false":
            self.click_shadow_element(js_path=self.TOGGLE_ENABLE_TORRENT_CLIENT)
            assert self.get_toggle_enable_torrent_client_status() == "false"

    def clear_all_setting_values_and_reload(
        self, is_need_to_open_downloads_setting=True
    ) -> None:
        # Open the setting download page if any
        if is_need_to_open_downloads_setting:
            self.open_settings_download()

        # Get the current value
        previous_value_max_number_connection_per_client = (
            self.get_max_number_connection_per_client()
        )
        previous_value_max_number_connection_per_item = (
            self.get_max_number_connection_per_item()
        )
        previous_value_peers_listening_port = self.get_peers_listening_port()
        previous_value_max_active_download = self.get_max_active_download()
        previous_value_max_active_seeding = self.get_max_active_seeding()

        # clear all and checking they're cleared (blank value)
        self.clear_text_of_shadow_element(self.TORRENT_MAX_NUMBER_CONNECTION_PER_CLIENT)
        assert (
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_NUMBER_CONNECTION_PER_CLIENT, "value"
            )
            == ""
        )
        self.clear_text_of_shadow_element(self.TORRENT_MAX_NUMBER_CONNECTION_PER_ITEM)
        assert (
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_NUMBER_CONNECTION_PER_ITEM, "value"
            )
            == ""
        )
        self.clear_text_of_shadow_element(self.TORRENT_PEERS_LISTENING_PORT)
        assert (
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_PEERS_LISTENING_PORT, "value"
            )
            == ""
        )
        self.clear_text_of_shadow_element(self.TORRENT_MAX_ACTIVE_SEEDING)
        assert (
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_ACTIVE_SEEDING, "value"
            )
            == ""
        )
        self.clear_text_of_shadow_element(self.TORRENT_MAX_ACTIVE_DOWNLOAD)
        assert (
            self.get_attribute_value_of_shadow_element(
                self.TORRENT_MAX_ACTIVE_DOWNLOAD, "value"
            )
            == ""
        )

        # Reload the page & checking the previous values are filled again
        self.reload_page()
        assert (
            self.get_max_number_connection_per_client()
            == previous_value_max_number_connection_per_client
        )
        assert (
            self.get_max_number_connection_per_item()
            == previous_value_max_number_connection_per_item
        )
        assert self.get_peers_listening_port() == previous_value_peers_listening_port
        assert self.get_max_active_download() == previous_value_max_active_download
        assert self.get_max_active_seeding() == previous_value_max_active_seeding
