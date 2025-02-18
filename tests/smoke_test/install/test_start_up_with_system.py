import time

from pytest_pytestrail import pytestrail
from src.utilities import os_utils
from src.pages.installations import installation_utils
from tests import setting
from src.pages.installations import installation_page
from src.pages.settings import settings_default_browser

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086601")
def test_install_coccoc_without_set_start_up(language=setting.coccoc_language):
    try:
        # file_utils.rename_and_copy_file_host()
        installation.install_coccoc_by_build_name(
            language,
            build_name=setting.coccoc_build_name,
            is_default_start_up=False,
            is_close_after_installed=True,
        )
        assert os_utils.check_coccoc_is_start_up() is False
        assert os_utils.check_auto_launch_enabled_is_true() is False
        assert "0" == settings_default_browser.get_toggle_status_of_start_up(
            language
        )  # 0 mean toggle is OFF
        time.sleep(2)
    finally:
        installation_utils.uninstall_coccoc_silently()
        # file_utils.remove_and_revert_file_host()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086604")
def test_install_coccoc_with_start_up(language=setting.coccoc_language):
    try:
        # file_utils.rename_and_copy_file_host()
        installation.install_coccoc_by_build_name(
            language, build_name=setting.coccoc_build_name, is_default_start_up=True
        )
        time.sleep(2)
        assert "1" == settings_default_browser.get_toggle_status_of_start_up(
            language
        )  # 1 mean toggle is ON
        assert os_utils.check_coccoc_is_start_up() is True
        assert os_utils.check_auto_launch_enabled_is_true() is True

    finally:
        installation_utils.uninstall_coccoc_silently()
        # file_utils.remove_and_revert_file_host()
