import time

import pytest
from pytest_pytestrail import pytestrail
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from pywinauto import Application
from playwright.sync_api import expect

from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles
from src.pages.extensions.savior_extension_detail_page import SaviorExtensionDetailPage
from src.pages.internal_page.bookmarks.bookmark_bar import BookmarkBar
from src.pages.internal_page.credits.credits_page import CreditsPage

# from src.pages.menus.main_menu import MainMenu as mm
from src.pages.menus.main_menu import MainMenu
from src.pages.new_tab.new_tab_page import NewTabPage
from src.pages.settings.settings_cookies import SettingsCookies
from src.pages.toolbar.toolbar import Toolbar
from src.pages.incognito import incognito_tor_page as tp
from src.utilities import file_utils, os_utils, process_id_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128535")
@pytest.mark.open_tor_window
def test_tor_1_profile(toolbar: Toolbar):
    toolbar.click_tor_1_profile()
    assert toolbar.is_element_appeared(toolbar.CLOSE_INCOGNITO_WITH_TOR) is True
    assert toolbar.is_element_appeared(toolbar.WINDOW_INCOGNITO_WITH_TOR) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128538")
@pytest.mark.open_tor_window
def test_tor_multiple_profile(toolbar: Toolbar, main_menu: MainMenu, lang: str):
    try:
        main_menu.open_tor_window_from_tor_window()
        time.sleep(4)
        main_menu.open_tor_window_from_tor_window()
        time.sleep(2)
        toolbar.click_tor_profile(no_of_profile=3)
        assert toolbar.is_element_appeared(toolbar.CLOSE_INCOGNITO_WITH_TOR) is True
        assert toolbar.is_element_appeared(toolbar.WINDOW_INCOGNITO_WITH_TOR) is True
        toolbar.check_number_of_tor_window_opening(no_of_window=3)
    finally:
        open_browser.close_coccoc_by_window_title(title=CocCocTitles.TOR_WINDOW_TITLE)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128541")
@pytest.mark.open_tor_window
def test_close_tor_profile(toolbar: Toolbar):
    toolbar.click_tor_1_profile()
    assert toolbar.is_element_appeared(toolbar.CLOSE_INCOGNITO_WITH_TOR) is True
    assert toolbar.is_element_appeared(toolbar.WINDOW_INCOGNITO_WITH_TOR) is True
    toolbar.click_close_tor()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128550")
def test_close_tor_by_disable_tor_from_setting(
    wad_session: AppiumWebDriver,
    wad_session2: AppiumWebDriver,
):
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver: WebDriver = coccoc_instance[0]
    window: Application = coccoc_instance[1]
    try:
        # Attach the appium driver into the CC window
        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.NEW_TAB_TITLE,
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        # Open new tor window and check it is appeared
        mm = MainMenu(session_driver)
        mm.snap_selected_window_to_the_left_half_screen()
        mm.open_new_tor_window_from_normal_window()
        time.sleep(5)

        # Attach the appium driver into the tor window
        session_driver2: AppiumWebDriver = wad_session2(
            title=CocCocTitles.TOR_WINDOW_TITLE,
            port=4730,
            timeout=5,
            implicitly_wait=5,
        )
        assert session_driver2.title == CocCocTitles.DEFAULT_TOR_WINDOW_TITLE
        # Turn off tor from setting
        tp.turn_off_tor_from_setting(driver=driver)

        # Checking the tor window is closed
        assert (
            open_browser.is_coccoc_window_disappeared(
                title=CocCocTitles.DEFAULT_TOR_WINDOW_TITLE
            )
            is True
        )
        time.sleep(2)
        assert (
            process_id_utils.is_process_running(process_name="tor-client-win32.exe")
            is False
        )
        # assert session_driver2 is None
        # print("window title is: ", session_driver2.title)
        # assert session_driver2.title is ""
    finally:
        tp.turn_on_tor_from_setting(driver=driver)
        driver.quit()
        window.window().set_focus().close()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128583")
@pytest.mark.open_tor_window2
def test_show_hide_bookmark(main_menu: MainMenu, main_menu2: MainMenu):
    try:
        main_menu2.snap_selected_window_to_the_right_half_screen()
        main_menu.show_bookmarks_bar()
        main_menu.snap_selected_window_to_the_left_half_screen()
        main_menu2.is_toolbar_bookmark_show()
    finally:
        main_menu.hide_bookmarks_bar()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128586")
@pytest.mark.open_tor_window2
def test_add_bookmark(
    copy_bookmark_file: None,
    toolbar: Toolbar,
    main_menu: MainMenu,
    bookmark_bar2: BookmarkBar,
):
    try:
        bookmark_bar2.snap_selected_window_to_the_right_half_screen()
        main_menu.show_bookmarks_bar()
        toolbar.add_current_site_to_bookmark(url="https://google.com")
        toolbar.add_current_site_to_bookmark(url="https://translate.google.com/")
        toolbar.snap_selected_window_to_the_left_half_screen()
        bookmark_bar2.check_bookmark_exist(name="Google")
        bookmark_bar2.check_bookmark_exist(name="Google Translate")
        # This cheat to detect the window at new tab
        toolbar.open_new_tab()
    finally:
        main_menu.hide_bookmarks_bar()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128592")
@pytest.mark.open_tor_window2
def test_remove_bookmark(
    copy_bookmark_file: None,
    toolbar: Toolbar,
    main_menu: MainMenu,
    bookmark_bar2: BookmarkBar,
):
    try:
        bookmark_bar2.snap_selected_window_to_the_right_half_screen()
        main_menu.show_bookmarks_bar()
        toolbar.add_current_site_to_bookmark(url="https://google.com")
        toolbar.add_current_site_to_bookmark(url="https://translate.google.com/")
        toolbar.snap_selected_window_to_the_left_half_screen()

        bookmark_bar2.check_bookmark_exist(name="Google")
        bookmark_bar2.check_bookmark_exist(name="Google Translate")

        toolbar.remove_current_bookmarked_site(url="https://google.com")
        toolbar.remove_current_bookmarked_site(url="https://translate.google.com/")

        toolbar.open_new_tab()  # This cheat to detect the window at new tab
        bookmark_bar2.check_bookmark_is_not_exist(name="Google")
        bookmark_bar2.check_bookmark_is_not_exist(name="Google Translate")

    finally:
        main_menu.hide_bookmarks_bar()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128607")
@pytest.mark.open_tor_window
@pytest.mark.open_incognito_window2
def test_data_download_separately_bw_tor_and_incognito(
    toolbar: Toolbar, toolbar2: Toolbar
):
    toolbar2.snap_selected_window_to_the_right_half_screen()
    toolbar2.make_search_value(
        search_str="https://filesamples.com/samples/document/csv/sample4.csv",
        is_press_enter=True,
    )
    toolbar2.make_search_value(search_str="coccoc://downloads/", is_press_enter=True)
    assert toolbar2.is_element_appeared((By.NAME, "sample4.csv"))
    assert toolbar2.is_element_disappeared((By.NAME, "file-sample_100kB.docx"))
    # Click to activate the window before snapping
    toolbar.click_address_and_search_bar()
    toolbar.snap_selected_window_to_the_left_half_screen()
    toolbar.make_search_value(
        search_str="https://file-examples.com/wp-content/storage/2017/02/file-sample_100kB.docx",
        is_press_enter=True,
    )
    time.sleep(10)
    file_utils.check_downloading_file_in_download_directory(
        file_name="file-sample_100kB.docx",
        directory=rf"C:\Users\{os_utils.get_username()}\Downloads",
    )
    toolbar.make_search_value(search_str="coccoc://downloads/", is_press_enter=True)
    assert toolbar.is_element_appeared((By.NAME, "file-sample_100kB.docx"))
    assert toolbar.is_element_disappeared((By.NAME, "sample4.csv"))
    # time.sleep(3)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128628")
@pytest.mark.open_tor_window
# @pytest.mark.open_incognito_window2
def test_cookies_tor(settings_cookies: SettingsCookies, toolbar: Toolbar):
    toolbar.allow_cookies(url="kenh14.vn", sleep_n_seconds=5)
    # print(settings_cookies.get_list_site_allowed_cookies())
    assert "kenh14" not in settings_cookies.get_list_site_allowed_cookies()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128562")
@pytest.mark.open_tor_window
# @pytest.mark.open_incognito_window2
def xtest_media_download_tor(
    toolbar: Toolbar,
    toolbar2: Toolbar,
    savior_extension_detail_page2: SaviorExtensionDetailPage,
):
    # TODO should fix later
    try:
        toolbar2.snap_selected_window_to_the_right_half_screen()
        # allow incognito mode
        savior_extension_detail_page2.turn_on_allow_in_incognito()
        # Dowwnloading
        toolbar.make_search_value(
            search_str="https://www.youtube.com/watch?v=Vq25ZJwZJzU",
            is_press_enter=True,
        )
        time.sleep(5)
        toolbar.click_accept_cookies()
        time.sleep(15)
        # toolbar.click_download_video_audio()
        toolbar.hover_on_youtube_movie()
        toolbar.click_btn_savior_dialog_download()
        file_utils.wait_for_file_downloaded2()

    finally:
        # turn of allow in incognito mode
        savior_extension_detail_page2.turn_off_allow_in_incognito()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128577")
@pytest.mark.open_tor_window
# @pytest.mark.open_incognito_window2
def test_adblock_function_in_tor(toolbar: Toolbar, new_tab_page: NewTabPage):
    new_tab_page.page.goto("https://minhngoc.net")
    toolbar.check_adblock_icon_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128955")
@pytest.mark.open_tor_window
def test_tor_can_access_restricted_site(toolbar: Toolbar, new_tab_page: NewTabPage):
    new_tab_page.page.goto("https://bbc.com")
    expect(new_tab_page.page).to_have_title("BBC - Homepage")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1141772")
# @pytest.mark.open_tor_window
def test_tor_licences(credits_page: CreditsPage):
    credits_page.open_credits_page()
    credits_page.click_to_show_tor_licences()
    credits_page.check_tor_licences_content_is_shown()
    credits_page.click_to_show_tor_licences()
    credits_page.click_to_show_tor_client_homepage()
