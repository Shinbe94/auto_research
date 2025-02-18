from time import sleep
from pytest_pytestrail import pytestrail
from src.pages.internal_page.extensions.extensions_page import (
    ExtensionsPageApp,
    ExtensionsPageSel,
)

from src.pages.support_pages.support_pages import WarningPageSel
from src.utilities import os_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C503337")
def test_extension_dark_list(
    add_extension_to_coccoc,
    add_testing_extensionid_to_darklist,
    sleep_for_test,  # sleep 60 seconds
    extensions_page_sel: ExtensionsPageSel,
    extensions_page_app: ExtensionsPageApp,
):
    # get extension name for later using
    extension_name = extensions_page_sel.get_extension_name_by_id(
        extension_id="jghecgabfgfdldnmbfkhmffcabddioke"
    )
    try:
        # Checking dark extension warning!
        extensions_page_sel.check_extension_darklist(
            extension_id="jghecgabfgfdldnmbfkhmffcabddioke", timeout=180
        )

    # Finally, remove the tested extension if any
    finally:
        extensions_page_sel.remove_extension(
            extension_id="jghecgabfgfdldnmbfkhmffcabddioke", sleep_n_seconds=2
        )
        extensions_page_app.click_btn_confirm_remove_extension(
            extension_name=extension_name
        )
        sleep(10)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C328908")
def test_no_black_list_extension(
    add_extension_to_coccoc,
    extensions_page_sel: ExtensionsPageSel,
    extensions_page_app: ExtensionsPageApp,
):
    # get extension name for later using
    extension_name = extensions_page_sel.get_extension_name_by_id(
        extension_id="jghecgabfgfdldnmbfkhmffcabddioke"
    )
    try:
        # checking no blacklist in LocalState file
        with open(
            file=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
            encoding="utf-8",
        ) as file:
            content = file.read()
            file.close()
            assert "blacklist" not in content

    # Finally, remove the tested extension if any
    finally:
        extensions_page_sel.remove_extension(
            extension_id="jghecgabfgfdldnmbfkhmffcabddioke", sleep_n_seconds=2
        )
        extensions_page_app.click_btn_confirm_remove_extension(
            extension_name=extension_name
        )
        sleep(10)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C503340")
def test_warning_malicious_sites(warning_page_sel: WarningPageSel):
    warning_page_sel.open_site(url="http://malware.wicar.org/data/eicar.com")
    warning_page_sel.check_main_message()
    warning_page_sel.check_bg_color()
