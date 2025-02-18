import faulthandler
import os
import time

import pywinauto
from playwright.sync_api import sync_playwright
from pywinauto import Application
from pywinauto.keyboard import send_keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from src.pages.base import BaseSelenium

from src.pages.coccoc_common import open_browser, interactions
from src.utilities import file_utils, browser_utils, os_utils
from tests import setting
from src.pages.constant import CocCocTitles, CocCocSettingTitle, LocatorJSPath

from time import sleep
from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pywinauto import Application

from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.constant import CocCocSettingTitle
from src.utilities import os_utils, file_utils
from src.pages.coccoc_common import open_browser, interactions
from tests import setting

lang = setting.coccoc_language

SETTINGS_DEFAULT_BROWSER_PAGE = (
    'document.querySelector("body > settings-ui").shadowRoot.querySelector('
    '"#leftMenu").shadowRoot.querySelector("#defaultBrowser") '
)
TOGGLE_START_UP = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("settings-toggle-button").shadowRoot.querySelector("#control")'
DEFAULT_BROWSER_MESSAGE = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("#isDefault")'
DEFAULT_BROWSER_TITLE = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("#canBeDefaultBrowser")'
DEFAULT_BROWSER_ASKING_MESS = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("div.cr-row.first > div.flex.cr-padded-text > div.secondary")'
MAKE_DEFAULT_BUTTON = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("div.cr-row.first > cr-button")'
MAKE_DEFAULT_BUTTON_CHROME = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("div > cr-button")'
HISTOGRAMS_DEFAULT_BROWSER = (
    By.XPATH,
    '//*[@id="histograms"]//div[@histogram-name="DefaultBrowser.State"]/span[3]',
)
CHROME_MAKE_DEFAULT_BUTTON = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-default-browser-page").shadowRoot.querySelector("div > cr-button")'
BTN_REFRESH_HISTOGRAM = (By.CSS_SELECTOR, "#refresh")


def get_executable_path():
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        return setting.coccoc_binary_64bit
    else:
        return setting.coccoc_binary_32bit


def get_default_browser_text_by_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=get_executable_path(),
            user_data_dir=setting.coccoc_default_profile,
            headless=False,
        )
        page_ = browser.new_page()
        page_.goto(setting.coccoc_settings_default_browser_page)
        text = page_.inner_text("#isDefault")
        return text


def open_settings_default_browser_page(language=setting.coccoc_language):
    driver = open_browser.open_and_connect_coccoc_by_selenium(language=language)[0]
    try:
        driver.get(setting.coccoc_settings_default_browser_page)
        if "en" in language:
            assert (
                driver.title
                == CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
            )
        else:
            assert (
                driver.title
                == CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
            )
    except Exception:
        browser_utils.kill_all_coccoc_process()
        driver = open_browser.open_and_connect_coccoc_by_selenium(language=language)[0]
        driver.get(setting.coccoc_settings_default_browser_page)
        if "en" in language:
            assert (
                driver.title
                == CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
            )
        else:
            assert (
                driver.title
                == CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
            )
    finally:
        return driver


def test_get_default_browser_text_by_selenium():
    print(get_default_browser_text_by_selenium())


def get_default_browser_text_by_selenium(language=setting.coccoc_language):
    # driver = open_browser.connect_to_coccoc_by_selenium()[0]
    driver = open_settings_default_browser_page(language)
    ele_text = None
    title = None
    try:
        title = driver.title
        ele_text = interactions.get_shadow_element3(
            driver, DEFAULT_BROWSER_MESSAGE
        ).text
        if ele_text is not None:
            pass
    finally:
        # close the coccoc browser
        open_browser.close_coccoc_by_window_title(title=title)
        # cleaning up driver
        if driver is not None:
            driver.quit()
        return ele_text


def check_default_browser_text_by_pywinauto(language=setting.coccoc_language):
    coccoc_window = open_browser.open_coccoc_by_pywinauto()
    # Verify the dialog "CocCoc isn't your default browser" at setting page
    try:
        if language == "en":
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Cốc Cốc is your default browser. Yay!", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
        else:
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title="Cốc Cốc là trình duyệt mặc định của bạn. Tuyệt!",
                    control_type=50020,
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
    finally:
        coccoc_window.window().close()


# ----------------------------------------------------------------------------------------------------------------------
def test_check_if_not_a_default_browser():
    check_if_not_a_default_browser(language=setting.coccoc_language)


def check_if_not_a_default_browser(language=setting.coccoc_language):
    # As we got problem with SSL cert after changing the time to future, so we should only use pywinauto for this verify
    try:
        coccoc_window = open_browser.open_coccoc_by_pywinauto()
        # Verify the dialog "CocCoc isn't your default browser" at new tab

        if language == "en":
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title="Infobar", control_type="Custom")
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )

            assert (
                coccoc_window.window()
                .child_window(
                    title="Cốc Cốc isn't your default browser", control_type="Text"
                )
                .is_visible()
                is True
            )

            assert (
                coccoc_window.window()
                .child_window(title="Set as default", control_type="Button")
                .is_visible()
                is True
            )

        else:
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title="Thanh thông tin", control_type="Custom")
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )

            assert (
                coccoc_window.window()
                .child_window(
                    title="Cốc Cốc không phải là trình duyệt mặc định của bạn",
                    control_type="Text",
                )
                .is_visible()
                is True
            )

            assert (
                coccoc_window.window()
                .child_window(
                    title="Đặt làm trình duyệt mặc định", control_type="Button"
                )
                .is_visible()
                is True
            )

        # Verify the dialog "CocCoc isn't your default browser" at setting page
        if language == "en":
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Make Cốc Cốc the default browser", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
        else:
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title="Đặt Cốc Cốc làm trình duyệt mặc định", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )

    finally:
        if "en" in language:
            open_browser.close_coccoc_by_window_title(
                title=CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
            )
        else:
            open_browser.close_coccoc_by_window_title(
                title=CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
            )
        time.sleep(2)


# ----------------------------------------------------------------------------------------------------------------------
def test_set_default_browser_from_setting_page():
    set_default_browser_from_setting_page()


def set_default_browser_from_setting_page(language=setting.coccoc_language):
    coccoc = open_browser.open_and_connect_coccoc_by_selenium(language=language)
    driver = coccoc[0]
    coccoc_window = coccoc[1]
    title = None
    if language == "en":
        try:
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(
                    title="Cốc Cốc isn't your default browser", control_type="Text"
                )
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title="Set as default", control_type="Button")
                .is_visible()
                is True
            )
            time.sleep(1)
            # Check the setting default browser page
            driver.get(setting.coccoc_settings_default_browser_page)
            title = driver.title
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_TITLE).text
                == "Default browser"
            )
            assert (
                interactions.get_shadow_element3(
                    driver, DEFAULT_BROWSER_ASKING_MESS
                ).text
                == "Make Cốc Cốc the default browser"
            )
            assert interactions.get_shadow_element3(
                driver, MAKE_DEFAULT_BUTTON
            ).is_displayed()

            # Click button 'make default'
            interactions.click_shadow_element(driver, MAKE_DEFAULT_BUTTON)
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_MESSAGE).text
                == "Cốc Cốc is your default browser. Yay!"
            )

        finally:
            open_browser.close_coccoc_by_window_title(title=title)
            if driver is not None:
                driver.quit()
    else:
        try:
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(
                    title="Cốc Cốc không phải là trình duyệt mặc định của bạn",
                    control_type="Text",
                )
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(
                    title="Đặt làm trình duyệt mặc định", control_type="Button"
                )
                .is_visible()
                is True
            )
            time.sleep(1)
            # Check the setting default browser page
            driver.get(setting.coccoc_settings_default_browser_page)
            title = driver.title
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_TITLE).text
                == "Trình duyệt mặc định"
            )
            assert (
                interactions.get_shadow_element3(
                    driver, DEFAULT_BROWSER_ASKING_MESS
                ).text
                == "Đặt Cốc Cốc làm trình duyệt mặc định"
            )
            assert interactions.get_shadow_element3(
                driver, MAKE_DEFAULT_BUTTON
            ).is_displayed()

            # Click button 'make default'
            interactions.click_shadow_element(driver, MAKE_DEFAULT_BUTTON)
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_MESSAGE).text
                == "Cốc Cốc là trình duyệt mặc định của bạn. Tuyệt!"
            )

        finally:
            open_browser.close_coccoc_by_window_title(title=title)
            if driver is not None:
                driver.quit()
    time.sleep(2)


def test_set_default_browser_from_setting_page_pywinauto():
    set_default_browser_from_setting_page_pywinauto(language="vi")


def set_default_browser_from_setting_page_pywinauto(language=setting.coccoc_language):
    coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
    # Verify the dialog "CocCoc isn't your default browser" at setting page
    try:
        if language == "en":
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(
                    title="Cốc Cốc isn't your default browser", control_type="Text"
                )
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title="Set as default", control_type="Button")
                .is_visible()
                is True
            )

            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(1)

            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Make Cốc Cốc the default browser", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
            coccoc_window[
                CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
            ].child_window(
                title="Make default", control_type="Button", found_index=0
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click_input()
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Cốc Cốc is your default browser. Yay!", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )

        else:
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(
                    title="Cốc Cốc không phải là trình duyệt mặc định của bạn",
                    control_type="Text",
                )
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(
                    title="Đặt làm trình duyệt mặc định", control_type="Button"
                )
                .is_visible()
                is True
            )

            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(1)

            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title="Đặt Cốc Cốc làm trình duyệt mặc định", control_type=50020
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
            coccoc_window[
                CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
            ].child_window(
                title="Đặt làm mặc định", control_type="Button", found_index=0
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click_input()
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title="Cốc Cốc là trình duyệt mặc định của bạn. Tuyệt!",
                    control_type=50020,
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
    finally:
        coccoc_window.window().close()


# ----------------------------------------------------------------------------------------------------------------------
def get_start_up_toggle_status(language=setting.coccoc_language):
    # driver = open_browser.open_coccoc_by_sel3()
    toggle_status = None
    driver = open_settings_default_browser_page(language)
    try:
        toggle_element = interactions.get_shadow_element3(driver, TOGGLE_START_UP)
        toggle_status = interactions.get_attribute_value_by_element(
            toggle_element, "aria-pressed"
        )
        if toggle_status is not None:
            pass
    except TimeoutException:
        driver.refresh()
    finally:
        open_browser.close_coccoc_by_window_title(title=driver.title)
        # cleaning up driver
        if driver is not None:
            driver.quit()
        return toggle_status


# ----------------------------------------------------------------------------------------------------------------------
def test_check_start_up_toggle_status_is_on():
    check_start_up_toggle_status_is_on()


def check_start_up_toggle_status_is_on(language=setting.coccoc_language):
    coccoc_window = open_browser.open_coccoc_by_pywinauto()
    # Verify the dialog "CocCoc isn't your default browser" at setting page
    try:
        if language == "en":
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(1)
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title=CocCocSettingTitle.START_UP_LABEL_EN,
                    control_type="Button",
                    auto_id="control",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title=CocCocSettingTitle.START_UP_LABEL_EN,
                    control_type="Button",
                    auto_id="control",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .get_toggle_state()
                == 1
            )  # mean on

        else:
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(1)
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title=CocCocSettingTitle.START_UP_LABEL_VI,
                    control_type=50020,
                    auto_id="control",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
            assert (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI]
                .child_window(
                    title=CocCocSettingTitle.START_UP_LABEL_VI,
                    control_type=50020,
                    auto_id="control",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .get_toggle_state()
                == 1
            )  # mean on

    finally:
        coccoc_window.window().close()


# ----------------------------------------------------------------------------------------------------------------------
def check_default_start_up_is_enabled(language=setting.coccoc_language):
    # driver = open_browser.connect_to_coccoc_by_selenium()[0]
    driver = open_browser.open_and_connect_coccoc_by_selenium()[0]
    try:
        driver.get(setting.coccoc_settings_page)
        interactions.click_shadow_element(driver, SETTINGS_DEFAULT_BROWSER_PAGE)
        time.sleep(5)
        toggle = interactions.get_shadow_element3(driver, TOGGLE_START_UP)
        txt = interactions.get_attribute_value_by_element(toggle, "aria-pressed")
        # print(txt)
        assert txt == "true"
    except TimeoutException:
        driver.navigate().refresh()
    finally:
        if language == "vi":
            title = CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
        else:
            title = CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
        app.window().set_focus().close()

        # cleaning up driver if any
        if driver is not None:
            driver.quit()


# ---------------------------------------------------------------------
def test_get_toggle_status_of_start_up():
    get_toggle_status_of_start_up()


def get_toggle_status_of_start_up(language=setting.coccoc_language):
    faulthandler.disable()
    coccoc_window = open_browser.open_coccoc_by_pywinauto(language)
    try:
        if language == "vi":
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(2)
            toggle_start_up = (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Khởi động cùng hệ thống",
                    auto_id="control",
                    control_type="Button",
                )
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )

            return str(toggle_start_up.get_toggle_state())

        else:
            address_bar_and_search = (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
                .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            time.sleep(2)
            toggle_start_up = (
                coccoc_window[CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN]
                .child_window(
                    title="Run automatically on system startup",
                    auto_id="control",
                    control_type="Button",
                )
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            )
            return str(toggle_start_up.get_toggle_state())
    finally:
        # Close the coccoc browser
        if language == "vi":
            title = CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_VI
        else:
            title = CocCocSettingTitle.SETTINGS_DEFAULT_BROWSER_PAGE_TITLE_EN
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
        app.window().set_focus().close()
        time.sleep(1)


def test_set_a_browser_to_default():
    set_a_browser_to_default()


# ----------------------------------------------------------------------------------------------------------------------
def set_a_browser_to_default():
    faulthandler.disable()
    windows_version = os_utils.get_windows_version()
    if windows_version in ("7", "8", "8.1"):
        # We can set default browser via command line
        os.system(
            browser_utils.get_chrome_executable_path()
            + " --make-default-browser --no-default-browser-check"
        )
        time.sleep(2)

    elif windows_version == "10":
        settings_window_10 = None
        try:
            # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
            os_utils.start_windows_settings()
            settings_window_10 = Application(backend="uia").connect(
                class_name="ApplicationFrameWindow",
                control_type=50032,
                title="Settings",
                timeout=setting.timeout_pywinauto,
            )
            # settings_window_10['Settings'].print_control_identifiers()
            settings_window_10[CocCocSettingTitle.SETTINGS].maximize()
            settings_window_10[CocCocSettingTitle.SETTINGS].set_focus()
            settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                title="Apps", control_type="ListItem"
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            ).click_input()
            time.sleep(1)
            settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                title="Default apps", control_type="ListItem"
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            ).click_input()
            time.sleep(1)
            if (
                settings_window_10[CocCocSettingTitle.SETTINGS]
                .child_window(
                    auto_id="SettingsGroupDefaultApps_GroupTitleTextBlock",
                    control_type=50020,
                    title="Choose default apps",
                )
                .exists(timeout=2)
            ):
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    auto_id="SettingsGroupDefaultApps_GroupTitleTextBlock",
                    control_type=50020,
                    title="Choose default apps",
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=1
                ).click_input()
            time.sleep(1)
            settings_window_10[CocCocSettingTitle.SETTINGS].wheel_mouse_input(
                wheel_dist=-10
            )
            time.sleep(1)
            # To check: Chrome is a default browser already
            # if settings_window_10['Settings'].child_window(auto_id='SystemSettings_DefaultApps_Browser_Button',
            #                                             control_type="Button").wait('visible',
            #                                                                         timeout=setting.time_out_pywinauto).is_visible():
            if (
                settings_window_10[CocCocSettingTitle.SETTINGS]
                .child_window(
                    auto_id="SystemSettings_DefaultApps_Browser_Button",
                    control_type="Button",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .window_text()
                != "Web browser, Google Chrome"
            ):
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    auto_id="SystemSettings_DefaultApps_Browser_Button",
                    control_type="Button",
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(2)
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    title="Google Chrome", control_type="Button"
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(5)
            else:  # If Chrome is already a default browser, skip
                pass
        finally:
            settings_window_10[CocCocSettingTitle.SETTINGS].close()
            time.sleep(2)

    elif windows_version == "11":
        settings_window = None
        try:
            # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
            os_utils.start_windows_settings()

            settings_window = Application(backend="uia").connect(
                class_name="ApplicationFrameWindow",
                control_type=50032,
                title="Settings",
                timeout=setting.timeout_pywinauto,
            )
            # settings_window['Settings'].print_control_identifiers()
            settings_window[CocCocSettingTitle.SETTINGS].maximize()
            settings_window[CocCocSettingTitle.SETTINGS].set_focus()
            settings_window[CocCocSettingTitle.SETTINGS].child_window(
                title="Apps", control_type="ListItem"
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(1)
            # settings_window['Settings'].print_control_identifiers()
            settings_window[CocCocSettingTitle.SETTINGS].child_window(
                title="Default apps", control_type="ListItem"
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(1)
            # settings_window['Settings'].print_control_identifiers()
            pywinauto.keyboard.send_keys("{TAB}")
            time.sleep(1)
            pywinauto.keyboard.send_keys("chrome", pause=0.1)
            time.sleep(2)
            settings_window[CocCocSettingTitle.SETTINGS].child_window(
                title="Google Chrome",
                auto_id="SystemSettings_DefaultApps_App_Machine_Google Chrome_ButtonEntityItem",
                control_type=50026,
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(2)
            # settings_window['Settings'].print_control_identifiers()
            settings_window[CocCocSettingTitle.SETTINGS].child_window(
                title="Make Google Chrome your default browser",
                auto_id="SystemSettings_DefaultApps_DefaultBrowserAction_Button",
                control_type="Button",
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(5)
        finally:
            settings_window[CocCocSettingTitle.SETTINGS].close()
            time.sleep(2)


def xtest_set_a_browser_to_default():
    set_a_browser_to_default()


def xtest_set_default_browser_to_chrome():
    set_default_browser_to_chrome()


def set_default_browser_to_chrome():
    faulthandler.disable()
    windows_version = os_utils.get_windows_version()
    driver = open_browser.open_chrome_by_selenium()
    driver.get("chrome://settings/defaultBrowser")
    if interactions.get_shadow_element3(driver, CHROME_MAKE_DEFAULT_BUTTON):
        interactions.click_shadow_element(driver, CHROME_MAKE_DEFAULT_BUTTON)
        time.sleep(2)
        if windows_version == "11":
            settings_window = None
            try:
                # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
                os_utils.start_windows_settings()

                settings_window = Application(backend="uia").connect(
                    class_name="ApplicationFrameWindow",
                    control_type=50032,
                    title="Settings",
                    timeout=setting.timeout_pywinauto,
                )
                # settings_window['Settings'].print_control_identifiers()
                settings_window[CocCocSettingTitle.SETTINGS].maximize()
                settings_window[CocCocSettingTitle.SETTINGS].set_focus()
                settings_window[CocCocSettingTitle.SETTINGS].child_window(
                    title="Apps", control_type="ListItem"
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(1)
                # settings_window['Settings'].print_control_identifiers()
                settings_window[CocCocSettingTitle.SETTINGS].child_window(
                    title="Default apps", control_type="ListItem"
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(1)
                # settings_window['Settings'].print_control_identifiers()
                pywinauto.keyboard.send_keys("{TAB}")
                time.sleep(1)
                pywinauto.keyboard.send_keys("chrome")
                settings_window[CocCocSettingTitle.SETTINGS].child_window(
                    title="Google Chrome",
                    auto_id="EntityItemButton",
                    control_type="Button",
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(2)
                # settings_window['Settings'].print_control_identifiers()
                settings_window[CocCocSettingTitle.SETTINGS].child_window(
                    title="Make Google Chrome your default browser",
                    auto_id="SystemSettings_DefaultApps_DefaultBrowserAction_Button",
                    control_type="Button",
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(5)
            finally:
                settings_window[CocCocSettingTitle.SETTINGS].close()
                if driver is not None:
                    driver.quit()
        elif windows_version == "10":
            settings_window_10 = None
            try:
                # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
                os_utils.start_windows_settings()
                settings_window_10 = Application(backend="uia").connect(
                    class_name="ApplicationFrameWindow",
                    control_type=50032,
                    title=CocCocSettingTitle.SETTINGS,
                    timeout=setting.timeout_pywinauto,
                )
                # settings_window_10['Settings'].print_control_identifiers()
                settings_window_10[CocCocSettingTitle.SETTINGS].maximize()
                settings_window_10[CocCocSettingTitle.SETTINGS].set_focus()
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    title="Apps", control_type="ListItem"
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(1)
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    title="Default apps", control_type="ListItem"
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(1)
                settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                    auto_id="SettingsGroupDefaultApps_GroupTitleTextBlock",
                    control_type=50020,
                    title="Choose default apps",
                ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                time.sleep(1)
                settings_window_10[CocCocSettingTitle.SETTINGS].wheel_mouse_input(
                    wheel_dist=-10
                )
                time.sleep(1)
                # To check: Chrome is a default browser already
                # if settings_window_10['Settings'].child_window(auto_id='SystemSettings_DefaultApps_Browser_Button',
                #                                             control_type="Button").wait('visible',
                #                                                                         timeout=setting.time_out_pywinauto).is_visible():
                if (
                    settings_window_10[CocCocSettingTitle.SETTINGS]
                    .child_window(
                        auto_id="SystemSettings_DefaultApps_Browser_Button",
                        control_type="Button",
                    )
                    .wait("visible", timeout=setting.timeout_pywinauto)
                    .window_text()
                    != "Web browser, Google Chrome"
                ):
                    settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                        auto_id="SystemSettings_DefaultApps_Browser_Button",
                        control_type="Button",
                    ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                    time.sleep(1)

                    settings_window_10[CocCocSettingTitle.SETTINGS].child_window(
                        title="Google Chrome", control_type="Button"
                    ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                    time.sleep(5)
                else:  # If Chrome is already a default browser, skip
                    pass
            finally:
                settings_window_10[CocCocSettingTitle.SETTINGS].close()
                if driver is not None:
                    driver.quit()
        else:
            pass
    else:
        pass
    time.sleep(3)


def open_coccoc_histograms(language=setting.coccoc_language) -> WebDriver:
    driver: WebDriver = open_browser.open_and_connect_coccoc_by_selenium(
        language=language
    )[0]
    try:
        driver.get(setting.coccoc_histograms)
        interactions.wait_for_title(driver, title=CocCocTitles.COCCOC_HISTOGRAMS_TITLE)
    finally:
        return driver


# ----------------------------------------------------------------------------------------------------------------------
def check_metric_default_browser(language=setting.coccoc_language):
    driver: WebDriver = open_coccoc_histograms(language)
    interactions.click_element(driver, BTN_REFRESH_HISTOGRAM)
    try:
        interactions.scroll_to_element(driver, HISTOGRAMS_DEFAULT_BROWSER)
        text = interactions.get_text_from_element_by_inner_text(
            driver, HISTOGRAMS_DEFAULT_BROWSER
        )
    except Exception as e:
        raise e
    else:
        assert "Histogram: DefaultBrowser.State recorded 1 samples" in text
    finally:
        # close the coccoc window
        if "en" in language:
            open_browser.close_coccoc_by_window_title(
                title=CocCocTitles.COCCOC_HISTOGRAMS_TITLE
            )
        else:
            open_browser.close_coccoc_by_window_title(
                title=CocCocTitles.COCCOC_HISTOGRAMS_TITLE
            )
        # cleaning up driver
        if driver is not None:
            driver.quit()


def test_check_metric_default_browser():
    check_metric_default_browser()


def check_no_metric_default_browser(language=setting.coccoc_language):
    # Connect to current coccoc window then open setting page
    # coccoc = open_browser.connect_to_coccoc_by_selenium(language=language)
    coccoc = open_browser.open_and_connect_coccoc_by_selenium(language=language)
    driver = coccoc[0]
    coccoc_window = coccoc[1]

    # Verify Histogram: DefaultBrowser.State
    driver.get(setting.coccoc_histograms)
    try:
        interactions.scroll_to_element(driver, HISTOGRAMS_DEFAULT_BROWSER)
        text = interactions.get_text_from_element_by_inner_text(
            driver, HISTOGRAMS_DEFAULT_BROWSER
        )
        assert "Histogram: DefaultBrowser.State recorded 1 samples" not in text

    finally:
        # close the coccoc window
        if language == "vi":
            open_browser.close_coccoc_by_window_title(title="Histograms - Cốc Cốc")
        else:
            open_browser.close_coccoc_by_window_title(title="Histograms - Cốc Cốc")
        # cleaning up driver
        if driver is not None:
            driver.quit()


def test_check_no_metric_default_browser():
    check_no_metric_default_browser()


def check_run_on_system_start_up_toggle_is_on(driver):
    driver.get(setting.coccoc_settings_page)
    interactions.click_shadow_element(driver, SETTINGS_DEFAULT_BROWSER_PAGE)
    toggle_element = interactions.get_shadow_element3(driver, TOGGLE_START_UP)
    toggle_status = interactions.get_attribute_value_by_element(
        toggle_element, "aria-pressed"
    )
    assert "true" == toggle_status


def set_default_browser_from_setting_page2(language=setting.coccoc_language):
    """To set coccoc as a default browser
        Note: just set a default, non-checking other
    Args:
        language (_type_, optional): _description_. Defaults to setting.coccoc_language.
    """
    coccoc = open_browser.open_and_connect_coccoc_by_selenium(language=language)
    driver = coccoc[0]
    coccoc_window = coccoc[1]
    title = None
    if language == "en":
        try:
            driver.get("coccoc://settings/defaultBrowser")
            # Check coccoc is a default or not
            if interactions.get_shadow_element3(driver, MAKE_DEFAULT_BUTTON, timeout=5):
                # Click button 'make default'
                interactions.click_shadow_element(driver, MAKE_DEFAULT_BUTTON)
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_MESSAGE).text
                == "Cốc Cốc is your default browser. Yay!"
            )
            title = driver.title
        finally:
            open_browser.close_coccoc_by_window_title(title=title)
            if driver is not None:
                driver.quit()
    else:
        try:
            driver.get("coccoc://settings/defaultBrowser")
            # Check coccoc is a default or not
            if (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_MESSAGE).text
                != "Cốc Cốc là trình duyệt mặc định của bạn. Tuyệt!"
            ):
                # Click button 'make default'
                interactions.click_shadow_element(driver, MAKE_DEFAULT_BUTTON)
            assert (
                interactions.get_shadow_element3(driver, DEFAULT_BROWSER_MESSAGE).text
                == "Cốc Cốc là trình duyệt mặc định của bạn. Tuyệt!"
            )
            title = driver.title
        finally:
            open_browser.close_coccoc_by_window_title(title=title)
            if driver is not None:
                driver.quit()
    time.sleep(1)


class SettingsDefaultBrowserSel(BaseSelenium):
    """this Class is for setting download by Selenium

    Args:
        BaseSelenium (_type_): _description_
    """

    # Locators
    TORRENT_MAKE_DEFAULT_BTN = rf'{LocatorJSPath.SETTINGS_DEFAULT_BROWSER_PRE}.shadowRoot.querySelector("div.settings-box.two-line cr-button")'

    TORRENT_MESSAGE_AFTER_MADE_DEFAULT = rf'{LocatorJSPath.SETTINGS_DEFAULT_BROWSER_PRE}.shadowRoot.querySelector("div.settings-box.two-line > div:nth-child(1) > div")'
    TORRENT_MESSAGE_NOT_A_DEFAULT = rf'{LocatorJSPath.SETTINGS_DEFAULT_BROWSER_PRE}.shadowRoot.querySelector("div.settings-box.two-line > div:nth-child(3)")'

    # Interaction methods
    def open_settings_default_browser(self):
        self.open_page("coccoc://settings/defaultBrowser")

    def make_coccoc_as_default_torrent(
        self, is_need_to_open_setting_default_browser=True
    ) -> None:
        if is_need_to_open_setting_default_browser:
            self.open_settings_default_browser()
        if self.get_shadow_element(self.TORRENT_MESSAGE_NOT_A_DEFAULT):
            self.click_shadow_element(self.TORRENT_MAKE_DEFAULT_BTN)
            assert self.get_text_shadow_element(
                js_path=self.TORRENT_MESSAGE_AFTER_MADE_DEFAULT
            )

    def check_message_not_a_default_torrent(
        self, is_need_to_open_setting_default_browser=False
    ) -> None:
        if is_need_to_open_setting_default_browser:
            self.open_settings_default_browser()
        if "en" in lang:
            assert (
                self.get_text_shadow_element(self.TORRENT_MESSAGE_NOT_A_DEFAULT)
                == "Cốc Cốc is not the default torrent client"
            )
        else:
            assert (
                self.get_text_shadow_element(self.TORRENT_MESSAGE_NOT_A_DEFAULT)
                == "Cốc Cốc chưa là ứng dụng torrent mặc định"
            )


def close_inforbar(language=setting.coccoc_language) -> None:
    """To close the inforbar (asking user set cc as default browser)

    Args:
        language (_type_, optional): _description_. Defaults to setting.coccoc_language.
    """
    coccoc_window: Application = Application(backend="uia").connect(
        class_name="Chrome_WidgetWin_1",
        control_type=50033,
        title=CocCocTitles.NEW_TAB_TITLE,
        timeout=2,
    )
    if "en" in language:
        try:
            if (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                .child_window(title="Infobar", control_type="Custom")
                .exists(timeout=10)
                is True
            ):
                coccoc_window[CocCocTitles.NEW_TAB_TITLE].child_window(
                    title="Infobar", control_type="Custom"
                ).child_window(title="Close", control_type="Button").click_input(
                    button="left", double=True
                )
                sleep(2)
        except Exception:
            pass  # ignore if not found, let the program continue

    else:
        try:
            if (
                coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                .child_window(title="Thanh thông tin", control_type="Custom")
                .exists(timeout=10)
                is True
            ):
                coccoc_window[CocCocTitles.NEW_TAB_TITLE].child_window(
                    title="Thanh thông tin", control_type="Custom"
                ).child_window(title="Đóng", control_type="Button").click_input(
                    button="left", double=True
                )
                sleep(2)
        except Exception:
            pass  # ignore if not found, let the program continue
