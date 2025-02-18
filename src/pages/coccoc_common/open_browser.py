import time
import win32gui
from playwright.sync_api import sync_playwright
from pywinauto import Application
from appium import webdriver as appium_driver
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from pywinauto.keyboard import send_keys
from pywinauto.findwindows import ElementAmbiguousError
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# from selenium.webdriver import webdriver
# Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src.pages.constant import CocCocTitles, ChromeTitles, TaskManagerText
from src.utilities import file_utils, os_utils, browser_utils
from tests import setting
from webdriver_manager.core.os_manager import ChromeType

# class ChromeType(object):
#     GOOGLE = "google-chrome"
#     CHROMIUM = "chromium"
#     BRAVE = "brave-browser"
#     MSEDGE = "edge"
#     COCCOC = "google-chrome"


def get_executable_path() -> str:
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        return setting.coccoc_binary_64bit
    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        return setting.coccoc_binary_32bit
    elif file_utils.check_file_is_exists(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
    ):
        return f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
    else:
        raise ValueError("No CocCoc installed")


def get_executable_path_debug() -> str:
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        return setting.coccoc_binary_64bit_debug
    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        return setting.coccoc_binary_32bit_debug
    elif file_utils.check_file_is_exists(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
    ):
        return f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe --remote-debugging-port=9222"
    else:
        raise ValueError("No CocCoc installed")


def get_chrome_executable_path():
    if file_utils.check_file_is_exists(setting.chrome_binary_64bit):
        return setting.chrome_binary_64bit
    elif file_utils.check_file_is_exists(setting.chrome_binary_32bit):
        return setting.chrome_binary_32bit
    else:
        raise ValueError("No Chrome installed")


def get_chome_default_profile() -> str:
    return f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"


def get_chrome_executable_path_debug():
    if file_utils.check_file_is_exists(setting.chrome_binary_64bit):
        return setting.chrome_binary_64bit_debug
    elif file_utils.check_file_is_exists(setting.chrome_binary_32bit):
        return setting.chrome_binary_32bit_debug
    else:
        raise ValueError("No Chrome installed")


def get_brave_executable_path():
    if file_utils.check_file_is_exists(setting.brave_binary_64bit):
        return setting.brave_binary_64bit
    elif file_utils.check_file_is_exists(setting.brave_binary_32bit):
        return setting.brave_binary_32bit
    else:
        raise ValueError("No Brave installed")


def open_coccoc_by_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=get_executable_path(),
            user_data_dir=setting.coccoc_default_profile,
            headless=False,
        )
        page = browser.new_page()
        return page


def open_coccoc_by_playwright_then_close_it():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=get_executable_path(),
            user_data_dir=setting.coccoc_default_profile,
            headless=True,
        )
        browser.close()
        # return page


def test_open_chrome_by_playwright():
    open_chrome_by_playwright()


def open_chrome_by_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            executable_path=get_chrome_executable_path(),
            user_data_dir=get_chome_default_profile(),
            headless=False,
        )
        page = browser.new_page()
        page.goto("chrome://downloads/")
        time.sleep(1)
        return page


def test_open_coccoc_by_selenium():
    driver = open_coccoc_by_selenium()
    driver.get("https://google.com")
    print(driver.title)
    time.sleep(2)
    driver.quit()


def open_coccoc_by_selenium(
    is_headless=False,
    language=setting.coccoc_language,
    is_enable_adblock=True,
    is_incognito=False,
) -> WebDriver:
    driver: WebDriver = None
    coccoc_options = ChromeOptions()
    if is_headless:
        coccoc_options.add_argument("--headless")
    coccoc_options.add_argument("--start-maximized")
    coccoc_options.add_argument(f"--lang={language}")
    if not is_enable_adblock:
        coccoc_options.add_argument("--disable-features=aCocCocAdblockPlus")
    if is_incognito:
        coccoc_options.add_argument("--incognito")
    coccoc_options.accept_insecure_certs = True
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    try:
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            options=coccoc_options,
        )
    except WebDriverException as e:
        raise e
    else:
        if driver is not None:
            return driver


def open_then_close_coccoc_headless_mode():
    driver = open_coccoc_by_selenium(is_headless=True)
    time.sleep(1)
    driver.quit()


def open_coccoc_by_pywinauto(
    language=setting.coccoc_language,
    sleep_n_seconds: int = 3,
    profile_name=None,
) -> Application:
    coccoc = Application(backend="uia")
    try:
        if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
            if profile_name is None:
                coccoc.start(
                    setting.coccoc_binary_64bit
                    + f" --lang={language} --start-maximized",
                    timeout=setting.timeout_pywinauto,
                )
            else:
                coccoc.start(
                    setting.coccoc_binary_64bit
                    + f' --lang={language} --profile-directory="{profile_name} --start-maximized"',
                    timeout=setting.timeout_pywinauto,
                )
            time.sleep(sleep_n_seconds)
        elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
            if profile_name is None:
                coccoc.start(
                    setting.coccoc_binary_32bit
                    + f" --lang={language} --start-maximized",
                    timeout=setting.timeout_pywinauto,
                )
            else:
                coccoc.start(
                    setting.coccoc_binary_32bit
                    + f' --lang={language} --profile-directory="{profile_name} --start-maximized"',
                    timeout=setting.timeout_pywinauto,
                )
            time.sleep(sleep_n_seconds)
        else:
            print("No CocCoc installed")
    finally:
        return coccoc


def open_coccoc_debug_by_pywinauto(
    language=setting.coccoc_language,
    profile_name="Default",
    is_tor=False,
    is_incognito=False,
    sleep_n_seconds: int = 1,
) -> Application:
    app: Application = None
    n: int = 0
    while n < 3:
        try:
            if is_tor:
                app: Application = Application(backend="uia").start(
                    get_executable_path_debug()
                    + f' --lang={language} --start-maximized --profile-directory="{profile_name}" --tor',
                    timeout=setting.timeout_pywinauto,
                )
            elif is_incognito:
                app: Application = Application(backend="uia").start(
                    get_executable_path_debug()
                    + f' --lang={language} --start-maximized --profile-directory="{profile_name}" --incognito',
                    timeout=setting.timeout_pywinauto,
                )
            else:
                app: Application = Application(backend="uia").start(
                    get_executable_path_debug()
                    + f' --lang={language} --start-maximized --profile-directory="{profile_name}"',
                    timeout=setting.timeout_pywinauto,
                )
            app.window().wait(
                "exists enabled visible ready",
                timeout=setting.timeout_pywinauto,
                retry_interval=1,
            )
            time.sleep(sleep_n_seconds)
        except Exception:
            n += 1
            browser_utils.kill_all_coccoc_process()
        else:
            if app:
                return app
            else:
                n += 1
                browser_utils.kill_all_coccoc_process()
                continue
        if n >= 3:
            raise ValueError(f"Error after retrying {n} times open coccoc")


def open_coccoc_by_pywinauto_then_close_it(
    language=setting.coccoc_language, is_first_time_opened=True, close_after_seconds=5
):
    title = None
    coccoc = Application(backend="uia")
    if is_first_time_opened:
        title = CocCocTitles.WELCOME_PAGE_TITLE
    else:
        title = CocCocTitles.NEW_TAB_TITLE
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        try:
            coccoc.start(
                setting.coccoc_binary_64bit + f" --lang={language} --start-maximized",
                timeout=setting.timeout_pywinauto,
            )
            time.sleep(close_after_seconds)
        finally:
            close_coccoc_by_window_title(title=title, language=language)

    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        try:
            coccoc.start(
                setting.coccoc_binary_32bit + f" --lang={language} --start-maximized",
                timeout=setting.timeout_pywinauto,
            )
            time.sleep(close_after_seconds)
        finally:
            close_coccoc_by_window_title(title=title, language=language)
    else:
        print("No CocCoc installed")
    time.sleep(2)


def close_coccoc_by_window_title(
    title: str,
    language=setting.coccoc_language,
    is_accept_closing_multiple_window=False,
    is_exact_name=False,
):
    if "en" in language:
        btn_yes = "Yes"
    else:
        btn_yes = "Có"

    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
            # found_index=0
        )
        app.window().set_focus().close()
        if is_accept_closing_multiple_window:
            if (
                app.window()
                .child_window(title=btn_yes, control_type=50000)
                .wait(
                    "visible",
                    timeout=3,
                    retry_interval=1,
                )
                .is_visible()
            ):
                app.window().child_window(title=btn_yes, control_type=50000).wait(
                    "visible",
                    timeout=3,
                    retry_interval=1,
                ).click()
        time.sleep(1)
    except ElementAmbiguousError:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
            found_index=0,
        )
        while app.window(found_index=0).exists():
            app.window(found_index=0).set_focus().close()
            time.sleep(1)


def test_close_coccoc_by_window_title():
    close_coccoc_by_window_title(title="Google - Cốc Cốc")


def connect_to_coccoc_by_playwright():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url="http://127.0.0.1:9222/")
        page_ = browser.new_page()
        page_.goto("coccoc://settings/defaultBrowser")


def test_connect_to_coccoc_by_pywinauto():
    connect_to_coccoc_by_pywinauto()


def connect_to_coccoc_by_pywinauto(
    title=None, language=setting.coccoc_language
) -> Application:
    app = None
    if title is None:
        if language == "en":
            title = CocCocTitles.NEW_TAB_TITLE_EN
        else:
            title = CocCocTitles.NEW_TAB_TITLE_VI
    else:
        title = title
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=title,
            timeout=setting.timeout_pywinauto,
        )
        app.window().wait(
            "exists enabled visible ready",
            timeout=setting.timeout_pywinauto,
            retry_interval=1,
        ).maximize()
    except Exception as the_exception:
        print(the_exception)
    finally:
        if app is not None:
            # app.window().print_control_identifiers()
            return app.window().set_focus()


def connect_to_coccoc_tor_by_pywinauto() -> Application:
    app = None
    title = CocCocTitles.TOR_WINDOW_TITLE
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
    except ElementAmbiguousError:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
            found_index=0,
        )
    finally:
        if app is not None:
            return app


def test_open_and_connect_coccoc_by_selenium():
    # driver = open_and_connect_coccoc_by_selenium()[0]
    driver = open_coccoc_by_selenium()
    driver.get("https://google.com")
    driver.quit()


def test_open_and_connect_coccoc_by_selenium():
    driver = open_and_connect_coccoc_by_selenium()[0]
    driver.get("https://google.com")
    time.sleep(3)


def open_and_connect_coccoc_by_selenium(
    language=setting.coccoc_language,
    timeout=setting.timeout_pywinauto,
):
    driver: WebDriver = None
    current_coccoc_language: str = None
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True

    coccoc_options.add_argument(
        rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data"
    )
    coccoc_options.add_argument("--profile-directory=Default")
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    coccoc_options.binary_location = browser_utils.get_coccoc_executable_path()
    app: Application = Application(backend="uia").start(
        browser_utils.get_coccoc_executable_path()
        + f" --lang={language} --remote-debugging-port=9222 --start-maximized",
        timeout=setting.timeout_pywinauto,
        retry_interval=4,
        # wait_for_idle=True,
    )
    app.window().wait(
        "exists enabled visible ready",
        timeout=timeout,
        retry_interval=1,
    )
    try:
        driver = webdriver.Chrome(
            executable_path=browser_utils.get_coccoc_driver_executable_path(),
            options=coccoc_options,
        )
    except Exception as e:
        raise e
    else:
        current_coccoc_language = driver.execute_script(
            "return window.navigator.userLanguage || window.navigator.language"
        )
        return driver, app, current_coccoc_language


def open_chrome_by_selenium(is_headless=False) -> WebDriver:
    driver: WebDriver = None
    chrome_options = ChromeOptions()
    # prefs = {'safebrowsing.enabled': 'false'}
    # Support for download
    prefs = {
        "download.default_directory": f"C:\\Users\\{os_utils.get_username()}\\Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    if is_headless:
        chrome_options.add_argument("--headless")
    chrome_options.accept_insecure_certs = True
    chrome_options.add_argument("--start-maximized")
    chrome_options.binary_location = get_chrome_executable_path()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    if driver is not None:
        return driver


def test_open_brave_by_selenium():
    open_brave_by_selenium()


def open_brave_by_selenium(is_headless=False) -> WebDriver:
    driver: WebDriver = None
    brave_options = ChromeOptions()
    # prefs = {'safebrowsing.enabled': 'false'}
    # chrome_options.add_experimental_option("prefs", prefs)
    if is_headless:
        brave_options.add_argument("--headless")
    brave_options.accept_insecure_certs = True
    brave_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--no-sandbox')
    brave_options.binary_location = get_brave_executable_path()
    driver = webdriver.Chrome(
        ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(),
        options=brave_options,
    )
    if driver is not None:
        return driver


def connect_to_opened_coccoc(title: str):
    coccoc = Application(backend="uia").connect(
        class_name="Chrome_WidgetWin_1",
        control_type=50033,
        title_re=title,
        timeout=setting.timeout_pywinauto,
    )
    return coccoc[title]


def test_open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium():
    coccoc_instance = open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    driver = coccoc_instance[0]
    window: Application = coccoc_instance[1]
    driver.get("https://google.com")
    driver.quit()
    window.window().close()


def open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
    profile_name="Default",
    is_tor=False,
    is_incognito=False,
    language=setting.coccoc_language,
):
    """
    This function opens coccoc debug by pywinauto then Selenium connect to it
    :param is_headless:
    :param timeout:
    :param is_tor:
    :return: Selenium CocCoc driver, Current Coccoc windows, and CocCoc language
    """
    driver: WebDriver = None
    current_coccoc_language: str = None
    n: int = 0
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True
    coccoc_options.add_argument(
        rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data"
    )
    coccoc_options.add_argument("--profile-directory=Default")
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    coccoc_options.set_capability(
        "goog:loggingPrefs", {"browser": "ALL"}  # old: loggingPrefs
    )
    coccoc_options.binary_location = get_executable_path()
    app: Application = open_coccoc_debug_by_pywinauto(
        language, profile_name, is_tor, is_incognito
    )
    while n < 3:
        try:
            driver = webdriver.Chrome(
                executable_path=browser_utils.get_coccoc_driver_executable_path(),
                options=coccoc_options,
            )

        except Exception:
            n += 1
            pass
        else:
            if driver:
                driver.switch_to.default_content()
                current_coccoc_language = driver.execute_script(
                    "return navigator.userLanguage || navigator.language"
                )
                return driver, app, current_coccoc_language
            else:
                n += 1
                continue
        if n >= 3:
            raise ValueError(f"Error after {n} times connect coccoc driver")


def close_coccoc_by_new_tab(language=setting.coccoc_language):
    app: Application = None
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=CocCocTitles.NEW_TAB_TITLE,
            timeout=setting.timeout_pywinauto,
        )
    except ElementAmbiguousError:
        close_coccoc_by_kill_process()
    else:
        app.window().wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).set_focus().close()
    time.sleep(1)


def close_coccoc_by_kill_process(sleep_n_seconds: int = 0):
    try:
        os_utils.kill_process_by_name("browser.exe")
    except Exception as e:
        raise e
    time.sleep(sleep_n_seconds)


def close_chrome_by_kill_process(sleep_n_seconds: int = 0):
    try:
        os_utils.kill_process_by_name("chrome.exe")
    except Exception as e:
        raise e
    time.sleep(sleep_n_seconds)


def connect_to_coccoc_by_title(title: str) -> Application:
    app: Application = None
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
    except Exception as e:
        raise e
    else:
        return app


def is_coccoc_window_appeared(
    title: str,
    timeout=setting.timeout,
    is_exact=True,
    interval_delay=1,
    control_type=50033,
) -> bool:
    is_appeared = False
    # interval_delay = 1
    total_delay = 0
    app = None
    while total_delay < timeout:
        try:
            if is_exact:
                app = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=control_type,
                    title=title,
                    timeout=1,
                )
            else:
                app = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=control_type,
                    title_re=title,
                    timeout=1,
                )
            if app is not None:
                is_appeared = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            print(
                f"Timeout for waiting the CocCoc window appear after {total_delay} seconds"
            )
            break
    return is_appeared


def is_coccoc_window_disappeared(title: str, timeout=6) -> bool:
    is_disappeared = False
    interval_delay = 1
    total_delay = 0

    while total_delay < timeout:
        try:
            Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title=title,
                timeout=3,
            )
        except Exception:
            is_disappeared = True
            break
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            print(
                rf"Timeout for waiting the CocCoc window disappear after {timeout} seconds"
            )
            break
    return is_disappeared


def restore_browser_window(title: str):
    try:
        app: Application = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=title,
            timeout=setting.timeout_pywinauto,
            visible_only=False,
        )
        app.window(found_index=0).restore().set_focus()
    except ElementAmbiguousError:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=title,
            timeout=setting.timeout_pywinauto,
            found_index=0,
        )
        app.window().wait(
            "exists enabled visible ready",
            timeout=setting.timeout_pywinauto,
            retry_interval=1,
        ).restore().set_focus()
    return app


def minimize_browser_window(title: str):
    try:
        app: Application = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title=title,
            timeout=setting.timeout_pywinauto,
            visible_only=False,
        )
        app.window().wait(
            "exists enabled visible ready",
            timeout=setting.timeout_pywinauto,
            retry_interval=1,
        ).set_focus()
        app.window().minimize()
    except Exception:
        pass


def is_coccoc_tor_window_appeared(
    title: str,
    timeout=setting.timeout_for_tor,
    interval_delay: int = 10,
    is_close_then=False,
) -> bool:
    """To check whether the Tor Windows shown or not by its title

    Args:
        title (str): the page title opening by TOR
        timeout (_type_, optional): timeout for waiting. Defaults to setting.time_out_for_tor.
        interval_delay (int, optional): Sleep interval before recheck. Defaults to 10.
        is_close_then (bool, optional): Close the window after found. Defaults to False.

    Returns:
        bool: _description_
    """
    is_appeared = False
    total_delay = 0
    app = None
    time.sleep(5)  # Sleep for Tor slow loading
    while total_delay < timeout:
        send_keys("{F5}")
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title=title,
                timeout=2,
            )
            if app is not None:
                is_appeared = True
                if is_close_then:
                    app.window(found_index=0).set_focus().close()
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay

    if total_delay >= timeout:
        print(rf"Timeout for waiting the CocCoc window appear after {timeout} seconds")
    return is_appeared


def find_window_handle(
    title: str, delay_time: int = 0, ignore_error: bool = True
) -> list:
    """To  find the window handler by its title,
    Args:
        title (str): _description_

    Raises:
        e: _description_

    Returns:
        list: _description_
    """
    handleList = []
    time.sleep(delay_time)

    def findit(hwnd, ctx):
        # check the title
        # "Initializing..., Cốc Cốc Installer"
        # win32gui.GetWindowText(hwnd) == "New Tab - Cốc Cốc"
        try:
            if win32gui.GetWindowText(hwnd) == title:
                handleList.append(hwnd)
        except Exception as e:
            if ignore_error:
                pass
            else:
                raise e

    win32gui.EnumWindows(findit, None)
    # print(handleList)
    return handleList


def test_find_window_handle():
    print(
        find_window_handle(
            title="sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion - Cốc Cốc"
        )
    )


def is_coccoc_torrent_notification_appears(timeout=6) -> bool:
    is_disappeared = False
    interval_delay = 0.1
    total_delay = 0

    while total_delay < timeout:
        try:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                timeout=3,
            )
            app.window(found_index=0).print_control_identifiers(filename="all.txt")
        except Exception:
            is_disappeared = True
            break
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            print(
                rf"Timeout for waiting the CocCoc window disappear after {timeout} seconds"
            )
            break
    return is_disappeared


def open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3(
    is_tor: bool = False, is_incognito: bool = False, profile_name: str = "Default"
):
    driver: WebDriver = None
    app: Application = None
    current_coccoc_language: str = ""
    coccoc_options = ChromeOptions()
    coccoc_options.accept_insecure_certs = True
    coccoc_options.add_argument(
        rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data"
    )
    coccoc_options.add_argument(f"--profile-directory={profile_name}")
    coccoc_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    coccoc_options.set_capability(
        "goog:loggingPrefs", {"browser": "ALL"}  # old: loggingPrefs
    )
    coccoc_options.binary_location = get_executable_path()
    n: int = 0

    while n < 3:
        if n == 3:
            raise ValueError(f"Error after retrying {n} times to connect coccoc driver")
        try:
            if is_tor:
                app = Application(backend="uia").start(
                    get_executable_path_debug() + " --tor --start-maximized",
                    timeout=setting.timeout_pywinauto,
                    retry_interval=1,
                )
            elif is_incognito:
                app = Application(backend="uia").start(
                    get_executable_path_debug() + " --incognito --start-maximized",
                    timeout=setting.timeout_pywinauto,
                    retry_interval=1,
                )
            else:
                app = Application(backend="uia").start(
                    get_executable_path_debug()
                    + " --disable-popup-blocking --start-maximized",
                    timeout=setting.timeout_pywinauto,
                    retry_interval=1,
                )

            app.window().wait(
                "exists enabled visible ready active",
                timeout=setting.timeout_pywinauto,
                retry_interval=1,
            )
            time.sleep(2)
        except Exception:
            n += 1
            close_coccoc_by_kill_process(sleep_n_seconds=2)
        else:
            try:
                driver = webdriver.Chrome(
                    executable_path=browser_utils.get_coccoc_driver_executable_path(),
                    options=coccoc_options,
                )  # Selenium 3
                time.sleep(2)
                if driver is not None:
                    n = 3
                    driver.switch_to.default_content()
                    current_coccoc_language = driver.execute_script(
                        "return navigator.userLanguage || navigator.language"
                    )
            except Exception:
                n += 1
                close_coccoc_by_kill_process(sleep_n_seconds=2)
        finally:
            if driver is not None:
                n = 3
                return driver, app, current_coccoc_language


# init coccoc driver Appium
def wad_coccoc_driver(sleep_n_seconds: int = 1):
    """This function support init CocCoc by Appium
    Args:
        sleep_n_seconds (int, optional): _description_. Defaults to 1.
    Returns:
        _type_: _description_
    """
    port = 4723

    def _open_win_app_driver_server(port: int = 4723):
        app = Application(backend="uia").start(
            f"{browser_utils.get_winappdriver_executable_path()} {port}",
            create_new_console=True,
            wait_for_idle=False,
            retry_interval=1,
        )
        # pywinauto.keyboard.send_keys(command)
        return int(app.process)  # type: ignore

    pid = _open_win_app_driver_server()
    desired_caps = {
        "app": rf"{browser_utils.get_coccoc_executable_path()}",
        "appArguments": f"--lang={setting.coccoc_language} --remote-debugging-port=9222 --start-maximized",
    }

    driver = appium_driver.Remote(
        command_executor=f"http://127.0.0.1:{port}", desired_capabilities=desired_caps
    )
    time.sleep(sleep_n_seconds)
    return driver, pid


def open_chrome() -> None:
    """Just to open chrome by Pywinauto"""
    Application(backend="uia").start(
        f"{get_chrome_executable_path_debug()} --start-maximized",
        timeout=setting.timeout_pywinauto,
        retry_interval=1,
    )


def open_chrome_by_pywinauto_then_connect_by_selenium():
    driver: WebDriver = None
    app: Application = None
    current_chrome_language: str = ""
    chrome_options = ChromeOptions()
    # chrome_options.accept_insecure_certs = True
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.set_capability(
        "goog:loggingPrefs", {"browser": "ALL"}  # old: loggingPrefs
    )
    chrome_options.binary_location = get_chrome_executable_path()
    n: int = 0

    while n < 3:
        if n == 3:
            raise ValueError(f"Error after retrying {n} times to connect coccoc driver")
        try:
            app = Application(backend="uia").start(
                f"{get_chrome_executable_path_debug()} --start-maximized",
                timeout=setting.timeout_pywinauto,
                retry_interval=1,
            )

            app.window().wait(
                "exists enabled visible ready active",
                timeout=setting.timeout_pywinauto,
                retry_interval=1,
            ).maximize()
            time.sleep(2)
        except Exception:
            n += 1
            close_chrome_by_kill_process(sleep_n_seconds=2)
        else:
            try:
                driver = webdriver.Chrome(
                    ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                    options=chrome_options,
                )  # Selenium 3
                time.sleep(2)
                if driver is not None:
                    n = 3
                    driver.switch_to.default_content()
                    current_chrome_language = driver.execute_script(
                        "return navigator.userLanguage || navigator.language"
                    )
            except Exception:
                n += 1
                close_chrome_by_kill_process(sleep_n_seconds=2)
        finally:
            if driver is not None:
                n = 3
                return driver, app, current_chrome_language


def verify_task_manager():
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50032,
            title=TaskManagerText.TASK_MANAGER_TITLE,
            timeout=setting.timeout_pywinauto,
            found_index=0,
        )

    except Exception as e:
        raise e
    else:
        # app.window(found_index=0).print_control_identifiers()
        assert (
            app.window(found_index=0)
            .child_window(title=TaskManagerText.TASK, control_type="Header")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
        )
        assert (
            app.window(found_index=0)
            .child_window(title=TaskManagerText.MEMORY_FOOTPRINT, control_type="Header")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
        )
        assert (
            app.window(found_index=0)
            .child_window(title=TaskManagerText.CPU, control_type="Header")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
        )
        assert (
            app.window(found_index=0)
            .child_window(title=TaskManagerText.PROCESS_ID, control_type="Header")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
        )
        assert (
            app.window(found_index=0)
            .child_window(title=TaskManagerText.BTN_END_PROCESS, control_type="Button")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
        )
    finally:
        app.window(found_index=0).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).close()


def open_url_from_coccoc_by_pywinauto(
    url: str = "https://google.com", language=setting.coccoc_language
):
    coccoc_window = open_coccoc_by_pywinauto(language)
    address_bar_and_search = None
    if language == "en":
        address_bar_and_search = (
            coccoc_window[CocCocTitles.NEW_TAB_TITLE_EN]
            .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
        )
        address_bar_and_search.type_keys(url)
        address_bar_and_search.type_keys("{ENTER}")
        time.sleep(1)
    else:
        address_bar_and_search = (
            coccoc_window[CocCocTitles.NEW_TAB_TITLE_VI]
            .child_window(title=CocCocTitles.ADDRESS_BAR, control_type="Edit")
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
        )
        # address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
        address_bar_and_search.type_keys(url)
        address_bar_and_search.type_keys("{ENTER}")
        time.sleep(1)
    return address_bar_and_search
