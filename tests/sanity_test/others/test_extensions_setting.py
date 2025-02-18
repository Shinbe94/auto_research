from time import sleep
import pytest

from pywinauto.keyboard import send_keys
from pytest_pytestrail import pytestrail

from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from src.utilities import file_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54477")
def test_coccoc_extensions_are_grouped(extensions_page_sel: ExtensionsPageSel):
    extensions_page_sel.check_list_coccoc_extensions_are_in_a_group()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C834333")
@pytest.mark.open_in_bootstrap_mode
def test_support_content_verifier_bootrap_mode(
    remove_file_verified_contents_of_extension,
    extensions_page_sel: ExtensionsPageSel,
    verify_file_verified_contents_appears_automatically_again,
):
    extensions_page_sel.open_extension_page()
    sleep(5)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1013644")
@pytest.mark.open_in_enforce_mode
def test_support_content_verifier_enforcing_mode(
    edit_some_data_for_test_enforing_mode,
    extensions_page_sel: ExtensionsPageSel,
    verify_content_verifier_enforcing_mode,
):
    extensions_page_sel.open_extension_page()
    sleep(5)
