import time

from pytest_pytestrail import pytestrail

from src.pages.internal_page.histograms import histograms as histo
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.settings.settings_side_bar import SettingsSidebar
from src.pages.sidebar.sidebar import Sidebar
from src.pages.sidebar.sidebar_custom_icon_context_menu import (
    SidebarCustomIconContextMenu,
)
from src.pages.sidebar.sidebar_edit_custom_icon import SidebarEditCustomIcon
from src.pages.sidebar.sidebar_web_panel import SidebarWebPanel

from src.utilities import os_utils, network_utils, file_utils, read_write_data_by


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54340")
def test_metric_sidebar_activated(histograms: Histograms):
    histograms.check_sidebar_activated()


@pytestrail.case("C54341")
def test_only_1_metric_sidebar_activated_recorded(histograms: Histograms):
    # Open new coccoc window and check
    histo.open_new_history_window()
    # Back to first window and check
    histograms.check_sidebar_activated()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54342")
def test_metric_sidebar_enable_will_not_be_showed_for_initialization(
    histograms: Histograms,
):
    histograms.check_sidebar_enable_metric()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54343")
def test_metric_sidebar_enable_is_recorded(
    histograms: Histograms, settings_side_bar: SettingsSidebar
):
    histograms.check_sidebar_enable_metric()

    settings_side_bar.hide_sidebar(is_need_to_open_new_tab=True)
    histograms.check_sidebar_enable_metric(count=1)
    assert histograms.get_total_samples_of_metric_sidebar_enable() == 1

    settings_side_bar.show_sidebar(is_need_to_open_new_tab=True)
    histograms.open_histograms_page()
    assert histograms.get_total_samples_of_metric_sidebar_enable() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54344")
def test_metric_sidebar_show_is_recorded(
    histograms: Histograms, settings_side_bar: SettingsSidebar
):
    histograms.open_histograms_page()
    assert histograms.get_total_samples_of_metric_sidebar_show() == 1

    # Open new tab and check
    new_tab = histograms.open_new_tab()
    new_tab.goto("coccoc://histograms/")
    histograms.page.reload()
    assert histograms.get_total_samples_of_metric_sidebar_show() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54346")
def test_metric_sidebar_setting_open_clicked(histograms: Histograms, sidebar: Sidebar):
    # check default Sidebar.SidebarSettings.OpenClicks is not showed
    histograms.check_sidebar_metric_setting_open_clicked()

    # Click sidebar setting and check
    sidebar.click_sidebar_setting()
    histograms.check_sidebar_metric_setting_open_clicked(count=1)
    assert histograms.get_total_samples_of_metric_setting_open_clicked() == 1

    # click again and check
    sidebar.click_sidebar_setting()
    histograms.page.reload()
    assert histograms.get_total_samples_of_metric_setting_open_clicked() == 2

    # click again and check
    sidebar.click_sidebar_setting()
    histograms.page.reload()
    assert histograms.get_total_samples_of_metric_setting_open_clicked() == 3


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54347")
def test_metric_sidebar_feature_icon_will_not_be_shown_for_initialization(
    histograms: Histograms,
):
    histograms.check_sidebar_feature_icons_clicked()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54348")
def test_metric_sidebar_feature_icon_recorded_correctly(
    histograms: Histograms, settings_side_bar: SettingsSidebar, sidebar: Sidebar
):
    # check default Sidebar.FeatureIcons.Clicked is not showed
    histograms.check_sidebar_feature_icons_clicked()

    # click feature icon
    sidebar.click_history()
    histograms.check_sidebar_feature_icons_clicked(count=1)
    assert histograms.get_total_samples_of_metric_feature_icons_clicked() == 1

    # click again and check
    sidebar.click_facebook_messenger()
    histograms.page.reload()
    assert histograms.get_total_samples_of_metric_feature_icons_clicked() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54349")
def test_metric_sidebar_custom_icon_will_not_be_shown_for_initialization(
    histograms: Histograms,
):
    histograms.check_sidebar_custom_icons_clicked()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54350")
def test_metric_sidebar_custom_icon_recorded_correctly(
    histograms: Histograms, sidebar: Sidebar, sidebar_web_panel: SidebarWebPanel
):
    # check default Sidebar.FeatureIcons.Clicked is not showed
    histograms.check_sidebar_custom_icons_clicked()

    # click custom icon
    sidebar.click_youtube()
    histograms.check_sidebar_custom_icons_clicked(count=1)
    assert histograms.get_total_samples_of_metric_custom_icons_clicked() == 1
    sidebar_web_panel.click_hide()

    # click again and check
    sidebar.click_youtube()
    histograms.page.reload()
    assert histograms.get_total_samples_of_metric_custom_icons_clicked() == 2


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54351")
def test_metric_sidebar_paid_icon_will_not_be_shown_for_initialization(
    histograms: Histograms,
):
    histograms.check_sidebar_paid_icons_clicked()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54352")
def test_metric_sidebar_paid_icon_recorded_correctly(
    get_paid_icons_name, histograms: Histograms, sidebar: Sidebar
):
    # check default Sidebar.PaidIcons.Clicked is not showed
    histograms.check_sidebar_paid_icons_clicked()

    # click paid icons one by one
    sidebar.click_all_paid_icon(get_paid_icons_name)
    histograms.check_sidebar_paid_icons_clicked(count=1)
    assert histograms.get_total_samples_of_metric_paid_icons_clicked() == len(
        get_paid_icons_name
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C204229")
def test_metric_sidebar_edit_custom_icon_recorded_correctly(
    histograms: Histograms,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
    sidebar_edit_custom_icon: SidebarEditCustomIcon,
):
    # check default Sidebar.CustomIcons.EditIconWithOpenInWebPanelCheckboxChanged is not showed
    histograms.check_sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked()

    # click to edit custom icon
    sidebar.right_click_custom_icon_by_its_name(icon_name="Youtube")
    sidebar_custom_icon_context_menu.click_to_edit_custom_icon()
    sidebar_edit_custom_icon.tick_open_in_new_sidebar_window()
    sidebar_edit_custom_icon.click_btn_done()
    histograms.page.reload()
    histograms.check_sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked()
        == 1
    )

    # click to edit again and check

    sidebar.right_click_custom_icon_by_its_name(icon_name="Youtube")
    sidebar_custom_icon_context_menu.click_to_edit_custom_icon()
    sidebar_edit_custom_icon.tick_open_in_new_sidebar_window()
    sidebar_edit_custom_icon.click_btn_done()
    histograms.page.reload()
    histograms.check_sidebar_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked(
        count=1
    )
    assert (
        histograms.get_total_samples_of_metric_custom_icons_edit_icon_with_open_in_web_panel_checkbox_changed_clicked()
        == 2
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54353")
def test_all_metrics_data_will_be_reset_after_restarted(histograms: Histograms):
    histograms.check_sidebar_activated()
    histograms.open_histograms_page()
    assert histograms.get_total_samples_of_metric_sidebar_show() == 1
    histograms.check_sidebar_metric_setting_open_clicked()
    histograms.check_sidebar_feature_icons_clicked()
    histograms.check_sidebar_custom_icons_clicked()
    histograms.check_sidebar_paid_icons_clicked()
    histograms.check_sidebar_enable_metric()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C248782")
def xtest_metric_for_sidebar_settings_will_be_recorded(
    histograms, sidebar, sidebar_custom_icon_context_menu, sidebar_edit_custom_icon
):
    # TODO Should be implemented later after dev support locator
    # https://coccoc.atlassian.net/browse/BR-3604
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C468156")
def test_request_sent_when_click_paid_icon(
    get_paid_icons_name, histograms: Histograms, sidebar: Sidebar
):
    # Get browser vid
    vid = histograms.get_vid()
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump
        network_utils.dump_network_log(file_name="paid_icons.py")
        sidebar.click_all_paid_icon(get_paid_icons_name)

        # Wait for the request log sent and be captured!
        assert histo.wait_for_paid_icon_metric_is_sent()
        request_data = read_write_data_by.read_json_file(
            file_name="paid_icon_metrics_log"
        )
        assert vid in request_data.get("Cookie")
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\paid_icon_metrics_log.json"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1070788")
def test_metric_fetching_response_code(histograms: Histograms, sidebar: Sidebar):
    # Add custom icon valid URL
    sidebar.add_favourite_url(url="https://google.com")
    # Add custom icon invalid url (404 not found)
    time.sleep(2)
    sidebar.add_favourite_url(url="https://somewrongwentthing.com")
    histograms.open_histograms_page()
    metric_detail = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.CustomIcons.FetchingResponseCode'])"
    )
    assert "200" in metric_detail
    assert "404" in metric_detail


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1070836")
def test_metric_icon_read_result_ok(sidebar: Sidebar, histograms: Histograms):
    histograms.open_histograms_page()
    paid_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.PaidIcons.ReadResult'])"
    )
    assert "0  -O" in paid_icon
    custom_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.CustomIcons.ReadResult'])"
    )
    assert "0  -O" in custom_icon


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1185951")
def test_metric_icon_read_result_file_missing(
    delete_sidebar_icon_files: None, sidebar: Sidebar, histograms: Histograms
):
    histograms.open_histograms_page()
    paid_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.PaidIcons.ReadResult'])"
    )
    assert "1  -O" in paid_icon
    custom_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.CustomIcons.ReadResult'])"
    )
    assert "1  -O" in custom_icon


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1185957")
def test_metric_icon_read_result_parse_failed(
    open_coccoc_then_close_it: None,
    edit_sidebar_icons_files: None,
    sidebar: Sidebar,
    histograms: Histograms,
):
    # Open page
    histograms.open_histograms_page()
    paid_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.PaidIcons.ReadResult'])"
    )
    assert "3  -O" in paid_icon
    custom_icon = histograms.get_metric_details(
        locator_text="div:below(div[histogram-name='Sidebar.CustomIcons.ReadResult'])"
    )
    assert "3  -O" in custom_icon


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088959")
def test_metric_for_autocomplete_url(
    copy_sidebar_icon_files: None, sidebar: Sidebar, histograms: Histograms
):
    # As the search autocomplete from history, so we need to access the intended test site before test
    histograms.page.goto("https://www.youtube.com/")

    histograms.check_sidebar_add_web_panel_autocomplete_selected()
    histograms.check_sidebar_add_web_panel_autocomplete_matches()
    sidebar.add_custom_icon_by_searching_its_name(
        icon_name="Youtube", icon_url=r"https://www.youtube.com/"
    )
    histograms.open_histograms_page()
    histograms.check_sidebar_add_web_panel_autocomplete_selected(count=1)
    histograms.check_sidebar_add_web_panel_autocomplete_matches(count=1)
