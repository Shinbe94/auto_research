import pytest
from pytest_pytestrail import pytestrail
from src.pages.menus.main_menu import MainMenu
from src.pages.settings.settings_side_bar import SettingsSidebar, get_sidebar_status
from src.pages.sidebar.sidebar import Sidebar

# ------------------------------------------------------------------------------------------------------------------
from src.utilities import os_utils


@pytestrail.case("C54313")
def test_sidebar_settings_on_settings_page(settings_side_bar: SettingsSidebar):
    settings_side_bar.open_page()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54314")
@pytest.mark.ignore_tear_down
def test_on_off_sidebar_from_settings_page(
    settings_side_bar: SettingsSidebar, sidebar: Sidebar
):
    settings_side_bar.open_page()
    settings_side_bar.on_off_sidebar(toggle_to="OFF")
    sidebar.is_sidebar_hidden()
    settings_side_bar.on_off_sidebar(toggle_to="ON")
    sidebar.is_sidebar_shown()

    # close all browser instance & WinAppDriver sessions
    settings_side_bar.page.close()
    sidebar.wad.quit()
    os_utils.kill_process_by_name("WinAppDriver.exe")

    # Start browser again for checking the sidebar status is kept after changing
    assert get_sidebar_status() is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C248821")
def test_on_off_sidebar_from_coccoc_menu(
    settings_side_bar: SettingsSidebar, main_menu: MainMenu, sidebar: Sidebar
):
    # Check case hide Sidebar from menu, first should ensure the sidebar is shown by enable it via api
    settings_side_bar.show_sidebar()
    main_menu.open_menu()
    main_menu.click_hide_sidebar()
    sidebar.is_sidebar_hidden()

    # Check case show Sidebar from menu, first should ensure the sidebar is hidden by enable it via api
    settings_side_bar.hide_sidebar()
    main_menu.open_menu()
    main_menu.click_show_sidebar()
    sidebar.is_sidebar_shown()
