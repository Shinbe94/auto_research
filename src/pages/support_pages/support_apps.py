from time import sleep
from appium import webdriver as appium_driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pywinauto import Application
from appium.webdriver import WebElement
from src.pages.base import BaseAppium
from src.utilities import os_utils
from tests import setting

lang = setting.coccoc_language


class UTorrent(BaseAppium):
    # Locators
    OPTIONS = (By.NAME, "Options")
    PREFERENCES = (By.NAME, "Preferences")
    GENERAL = (By.NAME, "General")
    BTN_CLOSE = (
        By.XPATH,
        '//Window[@ClassName="µTorrent4823DF041B09"]//TitleBar[@AutomationId="TitleBar"]/Button[@Name="Close"][@AutomationId="Close"]',
    )
    BTN_OK = (By.NAME, "OK")
    ASSOCIATE_WITH_TORRENT_FILES = (By.NAME, "Associate with torrent files")

    # Interaction methods
    @staticmethod
    def start_utorrent(sleep_n_seconds: int = 0) -> None:
        Application(backend="uia").start(
            rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\utorrent\uTorrent.exe",
            timeout=setting.timeout_pywinauto,
        )
        sleep(sleep_n_seconds)

    def click_options(self):
        self.click_element(self.OPTIONS)
        sleep(3)

    def click_preferences(self):
        try:
            self.click_element(self.PREFERENCES)
        except Exception:
            self.press_keyboard("p")

    def click_general(self):
        self.click_element(self.GENERAL)

    def click_btn_close(self):
        self.click_element(self.BTN_CLOSE)

    def click_associate_with_torrent_files(self) -> None:
        self.click_element(
            self.ASSOCIATE_WITH_TORRENT_FILES, is_wait_for_clickable=False
        )

    def click_btn_ok(self) -> None:
        self.click_element(self.BTN_OK)

    def set_utorrent_as_default(
        self, is_need_to_start_utorrent=True, is_kill_utorrent=True
    ) -> None:
        if is_need_to_start_utorrent:
            self.start_utorrent()
        self.click_options()
        self.click_preferences()
        self.click_general()
        self.click_associate_with_torrent_files()
        self.click_btn_ok()
        if is_kill_utorrent:
            self.click_btn_close()

    @staticmethod
    def kill_utorrent():
        os_utils.kill_process_by_name(pid_name="uTorrent.exe")


def start_utorrent(sleep_n_seconds: int = 0) -> None:
    Application(backend="uia").start(
        rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\utorrent\uTorrent.exe",
        timeout=setting.timeout_pywinauto,
    )
    sleep(sleep_n_seconds)


# init Utorrent driver
def utorrent_driver(sleep_n_seconds: int = 1):
    port = 4723

    def _open_win_app_driver_server(port: int = 4723):
        app = Application(backend="uia").start(
            rf"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe {port}",
            create_new_console=True,
            wait_for_idle=False,
            retry_interval=1,
        )
        # pywinauto.keyboard.send_keys(command)
        return int(app.process)  # type: ignore

    pid = _open_win_app_driver_server()
    desired_caps = {
        "app": rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\utorrent\uTorrent.exe",
    }

    driver = appium_driver.Remote(
        command_executor=rf"http://127.0.0.1:{port}", desired_capabilities=desired_caps
    )
    sleep(sleep_n_seconds)
    return driver, pid


def check_notepad_is_opening(
    window_name: str, timeout=setting.timeout_pywinauto
) -> bool:
    is_opening = False
    try:
        app = Application(backend="uia").connect(
            class_name="Notepad",
            control_type=50032,
            title=window_name,
            timeout=timeout,
            # found_index=0
        )
        if app.window().exists():
            is_opening = True
        app.window().close()
    finally:
        return is_opening
