from pytest_pytestrail import pytestrail

from src.pages.settings.settings_search import SettingsSearch


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54299")
def test_check_default_search_after_install_coccoc(
    settings_search: SettingsSearch, lang: str
):
    settings_search.open_page()
    settings_search.click_manage_search_engines_and_site_search()
    settings_search.check_default_search(search_vendor_name="Cốc Cốc")
    if "en" in lang:
        settings_search.check_text_is_not_appeared(
            text="Use results from Coc Coc search engine"
        )
    else:
        settings_search.check_text_is_not_appeared(
            text="Use results from Coc Coc search engine"
        )
