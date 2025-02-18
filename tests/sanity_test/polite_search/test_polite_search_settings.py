import time

from pytest_pytestrail import pytestrail
from src.pages.settings.settings_search import SettingsSearch
from src.pages.toolbar.toolbar import Toolbar

from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C750763")
def test_check_search_engine_from_its_settings(
    settings_search: SettingsSearch, lang: str
):
    settings_search.open_page()
    settings_search.click_manage_search_engines_and_site_search()

    # Check no Baidu from default search engines
    assert "Baidu" not in settings_search.get_list_search_vendor_name()

    # Check default search is Cốc Cốc
    settings_search.check_default_search(search_vendor_name="Cốc Cốc")

    # Check no 'Use results from Cốc Cốc search engine' option
    if "en" in lang:
        settings_search.check_text_is_not_appeared(
            text="Use results from Coc Coc search engine"
        )
    else:
        settings_search.check_text_is_not_appeared(
            text="Use results from Coc Coc search engine"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C718082")
def test_check_search_engines(settings_search: SettingsSearch, toolbar: Toolbar):
    try:
        settings_search.open_page()
        settings_search.click_manage_search_engines_and_site_search()
        list_search_vendor_name = settings_search.get_list_search_vendor_name()
        # Handle current default search engine
        first_default_search_engine = settings_search.get_default_search_engine()
        toolbar.make_search_value(search_str="váy hoa", is_press_enter=True)
        assert (
            setting.list_default_search_engine_vendor.get(first_default_search_engine)
            in toolbar.get_opening_url()
        )
        # Handle list remaining search engine
        list_search_vendor_name.remove(first_default_search_engine)
        for name in list_search_vendor_name:
            settings_search.open_page()
            settings_search.click_manage_search_engines_and_site_search()
            settings_search.click_btn_make_default(search_vendor_name=name)
            time.sleep(2)
            settings_search.reload_page()
            toolbar.make_search_value(
                search_str=rf"váy hoa {name}", is_press_enter=True
            )
            time.sleep(2)
            assert (
                setting.list_default_search_engine_vendor.get(name)
                in toolbar.get_opening_url()
            )
    finally:
        # Change default to CocCoc search
        settings_search.open_page()
        settings_search.click_manage_search_engines_and_site_search()
        settings_search.click_btn_make_default(search_vendor_name="Cốc Cốc")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1164228")
def test_recent_search(toolbar: Toolbar):
    toolbar.make_search_value(search_str=rf"váy hoa", is_press_enter=True)
    first_url = toolbar.get_opening_url()
    toolbar.open_new_tab()
    toolbar.click_address_and_search_bar()
    toolbar.check_recent_search_is_displayed(search_str="váy hoa")
    toolbar.click_recent_search_item(search_str="váy hoa")
    second_url = toolbar.get_opening_url()
    assert second_url in first_url
    time.sleep(2)
