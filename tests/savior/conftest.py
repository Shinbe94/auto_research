import pytest
from selenium.webdriver.chrome import webdriver
from tests import setting
from src.pages.coccoc_common.open_browser import get_executable_path
from src.utilities import os_utils

from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture
def savior_driver(request, is_headless=False, language=setting.coccoc_language):
    coccoc_options = ChromeOptions()
    if is_headless:
        coccoc_options.add_argument("--headless")
    coccoc_options.add_argument("--start-maximized")
    coccoc_options.add_argument(
        rf"user-data-dir=C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data"
    )
    coccoc_options.add_argument("--profile-directory=Default")
    # Disable the ERROR:device_event_log_impl.cc(214)]
    # By https://stackoverflow.com/questions/65080685/usb-usb-device-handle-win-cc1020-failed-to-read-descriptor-from-node-connectio
    coccoc_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    coccoc_options.add_argument(f"--lang={language}")

    # coccoc_options.accept_insecure_certs = True
    coccoc_options.binary_location = get_executable_path()
    # coccoc_service = ChromeService(ChromeDriverManager().install())
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=coccoc_options)
    request.cls.driver = driver
    yield driver
    driver.quit()


# @pytest.fixture
# def savior_
