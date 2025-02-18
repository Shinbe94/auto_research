from time import sleep

import pytest
from pywinauto.keyboard import send_keys

from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser
from src.pages.dialogs.pop_ups import OpenPickApplication, ReportIssue
from src.pages.internal_page.coccoc_url import CocCocURLSel
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.menus.main_menu import MainMenu
from src.pages.new_tab.new_tab_page import NewTabPage, NewTabPageSel
from src.pages.settings.setting_about_coccoc import SettingsAboutCocCocSel
from src.pages.settings.settings_system import SettingsSystemSel
from src.pages.sidebar.sidebar import Sidebar
from src.pages.toolbar.toolbar import Toolbar
from src.pages.topbar.top_bar import Topbar
from src.utilities import os_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508029")
def test_network_settings(settings_system_sel: SettingsSystemSel):
    settings_system_sel.open_computer_setting_proxy()
    os_utils.check_the_proxy_setting_show()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508035")
def test_task_manager(main_menu: MainMenu):
    main_menu.open_task_manager()
    open_browser.verify_task_manager()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508062")
def test_url_list(coccoc_url_sel: CocCocURLSel):
    coccoc_url_sel.check_cococ_scheme_correct()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1013650")
def test_remove_FTP_function(open_pick_application: OpenPickApplication):
    open_pick_application.verify_ui_ftp()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1070827")
def test_histogram_for_icon_services(
    copy_sidebar_icon_files, sidebar: Sidebar, histograms: Histograms
):
    histograms.check_sidebar_custom_icon_decode_image_time()
    histograms.check_sidebar_custom_icons_fetching_response_code()
    histograms.check_sidebar_custom_icon_fetching_time()
    sidebar.add_favourite_url(url="https://www.tinhte.vn")
    histograms.check_sidebar_custom_icon_decode_image_time(count=1)
    assert (
        histograms.get_total_samples_of_metric_sidebar_custom_icon_decode_image_time()
        == 1
    )
    histograms.check_sidebar_custom_icons_fetching_response_code(count=1)
    assert (
        histograms.get_total_samples_of_metric_custom_icons_fetching_response_code()
        == 1
    )
    histograms.check_sidebar_custom_icon_fetching_time(count=1)
    assert (
        histograms.get_total_samples_of_metric_sidebar_custom_icon_fetching_time() == 1
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1070830")
@pytest.mark.IPH_CocCocScrollToTop
def test_histogram_for_IPH(
    top_bar: Topbar,
    histograms: Histograms,
):
    histograms.page.keyboard.down("End")
    top_bar.click_new_tab_title()
    histograms.check_in_product_help_notify_event_ready_state(count=1)
    assert (
        histograms.get_total_samples_of_metric_in_product_help_notify_event_ready_state()
        == 1
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1063324")
def test_histogram_for_coccoc_newtab_search_action(
    new_tab_page: NewTabPage,
    histograms: Histograms,
):
    histograms.check_coccoc_newtab_search_action()
    new_tab_page.make_search(search_string="hello world!")
    sleep(3)
    histograms.check_coccoc_newtab_search_action(count=1)
    histograms.get_total_samples_of_metric_coccoc_newtab_search_action() == 1
    new_tab_page.make_search(search_string="hello automation!")
    sleep(3)
    histograms.check_coccoc_newtab_search_action(count=1)
    histograms.get_total_samples_of_metric_coccoc_newtab_search_action() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1129672")
def test_help_url_support_page(
    toolbar: Toolbar,
    main_menu: MainMenu,
    settings_about_coccoc_sel: SettingsAboutCocCocSel,
):
    settings_about_coccoc_sel.click_get_help_with_coccoc()
    assert toolbar.get_opening_url() in "https://support.coccoc.com/?ctx=settings"

    settings_about_coccoc_sel.open_page(url=setting.coccoc_homepage_newtab)
    main_menu.click_help_help_center()
    assert toolbar.get_opening_url() in "https://support.coccoc.com/?ctx=menu"

    send_keys("{F1}")
    assert toolbar.get_opening_url() in "https://support.coccoc.com/?ctx=keyboard"


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1164243")
def test_histogram_newtab_welcome_page(
    histograms: Histograms,
):
    sleep(2)
    histograms.open_page(url="https://coccoc.com/search")
    sleep(3)
    histograms.open_page(url="https://coccoc.com/welcome")

    # Verify for new tab
    histograms.check_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_first_contentful_paint()
        == 1
    )
    histograms.check_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_paint_timing_navigation_to_largest_contentful_paint()
        == 1
    )

    histograms.check_page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_remote_ntp_parse_timing_navigation_to_parse_start()
        == 1
    )

    # Verify for search
    histograms.check_page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_search_paint_timing_navigation_to_first_contentful_paint()
        == 1
    )
    histograms.check_page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_search_parse_timing_navigation_to_parse_start()
        == 1
    )

    # Verify others
    histograms.check_page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_others_paint_timing_navigation_to_first_contentful_paint()
        == 1
    )
    histograms.check_page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_page_load_clients_coccoc_others_parse_timing_navigation_to_parse_start()
        == 1
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1191153")
def test_api_open_report_an_issue(
    report_issue: ReportIssue, new_tab_page_sel: NewTabPageSel
):
    new_tab_page_sel.execute_js(
        js_command="ntp.apiHandle.newTabPage.openReportIssues()"
    )
    report_issue.check_report_issue_appeared_by_pywinauto()
