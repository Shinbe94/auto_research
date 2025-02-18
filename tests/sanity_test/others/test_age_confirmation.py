from time import sleep

import pytest
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser
from src.pages.dialogs.age_confirmation import AgeConfirmationSel
from src.pages.settings.settings_privacy_and_security import (
    SettingsPrivacyAndSecuritySel,
)
from src.pages.settings.settings_reset import SettingsResetSel
from src.utilities import file_utils, os_utils
from src.pages.settings import setting_about_coccoc
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494691")
def test_age_confirmation_popup_show(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
):
    age_confirmation_sel.verify_popup_appears()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C324778")
def test_keeping_age_confirmation_popup_after_showing(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
):
    age_confirmation_sel.verify_popup_appears()

    age_confirmation_sel.open_new_tab_with_specific_url(
        age_confirmation_sel.get_current_url()
    )
    age_confirmation_sel.switch_to_window(
        age_confirmation_sel.get_all_windows_handle()[1]
    )
    age_confirmation_sel.verify_popup_appears()

    age_confirmation_sel.open_new_tab_with_specific_url(
        age_confirmation_sel.get_current_url()
    )
    age_confirmation_sel.switch_to_window(
        age_confirmation_sel.get_all_windows_handle()[2]
    )
    age_confirmation_sel.verify_popup_appears()

    age_confirmation_sel.scroll_into_bottom_of_page()
    age_confirmation_sel.verify_popup_appears()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494673")
def test_dont_show_age_confirmation_popup_after_ignoring(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
):
    coccoc_instance_1 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_1 = coccoc_instance_1[0]
    cc_window_1 = coccoc_instance_1[1]
    try:
        acs_1 = AgeConfirmationSel(driver_1)
        acs_1.verify_popup_appears()
    finally:
        cc_window_1.window().close()
        if driver_1 is not None:
            driver_1.quit()
    sleep(3)
    # Check reopen and check there's no pop-up shows again.
    coccoc_instance_2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_2 = coccoc_instance_2[0]
    cc_window_2 = coccoc_instance_2[1]
    try:
        acs_2 = AgeConfirmationSel(driver_2)
        acs_2.verify_popup_does_not_appears()
    finally:
        cc_window_2.window().close()
        if driver_2 is not None:
            driver_2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494688")
def test_dont_show_age_confirmation_popup_after_clicking(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
):
    coccoc_instance_1 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_1 = coccoc_instance_1[0]
    cc_window_1 = coccoc_instance_1[1]
    try:
        acs_1 = AgeConfirmationSel(driver_1)
        acs_1.verify_popup_appears()
        acs_1.click_btn_yes()
    finally:
        cc_window_1.window().close()
        if driver_1 is not None:
            driver_1.quit()
    sleep(3)
    # Check reopen and check there's no pop-up shows again.
    coccoc_instance_2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_2 = coccoc_instance_2[0]
    cc_window_2 = coccoc_instance_2[1]
    try:
        acs_2 = AgeConfirmationSel(driver_2)
        acs_2.verify_popup_does_not_appears()
    finally:
        cc_window_2.window().close()
        if driver_2 is not None:
            driver_2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494679")
@pytest.mark.ignore_check_testing_build
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Stop testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_dont_show_age_confirmation_popup_again_after_upgrading(
    uninstall_coccoc,
    install_old_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    # verify_age_confirmation_popup_shown,
    verify_age_confirmation_popup_shown_playwright,
    upgrade_browser_via_about_us,
):
    # Check reopen and check there's no pop-up shows again after Upgrading
    coccoc_instance_2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_2 = coccoc_instance_2[0]
    cc_window_2 = coccoc_instance_2[1]
    try:
        acs_2 = AgeConfirmationSel(driver_2)
        acs_2.verify_popup_does_not_appears()
    finally:
        cc_window_2.window().close()
        if driver_2 is not None:
            driver_2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494682")
@pytest.mark.ignore_check_testing_build
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Stop testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_show_age_confirmation_popup_again_after_upgrading(
    uninstall_coccoc,
    install_old_coccoc,
    open_then_close_browser,
    upgrade_browser_via_about_us,
    change_system_date_to_tomorrow,
):
    # Check reopen and check there's no pop-up shows again after Upgrading
    coccoc_instance_2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_2 = coccoc_instance_2[0]
    cc_window_2 = coccoc_instance_2[1]
    try:
        acs_2 = AgeConfirmationSel(driver_2)
        acs_2.verify_popup_appears()
    finally:
        cc_window_2.window().close()
        if driver_2 is not None:
            driver_2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C324781")
def xtest_dont_show_age_confirmation_popup_if_has_skin_ads(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
):
    # Check reopen and check there's no pop-up shows again after Upgrading
    coccoc_instance_2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver_2 = coccoc_instance_2[0]
    cc_window_2 = coccoc_instance_2[1]
    try:
        acs_2 = AgeConfirmationSel(driver_2)
        acs_2.open_page(url="https://skinads.com")
        acs_2.verify_popup_does_not_appears()
    finally:
        cc_window_2.window().close()
        if driver_2 is not None:
            driver_2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1247556")
def test_UI_age_confirmation_at_setting(
    uninstall_coccoc,
    install_coccoc,
    settings_privacy_and_security_sel: SettingsPrivacyAndSecuritySel,
):
    settings_privacy_and_security_sel.verify_default_value_of_age_confirmation()
    settings_privacy_and_security_sel.verify_ui_age_confirmation()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C248839")
def test_age_confirmation_popup_at_setting_as_default(
    select_default_value_for_age_confirmation_from_setting,
):
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.get_age_verification_value() == "0"
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1247559")
def test_age_confirmation_popup_at_setting_as_im_under_18(
    select_im_under_18_for_age_confirmation_from_setting,
):
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.get_age_verification_value() == "1"
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1247562")
def test_age_confirmation_popup_at_setting_as_im_18_or_older(
    select_im_18_or_older_for_age_confirmation_from_setting,
):
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.get_age_verification_value() == "2"
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C248848")
@pytest.mark.ignore_check_testing_build
def test_age_confirmation_is_kept_after_upgrade(
    uninstall_coccoc,
    install_old_coccoc,
    # select_im_18_or_older_for_age_confirmation_from_setting,
    select_im_18_or_older_for_age_confirmation_from_setting_by_playwright,
    upgrade_browser_via_about_us,
):
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.get_age_verification_value() == "2"
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C249304")
def test_cookies_value_when_showing_popup_age_confirmation(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
):
    age_confirmation_sel.verify_popup_appears()
    sleep(3)
    assert (
        age_confirmation_sel.get_cookies_by_its_name("cc_adult_response").get("value")
        == "show"
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1247565")
def test_cookies_value_when_showing_popup_age_confirmation_click_yes(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
):
    age_confirmation_sel.verify_popup_appears()
    age_confirmation_sel.click_btn_yes()
    sleep(3)
    assert (
        age_confirmation_sel.get_cookies_by_its_name("cc_adult_response").get("value")
        == "yes"
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1247568")
def test_cookies_value_when_showing_popup_age_confirmation_click_no(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
):
    age_confirmation_sel.verify_popup_appears()
    age_confirmation_sel.click_btn_no()
    sleep(3)
    assert (
        age_confirmation_sel.get_cookies_by_its_name("cc_adult_response").get("value")
        == "no"
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C327972")
def test_age_confirmation_reset(
    uninstall_coccoc,
    install_coccoc,
    open_then_close_browser,
    change_system_date_to_tomorrow,
    age_confirmation_sel: AgeConfirmationSel,
    settings_reset_sel: SettingsResetSel,
    settings_privacy_and_security_sel: SettingsPrivacyAndSecuritySel,
):
    age_confirmation_sel.verify_popup_appears()
    age_confirmation_sel.click_btn_yes()
    sleep(3)
    assert (
        age_confirmation_sel.get_cookies_by_its_name("cc_adult_response").get("value")
        == "yes"
    )
    settings_reset_sel.reset_settings()
    sleep(3)
    assert settings_privacy_and_security_sel.get_age_verification_value() == "0"
    age_confirmation_sel.open_new_tab_with_specific_url(
        url=setting.coccoc_homepage_newtab
    )
    assert age_confirmation_sel.get_cookies_by_its_name("cc_adult_response") is None
