from pytest_pytestrail import pytestrail

from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles
from src.pages.internal_page.extensions.extensions_page import ExtensionsPage
from src.pages.internal_page.flags import flags_page as fp
from src.pages.settings.settings_adblock import SettingsAdblock
from src.pages.settings.settings_search import SettingsSearch
from src.pages.support_pages.support_pages import GooglePage
from src.pages.toolbar import toolbar as tb
from src.pages.toolbar.toolbar import Toolbar

# ------------------------------------------------------------------------------------------------------------------
from tests import setting


@pytestrail.case("C502884")
def test_suggestion_provide_when_no_history_bookmark(
    uninstall_coccoc_for_polite_search: None,
    install_coccoc: None,
    settings_search: SettingsSearch,
    toolbar: Toolbar,
):
    toolbar.make_search_value(search_str=rf"mp3", is_press_enter=False)
    toolbar.check_search_value_element_is_displayed(search_str="mp3")
    toolbar.check_search_suggestion_is_displayed(search_str="mp3 zing")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502887")
def test_suggestion_provide_when_has_history(google_page: GooglePage, toolbar: Toolbar):
    url = "tinhte.vn"
    google_page.open_page(url=rf"https://{url}")
    toolbar.open_new_tab()
    google_page.page.close()
    toolbar.make_search_value(search_str=rf"tinhte", is_press_enter=False)
    list_from_omni = toolbar.get_list_item_from_omni_dropdown()
    for item in list_from_omni:
        assert "tinhte" in item
    assert len([x for x in list_from_omni if url in x]) >= 1


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502890")
def xtest_suggestion_provide_when_has_bookmark(
    google_page: GooglePage, toolbar: Toolbar, lang: str
):
    url = "tinhte.vn"
    google_page.open_page(url=rf"https://{url}")
    toolbar.open_new_tab()
    google_page.page.close()
    toolbar.make_search_value(search_str=rf"tinhte", is_press_enter=False)
    list_from_omni = toolbar.get_list_item_from_omni_dropdown()
    for item in list_from_omni:
        assert "tinhte" in item
    assert len([x for x in list_from_omni if url in x]) >= 1


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502893")
def test_suggestion_provide_for_some_internal_page(toolbar: Toolbar):
    # Todo: Should clear the history relate to coccoc before test
    toolbar.make_search_value(search_str=r"coccoc", is_press_enter=False)
    list_from_omni = toolbar.get_list_item_from_omni_dropdown2()
    assert "coccoc://coccoc-urls/" in list_from_omni
    assert "coccoc://flags/" in list_from_omni
    assert "coccoc://settings/" in list_from_omni
    assert "coccoc://version/" in list_from_omni


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502899")
def test_smart_suggestion_provide_for_some_vietnamese_tone(toolbar: Toolbar):
    list_search_str = ["kênh 14", "ngôi sao"]
    for text in list_search_str:
        toolbar.make_search_value(search_str=text, is_press_enter=False)
        list_from_omni = toolbar.get_list_item_from_omni_dropdown()
        for item in list_from_omni:
            assert text in item


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502908")
def test_disable_adblock_will_make_it_wont_show_at_toolbar(
    settings_adblock: SettingsAdblock, toolbar: Toolbar
):
    try:
        settings_adblock.turn_off_toggle_enable_adblock_status()

        toolbar.make_search_value(
            search_str="https://www.minhngoc.net.vn/",
            is_press_enter=True,
            sleep_n_seconds=5,
        )

        assert toolbar.is_element_appeared(toolbar.ADBLOCK_ICON) is False
    finally:
        settings_adblock.turn_on_toggle_enable_adblock_status()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1207038")
def test_disable_savior_will_make_it_wont_show_at_toolbar(
    extensions_page: ExtensionsPage, toolbar: Toolbar
):
    try:
        extensions_page.turn_off_savior()
        assert toolbar.is_button_download_video_and_audio_appeared() is False
    finally:
        extensions_page.turn_on_savior()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C644204")
def test_built_in_suggestion_button_from_some_special_search_keyword(
    toolbar: Toolbar, lang: str
):
    if "en" in lang:
        toolbar.make_search_value(search_str="manage passwords", is_press_enter=False)
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Manage passwords button, press Enter to view and manage your passwords in Cốc Cốc settings",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )

        toolbar.open_new_tab()
        toolbar.make_search_value(search_str="update browser", is_press_enter=False)
        # list_from_omni = toolbar.get_list_item_from_omni_dropdown()
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Update Cốc Cốc button, press Enter to update Cốc Cốc from your Cốc Cốc settings",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )

        toolbar.open_new_tab()
        toolbar.make_search_value(search_str="clear browser", is_press_enter=False)
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Clear browsing data button, press Enter to clear your browsing history, cookies, cache, and more in Cốc Cốc settings",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
    else:
        toolbar.make_search_value(search_str="quản lý mật", is_press_enter=False)
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Nút Quản lý mật khẩu, nhấn phím Enter để xem và quản lý các mật khẩu của bạn trong phần cài đặt của Cốc Cốc",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )

        toolbar.open_new_tab()
        toolbar.make_search_value(search_str="cập nhật cốc cốc", is_press_enter=False)
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Nút Cập nhật Cốc Cốc, nhấn phím Enter để cập nhật Cốc Cốc trong phần cài đặt của Cốc Cốc",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )

        toolbar.open_new_tab()
        toolbar.make_search_value(search_str="xóa dữ liệu duyệt", is_press_enter=False)
        coccoc_window = open_browser.connect_to_coccoc_by_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        coccoc_window.window().child_window(
            title="Nút Xóa dữ liệu duyệt web, nhấn phím Enter để xóa lịch sử duyệt web, cookie, bộ nhớ đệm và nhiều nội dung khác trong phần cài đặt của Cốc Cốc",
            control_type="ListItem",
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
