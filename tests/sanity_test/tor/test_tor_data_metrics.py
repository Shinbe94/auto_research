import time
import pytest
from pytest_pytestrail import pytestrail
from src.pages.constant import CocCocTitles, TestingSiteTittles


from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.menus.main_menu import MainMenu
from src.pages.toolbar.toolbar import Toolbar
from src.pages.incognito.incognito_tor_page import IncognitoTorPage
from src.pages.unloaded_site.un_reach_site import UnReachSite

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207899")
# @pytest.mark.open_tor_window
def test_metric_open_new_tor_window_not_be_shown(histograms: Histograms):
    histograms.check_metric_open_new_tor_window()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207863")
# @pytest.mark.open_tor_window
def test_metric_open_new_tor_window_be_shown(
    main_menu: MainMenu,
    histograms: Histograms,
):
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()
    histograms.check_metric_open_new_tor_window(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207905")
def test_metric_open_new_tor_window_be_counted_correctly(
    toolbar: Toolbar,
    main_menu: MainMenu,
    histograms: Histograms,
):
    # Open first Tor window
    main_menu.open_new_tor_window_from_normal_window()
    time.sleep(5)
    # Bring the first tor window to the right
    main_menu.snap_selected_window_to_the_right_half_screen()
    # set active the normal window and open the 2nd tor window
    toolbar.click_address_and_search_bar()
    main_menu.open_new_tor_window_from_normal_window()
    # Verify data
    histograms.check_metric_open_new_tor_window(count=1)
    assert histograms.get_total_samples_of_metric_open_new_tor_window() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207911")
def test_metric_new_tor_connection_for_this_site_will_not_be_shown(
    histograms: Histograms,
):
    histograms.check_metric_new_tor_connection_for_this_site()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207881")
def test_metric_new_tor_connection_for_this_site_will_be_shown(
    main_menu: MainMenu,
    histograms: Histograms,
    toolbar: Toolbar,
    wad_session: AppiumWebDriver,
):
    # Open first tor window and stick it to the right of screen
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()

    # click to active the normal window then open the 2nd tor window
    toolbar.click_address_and_search_bar()

    # Attaching the current TOR window into new Winappdriver instance
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.TOR_WINDOW_TITLE, port=4729
    )
    try:
        # Click new tor connection for this site
        mm = MainMenu(session_driver)
        mm.open_coccoc_menu_tor()
        # session_driver.find_element(*main_menu.COCCOC_MENU_TOR).click()
        time.sleep(2)
        session_driver.find_element(*main_menu.NEW_TOR_CONNECTION_FOR_THIS_SITE).click()
    finally:
        session_driver.quit()
    histograms.check_metric_new_tor_connection_for_this_site(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207914")
def test_metric_new_tor_connection_for_this_site_will_be_counted_correctly(
    main_menu: MainMenu,
    histograms: Histograms,
    toolbar: Toolbar,
    wad_session: AppiumWebDriver,
):
    # Open first tor window and stick it to the right of screen
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()

    # click to active the normal window then open the 2nd tor window
    toolbar.click_address_and_search_bar()

    # Attaching the current TOR window into new Winappdriver instance
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.TOR_WINDOW_TITLE, port=4729
    )
    try:
        # Click new tor connection for this site
        session_driver.find_element(*main_menu.COCCOC_MENU_TOR).click()
        time.sleep(2)
        session_driver.find_element(*main_menu.NEW_TOR_CONNECTION_FOR_THIS_SITE).click()
        time.sleep(2)

        # Click new tor connection for this site again
        session_driver.find_element(*main_menu.COCCOC_MENU_TOR).click()
        time.sleep(2)
        session_driver.find_element(*main_menu.NEW_TOR_CONNECTION_FOR_THIS_SITE).click()
        time.sleep(2)
    finally:
        session_driver.quit()

    # verifying
    histograms.check_metric_new_tor_connection_for_this_site(count=1)
    assert (
        histograms.get_total_samples_of_metric_new_tor_connection_for_this_site() == 2
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207917")
def test_metric_new_tor_window_count_will_not_show(
    histograms: Histograms,
):
    histograms.check_metric_new_tor_window_count()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207920")
def test_metric_new_tor_window_count_will_be_record(
    main_menu: MainMenu,
    histograms: Histograms,
):
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()
    histograms.check_metric_new_tor_window_count(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207923")
def test_metric_new_tor_window_count_will_be_inscreased_1_unit(
    main_menu: MainMenu,
    toolbar: Toolbar,
    histograms: Histograms,
    wad_session: AppiumWebDriver,
):
    # Open first tor window and stick it to the right of screen
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()
    # click to active the normal window then open the 2nd tor window
    toolbar.click_address_and_search_bar()

    # Attaching the current TOR window into new Winappdriver instance
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.TOR_WINDOW_TITLE, port=4729
    )
    try:
        session_driver.find_element(*main_menu.COCCOC_MENU_TOR).click()
        session_driver.find_element(*main_menu.NEW_TOR_WINDOW).click()
    finally:
        session_driver.quit()

    # Verifying
    histograms.check_metric_new_tor_window_count(count=1)
    assert histograms.get_total_samples_of_metric_tor_window_count() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207926")
def test_metric_tor_error_page_retry_with_tor_will_not_show(
    histograms: Histograms,
):
    histograms.check_metric_tor_error_page_retry_with_tor()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207929")
def test_metric_tor_error_page_retry_with_tor_will_be_recorded(
    toolbar: Toolbar, un_reach_site: UnReachSite, histograms: Histograms
):
    toolbar.make_search_to_unreached_site(
        search_str="http://bbc.com/",
        is_press_enter=True,
        is_wait_for_retry_with_tor=True,
    )
    un_reach_site.click_btn_retry_with_tor()

    un_reach_site.check_new_tor_window_opened(
        window_name=TestingSiteTittles.BBC_INCOGNITO_COCCOC_WINDOW_TITLE
    )

    histograms.check_metric_tor_error_page_retry_with_tor(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207932")
def test_metric_tor_error_page_retry_with_tor_will_be_inscreased_1_unit(
    toolbar: Toolbar,
    un_reach_site: UnReachSite,
    histograms: Histograms,
    main_menu: MainMenu,
    wad_session: AppiumWebDriver,
):
    toolbar.make_search_value_with_tor_window(
        search_str="http://bbc.com/",
        is_press_enter=True,
        target_windows_title=TestingSiteTittles.UNLOADED_BBC_INCOGNITO_COCCOC_WINDOW_TITLE,
    )

    # click button retry with tor
    un_reach_site.click_btn_retry_with_tor()
    un_reach_site.check_new_tor_window_opened(
        window_name=TestingSiteTittles.BBC_INCOGNITO_COCCOC_WINDOW_TITLE
    )
    session_driver: AppiumWebDriver = wad_session(
        title=TestingSiteTittles.BBC_COCCOC_WINDOW_TITLE, port=4729
    )
    try:
        session_driver.find_element(*main_menu.COCCOC_BBC_HOME_PAGE_MENU_TOR).send_keys(
            Keys.ALT + Keys.F4
        )  # close the current tor window
    finally:
        session_driver.quit()

    # click button retry with tor again
    un_reach_site.click_btn_retry_with_tor()

    # un_reach_site.check_new_tor_window_opened(
    #     window_name=TestingSiteTittles.BBC_INCOGNITO_COCCOC_WINDOW_TITLE
    # )
    histograms.check_metric_tor_error_page_retry_with_tor(count=1)
    assert histograms.get_total_samples_of_metric_tor_error_page_retry_with_tor() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207935")
def test_metric_tor_tab_count_will_not_show(
    histograms: Histograms,
):
    histograms.check_metric_tor_tab_count()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207938")
def test_metric_tor_tab_count_will_be_recorded(
    main_menu: MainMenu,
    histograms: Histograms,
):
    main_menu.open_new_tor_window_from_normal_window()
    histograms.check_metric_tor_tab_count(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207941")
def test_metric_tor_tab_count_will_be_inscreased_1_unit(
    main_menu: MainMenu,
    toolbar: Toolbar,
    histograms: Histograms,
    wad_session: AppiumWebDriver,
):
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.TOR_WINDOW_TITLE, port=4729
    )
    try:
        session_driver.find_element(*toolbar.BTN_NEW_TAB).click()
    finally:
        session_driver.quit()
    histograms.check_metric_tor_tab_count(count=1)
    assert histograms.get_total_samples_of_metric_tor_tab_count() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207944")
def test_metric_tor_open_link_with_tor_will_not_show(
    histograms: Histograms,
):
    histograms.check_metric_tor_open_link_with_tor()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207947")
def test_metric_tor_open_link_with_tor_will_be_recorded(
    toolbar: Toolbar,
    histograms: Histograms,
):
    toolbar.right_click_coccoc_logo()
    toolbar.open_link_incognito_window_with_tor()
    histograms.check_metric_tor_open_link_with_tor(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207950")
def test_metric_tor_open_link_with_tor_will_be_inscreased_1_unit(
    toolbar: Toolbar,
    main_menu: MainMenu,
    histograms: Histograms,
    un_reach_site: UnReachSite,
    wad_session: AppiumWebDriver,
):
    toolbar.right_click_coccoc_logo()
    toolbar.open_link_incognito_window_with_tor()

    # Doing quick check while the page is still not loaded
    un_reach_site.check_new_tor_window_opened(
        window_name=CocCocTitles.UNTITLED_INCOGNITO_COCCOC
    )
    # attaching the session into the new tor windows just opened then close the tor window
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.UNTITLED_COCCOC, port=4729
    )
    try:
        session_driver.find_element(*main_menu.COCCOC_UNTITLE_PAGE_MENU_TOR).send_keys(
            Keys.ALT + Keys.F4
        )  # close the current tor window
    finally:
        session_driver.quit()

    # Start open hyperlink by new tor window again
    toolbar.right_click_coccoc_logo()
    toolbar.open_link_incognito_window_with_tor()

    # Verifying
    histograms.check_metric_tor_open_link_with_tor(count=1)
    assert histograms.get_total_samples_of_metric_open_link_with_tor() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207953")
def test_metric_tor_show_retry_with_tor_button_will_not_show(
    histograms: Histograms,
):
    histograms.check_metric_show_retry_with_tor_button()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207956")
def test_metric_show_retry_with_tor_button_will_be_recorded(
    toolbar: Toolbar, histograms: Histograms, un_reach_site: UnReachSite
):
    toolbar.make_search_to_unreached_site(
        search_str="http://bbc.com/", is_press_enter=True
    )
    un_reach_site.is_retry_with_tor_btn_show()
    histograms.check_metric_show_retry_with_tor_button(count=1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207959")
def test_metric_show_retry_with_tor_button_will_be_increased_1_unit(
    toolbar: Toolbar, histograms: Histograms, un_reach_site: UnReachSite
):
    # Access the unreaching site then wait for retry button appears
    toolbar.make_search_to_unreached_site(
        search_str="http://bbc.com/", is_press_enter=True
    )
    un_reach_site.is_retry_with_tor_btn_show()
    histograms.check_metric_show_retry_with_tor_button(count=1)

    # access the unreaching site again and wait for retry button appears again
    toolbar.make_search_to_unreached_site(
        search_str="http://bbc.com/ ", is_press_enter=True
    )
    un_reach_site.is_retry_with_tor_btn_show()

    # Verifying
    histograms.check_metric_show_retry_with_tor_button(count=1)
    assert histograms.get_total_samples_of_metric_show_retry_with_tor_button() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207962")
def test_all_metrics_reset(histograms: Histograms):
    histograms.check_metric_open_new_tor_window()
    histograms.check_metric_new_tor_connection_for_this_site()
    histograms.check_metric_new_tor_window_count()
    histograms.check_metric_tor_error_page_retry_with_tor()
    histograms.check_metric_tor_tab_count()
    histograms.check_metric_tor_open_link_with_tor()
    histograms.check_metric_show_retry_with_tor_button()
