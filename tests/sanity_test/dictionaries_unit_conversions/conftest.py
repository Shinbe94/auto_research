from time import sleep
import pytest
from appium.webdriver.webdriver import WebDriver
from pywinauto import Application
from src.pages.coccoc_common import open_browser
from src.pages.internal_page.extensions.extension_detail_page import (
    ExtensionDetailPageSel,
)
from src.pages.settings.settings_default_browser import close_inforbar

from src.pages.installations import installation_utils, installation_page

installation = installation_page.InstallationPage()


@pytest.fixture()
def turning_off_allow_incognito_dictionary() -> None:
    cococ_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = cococ_instance[0]
    coccoc_window: Application = cococ_instance[1]
    close_inforbar()  # close infobar default browser if any
    try:
        etps = ExtensionDetailPageSel(driver)
        etps.turning_off_allow_incognito_mode()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()
        sleep(2)


@pytest.fixture()
def turning_on_allow_incognito_dictionary() -> None:
    cococ_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = cococ_instance[0]
    coccoc_window: Application = cococ_instance[1]
    close_inforbar()  # close infobar default browser if any
    etps = ExtensionDetailPageSel(driver)
    try:
        etps.turning_on_allow_incognito_mode()
    finally:
        coccoc_window.window().close()
        if driver is not None:
            driver.quit()
        sleep(2)
    yield
    cococ_instance2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver2: WebDriver = cococ_instance2[0]
    coccoc_window2: Application = cococ_instance2[1]
    etps2 = ExtensionDetailPageSel(driver2)

    try:
        etps2.turning_off_allow_incognito_mode()
    finally:
        coccoc_window2.window().close()
        if driver2 is not None:
            driver2.quit()


@pytest.fixture(autouse=False)
def uninstall_coccoc_dict():
    installation_utils.uninstall_coccoc_silently()
