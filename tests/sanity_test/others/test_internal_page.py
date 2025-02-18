from selenium.webdriver.common.by import By

from pytest_pytestrail import pytestrail
from src.pages.dialogs.dictionary import DictionarySel
from src.pages.internal_page.coccoc_apps_page import CocCocAppsPageSel
from src.pages.internal_page.crashes.crashes_page import CrashesPageSel
from src.pages.internal_page.credits.credits_page import CreditsPageSel
from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.pages.internal_page.flags.flags_page import FlagsPageSel
from src.pages.settings.settings_on_startup import SettingsOnStartupSel
from src.pages.settings.settings_privacy_and_security import (
    SettingsPrivacyAndSecuritySel,
)
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C508077")
def test_don_not_offer_translation_for_internal_page(
    extensions_page_sel: ExtensionsPageSel,
    dictionary_sel: DictionarySel,
    crashes_page_sel: CrashesPageSel,
    credits_page_sel: CreditsPageSel,
):
    extensions_page_sel.open_page("https://en.wikipedia.org/wiki/Organization")
    TEXT_LOCATOR: tuple = (By.XPATH, '//span[text()="Organization"]')

    extensions_page_sel.double_click_element(TEXT_LOCATOR)
    dictionary_sel.check_dict_popup_shown()

    crashes_page_sel.double_click_text_crashes()
    dictionary_sel.check_dict_popup_never_shown_yet()

    credits_page_sel.double_click_text_credits()
    dictionary_sel.check_dict_popup_never_shown_yet()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C730981")
def test_unsign_text_coccoc_at_flags_page(flags_page_sel: FlagsPageSel):
    flags_page_sel.make_search_at_flags_page(
        search_str="Cốc Cốc"
    ).verify_search_no_results()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C731119")
def test_app_logo_at_coccoc_apps(coccoc_apps_page_sel: CocCocAppsPageSel):
    coccoc_apps_page_sel.check_logo_displayed_correctly().check_links_work_well()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C833265")
def test_internal_icon_shown_on_start_up_page(
    settings_on_startup_sel: SettingsOnStartupSel, toolbar: Toolbar
):
    list_internal_pages = [
        "coccoc://extensions/",
        "coccoc://bookmarks/",
        "coccoc://apps/",
        "coccoc://downloads/",
        "coccoc://flags/",
    ]
    for url in list_internal_pages:
        # settings_on_startup_sel.open_new_tab_with_specific_url(url=url)
        toolbar.open_new_tab()
        toolbar.make_search_value(search_str=url, is_press_enter=True)
    toolbar.switch_tab_by_tab_number(tab_number="1")
    try:
        settings_on_startup_sel.click_open_a_specify_page_or_set_of_pages()
        settings_on_startup_sel.click_use_current_page()
        settings_on_startup_sel.check_favicons()
    finally:
        settings_on_startup_sel.remove_all_added_page()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C833187")
def test_icon_location_appeared(
    settings_privacy_and_security_sel: SettingsPrivacyAndSecuritySel,
):
    settings_privacy_and_security_sel.verify_location_icon_appeared()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223913")
def test_url_scheme_share_this_page(toolbar: Toolbar):
    list_internal_pages = [
        "coccoc://extensions",
        "coccoc://bookmarks",
        "coccoc://apps",
        "coccoc://downloads",
        "coccoc://flags",
    ]

    for url in list_internal_pages:
        toolbar.make_search_value(search_str=url, is_press_enter=True)
        toolbar.click_btn_share_this_page()
        xpath = (By.XPATH, f'//Text[@Name="{url}"]')
        assert toolbar.is_element_appeared(xpath)


def reverse_str(s: str):
    if len(s) == 0:
        return s
    else:
        return reverse_str(s[1:]) + s[0]


def test_reverse():
    str_text = "I Love Python and Selenium Webdriver"
    # print(str_text[::-1])
    mylist = ["a", "b", "a", "c", "c"]
    # mylist = list(dict.fromkeys(mylist))
    # print(mylist)
    # mylist2 = ["a", "b", "a", "c", "c"]
    # mylist2 = set(mylist2)
    # print(mylist2)
    # str_text = "".join(reversed(str_text))
    # str_text = [str_text[i] for i in range(len(str_text) - 1, -1, -1)]
    # return "".join(str_text)
    # print("".join(str_text))
    # print(reverse_str(str_text))
    unique_list = []
    for i in mylist:
        if i not in unique_list:
            unique_list.append(i)
    print(unique_list)
