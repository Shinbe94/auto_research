import time

from pywinauto import Application
from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles, TestingSiteTittles
from tests import setting

lang = setting.coccoc_language
if "en" in lang:
    NEW_INCOGNITO_WINDOW_WITH_TOR = "New Incognito window with Tor"
else:
    NEW_INCOGNITO_WINDOW_WITH_TOR = "Cửa sổ Ẩn danh mới với Tor"


class MainMenu(BaseAppium):
    # Locators
    if lang == "en":
        HIDE_SIDEBAR = (By.NAME, "Hide Sidebar")
    else:
        HIDE_SIDEBAR = (By.NAME, "Ẩn thanh bên")

    if lang == "en":
        SHOW_SIDEBAR = (By.NAME, "Show Sidebar")
    else:
        SHOW_SIDEBAR = (By.NAME, "Hiển thị thanh bên")

    if lang == "en":
        COCCOC_NOTIFICATION = (By.NAME, "Cốc Cốc Notifications")
    else:
        COCCOC_NOTIFICATION = (By.NAME, "Thông báo Cốc Cốc")

    if "en" in lang:
        NEW_INCOGNITO_WINDOW = (By.NAME, "New Incognito window Ctrl+Shift+N")
    else:
        NEW_INCOGNITO_WINDOW = (By.NAME, "Cửa sổ Ẩn danh mới Ctrl+Shift+N")

    if "en" in lang:
        NEW_TOR_WINDOW = (By.NAME, "New Incognito window with Tor Alt+Shift+N")
    else:
        NEW_TOR_WINDOW = (By.NAME, "Cửa sổ Ẩn danh mới với Tor Alt+Shift+N")

    # if 'en' in lang:
    #     BOOKMARK = (By.NAME, 'Bookmarks')
    # else:
    #     BOOKMARK = (By.NAME, 'Dấu trang')

    if "en" in lang:
        BOOKMARK = (By.XPATH, '//MenuItem[@Name="Bookmarks"]')
    else:
        BOOKMARK = (By.XPATH, '//MenuItem[@Name="Dấu trang"]')
    if "en" in lang:
        TOOLBAR_BOOKMARK = (By.XPATH, '//ToolBar[@Name="Bookmarks"]')
    else:
        TOOLBAR_BOOKMARK = (By.XPATH, '//ToolBar[@Name="Dấu trang"]')

    if "en" in lang:
        SHOW_BOOKMARKS_BAR = (By.NAME, "Show bookmarks bar Ctrl+Shift+B")
    else:
        SHOW_BOOKMARKS_BAR = (By.NAME, "Hiển thị thanh dấu trang Ctrl+Shift+B")

    if lang == "en":
        MORE_TOOLS = (By.NAME, "More tools")
    else:
        MORE_TOOLS = (By.NAME, "Công cụ khác")

    if lang == "en":
        TASK_MANAGER = (By.NAME, "Task manager Shift+Esc")
    else:
        TASK_MANAGER = (By.NAME, "Trình quản lý tác vụ Shift+Esc")

    CC_MENU = (
        By.XPATH,
        rf'//Pane[@ClassName="Chrome_WidgetWin_1"]//MenuItem[@Name="Cốc Cốc"]',
    )

    if "en" in lang:
        COCCOC_MENU = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.NEW_TAB_TITLE}"]//MenuItem[@Name="Cốc Cốc"]',
        )
    else:
        COCCOC_MENU = (
            By.XPATH,
            rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.NEW_TAB_TITLE}"]//MenuItem[@Name="Cốc Cốc"]',
        )

    COCCOC_MENU_TOR = (
        By.XPATH,
        rf'//MenuItem[@Name="Cốc Cốc"]',
    )

    COCCOC_BBC_HOME_PAGE_MENU_TOR = (
        By.XPATH,
        rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{TestingSiteTittles.BBC_INCOGNITO_COCCOC_WINDOW_TITLE}"]//MenuItem[@Name="Cốc Cốc"]',
    )

    COCCOC_HOME_PAGE_MENU_TOR = (
        By.XPATH,
        rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.COCCOC_HOMEPAGE_TITLE_INCOGNITO_TOR}"]//MenuItem[@Name="Cốc Cốc"]',
    )
    COCCOC_UNTITLE_PAGE_MENU_TOR = (
        By.XPATH,
        rf'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.UNTITLED_INCOGNITO_COCCOC}"]//MenuItem[@Name="Cốc Cốc"]',
    )
    if "en" in lang:
        NEW_TOR_CONNECTION_FOR_THIS_SITE = (By.NAME, "New Tor connection for this site")
    else:
        NEW_TOR_CONNECTION_FOR_THIS_SITE = (
            By.NAME,
            "Kết nối Tor mới cho trang web này",
        )
    if "en" in lang:
        MENU_HELP = (By.XPATH, '//MenuBar//Menu/MenuItem[@Name="Help"]')
    else:
        MENU_HELP = (By.XPATH, '//MenuBar//Menu/MenuItem[@Name="Help"]')
    if "en" in lang:
        MENU_HELP_HELP_CENTER = (
            By.XPATH,
            '//MenuBar[@Name="Help"]/Pane/Pane/Menu[@Name="Help"]/MenuItem[@Name="Help center"]',
        )
    else:
        MENU_HELP_HELP_CENTER = (
            By.XPATH,
            '//MenuBar[@Name="Help"]/Pane/Pane/Menu[@Name="Help"]/MenuItem[@Name="Help center"]',
        )

    # Interaction methods
    @staticmethod
    def open_menu():
        app = open_browser.connect_to_coccoc_by_pywinauto(
            language=setting.coccoc_language
        )
        app.type_keys("%F")
        time.sleep(1)

    def open_coccoc_menu(self):
        """
        To click the main menu from any coccoc window
        """
        self.click_element(self.CC_MENU)

    def open_coccoc_menu_tor(self) -> None:
        self.click_element(self.COCCOC_MENU_TOR)

    def open_menu_from_newtab(self):
        """
        To click the main menu from the new tab window(normal window)
        """
        self.click_element(self.COCCOC_MENU)

    def open_menu_from_newtab_of_tor(self):
        """
        To click the main menu from the new tab of TOR window
        """
        self.click_element(self.COCCOC_MENU_TOR)

    @staticmethod
    def open_menu_tor_pywinauto():
        """Open coccoc menu from tor window by pywinauto

        Returns:
            _type_: _description_
        """
        app: Application = (
            open_browser.connect_to_coccoc_tor_by_pywinauto(
                language=setting.coccoc_language
            )
            .window(found_index=0)
            .set_focus()
        )
        app.type_keys("%F")
        time.sleep(1)
        return app

    def open_new_tor_connection_for_this_site(self):
        self.open_coccoc_menu()
        self.click_element(self.NEW_TOR_CONNECTION_FOR_THIS_SITE)

    def get_sidebar_status(self) -> str:
        """
        To get the status of sidebar, by workaround: checking the CocCoc Notification icon from sidebar is shown
        Returns: ON/OFF
        """
        if self.wait_for_element_disappear(self.COCCOC_NOTIFICATION):
            return "OFF"
        else:
            return "ON"

    def click_show_sidebar(self):
        self.click_element(self.SHOW_SIDEBAR)

    def click_hide_sidebar(self):
        self.click_element(self.HIDE_SIDEBAR)

    def open_new_tor_window_from_normal_window(self):
        """
        To open new TOR window from the normal profile
        Returns:
        """
        self.open_menu_from_newtab()
        self.click_element(self.NEW_TOR_WINDOW)

    def open_new_tor_window_from_tor_window(self):
        """
        To open new TOR window from the Tor window
        Returns:
        """
        # self.open_menu_tor_pywinauto()
        self.open_menu_from_newtab_of_tor()
        self.click_element(self.NEW_TOR_WINDOW)

    @staticmethod
    def open_tor_window_from_tor_window():
        """
        To open more Tor windows from a Tor window
        Returns:
        """
        app: Application = open_browser.connect_to_coccoc_tor_by_pywinauto(
            language=setting.coccoc_language
        ).window(found_index=0)
        app.set_focus().type_keys("%F")
        app.child_window(
            title_re=NEW_INCOGNITO_WINDOW_WITH_TOR, control_type="MenuItem"
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.1
        ).click_input()
        time.sleep(1)
        return app

    def click_to_open_incognito_window(self):
        self.open_menu_from_newtab()
        self.click_element(self.NEW_INCOGNITO_WINDOW)

    def click_menu_bookmark(self):
        # self.move_to_element_off_set(self.BOOKMARK, 50, 50)
        self.move_to_element(self.BOOKMARK)
        self.click_and_hold(self.BOOKMARK)
        # self.click_element(self.BOOKMARK)
        # self.fill_texts(self.BOOKMARK, 'b', is_press_enter=False)
        # self.press_keyboard('bb')

    def get_bookmark_bar_status(self) -> str:
        return self.get_element_attribute_by_its_name_and_locator(
            self.SHOW_BOOKMARKS_BAR, "Toggle.ToggleState"
        )

    def show_bookmarks_bar(self):
        if not self.is_toolbar_bookmark_show():
            self.open_menu_from_newtab()
            self.click_menu_bookmark()
            self.click_element(self.SHOW_BOOKMARKS_BAR)
            assert self.get_element(self.TOOLBAR_BOOKMARK)

    def is_toolbar_bookmark_show(self) -> bool:
        return self.is_element_appeared(self.TOOLBAR_BOOKMARK)

    def is_toolbar_bookmark_hide(self) -> bool:
        return self.is_element_disappeared(self.TOOLBAR_BOOKMARK)

    def hide_bookmarks_bar(self):
        if not self.is_toolbar_bookmark_hide():
            self.open_menu_from_newtab()
            self.click_menu_bookmark()
            self.click_element(self.SHOW_BOOKMARKS_BAR)

    def open_task_manager(self) -> None:
        self.open_coccoc_menu()
        self.click_element(self.MORE_TOOLS)
        self.click_element(self.TASK_MANAGER)

    def click_menu_help(self) -> None:
        # self.open_menu()
        self.open_coccoc_menu()
        self.click_element(self.MENU_HELP)

    def click_help_help_center(self) -> None:
        self.click_menu_help()
        self.click_element(self.MENU_HELP_HELP_CENTER)

    # def open_task_manager


"""OUTSIDE the class"""


def open_tor_window_from_normal_window():
    """
    To open  Tor windows from a normal window
    Returns:
    """
    if "en" in lang:
        title = CocCocTitles.NEW_TAB_TITLE_EN
    else:
        title = CocCocTitles.NEW_TAB_TITLE_VI
    app: Application = open_browser.connect_to_coccoc_by_title(title).window(
        found_index=0
    )
    app.set_focus().type_keys("%F")
    app.child_window(title=NEW_INCOGNITO_WINDOW_WITH_TOR, control_type="MenuItem").wait(
        "visible", timeout=setting.timeout_pywinauto, retry_interval=0.1
    ).click_input()
