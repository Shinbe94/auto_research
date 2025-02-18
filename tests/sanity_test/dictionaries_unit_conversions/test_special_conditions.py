from time import sleep

from selenium.webdriver.common.by import By
from pytest_pytestrail import pytestrail
from src.pages.dialogs.dictionary import DictionarySel
from src.pages.internal_page.extensions.extension_detail_page import (
    ExtensionDetailPageSel,
)
from src.pages.internal_page.extensions.extension_devtools import (
    ExtensionDevtool,
)
from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.settings.settings_default_browser import close_inforbar
from src.pages.support_pages.support_pages import FacebookSel, XePlayright


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502773")
def test_dictionary_work_on_foreign_site(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    sleep(2)
    close_inforbar()  # close infobar default browser
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')

    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.check_dict_tooltip_shown()
    dictionary_sel.click_dict_tooltips()
    dictionary_sel.check_dict_popup_shown()
    dictionary_sel.check_dict_popup_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502776")
def test_dictionary_functions_are_disabled_for_credentials_input(
    extension_detail_page_sel: ExtensionDetailPageSel,
    dictionary_sel: DictionarySel,
    facebook_sel: FacebookSel,
):
    try:
        extension_detail_page_sel.check_enable_double_click_translate_to_vietnamese()
        extension_detail_page_sel.check_enable_show_tooltip()
        extension_detail_page_sel.check_enable_dictionary_text_area()
        extension_detail_page_sel.check_enable_unix_converter()

        # enter value to credentials then double click on them
        facebook_sel.double_click_username(text="hello", is_need_open_facebook=True)
        dictionary_sel.check_dict_popup_never_shown_yet()
        facebook_sel.double_click_password(text="world", is_need_open_facebook=False)
        dictionary_sel.check_dict_popup_never_shown_yet()

    finally:
        extension_detail_page_sel.check_enable_double_click_translate_to_vietnamese()
        extension_detail_page_sel.check_enable_show_tooltip()
        extension_detail_page_sel.check_disable_dictionary_text_area()
        extension_detail_page_sel.check_enable_unix_converter()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502779")
def test_metric_record_dictionary(
    extension_devtool: ExtensionDevtool,
):
    extension_devtool.open_extension_background(
        extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
    )
    sleep(2)
    extension_devtool.evaluate_js(
        r"""
        Object.keys(chrome.metricsPrivate).forEach(function(key) {
        var method = chrome.metricsPrivate[key];
        if (typeof method !== 'function' || key.indexOf('recordCustomData') !== 0) {
        return;
        }
        chrome.metricsPrivate['__' + key] = method;
        chrome.metricsPrivate[key] = function() {
            if (key === 'recordCustomData' && arguments[0] && arguments[0].length === 1) {
                console.info(
                    JSON.parse(arguments[0][0].value)
                );
                return;
            }
            console.info.bind(console, key).apply(console, arguments);
            return chrome.metricsPrivate['__' + key].apply(chrome.metricsPrivate, arguments);
            }
        });
        """
    )
    logs = extension_devtool.get_console_logs_as_text()
    new_page = extension_devtool.open_new_tab()
    new_page.goto(url="https://en.wikipedia.org/wiki/Organization")
    new_page.locator('//span[text()="Organization"]').dblclick()
    extension_devtool.page.wait_for_timeout(5_000)

    assert (
        "page_url: https://en.wikipedia.org/wiki/Organization, type: dictionary"
        in str(logs)
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502782")
def test_metric_record_exchange(
    extension_devtool: ExtensionDevtool,
):
    close_inforbar()
    extension_devtool.open_extension_background(
        extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
    )
    sleep(2)
    extension_devtool.evaluate_js(
        r"""
        Object.keys(chrome.metricsPrivate).forEach(function(key) {
        var method = chrome.metricsPrivate[key];
        if (typeof method !== 'function' || key.indexOf('recordCustomData') !== 0) {
        return;
        }
        chrome.metricsPrivate['__' + key] = method;
        chrome.metricsPrivate[key] = function() {
            if (key === 'recordCustomData' && arguments[0] && arguments[0].length === 1) {
                console.info(
                    JSON.parse(arguments[0][0].value)
                );
                return;
            }
            console.info.bind(console, key).apply(console, arguments);
            return chrome.metricsPrivate['__' + key].apply(chrome.metricsPrivate, arguments);
            }
        });
        """
    )
    logs = extension_devtool.get_console_logs_as_text()
    new_page = extension_devtool.open_new_tab()
    xe = XePlayright(new_page)
    xe.blacken_1_usd(
        url="https://www.xe.com/currencyconverter/convert/?Amount=100&From=USD&To=EUR"
    )
    extension_devtool.page.wait_for_timeout(5_000)
    assert (
        "page_url: https://www.xe.com/currencyconverter/convert/?Amount=100&From=USD&To=EUR, type: converter:currency}"
        in str(logs)
    )
