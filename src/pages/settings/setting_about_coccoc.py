import faulthandler
import time

from pywinauto import Application
from appium.webdriver.webelement import WebElement
from appium.webdriver.webdriver import WebDriver
from src.pages.base import BaseSelenium
from src.pages.constant import CocCocSettingTitle, CocCocTitles, LocatorJSPath

from src.utilities import file_utils, browser_utils, os_utils
from tests import setting
from src.pages.coccoc_common import open_browser, interactions

RELAUNCH_BTN = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page").shadowRoot.querySelector("#relaunch")'
UPDATE_STATUS_MESSAGE = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page").shadowRoot.querySelector("#updateStatusMessage > div")'
COCCOC_VERSION_DETAIL = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page").shadowRoot.querySelector("settings-section div.flex.cr-padded-text > div.secondary")'


def open_about_coccoc(language=setting.coccoc_language, is_need_checking_message=True):
    driver = None
    try:
        driver = open_browser.open_coccoc_by_selenium()
        driver.get(setting.coccoc_about)
    except Exception:
        if driver is not None:
            driver.quit()
            driver = open_browser.open_coccoc_by_selenium()
            driver.get(setting.coccoc_about)
    if is_need_checking_message:
        if language == "en":
            assert "Checking for update" in interactions.get_text_from_js_path(
                driver, UPDATE_STATUS_MESSAGE
            )
        else:
            assert "Đang kiểm tra bản cập nhật" in interactions.get_text_from_js_path(
                driver, UPDATE_STATUS_MESSAGE
            )
    return driver


def is_relaunch_button_appeared(driver, timeout=setting.timeout_selenium) -> bool:
    is_appeared = False
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    while not is_appeared:
        try:
            element = interactions.get_shadow_element3(driver, js_path=RELAUNCH_BTN)
            display_text = element.value_of_css_property("display")
            if display_text == "inline-flex":
                is_appeared = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for wait for getting the button Relaunch appears")
                break
        except Exception as e:
            print(e)
    return is_appeared


def is_relaunch_button_disappeared(driver: WebDriver, timeout=setting.timeout_selenium):
    is_disappeared = False
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    while not is_disappeared:
        try:
            element = interactions.get_shadow_element2(driver, js_path=RELAUNCH_BTN)
            display_text = element.value_of_css_property("display")
            if display_text == "none":
                is_disappeared = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for wait for getting the button Relaunch disappears")
                break
        except Exception as e:
            print(e)
    if is_disappeared:
        return is_disappeared


def click_relaunch_button(language=setting.coccoc_language) -> bool:
    is_need_to_click_relaunch_btn = True
    driver = open_about_coccoc(language)
    detail_version_message = interactions.get_text_from_element_by_inner_text_js_path(
        driver, COCCOC_VERSION_DETAIL
    )

    # Check if current browser version is not the test version -> wait for update and relaunch
    if (
        browser_utils.chromium_version_to_coccoc_version(setting.coccoc_test_version)
        not in detail_version_message
    ):
        try:
            assert is_relaunch_button_appeared(
                driver, timeout=setting.timeout_for_waiting_browser_update
            )
            interactions.click_shadow_element(driver, RELAUNCH_BTN)
        except Exception as e:
            pass
        #     raise e
        # finally:
        #     if driver is not None:
        #         driver.quit()
    else:
        time.sleep(1)
        is_need_to_click_relaunch_btn = False
        if driver is not None:
            driver.quit()
    return is_need_to_click_relaunch_btn


def click_relaunch_button_pywinauto(language=setting.coccoc_language) -> bool:
    is_need_to_click_relaunch_btn = True
    coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
    address_bar_and_search = (
        coccoc_window[CocCocTitles.NEW_TAB_TITLE]
        .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
        .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
    )
    address_bar_and_search.type_keys("coccoc://settings/help{ENTER}")
    try:
        if "en" in language:
            detail_version_message = (
                coccoc_window[CocCocSettingTitle.ABOUT_COCCOC_TITLE]
                .child_window(title_re=r"Version", control_type="Text")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
                .window_text()
            )

            if (
                browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                not in detail_version_message
            ):
                assert is_relaunch_button_appeared_pywinauto(language)
                coccoc_window.window().child_window(
                    auto_id="relaunch", control_type="Button"
                ).click_input()

            else:
                time.sleep(1)
                is_need_to_click_relaunch_btn = False
                open_browser.close_coccoc_by_window_title(
                    title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
                )
        else:
            detail_version_message = (
                coccoc_window[CocCocSettingTitle.ABOUT_COCCOC_TITLE]
                .child_window(title_re=r"Phiên bản", control_type="Text")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
                .window_text()
            )

            if (
                browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                not in detail_version_message
            ):
                assert is_relaunch_button_appeared_pywinauto(language)
                coccoc_window.window().child_window(
                    auto_id="relaunch", control_type="Button"
                ).click_input()

            else:
                time.sleep(1)
                is_need_to_click_relaunch_btn = False
                open_browser.close_coccoc_by_window_title(
                    title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
                )
    finally:
        return is_need_to_click_relaunch_btn


def click_relaunch_button_pywinauto2(language=setting.coccoc_language) -> bool:
    is_need_to_click_relaunch_btn = True
    try:
        coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
        address_bar_and_search = (
            coccoc_window[CocCocTitles.NEW_TAB_TITLE]
            .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
        )
        address_bar_and_search.type_keys("coccoc://settings/help{ENTER}")
        if is_relaunch_button_appeared_pywinauto():
            coccoc_window[CocCocSettingTitle.ABOUT_COCCOC_TITLE].child_window(
                auto_id="relaunch", control_type="Button"
            ).click_input()
        else:
            is_need_to_click_relaunch_btn = False
            open_browser.close_coccoc_by_window_title(
                title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
            )

    finally:
        return is_need_to_click_relaunch_btn


def is_relaunch_button_appeared_pywinauto(
    language=setting.coccoc_language,
    timeout=setting.timeout_for_waiting_browser_update,
) -> bool:
    is_appeared = False
    interval_delay = 1
    total_delay = 0
    coccoc_window = Application(backend="uia").connect(
        class_name="Chrome_WidgetWin_1",
        control_type=50033,
        title_re=CocCocSettingTitle.ABOUT_COCCOC_TITLE,
        timeout=setting.timeout_pywinauto,
    )

    while not is_appeared:
        try:
            if (
                coccoc_window.window()
                .child_window(auto_id="relaunch", control_type="Button")
                .is_visible()
            ):
                if "en" in language:
                    assert (
                        coccoc_window.window()
                        .child_window(
                            title="Nearly up to date! Relaunch Cốc Cốc to finish updating.",
                            control_type="Text",
                        )
                        .is_visible()
                    )
                else:
                    assert (
                        coccoc_window.window()
                        .child_window(
                            title="Nearly up to date! Relaunch Cốc Cốc to finish updating.",
                            control_type="Text",
                        )
                        .is_visible()
                    )
                is_appeared = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > timeout:
                print(
                    rf"Timeout for wait for getting the button Relaunch appears after {timeout} seconds"
                )
                break
        except Exception as e:
            pass
            # print(e)
    return is_appeared


def check_browser_after_update(
    language=setting.coccoc_language, is_need_open_about_page_manually=False
):
    # Need start browser manually for checking after upgrade by task schedule
    if is_need_open_about_page_manually:
        open_about_coccoc(language, is_need_checking_message=False)

    app = None
    title = CocCocSettingTitle.ABOUT_COCCOC_TITLE
    if language == "en":
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            assert (
                app.window()
                .child_window(title="Cốc Cốc is up to date.", control_type="Text")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
                .is_visible()
                is True
            )

            title_version = (
                "Version "
                + browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                + " (Official Build)"
                + " ("
                + os_utils.get_real_system_platform()
                + ")"
            )
            assert (
                app[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            app.window().close()
    else:
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            assert (
                app.window()
                .child_window(title="Cốc Cốc đã được cập nhật.", control_type="Text")
                .is_visible()
                is True
            )
            title_version = (
                "Phiên bản "
                + browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                + " (Phiên bản Chính thức)"
                + " ("
                + os_utils.get_real_system_platform().replace("-", " ")
                + ")"
            )
            assert (
                app[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            app.window().close()

    time.sleep(2)


def check_browser_after_update_from_prod(
    language=setting.coccoc_language,
    is_need_open_about_page_manually=False,
    platform=setting.platform,
):
    """
    to check update from the prod to the merging build(Current dev build)
    Args:
        language:
        is_need_open_about_page_manually:
    Returns:

    """
    if platform == "64bit":
        platform = "64-bit"
    else:
        platform = "32-bit"
    # Need start browser manually for checking after upgrade by task schedule
    if is_need_open_about_page_manually:
        open_about_coccoc(language, is_need_checking_message=False)

    app = None
    title = CocCocSettingTitle.ABOUT_COCCOC_TITLE
    if language == "en":
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            assert (
                app[title]
                .child_window(title="Cốc Cốc is up to date.", control_type="Text")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
                .is_visible()
                is True
            )

            title_version = (
                "Version "
                + browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                + " (Official Build)"
                + " ("
                # + os_utils.get_real_system_platform()
                + platform
                + ")"
            )
            assert (
                app[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            app[title].close()
    else:
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            assert (
                app.window()
                .child_window(title="Cốc Cốc đã được cập nhật.", control_type="Text")
                .is_visible()
                is True
            )
            title_version = (
                "Phiên bản "
                + browser_utils.chromium_version_to_coccoc_version(
                    setting.coccoc_test_version
                )
                + " (Phiên bản Chính thức)"
                + " ("
                # + os_utils.get_real_system_platform().replace("-", " ")
                + platform
                + ")"
            )
            assert (
                app[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            app.window().close()

    time.sleep(2)


def test(previous_browser_build="101.0.4951.80"):
    check_folders_after_update(previous_browser_build)


def check_folders_after_update(previous_browser_build):
    time.sleep(2)
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        file_utils.open_folder_application_directory(
            r"C:\Program Files\CocCoc\Browser\Application", previous_browser_build
        )
        list_files_folders_in_application_64 = file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc\Browser\Application"
        )
        # Check folders and files in C:\Program Files \CocCoc :
        assert "Browser" in file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc"
        )
        assert "Application" in file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc\Browser"
        )
        assert setting.coccoc_test_version in list_files_folders_in_application_64
        assert previous_browser_build not in list_files_folders_in_application_64
        assert "SetupMetrics" in list_files_folders_in_application_64
        assert "browser.exe" in list_files_folders_in_application_64
        assert "browser_proxy.exe" in list_files_folders_in_application_64
        assert "VisualElementsManifest.xml" in list_files_folders_in_application_64

        # # Check files and folders in  C:\Users\<Account_login_Windows>\AppData\Local\CocCoc\ :
        # assert 'Browser' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc')
        # assert 'User Data' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser')
        #
        # # Check files and folders in C:\Users\<Account_login_Windows>\AppData\Roaming\CocCoc :
        # assert 'hid3' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc')
        # assert 'uid' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc')

    # Check for build 32 bit
    else:
        file_utils.open_folder_application_directory(
            r"C:\Program Files (x86)\CocCoc\Browser\Application", previous_browser_build
        )
        list_files_folders_in_application_32 = file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc\Browser\Application"
        )
        # Check files and folders in C:\Program\Files(x86)\CocCoc
        files_and_folder_in_coccoc = file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc"
        )
        assert "Browser" in files_and_folder_in_coccoc
        assert "CrashReports" in files_and_folder_in_coccoc
        assert "Update" in files_and_folder_in_coccoc
        assert "Temp" in files_and_folder_in_coccoc
        assert "Application" in file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc\Browser"
        )

        assert setting.coccoc_test_version in list_files_folders_in_application_32
        assert previous_browser_build not in list_files_folders_in_application_32
        assert "SetupMetrics" in list_files_folders_in_application_32
        assert "browser.exe" in list_files_folders_in_application_32
        assert "browser_proxy.exe" in list_files_folders_in_application_32
        assert "VisualElementsManifest.xml" in list_files_folders_in_application_32

        # # Check files and folders in  C:\Users\<Account_login_Windows>\AppData\Local\CocCoc\ :
        # assert 'Browser' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc')
        # assert 'User Data' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser')
        #
        # # Check files and folders in C:\Users\<Account_login_Windows>\AppData\Roaming\CocCoc :
        # assert 'hid3' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc')
        # assert 'uid' in file_utils.list_all_files_and_folders(
        #     rf'C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc')


def check_omaha_after_update(previous_omaha_version):
    # Check if is omaha is upgraded or not
    if browser_utils.get_active_omaha_version() == previous_omaha_version:
        # Check omaha folder is not empty
        assert (
            file_utils.check_folder_is_empty(
                # rf"C:\Program Files (x86)\CocCoc\Update\{browser_utils.get_active_omaha_version()}"
                f"{browser_utils.get_coccoc_update_folder()}\\{browser_utils.get_active_omaha_version()}"
            )
            is False
        )
    else:
        # Check previous omaha version is empty
        assert (
            file_utils.check_folder_is_empty(
                # rf"C:\Program Files (x86)\CocCoc\Update\{previous_omaha_version}"
                f"{browser_utils.get_coccoc_update_folder()}\\{previous_omaha_version}"
            )
            is True
        )
        # Check upgraded omaha version is not empty
        assert (
            file_utils.check_folder_is_empty(
                # rf"C:\Program Files (x86)\CocCoc\Update\{browser_utils.get_active_omaha_version()}"
                f"{browser_utils.get_coccoc_update_folder()}\\{browser_utils.get_active_omaha_version()}"
            )
            is False
        )


def wait_for_coccoc_updated_by_schedule_is_done(
    timeout=setting.timeout_for_waiting_browser_update,
) -> bool:
    is_upgraded = False
    interval_delay = 10
    total_delay = 0
    while not is_upgraded:
        if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
            list_files_folders_in_application_64 = (
                file_utils.list_all_files_and_folders(
                    r"C:\Program Files\CocCoc\Browser\Application"
                )
            )
            # Check folders version is created
            if setting.coccoc_test_version in list_files_folders_in_application_64:
                is_upgraded = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > timeout:
                print(
                    f"Timeout for wait for upgrade by Task schedule after waiting for {timeout} seconds"
                )
                break

        # Check for build 32 bit
        else:
            list_files_folders_in_application_32 = (
                file_utils.list_all_files_and_folders(
                    r"C:\Program Files (x86)\CocCoc\Browser\Application"
                )
            )
            # Check folders version is created
            if setting.coccoc_test_version in list_files_folders_in_application_32:
                is_upgraded = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > timeout:
                print(
                    f"Timeout for wait for upgrade by Task schedule after waiting for {timeout} seconds"
                )
                break
    # if is_upgraded:
    return is_upgraded


def test_check_browser_after_update_pywinauto(language=setting.coccoc_language):
    check_browser_after_update_pywinauto(language)


def check_browser_after_update_pywinauto(language, is_very_old_version=False):
    """

    :param language:
    :param is_very_old_version: old version is 32-bit, so after upgrade it still 32-bit
    :return:
    """
    faulthandler.disable()
    coccoc_windows = open_browser.open_coccoc_by_pywinauto(language)
    title = CocCocSettingTitle.SETTING_COCCOC
    if language == "vi":
        try:
            address_bar_and_search = (
                coccoc_windows[CocCocTitles.NEW_TAB_TITLE]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=10)
            )
            address_bar_and_search.type_keys("coccoc://settings/help{ENTER}")

            assert (
                coccoc_windows[title]
                .child_window(title="Cốc Cốc đã được cập nhật.", control_type="Text")
                .is_visible()
                is True
            )
            if is_very_old_version:
                title_version = (
                    "Phiên bản "
                    + browser_utils.chromium_version_to_coccoc_version(
                        setting.coccoc_test_version
                    )
                    + " (Phiên bản Chính thức)"
                    + " (32-bit)"
                )
            else:
                title_version = (
                    "Phiên bản "
                    + browser_utils.chromium_version_to_coccoc_version(
                        setting.coccoc_test_version
                    )
                    + " (Phiên bản Chính thức)"
                    + " ("
                    + os_utils.get_real_system_platform().replace("-", " ")
                    + ")"
                )
            assert (
                coccoc_windows[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            coccoc_windows[title].close()

    else:
        try:
            address_bar_and_search = (
                coccoc_windows[CocCocTitles.NEW_TAB_TITLE]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=10)
            )
            address_bar_and_search.type_keys("coccoc://settings/help{ENTER}")

            assert (
                coccoc_windows[title]
                .child_window(title="Cốc Cốc is up to date.", control_type="Text")
                .wait("visible", timeout=20)
                .is_visible()
                is True
            )
            if is_very_old_version:
                title_version = (
                    "Version "
                    + browser_utils.chromium_version_to_coccoc_version(
                        setting.coccoc_test_version
                    )
                    + " (Official Build)"
                    + " (32-bit)"
                )
            else:
                title_version = (
                    "Version "
                    + browser_utils.chromium_version_to_coccoc_version(
                        setting.coccoc_test_version
                    )
                    + " (Official Build)"
                    + " ("
                    + os_utils.get_real_system_platform()
                    + ")"
                )
            assert (
                coccoc_windows[title]
                .child_window(title=title_version, control_type="Text")
                .is_visible()
                is True
            )
        finally:
            coccoc_windows[title].close()
    time.sleep(2)


def access_setting_about_page_pywinauto(language=setting.coccoc_language):
    faulthandler.disable()
    coccoc_windows = open_browser.open_coccoc_by_pywinauto(language)
    title = CocCocSettingTitle.ABOUT_COCCOC_TITLE
    try:
        address_bar_and_search = (
            coccoc_windows[CocCocTitles.NEW_TAB_TITLE]
            .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
            .wait("visible", timeout=10)
        )
        address_bar_and_search.type_keys("coccoc://settings/help{ENTER}")

        is_relaunch_button_appeared_pywinauto(language)
    finally:
        coccoc_windows[title].close()

    time.sleep(2)


class SettingsAboutCocCocSel(BaseSelenium):
    # Locator
    JS_PATH_RELAUNCH_BTN = (
        f'{LocatorJSPath.SETTINGS_ABOUT_PAGE}.shadowRoot.querySelector("#relaunch")'
    )
    JS_UPDATE_TEXT = f'{LocatorJSPath.SETTINGS_ABOUT_PAGE}.shadowRoot.querySelector("#updateStatusMessage > div")'
    JS_GET_HELP_WITH_COCCOC = (
        f'{LocatorJSPath.SETTINGS_ABOUT_PAGE}.shadowRoot.querySelector("#help")'
    )

    # Interaction methods
    def open_setting_about_coccoc_page(self) -> None:
        self.open_page(url="coccoc://settings/help")

    def wait_for_relaunch_btn_appear(
        self,
        timeout=setting.timeout_for_waiting_browser_update,
    ) -> bool:
        self.open_setting_about_coccoc_page()
        interval_delay: int = 5
        total_delay: int = 0
        is_appeared: bool = False
        while total_delay < timeout:
            try:
                # Wait for attribute 'hidden' is disappeared
                if not self.get_attribute_value_of_shadow_element(
                    js_path=self.JS_PATH_RELAUNCH_BTN, attribute_name="hidden"
                ):
                    is_appeared = True
                    break

            except Exception:
                pass
            time.sleep(interval_delay + 5)
            total_delay += interval_delay + 5
            if total_delay >= timeout:
                break
        return is_appeared

    def click_relaunch_btn(
        self,
        is_close_after_checking: bool = True,
    ) -> None:
        if self.wait_for_relaunch_btn_appear():
            self.click_shadow_element(self.JS_PATH_RELAUNCH_BTN)
            time.sleep(2)
            if is_close_after_checking:
                open_browser.close_coccoc_by_window_title(
                    title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
                )

    def click_get_help_with_coccoc(self) -> None:
        self.open_setting_about_coccoc_page()
        self.click_shadow_element(self.JS_GET_HELP_WITH_COCCOC)
