import time

import pytest
from pytest_pytestrail import pytestrail
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from src.pages.coccoc_common import interactions_windows, open_browser
from src.pages.constant import CocCocTitles
from src.pages.menus.main_menu import MainMenu
from src.pages.settings.settings_appearance import SettingsAppearance
from src.pages.toolbar.toolbar import Toolbar
from src.pages.incognito.incognito_tor_page import IncognitoTorPage


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128484")
def test_open_tor_window_from_menu(
    main_menu: MainMenu,
    wad_session: AppiumWebDriver,
):
    try:
        main_menu.open_new_tor_window_from_normal_window()
        # interactions_windows.is_default_tor_window_appeared(is_closed=True)

        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.TOR_WINDOW_TITLE,
            port=4730,
            timeout=5,
            implicitly_wait=5,
        )
        assert session_driver.title == CocCocTitles.DEFAULT_TOR_WINDOW_TITLE
    finally:
        open_browser.close_coccoc_by_kill_process()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128544")
@pytest.mark.open_tor_window
def test_popup_tor_profile(toolbar: Toolbar, lang: str):
    toolbar.click_tor_1_profile()
    assert toolbar.is_element_appeared(toolbar.CLOSE_INCOGNITO_WITH_TOR) is True
    assert toolbar.is_element_appeared(toolbar.WINDOW_INCOGNITO_WITH_TOR) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128598")
@pytest.mark.open_tor_window
def test_tor_connecting_status(incognito_tor_page: IncognitoTorPage, lang: str):
    assert incognito_tor_page.wait_for_connecting(language=lang) is True
    time.sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128610")
@pytest.mark.open_tor_window
def test_tor_connect_failed(
    turn_off_then_on_network: None, incognito_tor_page: IncognitoTorPage, lang: str
):
    incognito_tor_page.reload_page()
    assert incognito_tor_page.wait_for_connection_is_failed(language=lang) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128613")
@pytest.mark.open_tor_window
def test_tor_connected_successfully(incognito_tor_page: IncognitoTorPage, lang: str):
    assert incognito_tor_page.wait_for_connected(language=lang) is True
    time.sleep(1)
