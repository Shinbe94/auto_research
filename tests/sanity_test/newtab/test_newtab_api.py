from time import sleep
from playwright.sync_api import expect
import pytest
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser
from src.pages.internal_page.flags.flags_page import FlagsPageSel
from src.pages.new_tab.new_tab_page import NewTabPage

from src.pages.sidebar.sidebar import Sidebar
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import windows_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C249301")
def test_get_age_verification(new_tab_page: NewTabPage):
    sleep(2)
    assert new_tab_page.evaluate_js(
        js_command="ntp.apiHandle.newTabPage.getAgeVerification()"
    ) in [0, 1, 2, 3]


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745262")
def test_set_age_verification(new_tab_page: NewTabPage):
    age_values = [0, 1, 2, 3]
    for i in age_values:
        new_tab_page.evaluate_js(
            js_command=f"ntp.apiHandle.newTabPage.setAgeVerification({i})"
        )
        sleep(2)
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.getAgeVerification()"
            )
            == i
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745265")
def test_get_token(new_tab_page: NewTabPage):
    try:
        token = new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.getToken()"
        )
        assert token is not None
        assert token != ""
        assert len(token) > 0
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745268")
def test_get_vid(new_tab_page: NewTabPage):
    try:
        vid = new_tab_page.evaluate_js(js_command="ntp.apiHandle.newTabPage.getVid()")
        assert vid is not None
        assert vid != ""
        assert len(vid) > 0
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745271")
def test_has_prefetch(new_tab_page: NewTabPage):
    try:
        has_prefetch = new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.hasPrefetch()"
        )
    except Exception as e:
        raise e
    else:
        assert has_prefetch is True


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C113455")
def test_set_pip(new_tab_page: NewTabPage, toolbar: Toolbar):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.setPIPProperties(400, 300, 'https://google.com.vn/', 30, false, false)"
        )
        sleep(2)
        toolbar.make_search_value(search_str="https://tinhte.vn", is_press_enter=True)
        # check PIP show and 30 seconds are set!

        assert open_browser.is_coccoc_window_appeared(
            title="Automatically close after 30 seconds",
            is_exact=True,
            timeout=3,
            interval_delay=0.1,
        )

        # check PIP window size is 400x300
        window_rect = windows_utils.get_window_size(
            window_name="Automatically close after"
        )
        assert window_rect[2] == 400
        assert window_rect[3] == 300
        # check PIP close after about 30 seconds
        sleep(35)
        assert (
            len(
                windows_utils.find_window_handle(
                    title="Automatically close after", is_exact_name=False
                )
            )
            == 0
        )
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745274")
def test_close_pip(new_tab_page: NewTabPage, toolbar: Toolbar):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.setPIPProperties(400, 300, 'https://google.com.vn/', 30, false, false)"
        )
        sleep(2)
        toolbar.make_search_value(search_str="https://tinhte.vn", is_press_enter=True)
        # check PIP show and 30 seconds are set!

        assert open_browser.is_coccoc_window_appeared(
            title="Automatically close after 30 seconds",
            is_exact=True,
            timeout=3,
            interval_delay=0.1,
        )

        # force close pip, should wrap inside the try/except to ignore an exception from Playwright
        try:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.closePIPPanel()"
            )
        except Exception:
            pass
        sleep(2)
        assert (
            len(
                windows_utils.find_window_handle(
                    title="Automatically close after", is_exact_name=False
                )
            )
            == 0
        )
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745277")
def test_set_audio_mute(new_tab_page: NewTabPage):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.setPIPProperties(400, 300, 'https://google.com.vn/', 30, false, false)"
        )
        new_tab_page.open_any_page(url="https://coccoc.com/webhp?type=2&show=17486613")
        expect(
            new_tab_page.page.frame_locator("#ntrb-vast").locator(
                "#container > div.muteButton.muted"
            )
        ).to_be_visible()
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745280")
def test_open_url_in_incognito_tab(new_tab_page: NewTabPage):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.openUrlInIncognitoTab('https://google.com')"
        )
        assert open_browser.is_coccoc_window_appeared(
            title="Google - Cốc Cốc (Incognito)", timeout=10, is_exact=True
        )
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745283")
def test_show_hide_sidebar(new_tab_page: NewTabPage, sidebar: Sidebar):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(true)"
        )
        sleep(1)
        sidebar.is_sidebar_shown()
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(false)"
        )
        sleep(2)
        sidebar.is_sidebar_hidden()
    finally:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(true)"
        )
        sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745286")
def test_goto_browser_settings(new_tab_page: NewTabPage, toolbar: Toolbar):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.goToBrowserSettings()"
        )
        sleep(5)
        assert toolbar.get_opening_url() == "coccoc://settings"
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745289")
def test_sidebar_status(new_tab_page: NewTabPage, toolbar: Toolbar):
    try:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(true)"
        )
        sleep(1)
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.isSidebarShown"
            )
            is True
        )
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(false)"
        )
        sleep(2)
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.isSidebarShown"
            )
            is False
        )
    finally:
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.showSidebar(true)"
        )
        sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1184802")
def test_switch_sidebar_positions(new_tab_page: NewTabPage, sidebar: Sidebar):
    # Get current sidebar position
    is_at_left: bool = new_tab_page.evaluate_js(
        js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
    )
    try:
        # Switch sidebar position
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
        )
        sleep(1)
        # Check after switching
        first_location: tuple = sidebar.get_element_location(
            sidebar.CONFIG_AND_CONTROL_SIDEBAR
        )
        # Switch sidebar position again
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
        )
        sleep(1)
        # Check after switching
        second_location: tuple = sidebar.get_element_location(
            sidebar.CONFIG_AND_CONTROL_SIDEBAR
        )
        assert first_location["y"] == second_location["y"]  # Check y-axis are same
        assert first_location["x"] != second_location["x"]  # Check x-axis must not same
    finally:
        current_position: bool = new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
        )
        if current_position is not is_at_left:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
            )
        sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1191144")
def test_get_sidebar_positions(new_tab_page: NewTabPage):
    # Get current sidebar position
    is_at_left: bool = new_tab_page.evaluate_js(
        js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
    )
    try:
        # Switch sidebar position to the Right if it is at the Left
        if is_at_left:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
            )
            sleep(1)
            # Check after switching
            assert (
                new_tab_page.evaluate_js(
                    js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
                )
                is False
            )

        # Switch sidebar position back
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
        )
        sleep(1)
        # Check after switching
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
            )
            is True
        )
    finally:
        # Make sure we always switch back to the Left
        current_position: bool = new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
        )
        if current_position is not True:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
            )
        sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220979")
def test_on_sidebar_position_changed(new_tab_page: NewTabPage):
    # Run the API to start listen sidebar position is changing?
    new_tab_page.evaluate_js(
        js_command="ntp.apiHandle.newTabPage.onSidebarPositionChanged = (a) => {console.log(a)}"
    )

    # Get current sidebar position
    is_at_left: bool = new_tab_page.evaluate_js(
        js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
    )

    try:
        # Start listen log
        # logs = new_tab_page.get_console_logs_text()
        logs = new_tab_page.get_console_logs_as_text()
        # Switch sidebar position to the Right if it is at the Left
        if is_at_left:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
            )
            sleep(1)
            # Check after switching
            assert (
                new_tab_page.evaluate_js(
                    js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
                )
                is False
            )
        # Switch sidebar position back
        new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
        )
        sleep(1)
        # Check after switching
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
            )
            is True
        )
        assert ["false", "true"] == logs
    finally:
        # Make sure we always switch back to the Left
        current_position: bool = new_tab_page.evaluate_js(
            js_command="ntp.apiHandle.newTabPage.isSidebarOnTheLeft"
        )
        if current_position is not True:
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.switchPositionSidebar()"
            )
        sleep(1)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220982")
def test_is_sidebar_coccoc_ai_feature_enable(
    enable_coccoc_ai_feature, new_tab_page: NewTabPage, flags_page_sel: FlagsPageSel
):
    try:
        # Check api after Enable coccoc ai sidebar
        assert (
            new_tab_page.evaluate_js(
                js_command="ntp.apiHandle.newTabPage.isSidebarCoccocAiFeatureEnabled"
            )
            is True
        )
    finally:
        # Change Coccoc AI sidebar back to default
        flags_page_sel.change_flag_status(flag_id="coccoc-sidebar-ai", status="Default")
