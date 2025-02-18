import pytest
from pytest import FixtureRequest
from src.pages.installations import installation_page, installation_utils
from src.pages.settings import setting_preferences

from src.utilities import browser_utils
from tests import setting

installation = installation_page.InstallationPage()


@pytest.fixture(autouse=True)
def check_testing_build(request):
    """
    To check if the intended testing build is already installed or No CocCoc installed,
    if not then process uninstall the current build then install the correct build before executing the test
    :return: None
    """
    if not "ignore_check_testing_build" in request.keywords:
        installed_build = browser_utils.get_version_of_coccoc()
        if installed_build is None:
            installation.install_coccoc_by_build_name(
                language=setting.coccoc_language, build_name=setting.coccoc_build_name
            )
        elif not installed_build == setting.coccoc_test_version:
            installation_utils.uninstall_coccoc_silently()
            installation.install_coccoc_by_build_name(
                language=setting.coccoc_language,
                build_name=setting.coccoc_build_name,
                is_delete_file_offscreen_cashback_extension=True,
            )
        else:
            pass


@pytest.fixture(autouse=True)
def disable_warning_closing_multiple_tabs():
    """
    To disable confirmation warning close multiple tabs
    Returns:
    """
    setting_preferences.disable_show_close_all_tabs_confirmation()


@pytest.fixture(autouse=True)
def disable_restore_popup_once_crash_or_killing_browser():
    """
    Disabling restore popup that comes when chrome process is killed
    Returns:
    """
    setting_preferences.disable_restore_popup()


# @pytest.fixture(autouse=True)
# def delete_cashback_offscreen_file(request: FixtureRequest):
#     """This fixture is for deleting the file 'offscreen.html' of Cashback extension
#     to prevent it affect to playwright
#     from V116 we have problem while open cc = playwright
#     this page: chrome-extension://afaljjbleihmahhpckngondmgohleljb/offscreen.html leads to error
#     """
#     if "dont_delete_cashback_offscreen_file" in request.keywords:
#         pass
#     else:
#         browser_utils.delete_file_offscreen_cashback_extension()
#     yield
#     if "dont_delete_cashback_offscreen_file" in request.keywords:
#         pass
#     else:
#         browser_utils.copy_back_file_offscreen_cashback_extension()
