from pytest_pytestrail import pytestrail
from src.pages.dialogs.pop_ups import Adblock
from src.pages.new_tab.new_tab_page import NewTabPageSel
from src.pages.settings.settings_adblock import SettingsAdblockSel
from src.pages.toolbar.toolbar import Toolbar
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C82303")
def test_when_enable_adblock_in_settings(
    settings_adblock_sel: SettingsAdblockSel,
    toolbar: Toolbar,
):
    settings_adblock_sel.toggle_on_adblock()
    settings_adblock_sel.verify_adblock_default_ui()
    for url in setting.list_sites_for_adblock_testing:
        settings_adblock_sel.open_page(url=url)
        toolbar.check_adblock_icon_shown()
        toolbar.click_adblock_icon()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C542808")
def test_when_disable_adblock_in_settings(
    settings_adblock_sel: SettingsAdblockSel,
    toolbar: Toolbar,
):
    try:
        settings_adblock_sel.toggle_off_adblock()
        settings_adblock_sel.verify_adblock_default_ui()
        for url in setting.list_sites_for_adblock_testing:
            settings_adblock_sel.open_page(url=url)
            toolbar.check_adblock_icon_is_not_shown()
    finally:
        settings_adblock_sel.toggle_on_adblock()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1214637")
def test_remove_sites_from_allow_ads_settings(
    new_tab_page_sel: NewTabPageSel,
    settings_adblock_sel: SettingsAdblockSel,
    toolbar: Toolbar,
    adblock: Adblock,
):
    for url in setting.list_sites_for_adblock_testing:
        new_tab_page_sel.open_page(url)
        toolbar.click_adblock_icon()
        adblock.toggle_off_for_this_site()
    try:
        list_added_site = settings_adblock_sel.get_list_white_list()
        for url in setting.list_sites_for_adblock_testing:
            assert url.replace("https://", "").replace("www.", "") in list_added_site
    finally:
        settings_adblock_sel.remove_all_white_sites()
