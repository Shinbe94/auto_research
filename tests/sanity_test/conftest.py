import codecs
import faulthandler
import time
from random import choice

import pytest
from pytest import FixtureRequest
from selenium.webdriver.common.by import By

from src.apis.paid_icons.paid_icons import PaidIcons
from src.pages.coccoc_common import open_browser, interactions
from src.pages.constant import CocCocSettingTitle
from src.pages.installations import installation_utils, base_window, installation_page
from src.pages.settings import setting_preferences
from src.pages.turn_on_sync import turn_on_sync
from src.utilities import (
    browser_utils,
    file_utils,
    os_utils,
    ftp_connection,
    read_write_data_by,
)
from tests import setting

installation = installation_page.InstallationPage()


@pytest.fixture()
def setup_file_for_test(
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    from_build_name=None,
    to_build_name=None,
):
    """
    Prepare the build for test
    :param build_name:
    :param version:
    :param from_build_name:
    :param to_build_name:
    :return:
    """
    faulthandler.disable()
    file_to_download_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{file_to_download_for_test}"
        )
        is False
    ):
        ftp_connection.get_file2(
            folder_version=version, file_to_download_for_test=file_to_download_for_test
        )

    yield file_to_download_for_test
    faulthandler.enable()


# @pytest.fixture(autouse=False, scope="session")
@pytest.fixture(autouse=False)
def uninstall_coccoc():
    installation_utils.uninstall_coccoc_silently()


@pytest.fixture(autouse=False)
def install_coccoc():
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language, build_name=setting.coccoc_build_name
    )


@pytest.fixture(autouse=False)
def install_old_coccoc():
    older_version = choice(setting.old_coccoc_version)
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language,
        build_name=setting.coccoc_build_name,
        version=older_version,
    )


@pytest.fixture(autouse=False)
def install_very_old_coccoc():
    older_version = choice(setting.very_old_coccoc_version)
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language,
        build_name=setting.coccoc_build_name,
        version=older_version,
    )


@pytest.fixture(autouse=True)
def close_coccoc_by_killing_its_process():
    """
    Closing the coccoc instances before and after test for sure
    Returns:
    """
    browser_utils.kill_all_coccoc_process()
    yield
    browser_utils.kill_all_coccoc_process()


# @pytest.fixture(autouse=True)
# def turn_of_warn_you_when_closing_multiple_tabs():
#     browser_utils.kill_all_coccoc_process()


# @pytest.fixture(autouse=True, scope="package")
@pytest.fixture(autouse=True)
def check_testing_build(request):
    """
    To check if the intended testing build is already installed or No CocCoc installed,
    if not then process uninstall the current build then install the correct build before executing the test
    :return: None
    """
    if not "ignore_check_testing_build" in request.keywords:
        installed_build = browser_utils.get_version_of_coccoc()
        if installed_build is None:
            installation.install_coccoc_by_build_name(
                language=setting.coccoc_language, build_name=setting.coccoc_build_name
            )
        elif not installed_build == setting.coccoc_test_version:
            installation_utils.uninstall_coccoc_silently()
            installation.install_coccoc_by_build_name(
                language=setting.coccoc_language, build_name=setting.coccoc_build_name
            )
        else:
            pass


@pytest.fixture(autouse=True, scope="session")
def lang() -> str:
    return setting.coccoc_language


@pytest.fixture()
def get_paid_icons() -> dict:
    paid_icons = PaidIcons()
    response = paid_icons.get_paid_icons()
    icons = response.as_dict
    return icons  # type: ignore


@pytest.fixture()
def get_paid_icons_name() -> list:
    paid_icons = PaidIcons()
    list_paid_icons_name = paid_icons.get_list_paid_icons_name()
    return list_paid_icons_name


@pytest.fixture()
def delete_sidebar_icon_files():
    try:
        # copy to safe location
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        # remove from appdata
        file_utils.remove_all_files_in_folder(
            directory=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar"
        )
        yield
    finally:
        # copy back to appdata
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        # clean for safe location
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons"
        )
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons"
        )


@pytest.fixture()
def edit_sidebar_icons_files():
    try:
        # wait for 2 files created automatically if any ( for case manually deleted before)
        file_utils.wait_for_file_exist(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons"
        )
        file_utils.wait_for_file_exist(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons"
        )

        # copy to safe location
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )

        # Edit 2 files
        read_write_data_by.write_text_to_file(
            file_name=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons",
            content="something",
        )
        read_write_data_by.write_text_to_file(
            file_name=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons",
            content="something",
        )

        yield
    finally:
        # Remove 2 edited files after test
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons"
        )
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons"
        )

        # copy back from Documents to appdata
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        # Delete from Documents
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons"
        )
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons"
        )


@pytest.fixture()
def copy_sidebar_icon_files():
    """
    Copy current custom icon list save to safe location, then execute test, then revert the custom icon list from safe
    location
    Returns:
    """
    try:
        # copy to safe location
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )

        yield
    finally:
        # Remove 2 edited files
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Ad Icons"
        )
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar\Custom Icons"
        )

        # copy back to appdata
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Sidebar",
        )
        # clean for safe location
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Ad Icons"
        )
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Custom Icons"
        )


@pytest.fixture()
def get_default_custom_icons():
    """
    To get the default custom icons that come along with the browser build by read the file Custom icon
    Returns: list default custom icons
    """

    def _default_custom_icon(profile_name: str = "Default") -> list:
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

    return _default_custom_icon


@pytest.fixture()
def change_flag_status():
    def _change_flag_status(
        flag_id: str,
        status: str,
        title=CocCocSettingTitle.COCCOC_FLAGS,
        is_keep_driver=False,
    ):
        drop_down = (By.CSS_SELECTOR, rf"#{flag_id} select.experiment-select")
        relaunch_btn = (By.CSS_SELECTOR, "#experiment-restart-button")
        driver = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
        )
        if is_keep_driver:
            try:
                driver.get("coccoc://flags/")
                interactions.scroll_to_element(driver, drop_down)
                interactions.scroll_up_down(driver, y=-150)
                interactions.click_element(driver, drop_down)
                interactions.select_by_visible_text(driver, drop_down, status)
                if (
                    interactions.get_attribute_value_by_element(
                        interactions.get_element(driver, relaunch_btn), "tabindex"
                    )
                    == "9"
                ):
                    interactions.click_element(driver, relaunch_btn)
                # driver.find_element(*element_flag_name)
                # yield driver
            finally:
                return driver
        else:
            try:
                driver.get("coccoc://flags/")
                interactions.scroll_to_element(driver, drop_down)
                interactions.scroll_up_down(driver, y=-150)
                interactions.click_element(driver, drop_down)
                interactions.select_by_visible_text(driver, drop_down, status)
                if (
                    interactions.get_attribute_value_by_element(
                        interactions.get_element(driver, relaunch_btn), "tabindex"
                    )
                    == "9"
                ):
                    interactions.click_element(driver, relaunch_btn)
                # driver.find_element(*element_flag_name)
                # yield driver
            finally:
                driver.quit()
                open_browser.close_coccoc_by_window_title(title=title)
            return True

    return _change_flag_status


@pytest.fixture()
def reset_sidebar_on_boarding() -> None:
    driver = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    try:
        driver.get("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        time.sleep(1)
        driver.execute_script("chrome.storage.local.set({ onboardTrack: {} });")

    finally:
        driver.quit()
        open_browser.close_coccoc_by_window_title(
            title="chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html - Cốc Cốc"
        )


@pytest.fixture()
def set_event_tracking_sidebar_on_boarding():
    driver = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    try:
        driver.get("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        time.sleep(1)
        driver.execute_script("chrome.storage.local.set({ onboardTrack: {} });")
        time.sleep(1)
        driver.execute_script(
            r"""
        Object.keys(chrome.metricsPrivate).forEach(function (key) {
        var method = chrome.metricsPrivate[key];
        if (typeof method !== 'function' || key.indexOf('record') !== 0) {
        return;
        }
        chrome.metricsPrivate['__' + key] = method;
        chrome.metricsPrivate[key] = function () {
        if (key === 'recordCustomData' && arguments[0] && arguments[0].length === 1) {
        console.info(
        'recordCustomData %c%s', 'color: lime',
        arguments[0][0].key,
        JSON.parse(arguments[0][0].value)
        );
        return;
        }
        console.info.bind(console, key).apply(console, arguments);
        return chrome.metricsPrivate['__' + key].apply(chrome.metricsPrivate, arguments);
        };
        });
        """
        )

    finally:
        driver.quit()
        open_browser.close_coccoc_by_window_title(
            title="chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html - Cốc Cốc"
        )


@pytest.fixture()
def copy_bookmark_file() -> None:  # type: ignore
    """
    Copy current bookmark list save to safe location, then execute test, then revert the bookmark list from safe
    location
    Returns:
    """
    try:
        # copy to safe location
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Bookmarks",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Bookmarks.bak",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )

        yield
    finally:
        # Remove 2 edited files
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Bookmarks"
        )
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Bookmarks.bak"
        )

        # copy back to appdata
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Bookmarks",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default",
        )
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Bookmarks.bak",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default",
        )
        # clean for safe location
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Bookmarks"
        )
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Bookmarks.bak"
        )


@pytest.fixture(autouse=True)
def disable_warning_closing_multiple_tabs():
    """
    To disable confirmation warning close multiple tabs
    Returns:
    """
    setting_preferences.disable_show_close_all_tabs_confirmation()


@pytest.fixture(autouse=True)
def disable_restore_popup_once_crash_or_killing_browser():
    """
    Disabling restore popup that comes when chrome process is killed
    Returns:
    """
    setting_preferences.disable_restore_popup()


@pytest.fixture()
def login_and_sync():
    turn_on_sync.turn_on_sync_from_setting(
        setting.cc_account_user, setting.cc_account_password
    )


@pytest.fixture()
def open_then_close_browser():
    """Sometime we need to open then close the browser, this fixture will help."""
    open_browser.open_coccoc_by_pywinauto_then_close_it(is_first_time_opened=False)


@pytest.fixture(autouse=True)
def delete_cashback_offscreen_file(request: FixtureRequest):
    """This fixture is for deleting the file 'offscreen.html' of Cashback extension
    to prevent it affect to playwright
    from V116 we have problem while open cc = playwright
    this page: chrome-extension://afaljjbleihmahhpckngondmgohleljb/offscreen.html leads to error
    """
    if "dont_delete_cashback_offscreen_file" in request.keywords:
        pass
    else:
        browser_utils.delete_file_offscreen_cashback_extension()
    yield
    if "dont_delete_cashback_offscreen_file" in request.keywords:
        pass
    else:
        browser_utils.copy_back_file_offscreen_cashback_extension()
