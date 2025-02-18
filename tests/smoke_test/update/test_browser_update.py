import faulthandler
import random
import subprocess

import pytest
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser

from src.pages.installations import installation_page, base_window, installation_utils
from src.pages.internal_page.version import coccoc_version_page
from src.pages.turn_on_sync import turn_on_sync
from src.pages.settings import setting_about_coccoc
from tests import setting
from src.utilities import (
    file_utils,
    os_utils,
    ftp_connection,
    browser_utils,
    string_number_utils,
)
from tests.conftest import close_win_app_driver_server_by_its_id, p_driver

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086835")
def test_update_browser_via_about_us(
    get_old_browser_build,
    language=setting.coccoc_language,
):
    """Install older browser"""
    installation.install_coccoc_by_build_name(
        language,
        build_name=setting.coccoc_build_name,
        version=get_old_browser_build[1],
        is_delete_file_offscreen_cashback_extension=True,
    )
    version_before_update = (
        browser_utils.get_current_browser_and_current_omaha_version()
    )

    """Execute upgrade browser via About us, then click Relaunch button"""
    try:
        """Adding host"""
        file_utils.rename_and_copy_file_host()
        """Execute upgrade browser via About us, then click Relaunch button"""
        # setting_about_coccoc.click_relaunch_button()

        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()

        """Assertions"""
        # if setting_about_coccoc.click_relaunch_button():
        if setting_about_coccoc.click_relaunch_button_pywinauto():
            # Check browser version after upgrade
            setting_about_coccoc.check_browser_after_update(language)
        # Check install folder
        setting_about_coccoc.check_folders_after_update(
            previous_browser_build=version_before_update[0]
        )
        # check Omaha after update
        setting_about_coccoc.check_omaha_after_update(
            previous_omaha_version=version_before_update[1]
        )

    finally:
        file_utils.remove_and_revert_file_host()
        file_utils.delete_installer_downloaded(build_name=get_old_browser_build[0])
        # Uninstall coccoc
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086844")
def test_update_from_very_old_version(
    get_very_old_browser_build,
    language=setting.coccoc_language,
):
    """
    very old versions: very_old_coccoc_version = ['85.0.4183.146', '86.0.4240.198', '87.0.4280.148', '88.0.4324.202']
    only has 32bit so after upgrade the coccoc still 32 bit
    :param process_uninstall_coccoc_if_any:
    :param get_very_old_browser_build:
    :param language:
    :return:
    """
    is_very_old_version = True
    """INSTALL A VERY OLD BROWSER"""
    try:
        installation.install_coccoc_by_build_name(
            language,
            build_name=setting.coccoc_build_name,
            version=get_very_old_browser_build[1],
            is_delete_file_offscreen_cashback_extension=True,
        )
        version_before_update = (
            browser_utils.get_current_browser_and_current_omaha_version()
        )
    finally:
        file_utils.delete_installer_downloaded(build_name=get_very_old_browser_build[0])
    open_browser.open_coccoc_by_pywinauto_then_close_it(is_first_time_opened=False)
    """CREATE TASK SCHEDULE UPDATE & WAIT FOR THE TIME IS CAME THEN THE UPDATING IS EXECUTED"""
    try:
        # Add host
        file_utils.rename_and_copy_file_host()
        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()

        # Edit task schedule's time for updating coccoc
        # os_utils.edit_coccoc_update_task_schedule()

        # Sleep for waiting the update is done silently
        assert setting_about_coccoc.wait_for_coccoc_updated_by_schedule_is_done()
        """ASSERTION"""
        setting_about_coccoc.check_browser_after_update_pywinauto(
            language, is_very_old_version=is_very_old_version
        )
    finally:
        file_utils.remove_and_revert_file_host()
        # os_utils.delete_coccoc_update_task_schedule()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086865")
def test_update_incremental(
    language=setting.coccoc_language,
    version=setting.coccoc_test_version,
    platform=os_utils.get_real_system_platform(is_format_for_chromium_based=False),
):
    list_builds = ftp_connection.get_list_available_incremental_builds()
    version_folder = version + "_x64" if platform == "64bit" else version
    try:
        for build in list_builds:
            # Install the based build(lower build to upgrade to the testing build)
            based_build = string_number_utils.get_string_between_2_str(
                build, rf"from_", r"_coccocsetup.exe"
            )
            try:
                based_build_folder = (
                    based_build + "_x64" if platform == "64bit" else based_build
                )
                file_name_with_path = rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{based_build_folder}\installers\standalone_coccoc_en_machine.exe"
                # print("file location", file_name_with_path)
                installation.install_coccoc_from_file_with_path(
                    file_name_with_path,
                    is_close_after_installed=False,
                    is_delete_file_offscreen_cashback_extension=True,
                )
                coccoc_version_page.get_coccoc_version_at_the_very_first_time_opening(
                    language, based_build
                )
            except Exception as e:
                raise e
            finally:
                pass

            # Execute upgrade
            try:
                cmd_incremental_update = rf"cd C:\Users\{os_utils.get_username()}\Downloads\corom\{version_folder}\installers && {build} --system-level"
                # subprocess.run(cmd, capture_output=True, shell=True)
                subprocess.check_call(cmd_incremental_update, shell=True, timeout=60)
            except Exception as e:
                # raise e
                print(e)
            finally:
                coccoc_version_page.get_coccoc_version_pywinauto(language, version)
                installation_utils.uninstall_coccoc_silently()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086853")
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
def test_update_from_old_syncing_version(
    get_old_browser_build,
    language=setting.coccoc_language,
):
    """INSTALL OLDER BROWSER & PROCESS SYNCING ..."""
    installation.install_coccoc_by_build_name(
        language,
        build_name=setting.coccoc_build_name,
        version=get_old_browser_build[1],
        is_delete_file_offscreen_cashback_extension=True,
    )
    turn_on_sync.turn_on_sync_from_setting(
        setting.cc_account_user, setting.cc_account_password
    )
    # tuple_context = p_driver()  # Start Coccoc by Winappdriver and connect by playwright
    # pcc = tuple_context[0]  # get playwright page
    # browser = tuple_context[1]
    # pw = tuple_context[2]
    # winappdriver = tuple_context[3]
    # pid = tuple_context[4]  # get winappdriver pid
    # turn_on_sync.turn_on_sync_from_setting_by_playwright(
    #     pcc, email=setting.cc_account_user, password=setting.cc_account_password
    # )
    # # pcc.close()
    # browser.close()
    # pw.stop()
    # winappdriver.quit()
    # close_win_app_driver_server_by_its_id(pid)  # Close current winappdriver instance

    """EXECUTE UPGRADE BROWSER VIA ABOUT US THEN CLICK RELAUNCH BUTTON"""
    try:
        # Adding host
        file_utils.rename_and_copy_file_host()

        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()
        # Execute upgrade browser via About us, then click Relaunch button
        """Assertions"""
        if setting_about_coccoc.click_relaunch_button_pywinauto():
            # Check browser version after upgrade
            setting_about_coccoc.check_browser_after_update(language)
    finally:
        file_utils.remove_and_revert_file_host()
        file_utils.delete_installer_downloaded(build_name=get_old_browser_build[0])
        browser_utils.kill_all_coccoc_process()
        # Check install folder
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086847")
def test_binaries_file_between_update_and_fresh_install(
    get_old_browser_build,
    language=setting.coccoc_language,
    folder1="application_upgrade",
    folder2="application_fresh_install",
):
    # installation_utils.uninstall_coccoc_silently()
    file_utils.remove_directory(
        directory=str(file_utils.get_project_root()) + rf"\data\{folder1}"
    )
    file_utils.remove_directory(
        directory=str(file_utils.get_project_root()) + rf"\data\{folder2}"
    )
    """Install older browser"""

    installation.install_coccoc_by_build_name(
        language,
        build_name=setting.coccoc_build_name,
        is_delete_setup_file_after_installed=True,
        version=get_old_browser_build[1],
        is_delete_file_offscreen_cashback_extension=True,
    )
    # Get application_version and omaha_version before executing update
    version_before_update = (
        browser_utils.get_current_browser_and_current_omaha_version()
    )

    """Execute upgrade browser via About us, then click Relaunch button"""
    try:
        """Adding host"""
        file_utils.rename_and_copy_file_host()

        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()

        """Assertions"""
        if setting_about_coccoc.click_relaunch_button_pywinauto():
            # Check browser version after upgrade
            setting_about_coccoc.check_browser_after_update(language)
    finally:
        file_utils.remove_and_revert_file_host()
        file_utils.delete_installer_downloaded(build_name=get_old_browser_build[0])

    """Copy file to a folder"""
    file_utils.copy_application_folder_to_new_folder(
        folder_name=folder1,
        previous_browser_build=version_before_update[0],
        is_open_folder_before_copying=True,
    )
    # a trick to remove unnecessary files before comparing
    file_utils.remove_all_files_in_folder(
        str(file_utils.get_project_root()) + rf"\data\application_upgrade\SetupMetrics"
    )
    # Uninstall the browser before fresh installation it
    installation_utils.uninstall_coccoc_silently()

    """Fresh install the testing build, downloaded from FTP server"""
    try:
        build_for_test = installation_utils.get_browser_build()
        installation.install_coccoc_by_build_name(
            language,
            build_name=setting.coccoc_build_name,
            is_delete_setup_file_after_installed=True,
        )
    finally:
        file_utils.delete_installer_downloaded(build_name=build_for_test)
    """Copy file to a folder"""
    file_utils.copy_application_folder_to_new_folder(
        folder_name=folder2,
        previous_browser_build=version_before_update[0],
        is_open_folder_before_copying=False,
    )

    """Comparing 2 folders"""
    try:
        assert (
            file_utils.compare_2_folders(
                dir1=str(file_utils.get_project_root()) + rf"\data\{folder1}",
                dir2=str(file_utils.get_project_root()) + rf"\data\{folder2}",
            )
            is True
        )
    finally:
        file_utils.remove_directory(
            directory=str(file_utils.get_project_root()) + rf"\data\{folder1}"
        )
        file_utils.remove_directory(
            directory=str(file_utils.get_project_root()) + rf"\data\{folder2}"
        )
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    setting.is_skip_test_update_download_cases == True,
    reason="Skip testing this test cases as update/upgrade feature is not enable yet for this build!",
)
@pytestrail.case("C1086856")
def test_update_from_production_version(language=setting.coccoc_language):
    installation_utils.uninstall_coccoc_silently()
    """INSTALL FROM PRODUCTION"""
    installation.install_coccoc_from_coccoc_com(
        language, is_delete_file_offscreen_cashback_extension=True
    )

    """EXECUTE UPDATE"""
    try:
        """Adding host"""
        file_utils.rename_and_copy_file_host()
        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()

        # browser_utils.kill_all_coccoc_process()
        """Execute upgrade browser via About us, then click Relaunch button if any"""
        if setting_about_coccoc.click_relaunch_button_pywinauto2():
            # Check browser version after upgrade
            setting_about_coccoc.check_browser_after_update_from_prod(language)
    finally:
        file_utils.remove_and_revert_file_host()
        file_utils.delete_build_by_name()
        installation_utils.uninstall_coccoc_silently()
