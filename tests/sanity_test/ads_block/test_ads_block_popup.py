from time import sleep
import pytest
from selenium.webdriver.common.by import By

from pytest_pytestrail import pytestrail
from src.pages.dialogs.pop_ups import Adblock
from src.pages.menus.context_menu import ContextMenu
from src.pages.new_tab.new_tab_page import NewTabPage, NewTabPageSel
from src.pages.settings.settings_adblock import SettingsAdblockSel
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import browser_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C85552")
def test_ads_block_after_fresh_install(
    uninstall_coccoc,
    install_coccoc,
    settings_adblock_sel: SettingsAdblockSel,
    toolbar: Toolbar,
):
    settings_adblock_sel.check_toggle_adblock_status_is_on_at_default()
    settings_adblock_sel.verify_adblock_default_ui()
    for url in setting.list_internal_sites:
        settings_adblock_sel.open_page(url=url)
        toolbar.check_adblock_icon_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C82300")
def test_ads_block_icon_shown(
    new_tab_page_sel: NewTabPageSel, toolbar: Toolbar, adblock: Adblock
):
    new_tab_page_sel.open_any_page(url="https://kenh14.vn/")
    toolbar.check_adblock_icon_shown()
    toolbar.click_adblock_icon()
    adblock.verify_adblock_popup_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C83202")
def test_settings_btn_work_well(toolbar: Toolbar, adblock: Adblock):
    toolbar.make_search_value(search_str="https://kenh14.vn/", is_press_enter=True)
    toolbar.click_adblock_icon()
    adblock.click_btn_settings()
    adblock.verify_adblock_setting_page_opening()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C88376")
def test_no_adblock_for_internal_sites(
    new_tab_page_sel: NewTabPageSel, toolbar: Toolbar
):
    for url in setting.list_internal_sites:
        new_tab_page_sel.open_any_page(url)
        toolbar.check_adblock_icon_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C88379")
def test_do_not_blocking_coccoc_ads(new_tab_page: NewTabPage, toolbar: Toolbar):
    new_tab_page.click_icon_ads()
    new_tab_page.click_list_newsfeed_ads()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C202927")
@pytest.mark.open_incognito_window
def test_adblock_function_well_on_incognito(
    new_tab_page_sel: NewTabPageSel, toolbar: Toolbar
):
    new_tab_page_sel.open_any_page(url="https://kenh14.vn/")
    toolbar.check_adblock_icon_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C542796")
def test_no_block_image_element(
    new_tab_page_sel: NewTabPageSel, context_menu: ContextMenu
):
    new_tab_page_sel.open_any_page(url="https://kenh14.vn/")
    FIRST_IMG = new_tab_page_sel.get_elements(
        (
            By.CSS_SELECTOR,
            'img[fetchpriority="high"]',
        )
    )[0]
    sleep(3)
    new_tab_page_sel.right_click_element_by_element(FIRST_IMG)
    assert context_menu.is_element_disappeared(context_menu.BLOCK_ELEMENT)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C542805")
def test_multiple_click_adblock_icon(
    new_tab_page_sel: NewTabPageSel, toolbar: Toolbar, adblock: Adblock
):
    new_tab_page_sel.open_any_page(url="https://kenh14.vn/")

    for _ in range(5):
        toolbar.click_adblock_icon()
        toolbar.check_adblock_icon_shown()
