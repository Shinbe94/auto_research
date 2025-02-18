from time import sleep


from pywinauto.keyboard import send_keys
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser
from src.pages.dialogs.pop_ups import WarningClosingTabs

from src.pages.settings.settings_appearance import SettingsAppearanceSel
from src.pages.settings.settings_on_startup import SettingsOnStartupSel
from src.pages.settings.settings_privacy_and_security import (
    SettingsPrivacyAndSecuritySel,
)
from src.pages.topbar.top_bar import Topbar
from src.utilities import process_id_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C507954")
def test_startup_open_newtab(set_open_newtab, top_bar: Topbar):
    top_bar.check_new_tab_opening()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C507957")
def test_startup_open_some_sites(
    set_continue_what_you_left_off,
    top_bar: Topbar,
    settings_on_startup_sel: SettingsOnStartupSel,
):
    try:
        top_bar.check_newtab_by_title(title="Bing - Cốc Cốc")
        send_keys("^1")  # press ctrl + 1 to switch to tab 1 using pywinauto
        top_bar.check_newtab_by_title(title="Google - Cốc Cốc")
    finally:
        send_keys("^2")  # Switch again for continueing interact by selenium
        settings_on_startup_sel.click_open_the_newtab_page()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C507960")
def test_startup_when_add_new_page(
    set_new_pages,
    top_bar: Topbar,
    settings_on_startup_sel: SettingsOnStartupSel,
):
    try:
        top_bar.check_newtab_by_title(title="Google - Cốc Cốc")
        send_keys("^2")  # press ctrl + 2 to switch to tab 2 using pywinauto
        top_bar.check_newtab_by_title(title="Bing - Cốc Cốc")

    finally:
        send_keys("^2")  # Switch again for continueing interact by selenium
        settings_on_startup_sel.remove_all_added_page()
        settings_on_startup_sel.click_open_the_newtab_page()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1225290")
def test_startup_when_use_current_page(
    set_use_current_pages,
    top_bar: Topbar,
    settings_on_startup_sel: SettingsOnStartupSel,
):
    try:
        top_bar.check_newtab_by_title(title="Google - Cốc Cốc")
        send_keys("^2")  # press ctrl + 2 to switch to tab 2 using pywinauto
        top_bar.check_newtab_by_title(title="Bing - Cốc Cốc")

    finally:
        send_keys("^2")  # Switch again for continueing interact by selenium
        settings_on_startup_sel.remove_all_added_page()
        settings_on_startup_sel.click_open_the_newtab_page()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C730993")
def test_warning_multiple_tabs_closing_is_off(
    settings_appearance_sel: SettingsAppearanceSel,
    warning_closing_tabs: WarningClosingTabs,
    top_bar: Topbar,
    set_open_newtab_after_test,
):
    # toggle off Google translate then check
    settings_appearance_sel.toggle_off_warning_close_multiple_tabs()
    first_window = settings_appearance_sel.get_current_window()

    settings_appearance_sel.open_new_tab().open_page(
        url="http://google.com"
    ).open_new_tab()

    # trying to close the coccoc window
    send_keys("%{F4}")
    sleep(3)
    # Make sure that no coccoc process is running on
    assert process_id_utils.is_process_running(process_name="browser.exe") is False


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1225416")
def test_warning_multiple_tabs_closing_is_on_with_1_tab_opening(
    settings_appearance_sel: SettingsAppearanceSel, set_open_newtab_after_test
):
    # toggle off Google translate then check
    settings_appearance_sel.toggle_on_warning_close_multiple_tabs()

    # Opening 1 tab
    settings_appearance_sel.open_page(url="http://google.com")

    # trying to close the coccoc window
    send_keys("%{F4}")
    sleep(3)
    # Make sure that no coccoc process is running on
    assert process_id_utils.is_process_running(process_name="browser.exe") is False


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1225422")
def test_warning_multiple_tabs_closing_is_on_with_more_than_1_tabs_opening(
    settings_appearance_sel: SettingsAppearanceSel,
    warning_closing_tabs: WarningClosingTabs,
    set_open_newtab_after_test,
):
    # toggle off Google translate then check
    settings_appearance_sel.toggle_on_warning_close_multiple_tabs()

    # Opening more than 1 tab
    settings_appearance_sel.open_page(url="http://google.com").open_new_tab().open_page(
        url="http://bing.com"
    )

    # trying to close the coccoc window
    send_keys("%{F4}")
    warning_closing_tabs.verify_popup_ui(total_tabs=2)
    warning_closing_tabs.click_btn_yes()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C762650")
def test_safety_check_function(
    login_and_sync,
    settings_privacy_and_security_sel: SettingsPrivacyAndSecuritySel,
    uninstall_coccoc_after_test,
):
    settings_privacy_and_security_sel.click_btn_checknow()
    settings_privacy_and_security_sel.verify_after_checknow()
