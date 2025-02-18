from time import sleep, time
from random import choice
import pytest
from pytest_pytestrail import pytestrail
from playwright._impl._api_types import TimeoutError
from playwright._impl._api_types import Error
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocSettingTitle, CocCocTitles, TestingSiteTittles
from src.pages.incognito.incognito_page import IncognitoPageSel
from src.pages.menus.main_menu import MainMenu
from src.pages.new_tab.new_tab_page import NewTabPage
from src.pages.settings.settings_cookies import SettingsCookiesAppium
from src.pages.settings.settings_tor_options import (
    SettingsTorOptions,
    SettingsTorOptionsSel,
)
from src.pages.support_pages.support_pages import InfoByIp, InfoByIpSel

from src.pages.toolbar.toolbar import Toolbar
from src.pages.incognito.incognito_tor_page import IncognitoTorPage
from src.pages.unloaded_site.un_reach_site import UnReachSite
from src.utilities import (
    assistant_apps_utils,
    network_utils,
    os_utils,
    process_id_utils,
)
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128487")
@pytest.mark.open_tor_window
def test_tor_kill_its_process_id(new_tab_page: NewTabPage):
    new_tab_page.open_coccoc_homepage()
    os_utils.kill_process_by_name(pid_name="tor-client-win32.exe")
    new_tab_page.reload_page()
    assert process_id_utils.is_process_running(process_name="tor-client-win32.exe")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128490")
@pytest.mark.open_tor_window
def test_tor_open_site_while_network_is_off(new_tab_page: NewTabPage):
    # Open page
    new_tab_page.open_coccoc_homepage()
    try:
        # Disable network
        network_utils.block_network_by_interface(interface_name="Ethernet")
        network_utils.block_network_by_interface(interface_name="Wi-Fi")

        # Reload page
        try:
            new_tab_page.reload_page()
        # except Exception as e:
        #     assert isinstance(
        #         e, TimeoutError
        #     )  # Very time out after disconnect the networkd
        except Error:
            pass
            # print(type(e))
        else:
            assert True is False
    finally:
        # Enable network again
        network_utils.enable_network_by_interface(interface_name="Ethernet")
        network_utils.enable_network_by_interface(interface_name="Wi-Fi")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128505")
@pytest.mark.open_tor_window
def test_tor_ip_is_differ_from_normal_ip(
    info_by_ip: InfoByIp, info_by_ip_sel3: InfoByIpSel
):
    # Get IP by Tor Windows
    ip_tor = info_by_ip.get_my_ip_address()
    # Get IP by normal windows
    ip_normal = info_by_ip_sel3.get_my_ip_address()
    assert ip_normal != ip_tor


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128514")
@pytest.mark.open_tor_window
@pytest.mark.open_tor_window3
def test_tor_ip_is_differ_from_different_profile_coccoc(
    info_by_ip: InfoByIp,
    toolbar: Toolbar,
    info_by_ip_sel3: InfoByIpSel,
    toolbar3: Toolbar,
):
    # Bring Incognito to the right
    toolbar3.snap_selected_window_to_the_right_half_screen()

    # click to active then bring the Incognito with Tor to the left
    toolbar.click_address_and_search_bar()
    toolbar.snap_selected_window_to_the_left_half_screen()

    # Get IP by Tor Windows
    ip_tor_profile1 = info_by_ip.get_my_ip_address()
    # Get IP by normal windows
    ip_tor_profile2 = info_by_ip_sel3.get_my_ip_address()
    assert ip_tor_profile2 != ip_tor_profile1


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128523")
@pytest.mark.open_tor_window
def test_tor_ip_is_changed_after_each_10_mins(info_by_ip: InfoByIp):
    # Get first IP by Tor Windows
    ip_tor_first = info_by_ip.get_my_ip_address()
    sleep(700)  # sleep 10 mins
    # Reload and Get second IP by Tor Windows
    info_by_ip.reload_page()
    ip_tor_second = info_by_ip.get_my_ip_address()
    assert ip_tor_first != ip_tor_second


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128565")
@pytest.mark.open_tor_window
def test_open_onion_site_when_turn_on_tor(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    incognito_tor_page: IncognitoTorPage,
):
    incognito_tor_page.open_any_page(
        url="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/"
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128568")
def test_open_onion_site_when_turn_off_both_tor_and_redirect_option(
    turn_off_both_tor_and_redirect_onion_sites,
    toolbar: Toolbar,
    settings_tor_options: SettingsTorOptions,
):
    try:
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=False,
        )
        # Verify there is not Tor retry button
        assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is False
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215531")
def test_open_onion_site_when_turn_off_both_tor_and_redirect_option_cc_is_default(
    set_then_unset_coccoc_as_default_browser,
    turn_off_both_tor_and_redirect_onion_sites,
    settings_tor_options: SettingsTorOptions,
    wad_session: AppiumWebDriver,
):
    try:
        assistant_apps_utils.open_url_by_python(
            url="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            sleep_n_seconds=3,
        )
        # Attach the appium driver into the tor window
        session_driver: AppiumWebDriver = wad_session(
            title="sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion - Cốc Cốc",
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        tb = Toolbar(session_driver)
        assert tb.is_element_disappeared(tb.BTN_RETRY_WITH_TOR, timeout=5) is True
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128580")
def test_open_onion_site_when_turn_on_tor_and_turn_off_redirect_option(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    toolbar: Toolbar,
    settings_tor_options: SettingsTorOptions,
):
    try:
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=False,
        )
        # Verify there is not Tor retry button
        assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is True
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215534")
def test_open_onion_site_when_turn_on_tor_and_turn_off_redirect_option_cc_as_default(
    set_then_unset_coccoc_as_default_browser,
    turn_on_incognito_with_tor_and_turn_off_redirect,
    wad_session: AppiumWebDriver,
    settings_tor_options: SettingsTorOptions,
):
    try:
        assistant_apps_utils.open_url_by_python(
            url="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            sleep_n_seconds=3,
        )
        # Attach the appium driver into the tor window
        session_driver: AppiumWebDriver = wad_session(
            title="sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion - Cốc Cốc",
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        tb = Toolbar(session_driver)
        # Verify there is not Tor retry button
        assert tb.is_element_appeared(tb.BTN_RETRY_WITH_TOR, timeout=5) is True
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128589")
def test_open_onion_site_when_turn_on_both_tor_and_redirect_option(
    turn_on_both_tor_and_redirect_onion_sites,
    toolbar: Toolbar,
    settings_tor_options: SettingsTorOptions,
):
    try:
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=False,
        )
        # Verify there is not Tor windows open the page
        assert open_browser.is_coccoc_tor_window_appeared(
            title=TestingSiteTittles.ONION_SITE_SHARE_DOCUMENT_WINDOW_TITLE,
            interval_delay=20,
        )
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215537")
def test_open_onion_site_when_turn_on_both_tor_and_redirect_option_cc_as_default(
    set_then_unset_coccoc_as_default_browser,
    turn_on_both_tor_and_redirect_onion_sites,
    settings_tor_options: SettingsTorOptions,
):
    try:
        assistant_apps_utils.open_url_by_python(
            url="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            sleep_n_seconds=3,
        )
        assert open_browser.is_coccoc_tor_window_appeared(
            title=TestingSiteTittles.ONION_SITE_SHARE_DOCUMENT_WINDOW_TITLE,
            interval_delay=20,
            is_close_then=True,
        )
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128604")
def test_open_onion_site_when_turn_off_tor_and_turn_on_redirect_option(
    turn_off_incognito_with_tor_and_turn_on_redirect,
    toolbar: Toolbar,
    un_reach_site: UnReachSite,
    settings_tor_options: SettingsTorOptions,
):
    try:
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=False,
        )

        # Verify the site cant be reached and ther is no Tor retry button
        un_reach_site.check_there_is_a_type_in()
        assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is False
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1215540")
def test_open_onion_site_when_turn_off_tor_and_turn_on_redirect_option_cc_as_default(
    set_then_unset_coccoc_as_default_browser,
    turn_off_incognito_with_tor_and_turn_on_redirect,
    toolbar: Toolbar,
    un_reach_site: UnReachSite,
    settings_tor_options: SettingsTorOptions,
):
    try:
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=False,
        )

        # Verify the site cant be reached and ther is no Tor retry button
        un_reach_site.check_there_is_a_type_in()
        assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is False
    finally:
        # reset to default tor option from its settings
        settings_tor_options.turn_on_incognito_with_tor()
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128616")
# @pytest.mark.open_tor_window
def test_can_retry_error_site_with_tor(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    toolbar: Toolbar,
):
    # for site in setting.list_sites_for_tor:
    #     toolbar.make_search_to_unreached_site(
    #         search_str=site, is_press_enter=True, is_wait_for_retry_with_tor=True
    #     )
    #     assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is True
    #     sleep(3)
    toolbar.make_search_to_unreached_site(
        search_str="https://bbc.com",
        is_press_enter=True,
        is_wait_for_retry_with_tor=True,
    )
    assert toolbar.is_element_appeared(toolbar.BTN_RETRY_WITH_TOR) is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128619")
def test_can_retry_reload_onion_site_with_tor(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    settings_tor_options: SettingsTorOptions,
    toolbar: Toolbar,
):
    try:
        toolbar.open_new_tab()  # New tab for opening onion sites
        toolbar.make_search_to_unreached_site(
            search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
            is_press_enter=True,
            is_wait_for_retry_with_tor=True,
        )
        # Turn on automatically redirect for onion sites
        settings_tor_options.turn_on_automatically_redirect_dot_onion_sites()
        sleep(3)
        toolbar.click_retry_with_tor()
        assert open_browser.is_coccoc_tor_window_appeared(
            title="Share and accept documents securely - Cốc Cốc (Incognito)",
            interval_delay=15,
            is_close_then=True,
        )
    finally:
        settings_tor_options.turn_off_automatically_redirect_dot_onion_sites(
            is_need_to_access_tor_setting=False
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128622")
def test_click_learn_more_btn(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    toolbar: Toolbar,
):
    toolbar.make_search_to_unreached_site(
        search_str="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/",
        is_press_enter=True,
        is_wait_for_retry_with_tor=True,
    )
    # Click learn more button and check the opening url
    toolbar.click_tor_learn_more_btn()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128625")
@pytest.mark.open_tor_window
def test_reconnection_with_tor_for_this_site(
    turn_on_incognito_with_tor_and_turn_off_redirect,
    toolbar: Toolbar,
    main_menu: MainMenu,
):
    toolbar.make_search_value_with_tor_window(
        search_str="https://coccoc.com",
        is_press_enter=True,
        target_windows_title=CocCocTitles.COCCOC_HOMEPAGE_TITLE_TOR,
    )
    main_menu.open_new_tor_connection_for_this_site()
    assert open_browser.is_coccoc_tor_window_appeared(
        title=CocCocTitles.COCCOC_HOMEPAGE_TITLE_INCOGNITO_TOR, interval_delay=30
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128802")
@pytest.mark.open_tor_window
@pytest.mark.open_incognito_window2
def test_cookies_setting_applied_for_both_incognito_and_incognito_with_tor(
    incognito_tor_page: IncognitoTorPage,  # Incognito Tor
    incognito_page_sel2: IncognitoPageSel,  # Incognito
    wad_session: AppiumWebDriver,
):
    # Open normal coccoc then open setting cookies
    open_browser.open_coccoc_by_pywinauto(sleep_n_seconds=5)
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.NEW_TAB_TITLE, port=4729
    )
    tb = Toolbar(session_driver)
    tb.make_search_value(
        search_str="coccoc://settings/cookies", is_press_enter=True, sleep_n_seconds=1
    )
    sc = SettingsCookiesAppium(session_driver)
    try:
        # Tick allow all cookies
        sc.tick_ratio_allow_all_cookies()
        assert incognito_tor_page.get_cookies_toggle_status() == "false"
        assert (
            incognito_tor_page.get_cookies_toggle_status()
            == incognito_page_sel2.get_cookies_toggle_status()
        )

        # Tick block 3rd cookies in incognito
        sc.tick_ratio_block_3rd_cookies_in_incognito()
        assert incognito_tor_page.get_cookies_toggle_status() == "true"
        assert (
            incognito_tor_page.get_cookies_toggle_status()
            == incognito_page_sel2.get_cookies_toggle_status()
        )

        # Tick block 3rd cookies
        sc.tick_ratio_block_3rd_cookies()
        assert incognito_tor_page.is_cookies_toggle_enable() is False
        assert incognito_page_sel2.is_cookies_toggle_enable() is False

        # ticket block all cookies
        sc.tick_ratio_block_all_cookies()
        assert incognito_tor_page.is_cookies_toggle_enable() is False
        assert incognito_page_sel2.is_cookies_toggle_enable() is False
    finally:
        sc.tick_ratio_allow_all_cookies()
        session_driver.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128805")
@pytest.mark.open_tor_window
@pytest.mark.open_incognito_window2
def test_block_3rd_cookies_setting_are_same_bw_incognito_and_incognito_with_tor(
    toolbar: Toolbar,
    incognito_tor_page: IncognitoTorPage,  # Incognito Tor
    toolbar2: Toolbar,
    incognito_page_sel2: IncognitoPageSel,  # Incognito
):
    # Bring Incognito to the right
    toolbar2.snap_selected_window_to_the_right_half_screen()

    # click to active then bring the Incognito with Tor to the left
    toolbar.click_address_and_search_bar()
    toolbar.snap_selected_window_to_the_left_half_screen()

    # Doing interactions
    incognito_tor_page.toggle_off_block_cookies_from_3rd()
    assert incognito_page_sel2.get_cookies_toggle_status() == "false"

    incognito_tor_page.toggle_on_block_cookies_from_3rd()
    assert incognito_page_sel2.get_cookies_toggle_status() == "true"

    incognito_page_sel2.toggle_on_block_cookies_from_3rd()
    assert incognito_tor_page.get_cookies_toggle_status() == "true"

    incognito_page_sel2.toggle_off_block_cookies_from_3rd()
    assert incognito_tor_page.get_cookies_toggle_status() == "false"
