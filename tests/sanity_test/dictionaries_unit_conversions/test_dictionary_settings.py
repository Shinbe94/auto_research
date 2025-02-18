from time import sleep
import pytest
from random import choice

from selenium.webdriver.common.by import By
from appium.webdriver.webdriver import WebDriver
from pywinauto import Application
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocSettingTitle


from src.pages.dialogs.dictionary import DictionarySel
from src.pages.dialogs.unit_converter import UnitConverterSel
from src.pages.internal_page.extensions.extension_detail_page import (
    ExtensionDetailPageSel,
)
from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.menus.context_menu import ContextMenu
from src.pages.settings.setting_about_coccoc import (
    SettingsAboutCocCocSel,
    click_relaunch_button_pywinauto,
)
from src.pages.settings.settings_default_browser import close_inforbar
from src.pages.support_pages.support_pages import W3SchoolSel, XeSel
from src.pages.installations import installation_page
from src.utilities import file_utils, os_utils
from tests import setting

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45021")
def test_setting_dictionary_is_on(
    extension_detail_page_sel: ExtensionDetailPageSel,
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser if any
    extension_detail_page_sel.turn_on_dictionary()
    try:
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')

        extensions_page_sel.blacken_text2(TEXT_LOCATOR)
        dictionary_sel.check_dict_tooltip_shown()
        dictionary_sel.click_dict_tooltips()
        dictionary_sel.check_dict_popup_shown()
        dictionary_sel.check_dict_popup_ui()
    finally:
        extension_detail_page_sel.turn_on_dictionary()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223772")
def test_setting_dictionary_is_off(
    extension_detail_page_sel: ExtensionDetailPageSel,
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser
    extension_detail_page_sel.turn_off_dictionary()
    try:
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
        extensions_page_sel.blacken_text2(TEXT_LOCATOR)
        dictionary_sel.check_dict_tooltip_never_shown_yet()
    finally:
        extension_detail_page_sel.turn_on_dictionary()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45026")
def test_default_status_dictionary(
    extension_detail_page_sel: ExtensionDetailPageSel,
    extensions_page_sel: ExtensionsPageSel,
):
    extensions_page_sel.open_extension_detail(
        extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
    )
    assert extension_detail_page_sel.extension_toggle_status() == "true"
    assert len(extension_detail_page_sel.get_extension_version()) > 0
    assert extension_detail_page_sel.get_allow_incognito_toggle_status() == "false"
    extension_detail_page_sel.open_dictionary_extention_options()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45027")
def test_layout_dictionary_options(
    extension_detail_page_sel: ExtensionDetailPageSel,
):
    extension_detail_page_sel.open_dictionary_extention_options_directly()
    extension_detail_page_sel.verify_ui_dictionary_options()
    extension_detail_page_sel.verify_status_dictionary_options()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502743")
@pytest.mark.open_incognito_window
def test_off_allow_dictionary_incognito(
    turning_off_allow_incognito_dictionary,
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.check_dict_tooltip_never_shown_yet()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223835")
@pytest.mark.open_incognito_window
def test_on_allow_dictionary_incognito(
    turning_on_allow_incognito_dictionary,
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.check_dict_tooltip_shown()
    dictionary_sel.click_dict_tooltips()
    dictionary_sel.check_dict_popup_shown()
    dictionary_sel.check_dict_popup_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502746")
def test_off_all_options(
    extensions_page_sel: ExtensionsPageSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
    context_menu: ContextMenu,
):
    close_inforbar()
    try:
        extension_detail_page_sel.check_disable_double_click_translate_to_vietnamese()
        extension_detail_page_sel.check_disable_show_tooltip()
        extension_detail_page_sel.check_disable_dictionary_text_area()
        extension_detail_page_sel.check_disable_unix_converter()

        # Double click word
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')
        extensions_page_sel.double_click_element(TEXT_LOCATOR)
        dictionary_sel.check_dict_popup_never_shown_yet()

        # Blacken word
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
        extensions_page_sel.blacken_text2(TEXT_LOCATOR)
        dictionary_sel.check_dict_tooltip_never_shown_yet()

        # right click on word then making search
        dictionary_sel.right_click_element(TEXT_LOCATOR)
        sleep(1)
        context_menu.translate_text(text="Encyclopedia")
        dictionary_sel.check_dict_popup_shown()
        dictionary_sel.check_dict_popup_ui()

    finally:
        extension_detail_page_sel.check_enable_double_click_translate_to_vietnamese()
        extension_detail_page_sel.check_enable_show_tooltip()
        extension_detail_page_sel.check_disable_dictionary_text_area()
        extension_detail_page_sel.check_enable_unix_converter()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502749")
def test_double_click_word_to_translate_to_vietnamese(
    extensions_page_sel: ExtensionsPageSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser if any
    try:
        # test disable double click a word to translate to vietnamese
        extension_detail_page_sel.check_disable_double_click_translate_to_vietnamese()
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')
        extensions_page_sel.double_click_element(TEXT_LOCATOR)
        dictionary_sel.check_dict_popup_never_shown_yet()

        # test enable double click a word to translate to vietnamese
        extension_detail_page_sel.check_enable_double_click_translate_to_vietnamese()
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')
        extensions_page_sel.double_click_element(TEXT_LOCATOR)
        dictionary_sel.check_dict_popup_shown()
        dictionary_sel.check_dict_popup_ui()
    finally:
        # To make sure this option is always ticked ON whether the test fails or passes
        extension_detail_page_sel.check_enable_double_click_translate_to_vietnamese()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502752")
def test_show_tooltip_while_blacken_text(
    extensions_page_sel: ExtensionsPageSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser if any
    try:
        # test disable show tooltip
        extension_detail_page_sel.check_disable_show_tooltip()
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
        extensions_page_sel.blacken_text2(TEXT_LOCATOR)
        dictionary_sel.check_dict_tooltip_never_shown_yet()

        # test enable show tooltip
        extension_detail_page_sel.check_enable_show_tooltip()
        extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
        TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')
        extensions_page_sel.blacken_text2(TEXT_LOCATOR)
        dictionary_sel.check_dict_tooltip_shown()
        dictionary_sel.click_dict_tooltips()
        dictionary_sel.check_dict_popup_shown()
        dictionary_sel.check_dict_popup_ui()
    finally:
        # To make sure this option is always ticked ON whether the test fails or passes
        extension_detail_page_sel.check_enable_show_tooltip()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502755")
def test_turning_on_off_translation_for_text_area(
    w3_school_sel: W3SchoolSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser if any
    try:
        extension_detail_page_sel.check_disable_dictionary_text_area()
        w3_school_sel.enter_text_in_textarea_then_double_click(text="hello")
        dictionary_sel.check_dict_tooltip_never_shown_yet()

        extension_detail_page_sel.check_enable_dictionary_text_area()
        w3_school_sel.enter_text_in_textarea_then_double_click(text="hello")
        dictionary_sel.check_dict_tooltip_shown()
        dictionary_sel.click_dict_tooltips()
        dictionary_sel.check_dict_popup_shown()
        dictionary_sel.check_dict_popup_ui()

    finally:
        extension_detail_page_sel.check_disable_dictionary_text_area()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223838")
def xtest_turning_on_off_translation_for_text_area_with_invalid_text(
    w3_school_sel: W3SchoolSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
):
    close_inforbar()  # close infobar default browser if any
    try:
        extension_detail_page_sel.check_enable_dictionary_text_area()
        w3_school_sel.enter_text_in_textarea_then_double_click(text="afhurewui")
        dictionary_sel.check_dict_tooltip_never_shown_yet()
        sleep(2)
        w3_school_sel.click_text_in_textarea()
        # dictionary_sel.click_dict_tooltips()
        # dictionary_sel.check_dict_popup_shown()
        # dictionary_sel.check_dict_popup_ui()

    finally:
        extension_detail_page_sel.check_disable_dictionary_text_area()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502740")
def test_setting_unit_exchange(
    unit_converter_sel: UnitConverterSel,
    xe_sel: XeSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
):
    close_inforbar()  # close infobar default browser if any
    try:
        # Disable unit exchange
        extension_detail_page_sel.check_disable_unix_converter()
        xe_sel.blacken_1_usd(is_open_xe_page=True)
        unit_converter_sel.check_unit_exchange_not_shown()

        # Enable unit exchange
        extension_detail_page_sel.check_enable_unix_converter()
        xe_sel.blacken_1_usd(is_open_xe_page=True)
        unit_converter_sel.check_exchange_1_usd()

    finally:
        extension_detail_page_sel.check_enable_unix_converter()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223787")
def test_dictionary_status_kept_off_after_restart_browser():
    coccoc_instance1 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver1: WebDriver = coccoc_instance1[0]
    coccoc_window1: Application = coccoc_instance1[1]
    coccoc_instance1_1: tuple = None
    driver1_1: WebDriver = None
    coccoc_window1_1: Application = None
    try:
        # OFF toggle
        eps1 = ExtensionsPageSel(driver1)
        eps1.turning_off_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        coccoc_window1.window().close()
        if driver1 is not None:
            driver1.quit()
        sleep(2)
        # Restart browser & Verify
        coccoc_instance1_1 = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
        )
        driver1_1 = coccoc_instance1_1[0]
        coccoc_window1_1 = coccoc_instance1_1[1]
        eps1_1 = ExtensionsPageSel(driver1_1)
        assert (
            eps1_1.get_extension_toggle_status(
                extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
            )
            == "false"
        )
    finally:
        coccoc_window1_1.window().close()
        if driver1_1 is not None:
            driver1_1.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223910")
def test_dictionary_status_kept_on_after_restart_browser():
    coccoc_instance2 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver2: WebDriver = coccoc_instance2[0]
    coccoc_window2: Application = coccoc_instance2[1]
    coccoc_instance2_1: tuple = None
    driver2_1: WebDriver = None
    coccoc_window2_1: Application = None
    try:
        # ON toggle
        eps2 = ExtensionsPageSel(driver2)
        eps2.turning_on_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        coccoc_window2.window().close()
        if driver2 is not None:
            driver2.quit()
        sleep(2)
        # Restart browser and verify
        coccoc_instance2_1 = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
        )
        driver2_1 = coccoc_instance2_1[0]
        coccoc_window2_1 = coccoc_instance2_1[1]
        eps2_1 = ExtensionsPageSel(driver2_1)
        assert (
            eps2_1.get_extension_toggle_status(
                extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
            )
            == "true"
        )
    finally:
        coccoc_window2_1.window().close()
        if driver2_1 is not None:
            driver2_1.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223790")
@pytest.mark.ignore_check_testing_build
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Stop testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_dictionary_status_kept_off_after_upgrade_browser(uninstall_coccoc):
    # Install old version
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language,
        build_name=setting.coccoc_build_name,
        version=choice(setting.old_coccoc_version),
    )

    coccoc_instance1 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver1: WebDriver = coccoc_instance1[0]
    eps1 = ExtensionsPageSel(driver1)
    eps2 = None
    saccs = SettingsAboutCocCocSel(driver1)
    coccoc_instance2: tuple = None
    driver2: WebDriver = None
    coccoc_window2: Application = None
    try:
        eps1.turning_off_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        # Adding host & restart 'Background intelligent tranfer service" for sure
        file_utils.rename_and_copy_file_host()
        os_utils.restart_background_intellignet_transfer()

        # Execute upgrade browser via About us, then click Relaunch button
        saccs.click_relaunch_btn(is_close_after_checking=False)
        open_browser.close_coccoc_by_window_title(
            title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
        )
        # Restart browser and checking
        coccoc_instance2 = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
        )
        driver2: WebDriver = coccoc_instance2[0]
        coccoc_window2 = coccoc_instance2[1]
        eps2 = ExtensionsPageSel(driver2)
        assert (
            eps2.get_extension_toggle_status(
                extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
            )
            == "false"
        )
    finally:
        file_utils.remove_and_revert_file_host()
        eps2.turning_on_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        coccoc_window2.window().close()
        if driver2 is not None:
            driver2.quit()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223907")
@pytest.mark.ignore_check_testing_build
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Stop testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_dictionary_status_kept_on_after_upgrade_browser(uninstall_coccoc):
    # Install old version
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language,
        build_name=setting.coccoc_build_name,
        version=choice(setting.old_coccoc_version),
    )

    coccoc_instance1 = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver1: WebDriver = coccoc_instance1[0]
    eps1 = ExtensionsPageSel(driver1)
    eps2 = None
    saccs = SettingsAboutCocCocSel(driver1)
    coccoc_instance2: tuple = None
    driver1: WebDriver = None
    coccoc_window2: Application = None
    try:
        eps1.turning_on_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        # Adding host & restart 'Background intelligent tranfer service" for sure
        file_utils.rename_and_copy_file_host()
        os_utils.restart_background_intellignet_transfer()

        # Execute upgrade browser via About us, then click Relaunch button
        saccs.click_relaunch_btn(is_close_after_checking=False)
        open_browser.close_coccoc_by_window_title(
            title=CocCocSettingTitle.ABOUT_COCCOC_TITLE
        )
        coccoc_instance2 = (
            open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
        )
        driver2: WebDriver = coccoc_instance2[0]
        coccoc_window2 = coccoc_instance2[1]
        eps2 = ExtensionsPageSel(driver2)
        assert (
            eps2.get_extension_toggle_status(
                extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
            )
            == "true"
        )
    finally:
        file_utils.remove_and_revert_file_host()
        eps2.turning_on_extension_toggle_status(
            extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
        )
        coccoc_window2.window().close()
        if driver2 is not None:
            driver2.quit()
