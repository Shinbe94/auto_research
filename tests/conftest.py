# Add option for command line
import faulthandler
import ftplib
import os
import time
from typing import List, Type, Generator
from datetime import datetime, timedelta, date

import ftputil
import pytest
import pywinauto
import win32gui
from appium import webdriver as appium_driver
from playwright.sync_api import sync_playwright, Page, Playwright
from playwright.sync_api import sync_playwright as sync_playwright2
from playwright.sync_api import sync_playwright as sync_playwright3
from pywinauto import Application
from selenium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles, ChromeType
from src.pages.dialogs.age_confirmation import AgeConfirmationSel
from src.pages.dialogs.dictionary import DictionarySel
from src.pages.dialogs.google_translate import GoogleTranslatePopUp
from src.pages.dialogs.infobar_container import InfobarContainer
from src.pages.dialogs.unit_converter import UnitConverterSel
from src.pages.dialogs.pop_ups import (
    Adblock,
    AdblockOnboarding,
    OpenPickApplication,
    ReportIssue,
    SafeBrowsingTooltip,
    WarningClosingTabs,
)
from src.pages.extensions.savior_extension_detail_page import SaviorExtensionDetailPage
from src.pages.incognito.incognito_page import IncognitoPageSel
from src.pages.internal_page.bookmarks.bookmark_bar import BookmarkBar
from src.pages.internal_page.coccoc_apps_page import CocCocAppsPageSel
from src.pages.internal_page.coccoc_url import CocCocURLSel
from src.pages.internal_page.components.components_page import ComponentsPage
from src.pages.internal_page.crashes.crash_page import CrashPage
from src.pages.internal_page.crashes.crashes_page import CrashesPage, CrashesPageSel
from src.pages.internal_page.downloads.download_bar import DownloadBar
from src.pages.internal_page.downloads.download_page import (
    DownloadPage,
    DownloadPageAppium,
    DownloadPageSel,
)
from src.pages.internal_page.extensions.extension_detail_page import (
    ExtensionDetailPageSel,
)
from src.pages.internal_page.extensions.extension_devtools import (
    ExtensionDevtool,
    ExtensionDevtoolApp,
    ExtensionDevtoolSel,
)
from src.pages.internal_page.extensions.extensions_page import (
    ExtensionsPage,
    ExtensionsPageApp,
    ExtensionsPageSel,
)
from src.pages.internal_page.flags.flags_page import FlagsPage, FlagsPageSel
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.menus.context_menu import ContextMenu
from src.pages.menus.main_menu import MainMenu
from src.pages.new_tab.new_tab_page import NewTabPage, NewTabPageSel
from src.pages.onboarding.onboarding import OnBoarding
from src.pages.onboarding.points_onboarding import PointsOnBoarding
from src.pages.savior.youtube_page import YoutubeAppium
from src.pages.settings import setting_about_coccoc
from src.pages.settings.setting_about_coccoc import SettingsAboutCocCocSel
from src.pages.settings.settings_adblock import SettingsAdblock, SettingsAdblockSel
from src.pages.settings.settings_appearance import (
    SettingsAppearance,
    SettingsAppearanceSel,
)
from src.pages.settings.settings_cookies import SettingsCookies
from src.pages.settings.settings_default_browser import SettingsDefaultBrowserSel
from src.pages.settings.settings_downloads import SettingsDownloadsSel
from src.pages.settings.settings_language import SettingsLanguageSel
from src.pages.settings.settings_on_startup import SettingsOnStartupSel
from src.pages.settings.settings_privacy_and_security import (
    SettingsPrivacyAndSecuritySel,
)
from src.pages.settings.settings_reset import SettingsResetSel
from src.pages.settings.settings_search import SettingsSearch
from src.pages.settings.settings_side_bar import SettingsSidebar
from src.pages.settings.settings_system import SettingsSystemSel
from src.pages.settings.settings_tor_options import (
    SettingsTorOptions,
    SettingsTorOptionsSel,
)
from src.pages.sidebar.sidebar import Sidebar
from src.pages.internal_page.credits.credits_page import CreditsPage, CreditsPageSel
from src.pages.sidebar.sidebar_custom_icon_context_menu import (
    SidebarCustomIconContextMenu,
)
from src.pages.sidebar.sidebar_edit_custom_icon import SidebarEditCustomIcon
from src.pages.sidebar.sidebar_web_panel import SidebarWebPanel
from src.pages.support_pages.support_pages import (
    ChromeStore,
    DeveloperMozillaSel,
    DownloadTestItim,
    FacebookSel,
    GooglePage,
    GooglePageSel,
    InfoByIp,
    InfoByIpSel,
    SafeBrowsingApp,
    SafeBrowsingSel,
    ThePirateBaySel,
    W3SchoolSel,
    WarningPageSel,
    WebTorrentSel,
    XeSel,
)
from src.pages.toolbar.toolbar import Toolbar
from src.pages.incognito.incognito_tor_page import IncognitoTorPage
from src.pages.topbar.top_bar import Topbar
from src.pages.unloaded_site.un_reach_site import UnReachSite
from src.utilities import os_utils, file_utils, ftp_connection, browser_utils
from tests import setting
from src.pages.installations import installation_utils


# from selenium.webdriver.chrome.service import Service as ChromeService


def pytest_addoption(parser):
    parser.addoption("--repeat", action="store", help="Repeat test")
    parser.addoption(
        "--platform", action="store", default=setting.platform, help="Repeat test"
    )


def pytest_generate_tests(metafunc):
    if metafunc.config.option.repeat is not None:
        count = int(metafunc.config.option.repeat)
        metafunc.fixturenames.append("tmp_ct")
        metafunc.parametrize("tmp_ct", range(count))


@pytest.fixture(autouse=True)
def get_platform(request):
    _platform = request.config.getoption("--platform")
    return _platform


@pytest.fixture(autouse=True)
def sleep_after_each_test():
    yield
    time.sleep(setting.sleep_n_seconds_after_each_test)


@pytest.fixture(autouse=False, scope="session")
def download_setup_files_to_local2():
    """
    Args:
        try to get all files from folder at local FTP (10.193.8.18) if lost connection or no files -->
        Get from remote FTP: browser3v.dev.itim.vn
    Returns:
    """
    ftp_connection.download_setup_file_to_local()


@pytest.fixture(autouse=True, scope="session")
def download_needed_builds():
    """
    Args:
        try to get all files from folder at local FTP (10.193.8.18) if lost connection or no files -->
        Get from remote FTP: browser3v.dev.itim.vn
    Returns:
    """
    ftp_connection.download_needed_builds()


@pytest.fixture(autouse=True, scope="session")
def check_coccoc_driver():
    """Automatically download coccoc-driver for testing"""
    ftp_connection.download_coccoc_drivers()


# Start coccoc by Playwright
@pytest.fixture()
def playwright_chrome():
    """
    Start CocCoc browser by Playwright Persistent context
    pc mean: Playwright CocCoc
    Returns:
    """
    p = sync_playwright().start()
    # browser = p.chromium.launch(
    #     headless=False
    # )
    browser = p.chromium.launch_persistent_context(
        headless=False,
        executable_path=browser_utils.get_chrome_executable_path(),
        user_data_dir=rf"C:\Users\{os_utils.get_username()}\AppData\Local\Google\Chrome\User Data\Default",
    )
    page = browser.new_page()
    yield page
    page.close()


# Start coccoc by selenium as default profile
@pytest.fixture()
def sc(request) -> Generator[WebDriver, None, None]:
    """This fixture is open coccoc by selenium with default user data (Default profile)
    Args:
        request (_type_): _description_

    Yields:
        _type_: _description_
    """
    driver = None
    coccoc_options = ChromeOptions()
    coccoc_options.add_argument("--start-maximized")
    # coccoc_options.add_argument(
    #     rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data")
    # if "profile_1" in request.keywords:
    #     coccoc_options.add_argument("--profile-directory=Profile 1")
    # elif "profile_2" in request.keywords:
    #     coccoc_options.add_argument("--profile-directory=Profile 2")
    # else:
    #     coccoc_options.add_argument("--profile-directory=Default")
    if "open_incognito_window" in request.keywords:
        coccoc_options.add_argument("--incognito")
    coccoc_options.add_argument(f"--lang={setting.coccoc_language}")
    coccoc_options.accept_insecure_certs = True
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()

    try:
        # selenium 3
        driver: WebDriver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
        time.sleep(1)
    finally:
        if driver is not None:
            yield driver
            driver.quit()


# Start coccoc by selenium with profile selection
@pytest.fixture()
def sc2(request) -> Generator[WebDriver, None, None]:
    # """
    # This fixture is support multiple profile with same 'User Data' folder
    # User Data folder has multiple profile: Default, Profile 1, Profile 2...
    # You want to start multiple instances of driver for each profile.
    # Using: using fixture 'sc' as a driver instance for Default, use 'sc2' as another driver instance for Profile 1 ...
    # Note: we should create profile folder already at C:\Users\your_user_name\AppData\Local\CocCoc\Browser\User Data, e.g Profile 1, Profile 2
    # by running cmd: browser.exe --profile-directory="Profile 1", browser.exe --profile-directory="Profile 2"
    # Args:
    #     request (_type_): _description_

    # Yields:
    #     _type_: _description_
    # """
    driver = None
    coccoc_options = ChromeOptions()
    coccoc_options.add_argument("--start-maximized")
    # coccoc_options.add_argument(
    #     rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data")
    if "profile_1" in request.keywords:
        coccoc_options.add_argument("--profile-directory=Profile 1")
    elif "profile_2" in request.keywords:
        coccoc_options.add_argument("--profile-directory=Profile 2")
    else:
        coccoc_options.add_argument("--profile-directory=Default")

    coccoc_options.add_argument(f"--lang={setting.coccoc_language}")
    coccoc_options.accept_insecure_certs = True
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    try:
        # selenium 3
        driver: WebDriver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
        time.sleep(1)
    finally:
        if driver is not None:
            yield driver
            driver.quit()


# Start coccoc by Playwright
@pytest.fixture()
def pc():
    """
    Start CocCoc browser by Playwright Persistent context
    pc mean: Playwright CocCoc
    Returns:
    """
    p = sync_playwright().start()
    # browser = p.chromium.launch(
    #     headless=False, executable_path=browser_utils.get_coccoc_executable_path()
    # )
    browser = p.chromium.launch_persistent_context(
        headless=False,
        executable_path=browser_utils.get_coccoc_executable_path(),
        user_data_dir=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default",
    )
    page = browser.new_page()
    yield page
    page.close()


# Connect to the current coccoc session which opening by WinAppDriver
@pytest.fixture()
# @pytest.mark.disable_extensions
def pcc(wad, request) -> Page:  # type: ignore
    """
    pcc means: 'Playwright CocCoc Connection', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad: win_app_driver
    Returns: page
    """
    # time.sleep(20)
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    # page.set_viewport_size({"width": 640, "height": 480})
    yield page

    if "keep_browser_opening" in request.keywords:
        pass
    else:
        page.close()
        default_context.close()
        browser.close()
        pw.stop()
    # with sync_playwright() as playwright:
    #     # Connect to an existing instance of Chrome using the connect_over_cdp method.
    #     browser = playwright.chromium.connect_over_cdp(
    #         "http://127.0.0.1:9222", timeout=30_000
    #     )

    #     # Retrieve the first context of the browser.
    #     default_context = browser.contexts[0]

    #     # Retrieve the first page in the context.
    #     page = default_context.pages[0]
    #     yield page
    #     page.close()
    #     browser.close()


# Connect to the current coccoc session which opening by WinAppDriver session2
@pytest.fixture()
def pcc2(wad2, request) -> Page:  # type: ignore
    """
    pcc means: 'Playwright CocCoc Connection', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad2: win_app_driver
    Returns: page
    """
    pw = sync_playwright2().start()
    browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9223")
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    # page.set_viewport_size({"width": 640, "height": 480})
    yield page

    if "keep_browser_opening2" in request.keywords:
        pass
    else:
        page.close()
        default_context.close()
        browser.close()
        pw.stop()


# Connect to the current coccoc session which opening by WinAppDriver session2
@pytest.fixture()
def pcc3(wad3, request) -> Page:  # type: ignore
    """
    Connect to coccoc instance with Custom user dir
    pcc means: 'Playwright CocCoc Connection', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad3: win_app_driver
    Returns: page
    """
    pw3 = sync_playwright3().start()
    browser = pw3.chromium.connect_over_cdp("http://127.0.0.1:9225")
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    # page.set_viewport_size({"width": 640, "height": 480})
    yield page

    if "keep_browser_opening3" in request.keywords:
        pass
    else:
        page.close()
        default_context.close()
        browser.close()
        pw3.stop()


def switch_to_coccoc_page(driver: WebDriver):
    for window in driver.window_handles:
        driver.switch_to.window(window)
        if "coccoc.com/webhp" in driver.current_url:
            break


# Connect to the current coccoc session which opening by WinAppDriver using Selenium
@pytest.fixture()
def scc(wad, request):  # type: ignore
    """
    pcc means: 'Selenium CocCoc Connect', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad: win_app_driver
    Returns: selenium driver
    """
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True  # type: ignore
    # coccoc_options.add_argument(
    #     rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data")
    # coccoc_options.add_argument("--profile-directory=Default")
    # coccoc_options.add_argument("--disable-gpu")
    coccoc_options.add_argument("--no-sandbox")
    coccoc_options.set_capability(
        "goog:loggingPrefs", {"browser": "ALL"}  # old: loggingPrefs
    )
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
    except WebDriverException:
        if driver is not None:
            driver.quit()
            time.sleep(1)
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
    else:
        # switch_to_coccoc_page(driver)
        yield driver

        if "keep_browser_opening" in request.keywords:
            pass
        else:
            if driver is not None:
                driver.quit()


# Connect to the current coccoc session which opening by WinAppDriver using Selenium
@pytest.fixture()
def scc2(wad2, request):  # type: ignore
    """
    pcc means: 'Selenium CocCoc Connect', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad2: win_app_driver 2
    Returns: selenium driver
    """
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True  # type: ignore
    # coccoc_options.add_argument(
    #     rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data")
    # coccoc_options.add_argument("--profile-directory=Default")
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # coccoc_options.set_capability("goog:loggingPrefs", {  # old: loggingPrefs
    #     "browser": "ALL"})
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    try:
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
    except Exception as e:
        raise e
    else:
        yield driver

        if "keep_browser_opening" in request.keywords:
            pass
        else:
            if driver is not None:
                driver.quit()


# Connect to the current coccoc session which opening by WinAppDriver using Selenium
@pytest.fixture()
def scc3(wad3, request):  # type: ignore
    """
    pcc means: 'Selenium CocCoc Connect', connect to the current session of CocCoc
    using Chrome DevTools protocol (opened by appium)
    Args:
        request: set keyword during test execution
        wad3: win_app_driver 3
    Returns: selenium driver
    """
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True  # type: ignore
    # coccoc_options.add_argument(
    #     rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data")
    # coccoc_options.add_argument("--profile-directory=Default")
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9225")
    # coccoc_options.set_capability("goog:loggingPrefs", {  # old: loggingPrefs
    #     "browser": "ALL"})
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    try:
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            # ChromeDriverManager(chrome_type=ChromeType.COCCOC).install(),
            options=coccoc_options,
        )
    except Exception as e:
        raise e
    else:
        yield driver

        if "keep_browser_opening" in request.keywords:
            pass
        else:
            if driver is not None:
                driver.quit()


@pytest.fixture()
def open_win_app_driver_server():
    """
    Start WinAppDriver server by using Pywinauto
    Returns: None
    """
    # Close current WinAppDriver if any
    close_win_app_driver_server()

    # Start new instance of WinAppDriver
    def _open_win_app_driver_server(port: int = 4723):
        app = Application(backend="uia").start(
            rf"{browser_utils.get_winappdriver_executable_path()} {port}",
            create_new_console=True,
            wait_for_idle=False,
            retry_interval=1,
        )
        # pywinauto.keyboard.send_keys(command)
        return int(app.process)  # type: ignore

    return _open_win_app_driver_server


@pytest.fixture(autouse=False)
def open_win_app_driver_server1() -> int:
    """
    Start WinAppDriver server by using Pywinauto
    Returns: None
    """
    # Close current WinAppDriver if any
    close_win_app_driver_server()

    # Start new instance of WinAppDriver
    app = Application(backend="uia").start(
        rf"{browser_utils.get_winappdriver_executable_path()}",
        create_new_console=True,
        wait_for_idle=False,
        retry_interval=1,
    )
    return int(app.process)  # type: ignoreopen_win_app_driver_server


def test_close_win_app_driver_server():
    close_win_app_driver_server()


def close_win_app_driver_server() -> None:
    """
    # Close WinAppDriver server, use to close WinAppDriver after test
    Returns: None
    """
    try:
        os_utils.kill_process_by_name("WinAppDriver.exe")
    except Exception as e:
        raise e


def close_win_app_driver_server_by_its_id(pid: int):
    """
    # Close WinAppDriver server by given pid, use to close WinAppDriver after test
    Returns: None
    """
    try:
        os_utils.kill_process_by_its_id(pid)
    except Exception as e:
        raise e


@pytest.fixture()
def wad(request, open_win_app_driver_server, language=setting.coccoc_language):
    """
    Get and Return WinAppDriver
    Args:
        request: request param for particular setup & teardown.
        open_win_app_driver_server: Start WinAppDriver server automatically
        language: en or vi
    Returns: Appium driver
    """
    port = 4723
    pid = open_win_app_driver_server(port=port)
    driver: WebDriver = None
    if "open_tor_window" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --tor",
        }
    elif "open_incognito_window" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --incognito",
        }
    elif "open_in_bootstrap_mode" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --extension-content-verification=bootstrap",
        }
    elif "open_in_enforce_mode" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --extension-content-verification=enforce",
        }
    elif "IPH_CocCocScrollToTop" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized  --enable-features=IPH_CocCocScrollToTop",
        }
    elif "DisableCocCocUseChromeUserAgent" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized  --disable-features=CocCocUseChromeUserAgent",
        }
    elif "EnableAdblockOnboarding" in request.keywords:
        desired_caps = {
            # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized  --enable-features=IPH_CocCocAdBlock",
        }
    # elif "open_profile_1" in request.keywords:
    #     desired_caps = {
    #         # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    #         "app": rf"{browser_utils.get_coccoc_executable_path()}",
    #         "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Profile 1"',
    #     }
    elif "disable_extensions" in request.keywords:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Default" --disable-popup-blocking --disable-extensions',
        }
    else:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Default" --disable-popup-blocking',
        }
    try:
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    except WebDriverException:
        close_win_app_driver_server_by_its_id(pid)
        browser_utils.kill_all_coccoc_process()
        time.sleep(2)
        pid = open_win_app_driver_server(port=port)
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    else:
        time.sleep(1)
        yield driver
        if "ignore_tear_down" in request.keywords:
            pass
        else:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
        close_win_app_driver_server_by_its_id(pid)


@pytest.fixture()
def wad2(
    request, open_win_app_driver_server, language=setting.coccoc_language
) -> AppiumWebDriver:
    """
    Get and Return WinAppDriver
    Args:
        request: request param for particular setup & teardown.
        open_win_app_driver_server: Start WinAppDriver server automatically
        language: en or vi
    Returns: Appium driver
    """
    port = 4724
    pid = open_win_app_driver_server(port=port)
    driver: WebDriver = None
    if "open_tor_window2" in request.keywords:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --tor",
        }
    elif "open_incognito_window2" in request.keywords:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized --incognito",
        }
    # elif "open_profile_1" in request.keywords:
    #     desired_caps = {
    #         # "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    #         "app": rf"{browser_utils.get_coccoc_executable_path()}",
    #         "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Profile 1"',
    #     }
    else:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9222 --start-maximized",
        }
    try:
        driver: AppiumWebDriver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    except WebDriverException:
        close_win_app_driver_server_by_its_id(pid)
        browser_utils.kill_all_coccoc_process()
        time.sleep(2)
        pid = open_win_app_driver_server(port=port)
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    else:
        yield driver
        if "ignore_tear_down2" in request.keywords:
            pass
        else:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
        close_win_app_driver_server_by_its_id(pid)


@pytest.fixture()
def wad3(
    request,
    open_win_app_driver_server,
    check_custom_user_dir_exist,
    language=setting.coccoc_language,
) -> AppiumWebDriver:
    """
    Get and Return WinAppDriver by start Custom profile user
    Note: We should create a custom folder such as "C:\browsers" to hold the custom profile
    Args:
        request: request param for particular setup & teardown.
        open_win_app_driver_server: Start WinAppDriver server automatically
        language: en or vi
    Returns: Appium driver
    """
    port = 4725
    pid = open_win_app_driver_server(port=port)
    driver: WebDriver = None
    fixed_user_dir = setting.fixed_custom_user_dir
    if "open_tor_window3" in request.keywords:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9225 --start-maximized --tor --user-data-dir={fixed_user_dir}",
        }
    elif "open_incognito_window3" in request.keywords:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9225 --start-maximized --incognito",
        }
    else:
        desired_caps = {
            "app": rf"{browser_utils.get_coccoc_executable_path()}",
            "appArguments": rf"--lang={language} --remote-debugging-port=9225 --start-maximized --user-data-dir={fixed_user_dir}",
        }
    try:
        driver: AppiumWebDriver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    except WebDriverException:
        close_win_app_driver_server_by_its_id(pid)
        browser_utils.kill_all_coccoc_process()
        time.sleep(2)
        pid = open_win_app_driver_server(port=port)
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    else:
        yield driver
        if "ignore_tear_down3" in request.keywords:
            pass
        else:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
        close_win_app_driver_server_by_its_id(pid)


@pytest.fixture()
def open_coccoc_then_close_it(
    language=setting.coccoc_language, is_first_time_opened=False, close_after_seconds=3
):
    """
    To open coccoc like normal user for init some setting
    Args:
        language:
        is_first_time_opened:
        close_after_seconds:
    Returns:
    """
    title = None
    coccoc = Application(backend="uia")
    if language == "en" and is_first_time_opened is True:
        title = CocCocTitles.WELCOME_PAGE_TITLE
    elif language == "en" and is_first_time_opened is False:
        title = CocCocTitles.NEW_TAB_TITLE_EN
    elif language == "vi" and is_first_time_opened is True:
        title = CocCocTitles.WELCOME_PAGE_TITLE
    elif language == "vi" and is_first_time_opened is False:
        title = CocCocTitles.NEW_TAB_TITLE_VI

    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        try:
            coccoc.start(
                setting.coccoc_binary_64bit + f" --lang={language}",
                timeout=setting.timeout_pywinauto,
            )
            time.sleep(close_after_seconds)
        finally:
            open_browser.close_coccoc_by_window_title(title=title, language=language)

    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        try:
            coccoc.start(
                setting.coccoc_binary_32bit + f" --lang={language}",
                timeout=setting.timeout_pywinauto,
            )
            time.sleep(close_after_seconds)
        finally:
            open_browser.close_coccoc_by_window_title(title=title, language=language)
    else:
        print("No CocCoc installed")
    time.sleep(2)


# ======================================================================================================================
# Pages fixtures part: playwright cocccoc
# ======================================================================================================================
@pytest.fixture()
def download_page(pcc: Page) -> Generator[DownloadPage, None, None]:
    download_page = DownloadPage(pcc)
    yield download_page


@pytest.fixture()
def on_boarding(pcc: Page) -> Generator[OnBoarding, None, None]:
    on_boarding = OnBoarding(pcc)
    yield on_boarding


@pytest.fixture()
def extensions_page(pcc: Page) -> Generator[ExtensionsPage, None, None]:
    extensions_page = ExtensionsPage(pcc)
    yield extensions_page


@pytest.fixture()
def google_page(pcc: Page) -> Generator[GooglePage, None, None]:
    google_page = GooglePage(pcc)
    yield google_page


@pytest.fixture()
def crashes_page(pcc: Page) -> Generator[CrashesPage, None, None]:
    crashes_page = CrashesPage(pcc)
    yield crashes_page


@pytest.fixture()
def settings_search(pcc: Page) -> Generator[SettingsSearch, None, None]:
    settings_search = SettingsSearch(pcc)
    yield settings_search


@pytest.fixture()
def flags_page(pcc: Page) -> Generator[FlagsPage, None, None]:
    flags_page = FlagsPage(pcc)
    yield flags_page


@pytest.fixture()
def incognito_tor_page(pcc: Page) -> Generator[IncognitoTorPage, None, None]:
    tor_page = IncognitoTorPage(pcc)
    yield tor_page


@pytest.fixture()
def settings_tor_options(pcc: Page) -> Generator[SettingsTorOptions, None, None]:
    settings_tor_options = SettingsTorOptions(pcc)
    yield settings_tor_options


@pytest.fixture()
def settings_appearance(pcc: Page) -> Generator[SettingsAppearance, None, None]:
    settings_appearance = SettingsAppearance(pcc)
    yield settings_appearance


@pytest.fixture()
def settings_side_bar(pcc: Page) -> Generator[SettingsSidebar, None, None]:
    settings_side_bar = SettingsSidebar(pcc)
    yield settings_side_bar


@pytest.fixture()
def histograms(pcc: Page) -> Generator[Histograms, None, None]:
    histograms = Histograms(pcc)
    yield histograms


@pytest.fixture()
def new_tab_page(pcc: Page) -> Generator[NewTabPage, None, None]:
    new_tab_page = NewTabPage(pcc)
    yield new_tab_page


@pytest.fixture()
def new_tab_page20(pw_wad: Page) -> Generator[NewTabPage, None, None]:
    new_tab_page20 = NewTabPage(pw_wad)
    yield new_tab_page20


@pytest.fixture()
def settings_cookies(pcc: Page) -> Generator[SettingsCookies, None, None]:
    settings_cookies = SettingsCookies(pcc)
    yield settings_cookies


@pytest.fixture()
def savior_extension_detail_page(
    pcc: Page,
) -> Generator[SaviorExtensionDetailPage, None, None]:
    settings_cookies = SaviorExtensionDetailPage(pcc)
    yield settings_cookies


@pytest.fixture()
def credits_page(
    pcc: Page,
) -> Generator[CreditsPage, None, None]:
    credits_page = CreditsPage(pcc)
    yield credits_page


@pytest.fixture()
def components_page(
    pcc: Page,
) -> Generator[ComponentsPage, None, None]:
    components_page = ComponentsPage(pcc)
    yield components_page


@pytest.fixture()
def info_by_ip(pcc: Page) -> Generator[InfoByIp, None, None]:
    info_by_ip = InfoByIp(pcc)
    yield info_by_ip


@pytest.fixture()
def settings_adblock(pcc: Page) -> Generator[SettingsAdblock, None, None]:
    settings_adblock = SettingsAdblock(pcc)
    yield settings_adblock


@pytest.fixture()
def extension_devtool(pcc: Page) -> Generator[ExtensionDevtool, None, None]:
    extension_devtool = ExtensionDevtool(pcc)
    yield extension_devtool


@pytest.fixture()
def points_on_boarding(pcc: Page) -> Generator[PointsOnBoarding, None, None]:
    points_on_boarding = PointsOnBoarding(pcc)
    yield points_on_boarding


# ======================================================================================================================
# Pages fixtures part: WinAppDriver Coccoc
# ======================================================================================================================


@pytest.fixture()
def download_bar(wad) -> Generator[DownloadBar, None, None]:
    download_bar = DownloadBar(wad)
    yield download_bar


@pytest.fixture()
def toolbar(wad) -> Generator[Toolbar, None, None]:
    toolbar = Toolbar(wad)
    yield toolbar


@pytest.fixture()
def toolbar30(cc_win_app_driver) -> Generator[Toolbar, None, None]:
    toolbar30 = Toolbar(cc_win_app_driver)
    yield toolbar30


@pytest.fixture()
def sidebar(wad) -> Generator[Sidebar, None, None]:
    sidebar = Sidebar(wad)
    yield sidebar


@pytest.fixture()
def main_menu(wad) -> Generator[MainMenu, None, None]:
    main_menu = MainMenu(wad)
    yield main_menu


@pytest.fixture()
def sidebar_web_panel(wad) -> Generator[SidebarWebPanel, None, None]:
    sidebar_web_panel = SidebarWebPanel(wad)
    yield sidebar_web_panel


@pytest.fixture()
def sidebar_custom_icon_context_menu(
    wad,
) -> Generator[SidebarCustomIconContextMenu, None, None]:
    sidebar_custom_icon_context_menu = SidebarCustomIconContextMenu(wad)
    yield sidebar_custom_icon_context_menu


@pytest.fixture()
def sidebar_edit_custom_icon(wad) -> Generator[SidebarEditCustomIcon, None, None]:
    sidebar_edit_custom_icon = SidebarEditCustomIcon(wad)
    yield sidebar_edit_custom_icon


@pytest.fixture()
def extension_devtools_app(wad) -> Generator[ExtensionDevtoolApp, None, None]:
    extension_devtools_app = ExtensionDevtoolApp(wad)
    yield extension_devtools_app


@pytest.fixture()
def crash_page(wad) -> Generator[CrashPage, None, None]:
    crash_page = CrashPage(wad)
    yield crash_page


@pytest.fixture()
def bookmark_bar(wad) -> Generator[BookmarkBar, None, None]:
    bookmark_bar = BookmarkBar(wad)
    yield bookmark_bar


@pytest.fixture()
def un_reach_site(wad) -> Generator[UnReachSite, None, None]:
    un_reach_site = UnReachSite(wad)
    yield un_reach_site


@pytest.fixture()
def context_menu(wad) -> Generator[ContextMenu, None, None]:
    context_menu = ContextMenu(wad)
    yield context_menu


@pytest.fixture()
def top_bar(wad) -> Generator[Topbar, None, None]:
    top_bar = Topbar(wad)
    yield top_bar


@pytest.fixture()
def download_page_appium(wad) -> Generator[DownloadPageAppium, None, None]:
    download_page_appium = DownloadPageAppium(wad)
    yield download_page_appium


@pytest.fixture()
def youtube_page_appium(wad) -> Generator[YoutubeAppium, None, None]:
    youtube_page_appium = YoutubeAppium(wad)
    yield youtube_page_appium


@pytest.fixture()
def extensions_page_app(wad) -> Generator[ExtensionsPageApp, None, None]:
    extensions_page_app = ExtensionsPageApp(wad)
    yield extensions_page_app


@pytest.fixture()
def google_translate_pop_up(wad) -> Generator[GoogleTranslatePopUp, None, None]:
    google_translate_pop_up = GoogleTranslatePopUp(wad)
    yield google_translate_pop_up


@pytest.fixture()
def warning_closing_tabs(wad) -> Generator[WarningClosingTabs, None, None]:
    warning_closing_tabs = WarningClosingTabs(wad)
    yield warning_closing_tabs


@pytest.fixture()
def chrome_store(wad) -> Generator[ChromeStore, None, None]:
    chrome_store = ChromeStore(wad)
    yield chrome_store


@pytest.fixture()
def infobar_container(wad) -> Generator[InfobarContainer, None, None]:
    infobar_container = InfobarContainer(wad)
    yield infobar_container


@pytest.fixture()
def open_pick_application(wad) -> Generator[OpenPickApplication, None, None]:
    open_pick_application = OpenPickApplication(wad)
    yield open_pick_application


@pytest.fixture()
def report_issue(wad) -> Generator[ReportIssue, None, None]:
    report_issue = ReportIssue(wad)
    yield report_issue


@pytest.fixture()
def adblock(wad) -> Generator[Adblock, None, None]:
    adblock = Adblock(wad)
    yield adblock


@pytest.fixture()
def adblock_on_boarding(wad) -> Generator[AdblockOnboarding, None, None]:
    adblock_on_boarding = AdblockOnboarding(wad)
    yield adblock_on_boarding


@pytest.fixture()
def safe_browsing_app(wad) -> Generator[SafeBrowsingApp, None, None]:
    safe_browsing_app = SafeBrowsingApp(wad)
    yield safe_browsing_app


@pytest.fixture()
def safe_browsing_tooltip(wad) -> Generator[SafeBrowsingTooltip, None, None]:
    safe_browsing_tooltip = SafeBrowsingTooltip(wad)
    yield safe_browsing_tooltip


# ======================================================================================================================
# Pages fixtures part: Selenium2 + Winappdriver
# ======================================================================================================================
@pytest.fixture()
def download_page_sel(scc) -> Generator[DownloadPageSel, None, None]:
    download_page_sel = DownloadPageSel(scc)
    yield download_page_sel


@pytest.fixture()
def settings_downloads_sel(scc) -> Generator[SettingsDownloadsSel, None, None]:
    settings_downloads_sel = SettingsDownloadsSel(scc)
    yield settings_downloads_sel


@pytest.fixture()
def settings_default_browser_sel(
    scc,
) -> Generator[SettingsDefaultBrowserSel, None, None]:
    settings_default_browser_sel = SettingsDefaultBrowserSel(scc)
    yield settings_default_browser_sel


@pytest.fixture()
def settings_tor_options_sel(scc) -> Generator[SettingsTorOptionsSel, None, None]:
    settings_tor_options_sel = SettingsTorOptionsSel(scc)
    yield settings_tor_options_sel


@pytest.fixture()
def web_torrent_sel(scc) -> Generator[WebTorrentSel, None, None]:
    web_torrent_sel = WebTorrentSel(scc)
    yield web_torrent_sel


@pytest.fixture()
def the_pirate_bay_sel(scc) -> Generator[ThePirateBaySel, None, None]:
    the_pirate_bay_sel = ThePirateBaySel(scc)
    yield the_pirate_bay_sel


@pytest.fixture()
def download_test_itim(scc) -> Generator[DownloadTestItim, None, None]:
    download_test_itim = DownloadTestItim(scc)
    yield download_test_itim


@pytest.fixture()
def flags_page_sel(scc) -> Generator[FlagsPageSel, None, None]:
    flags_page_sel = FlagsPageSel(scc)
    yield flags_page_sel


@pytest.fixture()
def extensions_page_sel(scc) -> Generator[ExtensionsPageSel, None, None]:
    extensions_page_sel = ExtensionsPageSel(scc)
    yield extensions_page_sel


@pytest.fixture()
def warning_page_sel(scc) -> Generator[WarningPageSel, None, None]:
    warning_page_sel = WarningPageSel(scc)
    yield warning_page_sel


@pytest.fixture()
def developer_mozilla_sel(scc) -> Generator[DeveloperMozillaSel, None, None]:
    developer_mozilla_sel = DeveloperMozillaSel(scc)
    yield developer_mozilla_sel


@pytest.fixture()
def dictionary_sel(scc) -> Generator[DictionarySel, None, None]:
    dictionary_sel = DictionarySel(scc)
    yield dictionary_sel


@pytest.fixture()
def w3_school_sel(scc) -> Generator[W3SchoolSel, None, None]:
    w3_school_sel = W3SchoolSel(scc)
    yield w3_school_sel


@pytest.fixture()
def extension_detail_page_sel(scc) -> Generator[ExtensionDetailPageSel, None, None]:
    extension_detail_page_sel = ExtensionDetailPageSel(scc)
    yield extension_detail_page_sel


@pytest.fixture()
def new_tab_page_sel(scc) -> Generator[NewTabPageSel, None, None]:
    new_tab_page_sel = NewTabPageSel(scc)
    yield new_tab_page_sel


@pytest.fixture()
def unit_converter_sel(scc) -> Generator[UnitConverterSel, None, None]:
    unit_converter_sel = UnitConverterSel(scc)
    yield unit_converter_sel


@pytest.fixture()
def xe_sel(scc) -> Generator[XeSel, None, None]:
    xe_sel = XeSel(scc)
    yield xe_sel


@pytest.fixture()
def extension_devtool_sel(scc) -> Generator[ExtensionDevtoolSel, None, None]:
    extension_devtool_sel = ExtensionDevtoolSel(scc)
    yield extension_devtool_sel


@pytest.fixture()
def facebook_sel(scc) -> Generator[FacebookSel, None, None]:
    facebook_sel = FacebookSel(scc)
    yield facebook_sel


@pytest.fixture()
def settings_language_sel(scc) -> Generator[SettingsLanguageSel, None, None]:
    settings_language_sel = SettingsLanguageSel(scc)
    yield settings_language_sel


@pytest.fixture()
def settings_on_startup_sel(scc) -> Generator[SettingsOnStartupSel, None, None]:
    settings_on_startup_sel = SettingsOnStartupSel(scc)
    yield settings_on_startup_sel


@pytest.fixture()
def settings_appearance_sel(scc) -> Generator[SettingsAppearanceSel, None, None]:
    settings_appearance_sel = SettingsAppearanceSel(scc)
    yield settings_appearance_sel


@pytest.fixture()
def settings_privacy_and_security_sel(
    scc,
) -> Generator[SettingsPrivacyAndSecuritySel, None, None]:
    settings_privacy_and_security_sel = SettingsPrivacyAndSecuritySel(scc)
    yield settings_privacy_and_security_sel


@pytest.fixture()
def age_confirmation_sel(
    scc,
) -> Generator[AgeConfirmationSel, None, None]:
    age_confirmation_sel = AgeConfirmationSel(scc)
    yield age_confirmation_sel


@pytest.fixture()
def settings_reset_sel(
    scc,
) -> Generator[SettingsResetSel, None, None]:
    settings_reset_sel = SettingsResetSel(scc)
    yield settings_reset_sel


@pytest.fixture()
def settings_system_sel(
    scc,
) -> Generator[SettingsSystemSel, None, None]:
    settings_system_sel = SettingsSystemSel(scc)
    yield settings_system_sel


@pytest.fixture()
def coccoc_url_sel(
    scc,
) -> Generator[CocCocURLSel, None, None]:
    coccoc_url_sel = CocCocURLSel(scc)
    yield coccoc_url_sel


@pytest.fixture()
def settings_about_coccoc_sel(
    scc,
) -> Generator[SettingsAboutCocCocSel, None, None]:
    settings_about_coccoc_sel = SettingsAboutCocCocSel(scc)
    yield settings_about_coccoc_sel


@pytest.fixture()
def crashes_page_sel(
    scc,
) -> Generator[CrashesPageSel, None, None]:
    crashes_page_sel = CrashesPageSel(scc)
    yield crashes_page_sel


@pytest.fixture()
def credits_page_sel(
    scc,
) -> Generator[CreditsPageSel, None, None]:
    credits_page_sel = CreditsPageSel(scc)
    yield credits_page_sel


@pytest.fixture()
def coccoc_apps_page_sel(
    scc,
) -> Generator[CocCocAppsPageSel, None, None]:
    coccoc_apps_page_sel = CocCocAppsPageSel(scc)
    yield coccoc_apps_page_sel


@pytest.fixture()
def settings_adblock_sel(
    scc,
) -> Generator[SettingsAdblockSel, None, None]:
    settings_adblock_sel = SettingsAdblockSel(scc)
    yield settings_adblock_sel


@pytest.fixture()
def google_page_sel(
    scc,
) -> Generator[GooglePageSel, None, None]:
    google_page_sel = GooglePageSel(scc)
    yield google_page_sel


@pytest.fixture()
def safe_browsing_sel(
    scc,
) -> Generator[SafeBrowsingSel, None, None]:
    safe_browsing_sel = SafeBrowsingSel(scc)
    yield safe_browsing_sel


@pytest.fixture()
def settings_tor_options_sel2(scc2) -> Generator[SettingsTorOptionsSel, None, None]:
    settings_tor_options_sel = SettingsTorOptionsSel(scc2)
    yield settings_tor_options_sel


@pytest.fixture()
def incognito_page_sel2(scc2) -> Generator[IncognitoPageSel, None, None]:
    incognito_page_sel2 = IncognitoPageSel(scc2)
    yield incognito_page_sel2


@pytest.fixture()
def settings_tor_options_sel3(scc3) -> Generator[SettingsTorOptionsSel, None, None]:
    settings_tor_options_sel = SettingsTorOptionsSel(scc3)
    yield settings_tor_options_sel


@pytest.fixture()
def download_page_sel2(scc2) -> Generator[DownloadPageSel, None, None]:
    download_page_sel = DownloadPageSel(scc2)
    yield download_page_sel


@pytest.fixture()
def info_by_ip_sel3(scc3) -> Generator[InfoByIpSel, None, None]:
    info_by_ip_sel = InfoByIpSel(scc3)
    yield info_by_ip_sel


# ======================================================================================================================
# Fixtures support testing
# ======================================================================================================================


# check there is any crash happen while testing
@pytest.fixture(autouse=True)
def check_any_crash_happen():
    """
    This fixture is called after a test to verify any crash happens during test
    and if any crash happens assert then delete that crash to prevent failing for other tests...
    Returns:
    """
    yield
    folders = [
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\CrashReports",
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports",
        r"C:\Program Files (x86)\CocCoc\CrashReports",
    ]

    for folder in folders:
        if file_utils.check_folder_is_exists(folder):
            for file in file_utils.list_all_files_and_folders(folder):
                try:
                    if ".dmp" in file:
                        file_utils.copy_single_file(
                            src_path=f"{folder}/{file}",
                            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
                        )
                        print(rf"A crash happened at {folder}")
                    assert ".dmp" not in file
                finally:
                    # file_utils.remove_file(file_name_with_path=folder + "''" + file)
                    file_utils.remove_file(file_name_with_path=f"{folder}/{file}")


# Delete any crash files before test to prevent Error for other test cases
@pytest.fixture(autouse=True)
def delete_any_crash_dump_file():
    """
    This fixture is called before test
    Returns:
    """
    folders = [
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\CrashReports",
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports",
        r"C:\Program Files (x86)\CocCoc\CrashReports",
    ]

    for folder in folders:
        if file_utils.check_folder_is_exists(folder):
            for file in file_utils.list_all_files_and_folders(folder):
                if ".dmp" in file:
                    file_utils.remove_file(file_name_with_path=f"{folder}/{file}")
    yield


@pytest.fixture(autouse=True)
def disable_faulthandler():
    """
    This fixture is to disable the window fatal error during pywinauto test
    :return:
    """
    faulthandler.disable()
    yield
    faulthandler.enable()


@pytest.fixture(autouse=False)
def check_custom_user_dir_exist() -> None:
    """This fixture is for creating the custom user-dir automatically if it's not existed!
    Note: Custom user-dir location is at "setting.fixed_custom_user_dir"
    Args:
        autouse (bool, optional): _description_. Defaults to False.
    """
    if (
        not file_utils.check_folder_is_exists(
            directory_with_path=setting.fixed_custom_user_dir
        )
        or len(
            file_utils.list_all_files_and_folders(
                directory=setting.fixed_custom_user_dir
            )
        )
        <= 0
    ):
        file_utils.create_folder(setting.fixed_custom_user_dir)
        app = Application(backend="uia").start(
            rf"{browser_utils.get_coccoc_executable_path()}"
            + " --start-maximized"
            + rf" --user-data-dir={setting.fixed_custom_user_dir}",
            timeout=setting.timeout_pywinauto,
        )
        app.window().set_focus().close()


# ======================================================================================================================
# Pages fixtures part2: Playwright Coccoc(using new winappdriver session with difference port)
# ======================================================================================================================


@pytest.fixture()
def main_menu2(wad2) -> Generator[MainMenu, None, None]:
    main_menu = MainMenu(wad2)
    yield main_menu


@pytest.fixture()
def toolbar2(wad2) -> Generator[Toolbar, None, None]:
    toolbar = Toolbar(wad2)
    yield toolbar


@pytest.fixture()
def bookmark_bar2(wad2) -> Generator[BookmarkBar, None, None]:
    bookmark_bar = BookmarkBar(wad2)
    yield bookmark_bar


@pytest.fixture()
def download_page2(pcc2: Page) -> Generator[DownloadPage, None, None]:
    download_page = DownloadPage(pcc2)
    yield download_page


@pytest.fixture()
def settings_cookies2(pcc2: Page) -> Generator[SettingsCookies, None, None]:
    settings_cookies = SettingsCookies(pcc2)
    yield settings_cookies


@pytest.fixture()
def savior_extension_detail_page2(
    pcc2: Page,
) -> Generator[SaviorExtensionDetailPage, None, None]:
    settings_cookies = SaviorExtensionDetailPage(pcc2)
    yield settings_cookies


@pytest.fixture()
def histograms2(pcc2: Page) -> Generator[Histograms, None, None]:
    histograms = Histograms(pcc2)
    yield histograms


# ======================================================================================================================
# Pages fixtures part3: Playwright Coccoc(using new winappdriver session with difference port and Custom coccoc profile)
# ======================================================================================================================


@pytest.fixture()
def main_menu3(wad3) -> Generator[MainMenu, None, None]:
    main_menu = MainMenu(wad3)
    yield main_menu


@pytest.fixture()
def toolbar3(wad3) -> Generator[Toolbar, None, None]:
    toolbar = Toolbar(wad3)
    yield toolbar


@pytest.fixture()
def bookmark_bar3(wad3) -> Generator[BookmarkBar, None, None]:
    bookmark_bar = BookmarkBar(wad3)
    yield bookmark_bar


@pytest.fixture()
def download_page3(pcc3: Page) -> Generator[DownloadPage, None, None]:
    download_page = DownloadPage(pcc3)
    yield download_page


@pytest.fixture()
def settings_cookies3(pcc3: Page) -> Generator[SettingsCookies, None, None]:
    settings_cookies = SettingsCookies(pcc3)
    yield settings_cookies


@pytest.fixture()
def savior_extension_detail_page3(
    pcc3: Page,
) -> Generator[SaviorExtensionDetailPage, None, None]:
    settings_cookies = SaviorExtensionDetailPage(pcc3)
    yield settings_cookies


@pytest.fixture()
def histograms3(pcc3: Page) -> Generator[Histograms, None, None]:
    histograms = Histograms(pcc3)
    yield histograms


@pytest.fixture()
def info_by_ip3(pcc3: Page) -> Generator[InfoByIp, None, None]:
    info_by_ip = InfoByIp(pcc3)
    yield info_by_ip


# ======================================================================================================================
# Assistants
# ======================================================================================================================
@pytest.fixture(autouse=True)
def kill_ultra_viewer_service():
    """
    To kill the ultra viewer service
    Returns:
    """
    os_utils.kill_process_by_name(pid_name="UltraViewer_Service.exe")


@pytest.fixture(autouse=True)
def remove_all_crdownload():
    """
    To trying to remove all file endwith '.crdownload'
    """
    try:
        file_utils.delete_files_by_regress_name_downloads_folder(file_name="crdownload")
    except Exception as e:
        raise e


# ======================================================================================================================
# Attaching the WinAppDriver session to the window by its title
# ======================================================================================================================


def test_find_window_handle():
    print(find_window_handle(title="Cốc Cốc"))


def find_window_handle(
    title: str, timeout=setting.timeout_selenium, is_exact_name=False
) -> list:
    """To  find the window handler by its title

    Args:
        title (str): _description_

    Raises:
        e: _description_

    Returns:
        list: _description_
    """

    handleList = []

    def findit(hwnd, ctx):
        total_delay = 0
        interval_delay = 1
        # check the title
        # "Initializing..., Cốc Cốc Installer"
        # win32gui.GetWindowText(hwnd) == "New Tab - Cốc Cốc"
        # while total_delay < timeout:
        try:
            if is_exact_name:
                if win32gui.GetWindowText(hwnd) == title:
                    handleList.append(hwnd)
            else:
                if title in win32gui.GetWindowText(hwnd):
                    handleList.append(hwnd)
                # if len(handleList) > 0:
                # break
        except Exception as e:
            raise e
            # time.sleep(interval_delay)
            # total_delay = total_delay + interval_delay

    win32gui.EnumWindows(findit, None)
    # print(handleList)
    return handleList


@pytest.fixture()
def wad_session() -> AppiumWebDriver:
    """
    This is attaching session into the window by its title

    """

    def _wad_session(
        title: str = CocCocTitles.NEW_TAB,
        port=4729,
        timeout=setting.timeout_selenium,
        is_exact_name=False,
        implicitly_wait: int = 10,
    ) -> AppiumWebDriver:
        def _open_win_app_driver_server(port=port) -> int:
            app = Application(backend="uia").start(
                rf"{browser_utils.get_winappdriver_executable_path()} {port}",
                create_new_console=True,
                wait_for_idle=False,
                retry_interval=1,
            )
            return int(app.process)  # type: ignore

        global wad_pid
        wad_pid = _open_win_app_driver_server(port=port)
        desired_caps = {}
        desired_caps["appTopLevelWindow"] = hex(
            find_window_handle(
                title=title, timeout=timeout, is_exact_name=is_exact_name
            )[0]
        )
        desired_caps["deviceName"] = "WindowsPC"
        desired_caps["platformName"] = "Windows"
        session: AppiumWebDriver = webdriver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
        session.implicitly_wait(implicitly_wait)
        return session
        # session.quit()

    yield _wad_session
    # _wad_session.quit()
    if wad_pid is not None:
        close_win_app_driver_server_by_its_id(pid=wad_pid)


@pytest.fixture()
def wad_session2() -> AppiumWebDriver:
    """
    This is attaching session into the window by its title

    """

    def _wad_session(
        title: str,
        port=4730,
        timeout=setting.timeout_selenium,
        is_exact_name=False,
        implicitly_wait: int = 10,
    ) -> AppiumWebDriver:
        def _open_win_app_driver_server(port=port) -> int:
            app = Application(backend="uia").start(
                rf"{browser_utils.get_winappdriver_executable_path()} {port}",
                create_new_console=True,
                wait_for_idle=False,
                retry_interval=1,
            )
            return int(app.process)  # type: ignore

        global wad_pid
        wad_pid = _open_win_app_driver_server(port=port)
        desired_caps = {}
        desired_caps["appTopLevelWindow"] = hex(
            find_window_handle(
                title=title, timeout=timeout, is_exact_name=is_exact_name
            )[0]
        )
        desired_caps["deviceName"] = "WindowsPC"
        desired_caps["platformName"] = "Windows"
        session: AppiumWebDriver = webdriver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
        session.implicitly_wait(implicitly_wait)
        return session
        # session.quit()

    yield _wad_session
    # _wad_session.quit()
    if wad_pid is not None:
        close_win_app_driver_server_by_its_id(pid=wad_pid)


@pytest.fixture(autouse=False)
def uninstall_coccoc_after_test():
    yield
    installation_utils.uninstall_coccoc_silently()


@pytest.fixture()
def upgrade_browser_via_about_us():
    file_utils.rename_and_copy_file_host()
    # After change host, trying to restart 'Background intelligent tranfer service" for sure
    os_utils.restart_background_intellignet_transfer()
    if setting_about_coccoc.click_relaunch_button_pywinauto():
        # Check browser version after upgrade
        setting_about_coccoc.check_browser_after_update(
            language=setting.coccoc_language
        )
    yield
    file_utils.remove_and_revert_file_host()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.start = call.start
    report.stop = call.stop


def pytest_terminal_summary(terminalreporter):
    terminalreporter.ensure_newline()
    terminalreporter.section("start/stop times", sep="-", bold=True)
    for stat in terminalreporter.stats.values():
        for report in stat:
            # if report.when == "call":
            if getattr(report, "when", None) == "call":
                start = datetime.fromtimestamp(report.start)
                stop = datetime.fromtimestamp(report.stop)
                terminalreporter.write_line(
                    f"{report.nodeid:20}: {start:%Y-%m-%d %H:%M:%S} - {stop:%Y-%m-%d %H:%M:%S}"
                )


def p_driver():
    """Connect the coccoc (start by WinAppDriver) via Playwright
    Returns:
        page: Playwright page
        browser: Playwright browser
        pw: Playwright engine

    """
    pwad = p_wad()
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    return page, browser, pw, pwad[0], pwad[1]


def p_wad(port=4723, language=setting.coccoc_language):
    """Start WinAppDriver instance + CocCoc
    Args:
        port (int, optional): _description_. Defaults to 4723.
        language (_type_, optional): _description_. Defaults to setting.coccoc_language.

    Returns:
        driver: WinAppDriver instance
        pid: WinAppDriver process_id
    """
    pid = open_winappdriver_server()
    driver: WebDriver = None

    desired_caps = {
        "app": rf"{browser_utils.get_coccoc_executable_path()}",
        "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Default" --disable-popup-blocking',
    }
    try:
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    except WebDriverException:
        close_win_app_driver_server_by_its_id(pid)
        browser_utils.kill_all_coccoc_process()
        time.sleep(2)
        pid = open_winappdriver_server()
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    else:
        return driver, pid


def open_winappdriver_server() -> int:
    """
    Start WinAppDriver server by using Pywinauto
    Returns: None
    """
    # Close current WinAppDriver if any
    close_win_app_driver_server()

    # Start new instance of WinAppDriver
    app = Application(backend="uia").start(
        rf"{browser_utils.get_winappdriver_executable_path()}",
        create_new_console=True,
        wait_for_idle=False,
        retry_interval=1,
    )
    return int(app.process)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if "session_date" not in config.stash:
        config.stash["session_date"] = datetime.now().strftime(
            "Report_at_%Y-%m-%d-%H-%M-%S"
        )

    [...]

    if config.option.collectonly == True:
        config.option.htmlpath = None

    else:
        [...]

        # Set run path
        run_path = config.rootpath.joinpath("reports", config.stash["session_date"])
        run_path.mkdir(parents=True, exist_ok=True)
        config.stash["run_path"] = run_path

        config.option.htmlpath = str(run_path / "report.html")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     outcome = yield
#     screen_file = ""
#     report = outcome.get_result()
#     extras = getattr(report, "extras", [])
#     if report.when == "call":
#         if report.failed and "page" in item.funcargs:
#             page: Page = item.funcargs["page"]
#             screenshot_dir = Path("screenshots")
#             screenshot_dir.mkdir(exist_ok=True)
#             screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
#             page.screenshot(path=screen_file, timeout=5000)
#         xfail = hasattr(report, "wasxfail")
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             # add the screenshots to the html report
#             extras.append(pytest_html.extras.png(screen_file))
#         report.extras = extras


@pytest.fixture()
def open_coccoc_pywinauto(
    language=setting.coccoc_language,
    sleep_n_seconds: int = 3,
    profile_name=None,
) -> Application:
    coccoc: Application = Application(backend="uia")
    try:
        if profile_name is None:
            coccoc.start(
                browser_utils.get_coccoc_executable_path() + f" --lang={language}",
                timeout=setting.timeout_pywinauto,
            )
        else:
            coccoc.start(
                browser_utils.get_coccoc_executable_path()
                + f' --lang={language} --profile-directory="{profile_name}"',
                timeout=setting.timeout_pywinauto,
            )
        time.sleep(sleep_n_seconds)
    except Exception as e:
        raise e
    else:
        yield coccoc
        coccoc.window().close()


@pytest.fixture()
def pw_wad(cc_win_app_driver, request):
    pw: Playwright = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    except Exception as e:
        raise e
    else:
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        yield page
        page.close()
        pw.stop()


@pytest.fixture()
def cc_win_app_driver(
    request, open_win_app_driver_server, language=setting.coccoc_language, port=4723
):
    pid = open_win_app_driver_server(port=port)
    driver: WebDriver = None
    desired_caps = {
        "app": rf"{browser_utils.get_coccoc_executable_path()}",
        # "app": "Browser", # CocCoc AppId
        "appArguments": rf'--lang={language} --remote-debugging-port=9222 --start-maximized --profile-directory="Default" --disable-popup-blocking',
    }
    try:
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    except WebDriverException:
        close_win_app_driver_server_by_its_id(pid)
        browser_utils.kill_all_coccoc_process()
        time.sleep(2)
        pid = open_win_app_driver_server(port=port)
        driver = appium_driver.Remote(
            command_executor=rf"http://127.0.0.1:{port}",
            desired_capabilities=desired_caps,
        )
    else:
        yield driver
        if driver is not None:
            driver.quit()
        close_win_app_driver_server_by_its_id(pid)


@pytest.fixture(autouse=True, scope="session")
def delete_reports_after_n_day(
    keep_reports_during_n_days: int = setting.keep_reports_during_n_days,
):
    """To keep the reports only for n recent days"""
    yield
    if keep_reports_during_n_days >= 1:
        today = date.today()
        exclude_dates = [str(today)]
        for i in range(keep_reports_during_n_days):
            exclude_dates.append(str(today - timedelta(days=i + 1)))
        file_utils.remove_old_reports(
            directory="reports", exclude_folder_names=exclude_dates
        )
    else:
        raise ValueError("keep_reports_during_n_days should >= 1")


@pytest.fixture(autouse=True, scope="session")
def remove_unused_builds():
    """Auto delete unused builds"""
    yield
    ftp_connection.delete_unused_build()  # Delete at download folder
    ftp_connection.delete_unused_build(
        directory="C:\\homeftp\\corom"
    )  # Delete at FTP local if any
