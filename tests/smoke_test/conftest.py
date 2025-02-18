import faulthandler
import random
import pytest
from src.pages.installations import base_window, installation_page, installation_utils

from src.utilities import browser_utils, file_utils, ftp_connection, os_utils
from tests import setting
from src.pages.settings import settings_default_browser

installation = installation_page.InstallationPage()


@pytest.fixture(autouse=True)
def initialization_before_test():
    file_utils.delete_all_installer_downloaded()  # delete exe files
    installation_utils.uninstall_coccoc_silently()  # Uninstall coccoc


# Download the build for test on this class
@pytest.fixture(autouse=True)
def setup_file_for_test(
    request,
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    from_build_name=None,
    to_build_name=None,
):
    # Disable error
    faulthandler.disable()
    # Uninstall coccoc
    installation_utils.uninstall_coccoc_silently()
    # Download the build for test
    file_to_download_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{file_to_download_for_test}"
        )
        is False
    ):
        ftp_connection.get_file2(
            folder_version=version,
            file_to_download_for_test=file_to_download_for_test,
        )

    if "is_test_first_time_run" in request.keywords:
        # Keep coccoc browser Windows opening to check
        installation.install_coccoc_by_build_name(
            language=setting.coccoc_language,
            build_name=setting.coccoc_build_name,
            is_close_after_installed=False,
            is_delete_file_offscreen_cashback_extension=True,
        )
    elif "do_not_install_coccoc" in request.keywords:
        pass
    elif "install_coccoc" in request.keywords:
        installation.install_coccoc_by_build_name(
            language=setting.coccoc_language,
            build_name=setting.coccoc_build_name,
            is_close_after_installed=True,
            is_delete_file_offscreen_cashback_extension=True,
        )
    elif "install_as_default_browser" in request.keywords:
        installation.install_coccoc_by_build_name(
            language=setting.coccoc_language,
            build_name=setting.coccoc_build_name,
            is_close_after_installed=True,
            is_default_browser=True,
            is_delete_file_offscreen_cashback_extension=True,
        )
    # else:
    #     # Close coccoc browser windows
    #     installation.install_coccoc_by_build_name(
    #         language=setting.coccoc_language,
    #         build_name=setting.coccoc_build_name,
    #         is_close_after_installed=True,
    #     )

    yield file_to_download_for_test
    faulthandler.enable()


# Fixture to get old coccoc browser build
@pytest.fixture(autouse=False)
def get_old_browser_build(
    request,
    build_name=setting.coccoc_build_name,
    version=random.choice(setting.old_coccoc_version),
    from_build_name=None,
    to_build_name=None,
):
    if "ignore_old_build" in request.keywords:
        yield None
    else:
        old_browser_build_for_test = base_window.BaseWindow.pre_process_setup_filename(
            version=version,
            build_name=build_name,
            from_build_name=from_build_name,
            to_build_name=to_build_name,
        )
        if (
            file_utils.check_file_is_exists(
                rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{old_browser_build_for_test}"
            )
            is False
        ):
            ftp_connection.get_file2(
                folder_version=version,
                file_to_download_for_test=old_browser_build_for_test,
            )
        yield old_browser_build_for_test, version


@pytest.fixture()
def get_very_old_browser_build(
    build_name=setting.coccoc_build_name,
    version=random.choice(setting.very_old_coccoc_version),
    from_build_name=None,
    to_build_name=None,
):
    old_browser_build_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{old_browser_build_for_test}"
        )
        is False
    ):
        ftp_connection.get_file2(
            folder_version=version,
            file_to_download_for_test=old_browser_build_for_test,
        )

    yield old_browser_build_for_test, version
    faulthandler.disable()


# @pytest.fixture(autouse=False)
# def process_uninstall_install_coccoc(self, request):
#     # Uninstall coccoc if any installed coccoc
#     installation_utils.uninstall_coccoc_silently()
#     # installation_utils.uninstall_coccoc_by_control_panel()

#     # In case we don't want to use the  'autouse fixture'
#     if "install_coccoc_32bit" in request.keywords:
#         """Install coccoc 32 bit (from coccoc.com or from FTP)"""
#         try:
#             installation.install_coccoc_from_coccoc_com(
#                 is_close_after_installed=True, platform="32bit"
#             )  # Install from coccoc.com
#         finally:
#             file_utils.delete_installer_downloaded()
#             time.sleep(1)
#     else:
#         # Install coccoc again ( Get the current prod build from coccoc.com)
#         try:
#             # installation.install_coccoc_from_coccoc_com(is_close_after_installed=True) # Install from coccoc.com
#             installation.install_coccoc_by_build_name(
#                 language=setting.coccoc_language,
#                 build_name=setting.coccoc_build_name,
#             )  # Install by build name
#         finally:
#             file_utils.delete_installer_downloaded()


@pytest.fixture(autouse=False)
def delete_metrics_file_if_exist():
    file_utils.remove_file(
        rf"C:\Users\{os_utils.get_username()}\Documents\metrics_log.json"
    )
    yield
    file_utils.remove_file(
        rf"C:\Users\{os_utils.get_username()}\Documents\metrics_log.json"
    )


@pytest.fixture(autouse=False)
def process_uninstall_if_any_then_install_coccoc(language=setting.coccoc_language):
    # platform = os_utils.get_window_platform_architecture(
    #     is_format_for_chromium_based=False
    # )
    try:
        file_utils.rename_and_copy_file_host()
        # download_setup_file.download_coccoc_setup(platform=platform)
        # installation.install_coccoc_from_coccoc_com(
        #     language,
        #     platform=platform,
        #     is_default_start_up=False,
        #     is_default_browser=False,
        #     is_close_after_installed=True,
        # )

        # installation.install_coccoc_by_coccocsetup_file(
        #     language,
        #     is_default_start_up=False,
        #     is_default_browser=False,
        #     is_close_after_installed=True,
        # )
        installation.install_coccoc_by_build_name(
            language, build_name=setting.coccoc_build_name, is_default_start_up=True
        )
    finally:
        file_utils.remove_and_revert_file_host()
        file_utils.delete_installer_downloaded()


@pytest.fixture(autouse=False)
def set_chrome_as_default_browser():
    settings_default_browser.set_a_browser_to_default()


@pytest.fixture(autouse=False)
def remove_dummy_data_for_request_uninstall():
    # remove request log
    file_utils.remove_file(
        rf"C:\Users\{os_utils.get_username()}\Documents\uninstall_log.json"
    )


@pytest.fixture(autouse=True)
def kill_all_coccoc_processes():
    browser_utils.kill_all_coccoc_process()
    yield
    browser_utils.kill_all_coccoc_process()
