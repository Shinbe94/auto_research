import time

import pytest
from selenium.webdriver.common.by import By
from pywinauto import Application
from src.pages.coccoc_common import open_browser, interactions
from src.pages.settings import settings_default_browser
from src.pages.settings.settings_tor_options import SettingsTorOptionsSel
from src.utilities import network_utils, file_utils
from tests import setting


@pytest.fixture(autouse=False)
def turn_off_then_on_network():
    try:
        # Block the network
        network_utils.block_network_by_interface(interface_name="Ethernet")
        network_utils.block_network_by_interface(interface_name="Wi-Fi")
        yield
    finally:
        # Enable network again
        network_utils.enable_network_by_interface(interface_name="Ethernet")
        network_utils.enable_network_by_interface(interface_name="Wi-Fi")


@pytest.fixture(autouse=False)
def turn_off_network():
    # Block the network
    network_utils.block_network_by_interface(interface_name="Ethernet")
    network_utils.block_network_by_interface(interface_name="Wi-Fi")


@pytest.fixture(autouse=False)
def check_tor_connected_by_sel_after_disconnect_network():
    coccoc_tor = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
        is_tor=True
    )
    driver = coccoc_tor[0]
    window = coccoc_tor[1]
    try:
        wait_for_connected(driver)

        # Block the network
        network_utils.block_network_by_interface(interface_name="Ethernet")
        network_utils.block_network_by_interface(interface_name="Wi-Fi")

        # Check the TOR status is still connected( like Brave's behavior)
        wait_for_connected(driver)
    finally:
        driver.quit()
        window.window().set_focus().close()


def get_tor_connection_status(driver):
    status_locator = (By.CSS_SELECTOR, "#tor-connection-status-description")
    return interactions.get_text_from_element(driver, status_locator)


def wait_for_connected(
    driver, timeout=setting.timeout, language=setting.coccoc_language
) -> bool:
    is_connected = False
    interval_delay = 0.1
    total_delay = 0
    if "en" in language:
        verify_text: str = "Connected to Tor successfully"
    else:
        verify_text: str = "Kết nối với Tor thành công"
    while total_delay < timeout:
        try:
            if verify_text in get_tor_connection_status(driver):
                is_connected = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    return is_connected


@pytest.fixture(autouse=True)
def delete_download_files():
    """
    To delete file before and after test
    :return:
    """
    file_utils.delete_files_by_regress_name_downloads_folder(file_name="sample")
    yield
    file_utils.delete_files_by_regress_name_downloads_folder(file_name="sample")


@pytest.fixture(autouse=False)
def turn_on_incognito_with_tor_and_turn_off_redirect() -> None:
    """
        This fixture is for turning on Tor feature + off redirect by selenium + pywinauto
    Then close the coccoc instane
    """
    coccoc_intance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver = coccoc_intance[0]
    window: Application = coccoc_intance[1]
    try:
        sto = SettingsTorOptionsSel(driver)
        sto.turn_on_incognito_with_tor()
        sto.turn_off_automatically_redirect_dot_onion_sites()
    finally:
        driver.quit()
        window.window().set_focus().close()


@pytest.fixture(autouse=False)
def turn_off_both_tor_and_redirect_onion_sites() -> None:
    """
        This fixture is for turning off Tor feature + redirect by selenium + pywinauto
    Then close the coccoc instane
    """
    coccoc_intance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver = coccoc_intance[0]
    window: Application = coccoc_intance[1]
    try:
        sto = SettingsTorOptionsSel(driver)
        sto.turn_off_incognito_with_tor()
        sto.turn_off_automatically_redirect_dot_onion_sites()
    finally:
        driver.quit()
        window.window().set_focus().close()


@pytest.fixture(autouse=False)
def turn_on_both_tor_and_redirect_onion_sites() -> None:
    """
        This fixture is for turning on Tor feature + on redirect by selenium + pywinauto
    Then close the coccoc instane
    """
    coccoc_intance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver = coccoc_intance[0]
    window: Application = coccoc_intance[1]
    try:
        sto = SettingsTorOptionsSel(driver)
        sto.turn_on_incognito_with_tor()
        sto.turn_on_automatically_redirect_dot_onion_sites()
    finally:
        driver.quit()
        window.window().set_focus().close()


@pytest.fixture(autouse=False)
def turn_off_incognito_with_tor_and_turn_on_redirect() -> None:
    """
        This fixture is for turning off Tor feature + on redirect by selenium + pywinauto
    Then close the coccoc instane
    """
    coccoc_intance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver = coccoc_intance[0]
    window: Application = coccoc_intance[1]
    try:
        sto = SettingsTorOptionsSel(driver)
        sto.turn_off_incognito_with_tor()
        sto.turn_on_automatically_redirect_dot_onion_sites()
    finally:
        driver.quit()
        window.window().set_focus().close()


@pytest.fixture(autouse=False)
def reset_tor_option_to_default() -> None:
    """
        This fixture is for turning on Tor feature by selenium + pywinauto
    Then close the coccoc instane
    """
    yield
    coccoc_intance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
    )
    driver = coccoc_intance[0]
    window: Application = coccoc_intance[1]
    try:
        sto = SettingsTorOptionsSel(driver)
        sto.turn_on_incognito_with_tor()
        sto.turn_off_automatically_redirect_dot_onion_sites()
    finally:
        driver.quit()
        window.window().set_focus().close()


@pytest.fixture(autouse=False)
def set_then_unset_coccoc_as_default_browser() -> None:
    settings_default_browser.set_default_browser_from_setting_page2()
    yield
    # Set default browser to Chrome
    settings_default_browser.set_a_browser_to_default()
