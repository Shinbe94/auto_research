import time

from appium.webdriver.webelement import WebElement as AppiumElement
from pywinauto import Application
from pywinauto.keyboard import send_keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from src.pages.constant import AWADL, CocCocTitles
from tests import setting

lang = setting.coccoc_language


class Toolbar(BaseAppium):
    # Locators

    if lang == "en":
        EXTENSION_BTN = (By.NAME, "Extensions")
    else:
        EXTENSION_BTN = (By.NAME, "Tiện ích mở rộng")
    if lang == "en":
        OPEN_DOWNLOAD_PAGE_BTN = (By.NAME, "Show 'Downloads' button")
    else:
        OPEN_DOWNLOAD_PAGE_BTN = (By.NAME, "Nút bấm mở trang 'Tải xuống'")
    if lang == "en":
        ADDRESS_AND_SEARCH_BAR = (By.NAME, "Address and search bar")
    else:
        ADDRESS_AND_SEARCH_BAR = (By.NAME, "Thanh địa chỉ và tìm kiếm")

    if "en" in lang:
        BTN_NEW_TAB = (By.NAME, "New Tab")
    else:
        BTN_NEW_TAB = (By.NAME, "Thẻ mới")

    if "en" in lang:
        BTN_NEW_TAB_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Tab/Button[@Name="New Tab"]',
        )
    else:
        BTN_NEW_TAB_XPATH = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Tab/Button[@Name="Thẻ mới"]',
        )

    if "en" in lang:
        ADBLOCK_ICON = (By.NAME, "Block ads on this page")
    else:
        ADBLOCK_ICON = (By.NAME, "Chặn quảng cáo trên trang này")
    if "en" in lang:
        DOWNLOAD_VIDEO_AUDIO_ICON = (By.NAME, "Download video, audio")
    else:
        DOWNLOAD_VIDEO_AUDIO_ICON = (By.NAME, "Tải video, audio")

    if "en" in lang:
        SHARE_THIS_PAGE = (By.XPATH, '//Button[@Name="Share this page"]')
    else:
        SHARE_THIS_PAGE = (By.XPATH, '//Button[@Name="Chia sẻ trang này"]')

    # if "en" in lang:
    #     RELOAD_THIS_PAGE = (By.NAME, "Reload this page")
    # else:
    #     RELOAD_THIS_PAGE = (By.NAME, "Tải lại trang này")
    if "en" in lang:
        RELOAD_THIS_PAGE = (By.XPATH, '//Pane/ToolBar//Button[@Name="Reload"]')
    else:
        RELOAD_THIS_PAGE = (By.XPATH, '//Pane/ToolBar//Button[@Name="Tải lại"]')

    if "en" in lang:
        STOP_LOADING_THIS_PAGE = (By.NAME, "Stop loading this page")
    else:
        STOP_LOADING_THIS_PAGE = (By.NAME, "Dừng tải trang này")

    SAVIOR_DIALOG_BTN_DOWNLOAD = (AWADL.AUTOMATION_ID, "media_video_Full_HD_1080p_mp4")

    if "en" in lang:
        TOR_PROFILE_ICON = (By.NAME, "Tor")
    else:
        TOR_PROFILE_ICON = (By.NAME, "Tor")

    if "en" in lang:
        CLOSE_INCOGNITO_WITH_TOR = (By.NAME, "Close Incognito with Tor")
    else:
        CLOSE_INCOGNITO_WITH_TOR = (By.NAME, "Đóng cửa sổ ẩn danh với Tor")

    if "en" in lang:
        WINDOW_INCOGNITO_WITH_TOR = (By.NAME, "Incognito with Tor")
    else:
        WINDOW_INCOGNITO_WITH_TOR = (By.NAME, "Cửa sổ ẩn danh với Tor")

    if "en" in lang:
        BTN_BOOKMARK_THIS_TAB = (By.NAME, "Bookmark this tab")
    else:
        BTN_BOOKMARK_THIS_TAB = (By.NAME, "Đánh dấu thẻ này")

    if "en" in lang:
        EDIT_BOOKMARK_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit bookmark"]',
        )
    else:
        EDIT_BOOKMARK_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa dấu trang"]',
        )
    if "en" in lang:
        BTN_EDIT_BOOKMARK_FOR_THIS_TAB = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//ToolBar//Button[@Name="Bookmark this tab"]',
        )
    else:
        BTN_EDIT_BOOKMARK_FOR_THIS_TAB = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//ToolBar//Button[@Name="Đánh dấu thẻ này"]',
        )
    if "en" in lang:
        EDIT_BOOKMARK_DIALOG_BTN_REMOVE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit bookmark"]//Button[@Name="Remove"]',
        )
    else:
        EDIT_BOOKMARK_DIALOG_BTN_REMOVE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa dấu trang"]//Button[@Name="Xóa"]',
        )

    if "en" in lang:
        BOOKMARK_ADDED_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Bookmark added"]',
        )
    else:
        BOOKMARK_ADDED_DIALOG = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Đã thêm dấu trang"]',
        )

    if "en" in lang:
        EDIT_BOOKMARK_DIALOG_BTN_CLOSE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit bookmark"]//Button[@Name="Close"]',
        )
    else:
        EDIT_BOOKMARK_DIALOG_BTN_CLOSE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa dấu trang"]//Button[@Name="Đóng"]',
        )

    if "en" in lang:
        BOOKMARK_ADDED_DIALOG_BTN_DONE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Bookmark added"]//Button[@Name="Done"]',
        )
    else:
        BOOKMARK_ADDED_DIALOG_BTN_DONE = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Đã thêm dấu trang"]//Button[@Name="Xong"]',
        )

    if "en" in lang:
        COOKIES_BTN = (By.NAME, "Block third-party cookies on this page")
    else:
        COOKIES_BTN = (By.NAME, "Chặn cookie của bên thứ ba trên trang này")

    if "en" in lang:
        SITE_NOT_WORKING_BTN = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Text[@Name="Site not working?"]',
        )
    else:
        SITE_NOT_WORKING_BTN = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Text[@Name="Trang web không hoạt động?"]',
        )
    if "en" in lang:
        ALLOW_COOKIES_BTN = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Allow cookies"]',
        )
    else:
        ALLOW_COOKIES_BTN = (
            By.XPATH,
            '//Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Cho phép cookie"]',
        )
    if "en" in lang:
        BTN_CLOSE_INFOBAR = (
            By.XPATH,
            '/Pane[@ClassName="#32769"][@Name="Desktop 1"]/Pane[@ClassName="Chrome_WidgetWin_1"][@Name="New Tab - Cốc Cốc"]/Pane/Pane/Pane/Group[@Name="Infobar Container"]/Custom[@Name="Infobar"]/Button[@Name="Close"]',
        )
    else:
        BTN_CLOSE_INFOBAR = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.NEW_TAB_TITLE}"]//Group[@Name="Bộ chứa Thanh thông tin"]/Custom[@Name="Thanh thông tin"]/Button[@Name="Đóng"]',
        )

    ACCEPT_COOKIES_YOUTUBE = (By.NAME, "Accept all")
    YOUTUBE_MOVIE_PLAYER = (AWADL.AUTOMATION_ID, "movie_player")
    YOUTUBE_VIDEO_ARE = (By.NAME, "YouTube Video Player")
    # COCCOC_LOGO = (
    #     By.XPATH,
    #     '//Pane[@ClassName="Chrome_WidgetWin_1"]//Group[@AutomationId="__next"]//Hyperlink[@Name="Coccoc logo"]',
    # )

    COCCOC_LOGO = (By.NAME, "Coccoc logo")
    if "en" in lang:
        CONTEXT_MENU_OPEN_IN_INCOGNITO_WINDOW_WITH_TOR = (
            By.NAME,
            "Open in Incognito window with Tor",
        )
    else:
        CONTEXT_MENU_OPEN_IN_INCOGNITO_WINDOW_WITH_TOR = (
            By.NAME,
            "Mở trong cửa sổ Ẩn danh với Tor",
        )

    if lang == "en":
        BTN_RETRY_WITH_TOR = (By.NAME, "Retry with Tor")
    else:
        BTN_RETRY_WITH_TOR = (By.NAME, "Thử lại với Tor")

    if lang == "en":
        BTN_LEARN_MORE_TOR = (By.NAME, "Learn more")
    else:
        BTN_LEARN_MORE_TOR = (By.NAME, "Tìm hiểu thêm")

    if "en" in lang:
        YOU = (By.XPATH, '//ToolBar//Button[@Name="You"]')
    else:
        YOU = (By.XPATH, '//ToolBar//Button[@Name="Bạn"]')

    if "en" in lang:
        PERSON_1 = (By.XPATH, '//ToolBar//Button[@Name="Person 1"]')
    else:
        PERSON_1 = (By.XPATH, '//ToolBar//Button[@Name="Person 1"]')

    if "en" in lang:
        MANAGE_PROFILES = (By.XPATH, '//Button[@Name="Manage profiles"]')
    else:
        MANAGE_PROFILES = (By.XPATH, '//Button[@Name="Quản lý hồ sơ"]')

    if "en" in lang:
        HOME_BTN = (By.XPATH, '//Pane/ToolBar/Button[@Name="Home"]')
    else:
        HOME_BTN = (By.XPATH, '//Pane/ToolBar/Button[@Name="Trang chủ"]')

    # if "en" in lang:
    #     VIEW_SITE_INFOMATION = (
    #         By.XPATH,
    #         '//Pane/ToolBar/Group/MenuItem[@Name="View site information"]',
    #     )
    # else:
    #     VIEW_SITE_INFOMATION = (
    #         By.XPATH,
    #         '//Pane/ToolBar/Group/MenuItem[@Name="Xem thông tin trang web"]',
    #     )
    if "en" in lang:
        VIEW_SITE_INFOMATION = (
            By.NAME,
            "View site information",
        )
    else:
        VIEW_SITE_INFOMATION = (
            By.NAME,
            "Xem thông tin trang web",
        )

    # Interaction methods
    def open_download_page(self):
        self.click_element(self.OPEN_DOWNLOAD_PAGE_BTN)

    def open_extension_page(self):
        self.click_element(self.EXTENSION_BTN)

    def get_opening_url(self, timeout=15) -> str:
        """
        To get the current url at omni box
        :param timeout:
        :return:
        """
        element = self.get_element(self.ADDRESS_AND_SEARCH_BAR)
        interval_delay = 1
        total_delay = 0
        url = None
        while total_delay < timeout:
            try:
                url = self.get_element_attribute_by_its_name_and_its_element(
                    element, "Value.Value"
                )
                if (url is not None) and ("about:blank" not in url):
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        # return is_exist
        # url = self.get_element_attribute_by_its_name_and_its_element(element, 'Value.Value')
        return url

    def click_address_and_search_bar(self, is_clear_data=False):
        """
        Click to target the mouse on the omni box
        to active the window on top or to set the text for it
        :param is_clear_data:
        :return:
        """
        self.click_element(self.ADDRESS_AND_SEARCH_BAR)
        if is_clear_data:
            self.clear_text_of_element(self.ADDRESS_AND_SEARCH_BAR)

    def clear_text_of_address_and_search_bar(self):
        self.clear_text_of_element(self.ADDRESS_AND_SEARCH_BAR)

    def make_search_value(
        self, search_str: str, is_press_enter: bool, sleep_n_seconds: int = 0
    ) -> None:
        """
        Make a search or enter url to load the page
        Args:
            search_str: search text or full url
            is_press_enter: True -> press enter
            sleep_n_seconds: --> sleep n seconds if any
        Returns:
        """
        self.fill_texts(self.ADDRESS_AND_SEARCH_BAR, search_str, is_press_enter)
        if is_press_enter:
            time.sleep(sleep_n_seconds)

    def make_search_value_with_tor_window(
        self,
        search_str: str,
        is_press_enter: bool,
        target_windows_title: str = None,
        timeout=setting.timeout_for_tor_loadpage_playwright,
    ) -> None:
        """
        Make a search or enter url to load the page from Tor window
        Logic check and wait for the window is loaded ok by TOR
        Args:
            search_str: search text or full url
            is_press_enter: True -> press enter
            target_windows_title: the target window title, specify if checking needed
        Returns:
        """
        self.fill_texts(self.ADDRESS_AND_SEARCH_BAR, search_str, is_press_enter)
        interval_delay = 15
        total_delay = 0
        if target_windows_title is not None:
            time.sleep(10)  # Sleep for loading as TOR network is always slow
            while total_delay < timeout:
                try:
                    if (
                        len(open_browser.find_window_handle(title=target_windows_title))
                        > 0
                    ):
                        break
                    elif (
                        len(open_browser.find_window_handle(title="404 Page - Cốc Cốc"))
                        > 0
                    ):
                        send_keys("{F5}")
                except Exception:
                    pass
                time.sleep(interval_delay)
                total_delay += interval_delay
            if total_delay > timeout:
                print(rf"Timeout for loading the page after {timeout} seconds")

    def make_search_to_unreached_site(
        self,
        search_str: str,
        is_press_enter: bool,
        timeout=setting.timeout_for_tor,
        is_wait_for_retry_with_tor=True,
    ) -> None:
        """
        Make a search or enter url to the unreachable site
        Logic check and wait for the Retry with TOR option is appeared
        Args:
            search_str: search text or full url
            is_press_enter: True -> press enter
            timeout:
            is_wait_for_retry_with_tor: True -> wait for the button retry with tor appears
        Returns:
        """
        self.fill_texts(self.ADDRESS_AND_SEARCH_BAR, search_str, is_press_enter)
        interval_delay = 10
        total_delay = 0
        if is_wait_for_retry_with_tor:
            while total_delay < timeout:
                try:
                    if (
                        len(open_browser.find_window_handle(title="404 Page - Cốc Cốc"))
                        > 0
                    ):
                        send_keys("{F5}")
                    elif self.is_element_appeared(self.BTN_RETRY_WITH_TOR):
                        break
                except Exception:
                    pass
                time.sleep(interval_delay)
                total_delay += interval_delay
            if total_delay > timeout:
                print(
                    rf"Timeout after {timeout} seconds for waiting the button: Retry with tor"
                )

    def click_accept_cookies(self) -> None:
        """To click accept cookies once access Youtube from TOR"""
        if self.is_element_appeared(self.ACCEPT_COOKIES_YOUTUBE, timeout=30):
            self.click_element(self.ACCEPT_COOKIES_YOUTUBE)

    def get_recent_search_element(
        self, search_str: str, language=setting.coccoc_language
    ) -> AppiumElement:
        if "en" in language:
            return self.get_element((By.NAME, rf"{search_str} search from history"))
        else:
            return self.get_element(
                (By.NAME, rf"Cụm từ tìm kiếm {search_str} từ lịch sử")
            )

    def get_search_suggestion_element(
        self, search_str: str, language=setting.coccoc_language
    ) -> AppiumElement:
        if "en" in language:
            return self.get_element((By.NAME, rf"{search_str} search suggestion"))
        else:
            return self.get_element((By.NAME, rf"Đề xuất tìm kiếm {search_str}"))

    def get_search_value_element(
        self, search_str: str, language=setting.coccoc_language
    ) -> AppiumElement:
        if "en" in language:
            return self.get_element((By.NAME, rf"{search_str} search"))
        else:
            return self.get_element((By.NAME, rf"Cụm từ tìm kiếm {search_str}"))

    def check_recent_search_is_displayed(
        self, search_str: str, language=setting.coccoc_language
    ):
        """
        Check the suggestion list after typing the search criteria (already pressed enter to search)
        Args:
            search_str: search string
            language:
        Returns:
        """
        assert self.get_recent_search_element(search_str, language=language)

    def check_search_suggestion_is_displayed(
        self, search_str: str, language=setting.coccoc_language
    ):
        """
        Check the suggestion list after typing the search criteria (don't press enter to search)
        Args:
            search_str: search string
            language:
        Returns:
        """
        assert self.get_search_suggestion_element(search_str, language=language)

    def check_search_value_element_is_displayed(
        self, search_str: str, language=setting.coccoc_language
    ):
        """
        Check the suggestion list after typing the search criteria (The value is inputted)
        Args:
            search_str: search string
            language:
        Returns:
        """
        assert self.get_search_value_element(search_str, language=language)

    def click_recent_search_item(
        self, search_str: str, language=setting.coccoc_language
    ):
        self.get_recent_search_element(search_str, language=language).click()

    def open_new_tab(self):
        """
        To open newtab by click plus button
        :return:
        """
        self.click_element(self.BTN_NEW_TAB_XPATH)

    def click_to_tab_by_its_name(self, tab_name: str = CocCocTitles.NEW_TAB) -> None:
        xpath_tab = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{tab_name} - Cốc Cốc"]//Tab',
        )
        self.click_element(xpath_tab)

    def click_to_tab_by_its_name_unloaded_site(self, tab_name: str) -> None:
        xpath_tab = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][starts-with(@Name,"{tab_name} -")]/Pane/Pane/Pane/Pane/Tab/Pane/Pane',
        )
        self.click_element(xpath_tab)

    def close_tab_by_its_name(self, tab_name: str) -> None:
        xpath_tab = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{tab_name} - Cốc Cốc"]//Tab/Button[@Name="Close"]',
        )
        self.click_element(xpath_tab)

    def close_tab_by_keyboard(self, tab_name: str) -> None:
        xpath_tab = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{tab_name} - Cốc Cốc"]//Tab',
        )
        self.get_element(xpath_tab).send_keys(Keys.CONTROL + "w")

    @staticmethod
    def get_list_item_from_omni_dropdown() -> list:
        list_drop: list = []
        if "en" in lang:
            browser_window = open_browser.connect_to_coccoc_by_title(
                CocCocTitles.NEW_TAB_TITLE_EN
            )
        else:
            browser_window = open_browser.connect_to_coccoc_by_title(
                CocCocTitles.NEW_TAB_TITLE_VI
            )

        # browser.window().print_control_identifiers()
        for window in browser_window.windows():
            for item in window.descendants(control_type="ListItem"):
                text: str = item.window_text()
                if len(text) > 0:
                    if text.startswith("Remove Suggestion button") or text.startswith(
                        "Resume journey button"
                    ):
                        pass
                    else:
                        list_drop.append(item.window_text())
                # print(item.window_text())
        return list_drop

    def get_list_item_from_omni_dropdown2(self) -> list:
        """
        Get the dropdown list while entering text from omni box
        :return:
        """
        list_item = (By.XPATH, '//Pane[@ClassName="Chrome_WidgetWin_1"]//ListItem')
        elements = self.get_elements(list_item)
        texts = [
            self.get_element_attribute_by_its_name_and_its_element(x, "Name")
            for x in elements
            if self.get_element_attribute_by_its_name_and_its_element(x, "Name")
            is not None
        ]
        return texts
        # return
        # for ele in elements:
        #     print(self.get_element_attribute_by_its_name_and_its_element(ele, 'Name'))

    def is_button_download_video_and_audio_appeared(self) -> bool:
        if self.is_element_appeared(self.DOWNLOAD_VIDEO_AUDIO_ICON) is True:
            return True
        else:
            return False

    def click_tor_1_profile(self):
        """
        to click Tor profile( only 1 Tor window is opened)
        Returns:
        """
        self.click_element(self.TOR_PROFILE_ICON)
        time.sleep(1)

    def click_tor_profile(self, no_of_profile: int):
        """
        to click Tor profile( multiple Tor window is opened)
        Returns:
        """
        tor_profile_icon = (By.NAME, rf"Tor ({str(no_of_profile)})")
        self.click_element(tor_profile_icon)
        time.sleep(1)

    def check_number_of_tor_window_opening(self, no_of_window: int):
        """
        To check how many to windows are opening
        :param no_of_window: the number want to check
        :return:
        """
        if "en" in lang:
            no_of_window_locator = (By.NAME, rf"{no_of_window} open Incognito windows")
        else:
            no_of_window_locator = (By.NAME, rf"{no_of_window} cửa sổ Ẩn danh đang mở")
        assert self.is_element_appeared(no_of_window_locator)

    def click_close_tor(self):
        self.click_element(self.CLOSE_INCOGNITO_WITH_TOR)

    def click_btn_bookmark_this_tab(self):
        self.click_element(self.BTN_BOOKMARK_THIS_TAB)

    def click_btn_edit_bookmark_this_tab(self):
        self.click_element(self.BTN_EDIT_BOOKMARK_FOR_THIS_TAB)

    def click_to_close_edit_bookmark_dialog(self):
        self.click_element(self.EDIT_BOOKMARK_DIALOG_BTN_CLOSE)

    def click_btn_done_bookmark_dialog(self):
        self.click_element(self.BOOKMARK_ADDED_DIALOG_BTN_DONE)

    def add_current_site_to_bookmark(self, url: str, is_click_btn_done=True):
        """
        Accessing the site, click star button then save the current site to the bookmark
        Args:
            url: accessing site
            is_click_btn_done: Click done to complete action
        Returns:
        """
        self.make_search_value(search_str=url, is_press_enter=True)
        time.sleep(2)
        self.click_btn_bookmark_this_tab()
        assert self.get_element(self.BOOKMARK_ADDED_DIALOG)
        if is_click_btn_done:
            self.click_btn_done_bookmark_dialog()

    def remove_current_bookmarked_site(self, url: str):
        """
        Accessing the bookmarked site then click btn to remove it
        To remove the bookmarked site by accessing it
        Args:
            url: the url that bookmarked
        Returns:
        """
        self.make_search_value(search_str=url, is_press_enter=True)
        self.click_btn_edit_bookmark_this_tab()
        # May try to double-click to target to the current view
        self.double_click_element(self.EDIT_BOOKMARK_DIALOG_BTN_REMOVE)

    def allow_cookies(self, url, sleep_n_seconds: int = 0):
        self.make_search_value(
            url, is_press_enter=True, sleep_n_seconds=sleep_n_seconds
        )
        assert self.is_element_appeared(self.COOKIES_BTN, timeout=60)
        self.click_element(self.COOKIES_BTN)
        self.double_click_element(self.SITE_NOT_WORKING_BTN)
        self.click_element(self.ALLOW_COOKIES_BTN)

    def click_download_video_audio(self) -> None:
        """
        To click the btn download media( after accessing the media site)
        """
        self.click_element(self.DOWNLOAD_VIDEO_AUDIO_ICON)

    def click_btn_savior_dialog_download(self) -> None:
        """
        To click the btn download from Savior dialog
        """
        self.click_ele(self.SAVIOR_DIALOG_BTN_DOWNLOAD)

    def hover_on_youtube_movie(self) -> None:
        # self.move_to_element(self.YOUTUBE_MOVIE_PLAYER)
        self.move_to_element(self.YOUTUBE_VIDEO_ARE)

    def check_adblock_icon_shown(self) -> None:
        assert self.is_element_appeared(self.ADBLOCK_ICON)

    def check_adblock_icon_is_not_shown(self) -> None:
        assert self.is_element_disappeared(self.ADBLOCK_ICON)

    def click_adblock_icon(self) -> None:
        self.click_element(self.ADBLOCK_ICON)

    def right_click_coccoc_logo(self) -> None:
        """
        Access coccoc.com then right click the logo
        """
        self.make_search_value(
            search_str="https://coccoc.com", is_press_enter=True, sleep_n_seconds=3
        )
        self.right_click_element(self.COCCOC_LOGO)

    def open_link_incognito_window_with_tor(self) -> None:
        self.click_element(self.CONTEXT_MENU_OPEN_IN_INCOGNITO_WINDOW_WITH_TOR)
        time.sleep(1)

    def wait_for_reload_this_page_button_shown(self) -> bool:
        return self.is_element_appeared(
            self.RELOAD_THIS_PAGE, timeout=setting.timeout_for_tor
        )

    def click_reload_this_page_btn(self) -> None:
        self.double_click_element(self.RELOAD_THIS_PAGE)

    def click_retry_with_tor(self) -> None:
        self.click_element(self.BTN_RETRY_WITH_TOR)

    def get_link_learn_more_tor(self) -> str:
        """
        Get the actual link of btn learn more
        """
        return self.get_element_attribute_by_its_name_and_locator(
            self.BTN_LEARN_MORE_TOR, "Value.Value"
        )

    def click_tor_learn_more_btn(self) -> None:
        assert self.get_link_learn_more_tor()
        self.click_element(self.BTN_LEARN_MORE_TOR)
        assert (
            self.get_opening_url()
            in "https://blog.coccoc.com/gioi-thieu-che-do-an-danh-voi-tor-tren-trinh-duyet-may-tinh-coc-coc/"
        )

    def click_you_btn(self) -> None:
        """To open sysncing dialog by default user"""
        self.click_element(self.YOU)

    def click_person_1_btn(self) -> None:
        """To open sysncing dialog of Person 1"""
        self.click_element(self.PERSON_1)

    def click_manage_profiles(self) -> None:
        # self.click_element(self.MANAGE_PROFILES)
        self.double_click_element(self.MANAGE_PROFILES)
        time.sleep(3)

    def click_close_infobar(self) -> None:
        # if self.is_element_appeared(self.BTN_CLOSE_INFOBAR, timeout=10):
        #     self.double_click_element(self.BTN_CLOSE_INFOBAR)
        #     print("Element clicked")
        #     time.sleep(2)
        # else:
        #     print("Element is not appeared")
        self.double_click_element(self.BTN_CLOSE_INFOBAR)

    def check_home_btn_appeared(self) -> None:
        assert self.is_element_appeared(self.HOME_BTN)

    def check_home_btn_disappeared(self) -> None:
        assert self.is_element_disappeared(self.HOME_BTN)

    def click_home_btn(self):
        if self.is_element_appeared(self.HOME_BTN):
            self.click_element(self.HOME_BTN)
            self.click_element(self.HOME_BTN)

    def click_btn_share_this_page(self) -> None:
        self.click_element(self.SHARE_THIS_PAGE)

    def click_view_site_infomation(self) -> None:
        self.click_element(self.VIEW_SITE_INFOMATION)


"""Outside the class, pywinauto section"""


def is_icon_appeared(window: Application, icon_name: str, timeout=5) -> bool:
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    # element = None
    is_existed = False
    # start_time = time.time()
    while total_delay < max_delay:
        try:
            # element = window.window().child_window(title=icon_name)
            if window.window().child_window(title=icon_name).exists(timeout=1) is True:
                is_existed = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    # end_time = time.time()
    # print(rf'is exist {is_existed}, time elapsed {end_time - start_time}')
    return is_existed
