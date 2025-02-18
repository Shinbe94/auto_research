import pytest
from pytest_pytestrail import pytestrail

from src.pages.settings import first_time_run
from src.pages.installations import (
    download_setup_file,
    installation_page,
    installation_utils,
)
from src.utilities import browser_utils, file_utils, os_utils
from tests import setting

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086883")
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_download_from_homepage(language=setting.coccoc_language):
    platform = os_utils.get_real_system_platform(is_format_for_chromium_based=False)
    try:
        # file_utils.rename_and_copy_file_host()
        download_setup_file.download_setup_file_automatically(is_headless=False)
        installation.install_coccoc_by_coccocsetup_file(
            language,
            is_default_start_up=False,
            is_default_browser=False,
            is_close_after_installed=True,
            is_delete_file_offscreen_cashback_extension=True,
        )
        first_time_run.check_browser_after_installed(platform, language=language)

    finally:
        file_utils.remove_and_revert_file_host()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086889")
def test_term_of_use():
    platform = os_utils.get_real_system_platform(is_format_for_chromium_based=False)
    languages = ["en", "vi"]
    try:
        file_utils.rename_and_copy_file_host()
        for language in languages:
            try:
                download_setup_file.download_setup_file_automatically(
                    language, is_headless=False
                )
                installation.install_coccoc_by_coccocsetup_file(
                    language,
                    is_default_start_up=False,
                    is_default_browser=False,
                    is_close_after_installed=True,
                    is_delete_file_offscreen_cashback_extension=True,
                )
                first_time_run.check_browser_after_installed(platform, language)
                browser_utils.delete_file_offscreen_cashback_extension()
                first_time_run.check_terms(language)

            finally:
                installation_utils.uninstall_coccoc_silently()
    finally:
        file_utils.remove_and_revert_file_host()
