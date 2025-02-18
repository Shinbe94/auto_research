from time import sleep


from selenium.webdriver.common.by import By
from pytest_pytestrail import pytestrail
from src.pages.dialogs.dictionary import DictionarySel

from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.settings.settings_default_browser import close_inforbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45021")
def test_dictionary_blacken_word(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    sleep(2)
    close_inforbar()  # close infobar default browser if any
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')

    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.check_dict_tooltip_shown()
    dictionary_sel.click_dict_tooltips()
    dictionary_sel.check_dict_popup_shown()
    dictionary_sel.check_dict_popup_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45025")
def test_redirect_search_option(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    sleep(2)
    close_inforbar()  # close infobar default browser
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')

    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.click_dict_tooltips()
    dictionary_sel.click_btn_more(text="Encyclopedia")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1208189")
def test_display_of_tooltip(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    sleep(2)
    close_inforbar()  # close infobar default browser
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Encyclopedia")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Encyclopedia"]')

    extensions_page_sel.blacken_text2(TEXT_LOCATOR)
    dictionary_sel.check_dict_tooltip_shown()
    dictionary_sel.dummy_click()
    sleep(1)
    dictionary_sel.check_tooltip_is_hidden()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1208163")
def test_click_setting_icon(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')

    extensions_page_sel.double_click_element(TEXT_LOCATOR)
    dictionary_sel.click_btn_setting()
