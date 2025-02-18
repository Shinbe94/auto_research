from time import sleep
import pytest
from selenium.webdriver.common.keys import Keys
from pytest_pytestrail import pytestrail
from src.pages.dialogs.pop_ups import Adblock, AdblockOnboarding
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.new_tab.new_tab_page import NewTabPageSel
from src.pages.settings.settings_adblock import SettingsAdblockSel
from src.pages.sidebar.sidebar import Sidebar
from src.pages.toolbar.toolbar import Toolbar
from tests import setting

list_site_test_ads_block_onboarding = [
    "youtube.com",
    "animevietsub.tv",
    "truyenfull.vn",
]


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214685")
@pytest.mark.EnableAdblockOnboarding
def test_when_enable_adblock_in_settings(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
):
    sleep(5)
    for url in list_site_test_ads_block_onboarding:
        toolbar.open_new_tab()
        toolbar.make_search_value(
            search_str=url,
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        if adblock_on_boarding.wait_for_onboarding_displays():
            break
    adblock_on_boarding.verify_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214688")
@pytest.mark.EnableAdblockOnboarding
def test_onboarding_ui_for_video(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
):
    sleep(5)
    toolbar.open_new_tab()
    toolbar.make_search_value(
        search_str="https://www.youtube.com/",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    assert adblock_on_boarding.wait_for_onboarding_displays()
    adblock_on_boarding.verify_video_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1252839")
@pytest.mark.EnableAdblockOnboarding
def test_onboarding_ui_for_comics(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
):
    sleep(5)
    toolbar.open_new_tab()
    toolbar.make_search_value(
        search_str="https://www.truyenfull.vn/",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    assert adblock_on_boarding.wait_for_onboarding_displays()
    adblock_on_boarding.verify_comics_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214691")
@pytest.mark.EnableAdblockOnboarding
def test_onboarding_only_show_1_time(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
):
    sleep(5)
    for url in list_site_test_ads_block_onboarding:
        toolbar.open_new_tab()
        toolbar.make_search_value(
            search_str=url,
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        if adblock_on_boarding.wait_for_onboarding_displays():
            break
    adblock_on_boarding.verify_ui()
    adblock_on_boarding.click_btn_i_understand()
    toolbar.click_reload_this_page_btn()
    adblock_on_boarding.verify_no_onboarding_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1252686")
@pytest.mark.EnableAdblockOnboarding
def test_onboarding_close_after_open_newtab(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
):
    sleep(5)
    for url in list_site_test_ads_block_onboarding:
        toolbar.open_new_tab()
        toolbar.make_search_value(
            search_str=url,
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        if adblock_on_boarding.wait_for_onboarding_displays():
            break
    toolbar.open_new_tab()
    toolbar.click_reload_this_page_btn()
    adblock_on_boarding.verify_no_onboarding_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1252689")
@pytest.mark.EnableAdblockOnboarding
def test_onboarding_does_not_close_while_playing_around_on_current_tab(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    toolbar: Toolbar,
    sidebar: Sidebar,
):
    sleep(5)
    for url in list_site_test_ads_block_onboarding:
        toolbar.open_new_tab()
        toolbar.make_search_value(
            search_str=url,
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        if adblock_on_boarding.wait_for_onboarding_displays():
            break
    # try to do stuff around the tab
    toolbar.click_you_btn()
    sidebar.click_sidebar_setting()
    toolbar.press_keyboard(Keys.ARROW_DOWN)
    adblock_on_boarding.verify_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1129700")
@pytest.mark.EnableAdblockOnboarding
def test_event_tracking_onboarding(
    uninstall_coccoc,
    install_coccoc,
    adblock_on_boarding: AdblockOnboarding,
    histograms: Histograms,
    toolbar: Toolbar,
):
    sleep(5)
    for url in list_site_test_ads_block_onboarding:
        toolbar.open_new_tab()
        toolbar.make_search_value(
            search_str=url,
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        if adblock_on_boarding.wait_for_onboarding_displays():
            break
    histograms.check_coccoc_adblock_metric(count=1)
    assert histograms.get_total_samples_of_metric_coccoc_adblock() == 1
