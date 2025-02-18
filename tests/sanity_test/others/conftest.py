import shutil

from time import sleep
import pytest

from src.pages.coccoc_common import open_browser
from src.pages.dialogs.age_confirmation import AgeConfirmationPlay, AgeConfirmationSel
from src.pages.settings.settings_on_startup import SettingsOnStartupSel
from src.pages.settings.settings_privacy_and_security import (
    SettingsPrivacyAndSecurityPlay,
    SettingsPrivacyAndSecuritySel,
)
from src.utilities import file_utils, os_utils
from tests import setting
from tests.conftest import p_driver, close_win_app_driver_server_by_its_id


@pytest.fixture()
def set_open_newtab():
    """To pre-select option "Open the New Tab page" """
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    coccoc_window = coccoc_instance[1]
    sose = SettingsOnStartupSel(driver)
    try:
        sose.click_open_the_newtab_page()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def set_open_newtab_after_test():
    yield
    """To pre-select option "Open the New Tab page" """
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    coccoc_window = coccoc_instance[1]
    sose = SettingsOnStartupSel(driver)
    try:
        sose.click_open_the_newtab_page()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def set_continue_what_you_left_off():
    """To pre-select option "Continue where you left off" """
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    coccoc_window = coccoc_instance[1]
    sose = SettingsOnStartupSel(driver)
    try:
        sose.click_continue_where_you_left_off()
        sose.open_page("https://google.com")
        sleep(2)
        sose.open_new_tab()
        sleep(2)
        # sose.open_new_tab_with_specific_url(url="https://bing.com")
        sose.switch_to_window(sose.get_all_windows_handle()[1])
        sose.open_page("https://bing.com")
        sleep(2)
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def set_new_pages():
    """To pre-select option "Open a specific page or set of page" then add some new pages for it"""
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    coccoc_window = coccoc_instance[1]
    sose = SettingsOnStartupSel(driver)
    try:
        sose.click_open_a_specify_page_or_set_of_pages()
        sose.add_new_page(
            text="https://google.com", is_need_open_setting_startup_page=True
        )
        sose.add_new_page(text="https://bing.com")
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def set_use_current_pages():
    """To pre-select option "Open a specific page or set of page" select 'User current page'
    Note: should open some non-coccoc-setting page first
    """
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    coccoc_window = coccoc_instance[1]
    sose = SettingsOnStartupSel(driver)
    try:
        sose.open_page("https://google.com")
        sleep(2)
        sose.open_new_tab()
        sleep(2)

        sose.switch_to_window(sose.get_all_windows_handle()[1])
        sose.open_page("https://bing.com")
        sleep(2)

        sose.open_new_tab()
        sose.switch_to_window(sose.get_all_windows_handle()[2])
        sose.click_open_a_specify_page_or_set_of_pages()
        sose.click_use_current_page()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()


def get_latest_extension_version_from_disk(extension_id: str, profile="Default") -> str:
    return file_utils.list_all_files_and_folders(
        directory=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}"
    )[-1]


@pytest.fixture()
def remove_file_verified_contents_of_extension(profile="Default"):
    """To remove the file 'verified_contents.json' of extension before test
    Then
        Verify 'verified_contents.json' appears again after test

    Args:
        extension_id (str): _description_
        profile (str, optional): _description_. Defaults to 'Default'.
    """
    for extension_id in setting.list_default_coccoc_extension_id:
        version_extension = get_latest_extension_version_from_disk(
            extension_id=extension_id, profile=profile
        )
        if file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\_metadata\verified_contents.json"
        ):
            file_utils.remove_a_file(
                file_name=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\_metadata\verified_contents.json"
            )
        assert (
            file_utils.check_file_is_exists(
                file_name_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\_metadata\verified_contents.json"
            )
            is False
        )


@pytest.fixture()
def verify_file_verified_contents_appears_automatically_again(profile="Default"):
    yield
    """To check the file 'verified_contents.json' appears again
    Args:
        extension_id (str): _description_
        profile (str, optional): _description_. Defaults to 'Default'.
    """
    for extension_id in setting.list_default_coccoc_extension_id:
        version_extension = get_latest_extension_version_from_disk(
            extension_id=extension_id, profile=profile
        )
        assert (
            file_utils.check_file_is_exists(
                file_name_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\_metadata\verified_contents.json"
            )
            is True
        )


@pytest.fixture()
def edit_some_data_for_test_enforing_mode(profile="Default"):
    list_test_extensions = setting.list_default_coccoc_extension_id
    if "afaljjbleihmahhpckngondmgohleljb" in list_test_extensions:
        list_test_extensions.remove("afaljjbleihmahhpckngondmgohleljb")
    for extension_id in list_test_extensions:
        version_extension = get_latest_extension_version_from_disk(
            extension_id=extension_id, profile=profile
        )
        file_utils.edit_file(
            filename_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\background.html",
            text="testing only",
        )


@pytest.fixture()
def verify_content_verifier_enforcing_mode(profile="Default"):
    yield
    list_test_extensions = setting.list_default_coccoc_extension_id
    if "afaljjbleihmahhpckngondmgohleljb" in list_test_extensions:
        list_test_extensions.remove("afaljjbleihmahhpckngondmgohleljb")
    for extension_id in list_test_extensions:
        version_extension = get_latest_extension_version_from_disk(
            extension_id=extension_id, profile=profile
        )
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\background.html"
        )
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\{profile}\Extensions\{extension_id}\{version_extension}\_metadata\verified_contents.json"
        )


@pytest.fixture()
def change_system_date_to_tomorrow():
    today: str = os_utils.get_today()
    os_utils.change_os_date(
        date=os_utils.get_the_day_after_tomorrow(), is_close_cmd_after_changed=True
    )
    yield
    os_utils.change_os_date(date=today, is_close_cmd_after_changed=True)


@pytest.fixture()
def verify_age_confirmation_popup_shown():
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


@pytest.fixture()
def verify_age_confirmation_popup_shown_playwright():
    tuple_context = p_driver()  # Start Coccoc by Winappdriver and connect by playwright
    pcc = tuple_context[0]  # get playwright page
    browser = tuple_context[1]
    pw = tuple_context[2]
    winappdriver = tuple_context[3]
    pid = tuple_context[4]  # get winappdriver pid
    try:
        asp = AgeConfirmationPlay(pcc)
        asp.verify_popup_appears()
        asp.click_btn_yes()
    finally:
        browser.close()
        pw.stop()
        winappdriver.quit()
        close_win_app_driver_server_by_its_id(
            pid
        )  # Close current winappdriver instance


@pytest.fixture()
def select_default_value_for_age_confirmation_from_setting():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.select_default_option_age_confirmation()
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def select_im_under_18_for_age_confirmation_from_setting():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.select_im_under_18_option_age_confirmation()
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def select_im_18_or_older_for_age_confirmation_from_setting():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        spass = SettingsPrivacyAndSecuritySel(driver)
        spass.select_im_18_or_older_option_age_confirmation()
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()


@pytest.fixture()
def select_im_18_or_older_for_age_confirmation_from_setting_by_playwright():
    tuple_context = p_driver()  # Start Coccoc by Winappdriver and connect by playwright
    pcc = tuple_context[0]  # get playwright page
    browser = tuple_context[1]
    pw = tuple_context[2]
    winappdriver = tuple_context[3]
    pid = tuple_context[4]  # get winappdriver pid
    try:
        spasp = SettingsPrivacyAndSecurityPlay(pcc)
        spasp.select_im_18_or_older_option_age_confirmation()
    finally:
        browser.close()
        pw.stop()
        winappdriver.quit()
        close_win_app_driver_server_by_its_id(
            pid
        )  # Close current winappdriver instance
