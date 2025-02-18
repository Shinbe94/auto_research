from pytest_pytestrail import pytestrail
from src.pages.dialogs.infobar_container import InfobarContainer
from src.pages.internal_page.bookmarks.bookmark_bar import BookmarkBar
from src.pages.settings.settings_appearance import SettingsAppearanceSel
from src.pages.support_pages.support_pages import ChromeStore
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508005")
def test_get_theme(
    chrome_store: ChromeStore,
    infobar_container: InfobarContainer,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        chrome_store.add_theme(
            url="https://chrome.google.com/webstore/detail/space-catboy/gmbjjjdjenobhcpmhbjaljalfmbjmkap?hl=en"
        )
        infobar_container.verify_theme_installed(theme_name="Space Catboy")
        assert settings_appearance_sel.get_theme_name() == "Space Catboy"
    finally:
        settings_appearance_sel.restore_default_theme()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508008")
def test_remove_theme(
    chrome_store: ChromeStore,
    infobar_container: InfobarContainer,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        chrome_store.add_theme(
            url="https://chrome.google.com/webstore/detail/space-catboy/gmbjjjdjenobhcpmhbjaljalfmbjmkap?hl=en"
        )
        infobar_container.verify_theme_installed(theme_name="Space Catboy")
        assert settings_appearance_sel.get_theme_name() == "Space Catboy"
    finally:
        settings_appearance_sel.restore_default_theme()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508011")
def test_setting_show_home_button(
    toolbar: Toolbar,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        settings_appearance_sel.toggle_on_show_home_button()
        toolbar.check_home_btn_appeared()
        toolbar.click_home_btn()
        assert toolbar.get_opening_url() is None
        assert toolbar.get_opening_url() != "coccoc://settings/appearance"
    finally:
        settings_appearance_sel.toggle_off_show_home_button()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508014")
def test_setting_show_home_button_with_specific_page(
    toolbar: Toolbar,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        settings_appearance_sel.enter_custom_web_address(url="https://google.com")
        toolbar.check_home_btn_appeared()
        toolbar.click_home_btn()
        assert toolbar.get_opening_url() in "https://www.google.com/"
    finally:
        settings_appearance_sel.clear_custom_web_address()
        settings_appearance_sel.toggle_off_show_home_button()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508017")
def test_hide_home_btn(
    toolbar: Toolbar,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        settings_appearance_sel.toggle_on_show_home_button()
        toolbar.check_home_btn_appeared()
        settings_appearance_sel.toggle_off_show_home_button()
        toolbar.check_home_btn_disappeared()
    finally:
        settings_appearance_sel.toggle_off_show_home_button()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508023")
def test_show_bookmark_bar(
    bookmark_bar: BookmarkBar,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        settings_appearance_sel.toggle_on_show_bookmark_bar()
        bookmark_bar.check_bookmar_bar_shown()
    finally:
        settings_appearance_sel.toggle_off_show_bookmark_bar()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508020")
def test_hide_bookmark_bar(
    bookmark_bar: BookmarkBar,
    settings_appearance_sel: SettingsAppearanceSel,
):
    try:
        settings_appearance_sel.toggle_off_show_bookmark_bar()
        bookmark_bar.check_bookmar_bar_hidden()
    finally:
        settings_appearance_sel.toggle_off_show_bookmark_bar()
