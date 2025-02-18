from time import sleep


from selenium.webdriver.common.by import By
from pytest_pytestrail import pytestrail
from src.pages.dialogs.dictionary import DictionarySel
from src.pages.dialogs.unit_converter import UnitConverterSel

from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.settings.settings_default_browser import close_inforbar
from src.pages.support_pages.support_pages import XeSel
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45033")
def test_unit_exchange_works_by_blacken(
    unit_converter_sel: UnitConverterSel, xe_sel: XeSel
):
    sleep(2)
    # toolbar.click_close_infobar()
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.check_exchange_1_usd()
    xe_sel.blacken_1_eur(is_open_xe_page=False)
    unit_converter_sel.check_exchange_1_eur()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C45034")
def test_close_unit(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    sleep(2)
    # toolbar.click_close_infobar()
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.check_exchange_1_usd()
    unit_converter_sel.check_unit_exchange_is_hidden()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502758")
def test_unit_exchange_infomation(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.click_btn_info()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502761")
def test_copy_action_unit_exchange(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.copy_value_from()
    unit_converter_sel.copy_value_to()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502764")
def test_btn_copy_unit_exchange(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.click_btn_copy(text="1 USD")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502767")
def test_btn_more_unit_exchange(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.click_btn_more()
    unit_converter_sel.check_ui_after_click_btn_more()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502770")
def test_add_more_currency(unit_converter_sel: UnitConverterSel, xe_sel: XeSel):
    close_inforbar()  # close infobar default browser
    xe_sel.blacken_1_usd(is_open_xe_page=True)
    unit_converter_sel.click_btn_add_more_currency()
