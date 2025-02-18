from time import sleep
from pytest_pytestrail import pytestrail
from src.pages.constant import CocCocTitles
from src.pages.dialogs.pop_ups import Adblock, SafeBrowsingTooltip
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.menus.context_menu import ContextMenu
from src.pages.new_tab.new_tab_page import NewTabPageSel
from src.pages.settings.settings_adblock import SettingsAdblockSel
from src.pages.support_pages.support_pages import (
    GooglePageSel,
    SafeBrowsingApp,
    SafeBrowsingSel,
)
from src.pages.toolbar.toolbar import Toolbar
from src.pages.topbar.top_bar import Topbar
from src.utilities.encode_decode import url_decode
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C550509")
def test_access_safe_site_directly(safe_browsing_sel: SafeBrowsingSel):
    safe_browsing_sel.check_no_domain_site_url_added_as_default()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C550512")
def test_landing_safe_browsing_when_report_site(
    google_page_sel: GooglePageSel,
    context_menu: ContextMenu,
    toolbar: Toolbar,
    safe_browsing_app: SafeBrowsingApp,
):
    google_page_sel.open_google_page()
    google_page_sel.right_click_google_page()
    context_menu.click_report_unsafe_content()
    assert "url=https://www.google.com" in url_decode(toolbar.get_opening_url())
    assert "google.com" in url_decode(safe_browsing_app.get_current_domain_site_url())


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C550536")
def test_validate_fields_before_submit_form(safe_browsing_sel: SafeBrowsingSel):
    safe_browsing_sel.verify_type_of_violations()
    safe_browsing_sel.select_all_options()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C550542")
def test_select_dropdown_options(safe_browsing_sel: SafeBrowsingSel):
    safe_browsing_sel.verify_error_when_submiting_with_no_input()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1152561")
def test_warning_tooltip_when_accessing_secure_page(
    new_tab_page_sel: NewTabPageSel,
    safe_browsing_tooltip: SafeBrowsingTooltip,
):
    new_tab_page_sel.open_page(url="https://kenh14.vn")
    safe_browsing_tooltip.verify_secure_page_ui()
    safe_browsing_tooltip.click_btn_connection_is_secure()
    safe_browsing_tooltip.verify_connection_is_secure_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1152570")
def test_warning_tooltip_when_accessing_unsecure_page(
    safe_browsing_tooltip: SafeBrowsingTooltip,
    toolbar: Toolbar,
):
    toolbar.make_search_value(
        search_str="https://2xzqux.xyz/ap/signin",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_page_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1152945")
def test_warning_tooltip_when_accessing_unsecure_and_unsafe_page(
    new_tab_page_sel: NewTabPageSel,
    safe_browsing_tooltip: SafeBrowsingTooltip,
):
    new_tab_page_sel.open_page(url="http://hotrotaichinh.wapath.com/thanhtoan")
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    safe_browsing_tooltip.click_X_btn_to_close_popup()
    safe_browsing_tooltip.click_warning()
    safe_browsing_tooltip.verify_unsecure_and_unsafe_page_ui_after_click_warning()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C550530")
def test_safe_browsing_when_turning_off_adblock_feature(
    settings_adblock_sel: SettingsAdblockSel,
    safe_browsing_tooltip: SafeBrowsingTooltip,
    toolbar: Toolbar,
):
    try:
        settings_adblock_sel.toggle_off_adblock()
        settings_adblock_sel.open_page(url="http://hotrotaichinh.wapath.com/thanhtoan")
        safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
        toolbar.check_adblock_icon_is_not_shown()
        safe_browsing_tooltip.click_X_btn_to_close_popup()
    finally:
        settings_adblock_sel.toggle_on_adblock()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494751")
def test_warning_status_when_switching_tabs(
    safe_browsing_tooltip: SafeBrowsingTooltip,
    top_bar: Topbar,
    toolbar: Toolbar,
):
    # Open 3 tabs with 3 sites
    toolbar.make_search_value(
        search_str="https://coccoc.com/", is_press_enter=True, sleep_n_seconds=5
    )
    toolbar.open_new_tab()
    toolbar.make_search_value(
        search_str="http://hdsaisonc.com/", is_press_enter=True, sleep_n_seconds=5
    )
    toolbar.open_new_tab()
    toolbar.make_search_value(
        search_str="http://hotrotaichinh.wapath.com/thanhtoan",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    # Switch and checking
    top_bar.switch_tab_by_its_name(
        tab_title="Trình duyệt Cốc Cốc | Trình duyệt web dành cho người Việt"
    )
    safe_browsing_tooltip.verify_secure_page_ui()

    top_bar.switch_tab_by_its_name(tab_title=r"hdsaisonc.com - Network error")
    safe_browsing_tooltip.verify_popup_unsecure_page_ui()

    top_bar.switch_tab_by_its_name(tab_title="XtGem.com - Not Found")
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()

    # Switching again and checking
    top_bar.switch_tab_by_its_name(
        tab_title="Trình duyệt Cốc Cốc | Trình duyệt web dành cho người Việt"
    )
    safe_browsing_tooltip.verify_secure_page_ui()

    top_bar.switch_tab_by_its_name(tab_title=r"hdsaisonc.com - Network error")
    safe_browsing_tooltip.verify_popup_unsecure_page_ui()

    top_bar.switch_tab_by_its_name(tab_title="XtGem.com - Not Found")
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1152573")
def test_warning_popup_when_accessing_unsafe_domain(
    safe_browsing_tooltip: SafeBrowsingTooltip,
    toolbar: Toolbar,
):
    toolbar.make_search_value(
        search_str="https://tafcak.com", is_press_enter=True, sleep_n_seconds=5
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1261106")
def test_warning_popup_when_switching_to_other_tab(
    safe_browsing_tooltip: SafeBrowsingTooltip, toolbar: Toolbar, top_bar: Topbar
):
    # Access unsecure page and verify popup shown
    toolbar.make_search_value(
        search_str="http://hotrotaichinh.wapath.com/thanhtoan",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()

    # Open new tab then verify popup hidden
    toolbar.open_new_tab()
    safe_browsing_tooltip.verify_no_popup_and_warning_text_of_unsecure_and_unsafe_show()

    # Click back to unsecure tab and check popup shown
    top_bar.switch_tab_by_its_name(tab_title="XtGem.com - Not Found")
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()

    # Switch to new tab and check popup hidden
    toolbar.open_new_tab()
    safe_browsing_tooltip.verify_no_popup_and_warning_text_of_unsecure_and_unsafe_show()

    # Click back to unsecure tab and check popup shown
    top_bar.switch_tab_by_its_name(tab_title="XtGem.com - Not Found")
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1261109")
def test_warning_popup_when_reload_the_page(
    safe_browsing_tooltip: SafeBrowsingTooltip, toolbar: Toolbar
):
    # Access unsecure page and verify popup shown
    toolbar.make_search_value(
        search_str="http://hotrotaichinh.wapath.com/thanhtoan",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    toolbar.click_reload_this_page_btn()
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    sleep(3)
    toolbar.click_reload_this_page_btn()
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1261112")
def test_warning_popup_close_after_clicking_x_btn(
    safe_browsing_tooltip: SafeBrowsingTooltip, toolbar: Toolbar
):
    # Access unsecure page and verify popup shown
    toolbar.make_search_value(
        search_str="http://hotrotaichinh.wapath.com/thanhtoan",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    safe_browsing_tooltip.click_X_btn_to_close_popup()
    safe_browsing_tooltip.verify_popup_warning_hidden()
    toolbar.click_reload_this_page_btn()
    safe_browsing_tooltip.verify_popup_warning_hidden()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1297880")
def test_warning_popup_close_after_clicking_got_it_btn(
    safe_browsing_tooltip: SafeBrowsingTooltip, toolbar: Toolbar
):
    # Access unsecure page and verify popup shown
    toolbar.make_search_value(
        search_str="http://hotrotaichinh.wapath.com/thanhtoan",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    safe_browsing_tooltip.click_btn_got_it()
    safe_browsing_tooltip.verify_popup_warning_hidden()
    toolbar.click_reload_this_page_btn()
    safe_browsing_tooltip.verify_popup_warning_hidden()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1261115")
def test_warning_popup_close_after_clicking_close_tab(
    safe_browsing_tooltip: SafeBrowsingTooltip, toolbar: Toolbar, top_bar: Topbar
):
    # Access unsecure page and verify popup shown
    toolbar.make_search_value(
        search_str="https://tafcak.com",
        is_press_enter=True,
        sleep_n_seconds=5,
    )
    safe_browsing_tooltip.verify_popup_unsecure_and_unsafe_page_ui()
    safe_browsing_tooltip.click_btn_close_tab()
    safe_browsing_tooltip.verify_popup_warning_hidden()
    top_bar.check_new_tab_opening()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1297565")
def test_histograms_data(get_safe_browsing_data, histograms: Histograms):
    assert (
        get_safe_browsing_data
        == histograms.get_value_of_domain_size_mean()
        + histograms.get_value_of_url_size_mean()
    )
