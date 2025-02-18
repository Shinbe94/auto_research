from time import sleep
from pytest_pytestrail import pytestrail
from pywinauto import Application
from selenium.webdriver.common.by import By
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocSettingTitle, CocCocTitles
from src.pages.internal_page.downloads.download_bar import DownloadBar
from src.pages.internal_page.downloads.download_page import (
    DownloadPage,
    DownloadPageSel,
)
from src.utilities import file_utils, os_utils
from src.pages.internal_page.extensions.extensions_page import ExtensionsPage
from src.pages.internal_page.flags import flags_page as fp
from src.pages.settings.settings_adblock import SettingsAdblock
from src.pages.settings.settings_downloads import SettingsDownloadsSel
from src.pages.settings.settings_search import SettingsSearch
from src.pages.support_pages.support_pages import GooglePage
from src.pages.toolbar import toolbar as tb
from src.pages.toolbar.toolbar import Toolbar

from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54218")
def test_download_page_layout(download_page: DownloadPage):
    try:
        download_page.clear_all_downloads_data()
        download_page.verify_download_page_ui()
    finally:
        download_page.clear_all_downloads_data(is_need_open_download_page=False)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1013247")
def test_download_bar_shown(
    toolbar: Toolbar,
    download_bar: DownloadBar,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Make some download
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample2.xlsx",
            is_press_enter=True,
        )
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample4.csv",
            is_press_enter=True,
        )
        # click btn show all
        download_bar.click_btn_show_all()
        window = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
            timeout=setting.timeout_pywinauto,
        )
        # Click 'X' button to close the Downloads bar
        window.window().child_window(
            title="Close", control_type="Button", found_index=2
        ).click_input()
        assert download_bar.is_element_disappeared(download_bar.DOWNLOAD_BAR) is True
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54220")
def test_click_downloader_icon_from_toolbar(
    toolbar: Toolbar,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        download_page_sel.open_page(url=setting.coccoc_homepage_newtab)
        # Make some download
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample2.xlsx",
            is_press_enter=True,
        )
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample4.csv",
            is_press_enter=True,
        )
        # click downloader icon
        toolbar.open_download_page()
        assert toolbar.is_element_appeared((By.NAME, "sample2.xlsx"))
        assert toolbar.is_element_appeared((By.NAME, "sample4.csv"))
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54220")
def test_default_option_ask_where_to_save(
    toolbar: Toolbar,
    settings_downloads_sel: SettingsDownloadsSel,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.check_default_toggle_ask_where_to_save_status_is_off(
            is_need_to_open_downloads_setting=True
        )
        first_window = settings_downloads_sel.get_current_window()
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample2.xlsx",
            is_press_enter=True,
        )
        toolbar.open_download_page()
        assert toolbar.is_element_appeared((By.NAME, "sample2.xlsx"))
    finally:
        settings_downloads_sel.switch_to_window(first_window)
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220547")
def test_turn_off_option_ask_where_to_save(
    toolbar: Toolbar,
    settings_downloads_sel: SettingsDownloadsSel,
    download_page_sel: DownloadPageSel,
):
    download_path: str = settings_downloads_sel.get_download_path(
        is_need_to_open_downloads_setting=True
    )
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.turn_on_toggle_ask_where_to_save(
            is_need_to_open_downloads_setting=True
        )
        first_window = settings_downloads_sel.get_current_window()
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample2.xlsx",
            is_press_enter=True,
        )
        # Check ask where to save dialog appears
        window_dialog: Application = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=CocCocSettingTitle.SETTINGS_DOWNLOADS_TITLE,
            timeout=setting.timeout_pywinauto,
        )
        assert (
            window_dialog.window()
            .child_window(title="Save As", control_type="Window")
            .exists(timeout=setting.timeout_pywinauto)
        )
        window_dialog.window().child_window(
            title="Save", auto_id="1", control_type="Button"
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).click_input()
        sleep(5)
        # file_utils.wait_for_file_downloaded2(download_path=download_path)
        # Check file is saved
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"{download_path}\sample2.xlsx"
        )
    finally:
        settings_downloads_sel.switch_to_window(first_window)
        settings_downloads_sel.turn_off_toggle_ask_where_to_save(
            is_need_to_open_downloads_setting=True
        )
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494589")
def test_download_dir_function_well(
    toolbar: Toolbar,
    download_page_sel: DownloadPageSel,
    settings_downloads_sel: SettingsDownloadsSel,
):
    download_path_test: str = rf"C:\Users\{os_utils.get_username()}\Documents"
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.change_download_path(change_to_where=download_path_test)
        toolbar.make_search_value(
            search_str=r"https://download-tests.itim.vn/file/download?file=sample2.xlsx",
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"{download_path_test}\sample2.xlsx"
        )
        file_utils.remove_a_file(file_name=rf"{download_path_test}\sample2.xlsx")
    finally:
        settings_downloads_sel.change_download_path()
        download_page_sel.clear_all_downloads_data()
