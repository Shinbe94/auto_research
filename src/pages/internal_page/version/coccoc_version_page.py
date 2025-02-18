import faulthandler
import time

from pywinauto import Application
from selenium.webdriver.common.by import By

from src.pages.coccoc_common import open_browser, interactions, interactions_windows
from src.pages.constant import CocCocTitles
from tests import setting
from src.utilities import browser_utils

COCCOC_PLATFORM = (By.CSS_SELECTOR, "#copy-content span:nth-child(4)")


def open_coccoc_version_page():
    faulthandler.disable()
    driver = open_browser.open_and_connect_coccoc_by_selenium()[0]
    driver.get(setting.coccoc_version_page)
    return driver


def get_coccoc_version_full():
    pass


def get_coccoc_platform(is_close=True):
    faulthandler.disable()
    driver = open_coccoc_version_page()
    text = str(interactions.get_text_from_element(driver, COCCOC_PLATFORM))
    if is_close:
        interactions_windows.close_coccoc_by_window_title(
            title=driver.title + " - Cốc Cốc"
        )
        if driver is not None:
            driver.quit()
    return text.replace("(", "").replace(")", "").replace("-", "")


def test_get_coccoc_platform():
    assert get_coccoc_platform() == "64bit"


def get_coccoc_executable_path():
    pass


def test_get_coccoc_version_pywinauto():
    print(get_coccoc_version_pywinauto())


def get_coccoc_version_pywinauto(
    language=setting.coccoc_language, version=setting.coccoc_test_version
) -> str:
    """
    This is for check the version by pywinauto
    Args:
        language:
        version:
    Returns: coccoc version
    """
    coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
    version_text = None
    # Verify the dialog "CocCoc isn't your default browser" at setting page
    try:
        if language == "en":
            address_bar_and_search = (
                coccoc_window[setting.NEW_TAB_TITLE_EN]
                .child_window(title=setting.ADDRESS_BAR_EN, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("^a")
            address_bar_and_search.type_keys("coccoc://version/{ENTER}")
            time.sleep(1)
            version_text = (
                coccoc_window.window()
                .child_window(auto_id="version", control_type="DataItem")
                .window_text()
            )
            assert (
                browser_utils.chromium_version_to_coccoc_version(version)
                in version_text
            )
        else:
            address_bar_and_search = (
                coccoc_window[setting.NEW_TAB_TITLE_VI]
                .child_window(title=setting.ADDRESS_BAR_VI, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("^a")
            address_bar_and_search.type_keys("coccoc://version/{ENTER}")
            time.sleep(1)
            version_text = (
                coccoc_window.window()
                .child_window(auto_id="version", control_type="DataItem")
                .window_text()
            )
            assert (
                browser_utils.chromium_version_to_coccoc_version(version)
                in version_text
            )
    finally:
        coccoc_window.window().set_focus().close()
        time.sleep(2)
        if version_text is not None:
            return version_text


def test_open_coccoc_at_the_very_first_time_and_check_version():
    get_coccoc_version_at_the_very_first_time_opening()


def get_coccoc_version_at_the_very_first_time_opening(
    language=setting.coccoc_language, version=setting.coccoc_test_version
) -> str:
    """
    This is for check the version after just installed (open coccoc at the first time, having welcome page)
    Args:
        language:
        version:
    Returns: coccoc version
    """
    # coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
    coccoc_window = None
    version_text = None
    try:
        if language == "en":
            # Verify Welcome page
            coccoc_window = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=setting.WELCOME_TITLE_EN,
                timeout=setting.timeout_pywinauto,
            )
            # Verify version
            address_bar_and_search = (
                coccoc_window.window()
                .child_window(title=setting.ADDRESS_BAR_EN, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("^a")
            address_bar_and_search.type_keys("coccoc://version/{ENTER}")
            time.sleep(1)
            version_text = (
                coccoc_window[CocCocTitles.VERSION_PAGE_TITLE]
                .child_window(auto_id="version", control_type="DataItem")
                .window_text()
            )
            assert (
                browser_utils.chromium_version_to_coccoc_version(version)
                in version_text
            )
        else:
            # Verify Welcome page
            assert Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=setting.WELCOME_TITLE_VI,
                timeout=setting.timeout_pywinauto,
                retry_interval=1,
            )
            # Verify version
            address_bar_and_search = (
                coccoc_window[setting.NEW_TAB_TITLE_VI]
                .child_window(title=setting.ADDRESS_BAR_VI, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("^a")
            address_bar_and_search.type_keys("coccoc://version/{ENTER}")
            time.sleep(1)
            version_text = (
                coccoc_window[CocCocTitles.VERSION_PAGE_TITLE]
                .child_window(auto_id="version", control_type="DataItem")
                .window_text()
            )
            assert (
                browser_utils.chromium_version_to_coccoc_version(version)
                in version_text
            )
    finally:
        coccoc_window.window().set_focus().close()
        time.sleep(2)
        if version_text is not None:
            return version_text
