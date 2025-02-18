import time

import pytest
from pytest_pytestrail import pytestrail
from src.pages.incognito.incognito_tor_page import IncognitoTorPage

# ------------------------------------------------------------------------------------------------------------------
from src.utilities import network_utils


@pytestrail.case("C1128496")
@pytest.mark.open_tor_window
def test_tor_connection_state_stability_speed(
    incognito_tor_page: IncognitoTorPage, lang: str
):
    assert incognito_tor_page.wait_for_connecting(language=lang) is True
    assert incognito_tor_page.wait_for_connected(language=lang) is True
    time.sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128499")
@pytest.mark.open_tor_window
def test_tor_connection_when_disconnect_the_network(
    turn_off_then_on_network: None, incognito_tor_page: IncognitoTorPage, lang: str
):
    incognito_tor_page.reload_page()
    assert incognito_tor_page.wait_for_connection_is_failed(language=lang) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128499")
@pytest.mark.open_tor_window
def test_tor_reconnect_when_network_up_again(
    turn_off_network: None, incognito_tor_page: IncognitoTorPage, lang: str
):
    try:
        assert incognito_tor_page.wait_for_connection_is_failed(language=lang) is True
    finally:
        # Enable network again
        network_utils.enable_network_by_interface(interface_name="Ethernet")
        network_utils.enable_network_by_interface(interface_name="Wi-Fi")
        assert incognito_tor_page.wait_for_connected(language=lang) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207047")
@pytest.mark.open_tor_window
def test_disconnect_network_during_tor_session(
    check_tor_connected_by_sel_after_disconnect_network: None,
    incognito_tor_page: IncognitoTorPage,
    lang: str,
):
    try:
        assert incognito_tor_page.wait_for_connection_is_failed(language=lang) is True
    finally:
        # Enable network again
        network_utils.enable_network_by_interface(interface_name="Ethernet")
        network_utils.enable_network_by_interface(interface_name="Wi-Fi")
        assert incognito_tor_page.wait_for_connected(language=lang) is True
