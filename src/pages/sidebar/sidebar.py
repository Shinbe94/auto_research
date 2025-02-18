import codecs
import random
import time
from typing import Tuple

from selenium.webdriver.common.by import By

from src.apis.paid_icons.paid_icons import PaidIcons
from src.pages.base import BaseAppium
from src.pages.constant import AWADL
from src.pages.sidebar.sidebar_custom_icon_context_menu import (
    SidebarCustomIconContextMenu,
)
from src.utilities import os_utils
from tests import setting

paid_icons = PaidIcons()


class Sidebar(BaseAppium):
    lang = setting.coccoc_language

    # Locators
    if lang == "en":
        HISTORY = (By.NAME, "History")
    else:
        HISTORY = (By.NAME, "Lịch sử")
    FACEBOOK_MESSENGER = (By.NAME, "Facebook Messenger")
    ZALO = (By.NAME, "Zalo")
    COCCOC_GAME = (By.NAME, "Cốc Cốc Games")
    TELEGRAM = (By.NAME, "Telegram")
    SKYPE = (By.NAME, "Skype")
    COCCOC_POINTS = (By.NAME, "Cốc Cốc Points")
    YOUTUBE = (By.NAME, "Youtube")
    FACEBOOK = (By.NAME, "Facebook")
    if lang == "en":
        ADDRESS_AND_SEARCH_BAR = (By.NAME, "Address and search bar")
    else:
        ADDRESS_AND_SEARCH_BAR = (By.NAME, "Thanh địa chỉ và tìm kiếm")
    if lang == "en":
        COCCOC_NOTIFICATION = (By.NAME, "Cốc Cốc Notifications")
    else:
        COCCOC_NOTIFICATION = (By.NAME, "Thông báo Cốc Cốc")

    if lang == "en":
        CONFIG_AND_CONTROL_SIDEBAR = (By.NAME, "Config and control Sidebar")
    else:
        CONFIG_AND_CONTROL_SIDEBAR = (By.NAME, "Tùy chọn và điều khiển thanh bên")

    if lang == "en":
        ADD_YOUR_FAVORITE_SITE = (By.NAME, "Add your favorite site")
    else:
        ADD_YOUR_FAVORITE_SITE = (By.NAME, "Thêm trang web ưa thích")
    if lang == "en":
        SIDEBAR_WEB_PANEL_BTN_HIDE = (By.NAME, "Hide")
    else:
        SIDEBAR_WEB_PANEL_BTN_HIDE = (By.NAME, "Hide")

    if lang == "en":
        BTN_EDIT = (By.NAME, "Edit")
    else:
        BTN_EDIT = (By.NAME, "Chỉnh sửa")

    if lang == "en":
        REMOVE_FROM_SIDEBAR = (By.NAME, "Remove from Sidebar")
    else:
        REMOVE_FROM_SIDEBAR = (By.NAME, "Xóa khỏi thanh bên")

    TYPE_URL = (AWADL.AUTOMATION_ID, "submit-input")
    ADD_BTN = (AWADL.AUTOMATION_ID, "submit-btn")
    OPEN_IN_SIDEBAR_WINDOW_CHECKBOX = (AWADL.AUTOMATION_ID, "checkbox")

    # Interaction Methods

    def is_sidebar_shown(self):
        assert self.is_element_appeared(self.CONFIG_AND_CONTROL_SIDEBAR)

    def is_sidebar_hidden(self):
        assert self.is_element_disappeared(self.CONFIG_AND_CONTROL_SIDEBAR) is True

    def is_skype_feature_icon_shown(self):
        assert self.get_element(self.SKYPE)

    def check_feature_icon_show(self, icon_name: str):
        """
        To check the feature shown by name
        Args:
            icon_name:
        Returns:
        """
        icon = (By.NAME, icon_name)
        assert self.get_element(icon)

    def click_to_hide_sidebar_web_panel(self):
        """
        To close the sidebar web panel
        Returns:
        """
        if self.is_element_appeared(self.SIDEBAR_WEB_PANEL_BTN_HIDE):
            self.click_element(self.SIDEBAR_WEB_PANEL_BTN_HIDE)

    def check_paid_icons(self):
        icons = paid_icons.get_paid_icons().as_dict
        icon_names = [icon.get("title") for icon in icons]
        icon_urls = [icon.get("url") for icon in icons]

        self.check_correct_paid_icons(icon_names)
        # self.check_click_paid_icon(icon_names, icon_urls)

    def check_correct_paid_icons(self, icon_names: list):
        """
        To check the correct list paid icons are showed on sidebar
        Args:
            icon_names: list paid icon
        Returns:
        """
        for icon_name in icon_names:
            paid_icon_locator = (By.NAME, f"{icon_name}")
            assert self.get_element(paid_icon_locator)
            self.right_click_element(paid_icon_locator)

    def click_all_paid_icon(self, icon_names: list):
        """
        To click all paid icon one by one
        Args:
            icon_names: list paid icons
        Returns:
        """
        for icon_name in icon_names:
            paid_icon_locator = (By.NAME, f"{icon_name}")
            self.click_element(paid_icon_locator)

    def click_all_custom_icons(self, icon_names: list, is_hide=True):
        """
        To click all customs icon one by one
        Args:
            icon_names: list custom icons
            is_hide: close the sidebar web panel if True
        Returns:
        """
        for icon_name in icon_names:
            custom_icon_locator = (By.NAME, f"{icon_name}")
            self.click_element(custom_icon_locator)
            time.sleep(3)
            if is_hide:
                self.click_to_hide_sidebar_web_panel()

    def click_custom_icon(self, icon_name: str, is_hide=True):
        """
        To click  custom icon
        Args:
            icon_name: list custom icons
            is_hide: close the sidebar web panel if True
        Returns:
        """

        custom_icon_locator = (By.NAME, f"{icon_name}")
        self.click_element(custom_icon_locator)
        time.sleep(3)
        if is_hide:
            self.click_to_hide_sidebar_web_panel()

    def get_all_opening_url(self):
        elements = self.get_elements(self.ADDRESS_AND_SEARCH_BAR)
        list_url = [
            self.get_element_attribute_by_its_name_and_its_element(
                element, "Value.Value"
            )
            for element in elements
        ]
        return list_url

    def get_opening_url(self):
        elements = self.get_elements(self.ADDRESS_AND_SEARCH_BAR)
        list_url = [
            self.get_element_attribute_by_its_name_and_its_element(
                element, "Value.Value"
            )
            for element in elements
        ]
        return list_url

    def click_sidebar_setting(self):
        """
        To open sidebar setting dialog
        Returns:
        """
        self.click_element(self.CONFIG_AND_CONTROL_SIDEBAR)

    def click_history(self):
        self.click_element(self.HISTORY)

    def click_facebook_messenger(self):
        self.click_element(self.FACEBOOK_MESSENGER)

    def click_youtube(self):
        self.click_element(self.YOUTUBE)

    def click_facebook(self):
        self.click_element(self.FACEBOOK)

    def right_click_custom_icon_by_its_name(self, icon_name: str):
        """
        Right click to custom icon
        Args:
            icon_name:
        Returns:
        """
        by_locator = (By.NAME, icon_name)
        self.right_click_element(by_locator)

    def click_btn_add_your_favourite_site(self):
        """
        Click the btn add icon into the sidebar
        Returns:
        """
        self.click_element(self.ADD_YOUR_FAVORITE_SITE)

    def click_add_btn(self):
        """
        click add btn to complete add custom icon
        Returns:
        """
        self.click_ele(self.ADD_BTN)

    def add_favourite_url(self, url: str):
        """
        Add the url then click add btn to add the custom icon into the sidebar
        Args:
            url:
        Returns:
        """
        self.click_btn_add_your_favourite_site()
        self.send_keys_ele(self.TYPE_URL, url)
        self.click_add_btn()
        time.sleep(2)
        self.click_to_hide_sidebar_web_panel()

    def search_url_by_name(self, icon_name: str):
        """
        To search site by name, autocomplete
        Args:
            icon_name:
        Returns:
        """
        self.send_keys_ele(self.TYPE_URL, icon_name)

    def add_custom_icon_by_searching_its_name(self, icon_name: str, icon_url: str):
        """
        Search the icon from the search box, (query from history)
        Args:
            icon_name: the search value
            icon_url: the url of value
        Returns:
        """
        self.click_btn_add_your_favourite_site()
        self.search_url_by_name(icon_name)
        self.click_autocomplete_icon(icon_url)
        self.click_add_btn()
        # Sleep for the sidebar web panel to load the page contents
        time.sleep(5)
        self.click_to_hide_sidebar_web_panel()

    def click_autocomplete_icon(self, icon_url: str):
        """
        To select the result from the search drop down list by the url
        Args:
            icon_url: url
        Returns:
        """
        autocomplete_ele = (AWADL.NAME, icon_url)
        self.click_ele(autocomplete_ele)

    def right_click_all_custom_icons(self, icon_names: list):
        custom_icon_context_menu = SidebarCustomIconContextMenu(self.wad)

        for icon_name in icon_names:
            self.right_click_custom_icon_by_its_name(icon_name)
            custom_icon_context_menu.verify_ui()

    def get_status_add_btn(self) -> str:
        """
        to get the current state of the button complete add icon in to the sidebar
        Returns: 'true' or 'false'
        """
        return self.get_ele_attribute_by_its_name_and_locator(self.ADD_BTN, "IsEnabled")

    def check_open_in_sidebar_window_checkbox(self):
        """
        To check/uncheck the option: Open In Sidebar Window
        Returns:
        """
        self.click_ele(self.OPEN_IN_SIDEBAR_WINDOW_CHECKBOX)

    def add_recommended_icon(
        self, icon_name: str, is_checked_on_open_in_sidebar_window=True
    ):
        """
        To quickly add the custom icon from recommended sites
        Args:
            is_checked_on_open_in_sidebar_window: True checked, False: uncheck
            icon_name:
        Returns:
        """
        self.click_btn_add_your_favourite_site()
        if not is_checked_on_open_in_sidebar_window:
            self.check_open_in_sidebar_window_checkbox()
        icon_name_locator = (By.NAME, icon_name)
        self.click_element(icon_name_locator)
        time.sleep(2)
        self.click_to_hide_sidebar_web_panel()

    def get_list_recommended_icons(self) -> dict:
        self.click_btn_add_your_favourite_site()
        actual_list: dict = {}
        for icon_name in list(setting.list_recommended_custom_icons.keys()):
            icon_name_locator = (By.NAME, icon_name)
            if self.get_element(icon_name_locator):
                actual_list[icon_name] = setting.list_recommended_custom_icons.get(
                    icon_name
                )
        # if len(actual_list) > 0:
        #     read_write_data_by.write_text_to_file(
        #         file_name=rf'C:\Users\{os_utils.get_username()}\Documents\\Recommended Icons',
        #         content=str(actual_list))
        self.click_to_hide_sidebar_web_panel()
        return actual_list

    @staticmethod
    def get_list_default_custom_icon(profile_name: str = "Default") -> list:
        list_icons: list = []
        with codecs.open(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile_name}\Sidebar\Custom Icons",
            mode="r",
            encoding="utf-8",
            errors="ignore",
        ) as file:
            lines = file.read()

            for name in setting.list_possible_default_custom_icons:
                if name in lines:
                    list_icons.append(name)
        return list_icons

    def get_random_recommended_icon(
        self, is_ignored_default_custom_icon=True
    ) -> Tuple[str, str]:
        ignore_list = self.get_list_default_custom_icon()
        recommended_list: dict = self.get_list_recommended_icons()
        if is_ignored_default_custom_icon:
            for i in ignore_list:
                if i in recommended_list.keys():
                    del recommended_list[i]

        # print(recommended_list)
        icon_name, url = random.choice(list(recommended_list.items()))
        return icon_name, url

    def click_btn_edit_from_custom_icon_context_menu(self):
        self.click_element(self.BTN_EDIT)

    def click_to_edit_custom_icon(self, icon_name):
        self.right_click_custom_icon_by_its_name(icon_name)
        self.click_btn_edit_from_custom_icon_context_menu()

    def remove_custom_icon_by_its_name(self, icon_name):
        icon_name_locator = (By.NAME, icon_name)
        if not self.is_element_disappeared(icon_name_locator):
            self.right_click_custom_icon_by_its_name(icon_name=icon_name)
            self.click_element(self.REMOVE_FROM_SIDEBAR)
            time.sleep(1)


""" OUTSIDE THE CLASS"""
