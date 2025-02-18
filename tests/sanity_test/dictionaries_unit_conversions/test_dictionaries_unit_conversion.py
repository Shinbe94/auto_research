from time import sleep


from selenium.webdriver.common.by import By
from pytest_pytestrail import pytestrail
from src.pages.dialogs.dictionary import DictionarySel
from src.pages.dialogs.unit_converter import UnitConverterSel
from src.pages.internal_page.extensions.extension_detail_page import (
    ExtensionDetailPageSel,
)

from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.settings.settings_default_browser import close_inforbar
from src.pages.support_pages.support_pages import (
    W3SchoolSel,
    XeSel,
)
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502731")
def test_permissions(
    extensions_page_sel: ExtensionsPageSel,
    extension_detail_page_sel: ExtensionDetailPageSel,
    lang,
):
    extensions_page_sel.open_extension_detail(
        extension_id="gfgbmghkdjckppeomloefmbphdfmokgd"
    )
    list_permisions = extension_detail_page_sel.get_list_permissions_ele()
    assert len(list_permisions) == 1  # Check only 1 permission
    if "en" in lang:
        assert list_permisions[0].text == "Read your browsing history"
    else:
        assert list_permisions[0].text == "Đọc nhật ký duyệt web của bạn"


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C750865")
def test_enable_dictionary_inside_the_textarea(
    w3_school_sel: W3SchoolSel,
    dictionary_sel: DictionarySel,
    extension_detail_page_sel: ExtensionDetailPageSel,
):
    extension_detail_page_sel.check_enable_dictionary_text_area()
    try:
        w3_school_sel.enter_text_in_textarea_then_double_click(text="hello")
        dictionary_sel.check_dict_tooltip_shown()
        dictionary_sel.click_dict_tooltips()
    finally:
        extension_detail_page_sel.check_disable_dictionary_text_area()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502734")
def test_disable_dictionary_inside_the_textarea(
    w3_school_sel: W3SchoolSel,
    dictionary_sel: DictionarySel,
    extension_detail_page_sel: ExtensionDetailPageSel,
):
    extension_detail_page_sel.check_disable_dictionary_text_area()
    try:
        w3_school_sel.enter_text_in_textarea_then_double_click(text="hello")
        dictionary_sel.check_dict_tooltip_never_shown_yet()
    finally:
        extension_detail_page_sel.check_disable_dictionary_text_area()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502737")
def test_dictionary_once_double_click_word(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
):
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')

    extensions_page_sel.double_click_element(TEXT_LOCATOR)
    dictionary_sel.check_dict_popup_shown()
    dictionary_sel.check_dict_popup_ui()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502740")
def test_unit_exchange_works(
    unit_converter_sel: UnitConverterSel, xe_sel: XeSel, toolbar: Toolbar
):
    sleep(2)
    # toolbar.click_close_infobar()
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.check_exchange_1_usd()
    xe_sel.blacken_5_usd(is_open_xe_page=False)
    unit_converter_sel.check_exchange_5_usd()

    xe_sel.blacken_1_eur(is_open_xe_page=False)
    unit_converter_sel.check_exchange_1_eur()
    xe_sel.blacken_5_eur(is_open_xe_page=False)
    unit_converter_sel.check_exchange_5_eur()
