import time

import pytest
from pytest_pytestrail import pytestrail

from tests import setting

from src.pages.turn_on_sync import turn_on_sync
from src.pages.internal_page.bookmarks.bookmark_page import (
    get_list_bookmark_from_file_for_default_profile,
)
from src.pages.extensions.extensions_page import (
    get_user_extension_list_for_default_profile,
)
from src.pages.internal_page.version import coccoc_version_page
from src.pages.installations import installation_utils, installation_page, base_window
from src.utilities import file_utils, ftp_connection, os_utils, browser_utils
from tests.conftest import (
    close_win_app_driver_server_by_its_id,
    p_driver,
)

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086367")
def test_install_new_version_above_old_version(
    get_old_browser_build,
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    platform=setting.platform,
    from_build_name=None,
    to_build_name=None,
    is_needed_download=True,
    is_remove_coccoc_after_test=True,
    language=setting.coccoc_language,
):
    installation_utils.uninstall_coccoc_silently()
    """INSTALL OLD BROWSER BUILD"""
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            version=get_old_browser_build[1],
            is_upgraded=False,
            is_delete_file_offscreen_cashback_extension=True,
        )  # Install by build name
    finally:
        file_utils.delete_installer_downloaded(build_name=get_old_browser_build[0])

    time.sleep(2)

    """PROCESS SYNCING TO SETUP DATA"""
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

    # Get data for verification (this data should be used to verify after installed newer coccoc version)
    list_bookmark = get_list_bookmark_from_file_for_default_profile()
    list_extension = get_user_extension_list_for_default_profile()
    if (
        browser_utils.get_coccoc_major_build() >= 108
        and "jeoooddfnfogpngdoijplcijdcoeckgm" in list_extension
    ):
        list_extension.remove("jeoooddfnfogpngdoijplcijdcoeckgm")

    """DOWNLOAD & INSTALL THE TESTING BUILD"""
    # Process install the newer version of browser (the test build gets from FTP server)
    file_to_download_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_to_download_for_test}"
        )
        is False
    ):
        ftp_connection.get_file(
            folder_version=version,
            file_to_download_for_test=file_to_download_for_test,
            platform=platform,
        )
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=setting.coccoc_build_name,
            is_upgraded=True,
            is_close_after_installed=True,
        )

        # Verify the data after upgrade:
        # 1. Verify bookmarks
        assert list_bookmark == get_list_bookmark_from_file_for_default_profile()
        # 2. Verify list extensions
        assert list_extension == get_user_extension_list_for_default_profile()
        # TODO verify history
    finally:
        installation_utils.uninstall_coccoc_silently()
        print("===========uninstalling is done========")


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.do_not_install_coccoc
@pytestrail.case("C1086376")
def test_install_new_version_after_remove_old_version_without_clear_user_data(
    get_old_browser_build,
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    platform=setting.platform,
    from_build_name=None,
    to_build_name=None,
    is_needed_download=True,
    is_remove_coccoc_after_test=True,
    language=setting.coccoc_language,
    is_delete_user_data=False,
    is_uninstall=True,
):
    """INSTALL OLD BROWSER BUILD"""
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            version=get_old_browser_build[1],
            is_upgraded=False,
            is_delete_file_offscreen_cashback_extension=True,
        )  # Install by build name
    finally:
        file_utils.delete_installer_downloaded(build_name=get_old_browser_build[0])

    time.sleep(2)

    """PROCESS SYNCING TO SETUP DATA"""
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

    # Get data for verification (this data should be used to verify after installed newer coccoc version)
    list_bookmark = get_list_bookmark_from_file_for_default_profile()
    list_extension = get_user_extension_list_for_default_profile()
    if (
        browser_utils.get_coccoc_major_build() >= 108
        and "jeoooddfnfogpngdoijplcijdcoeckgm" in list_extension
    ):
        list_extension.remove("jeoooddfnfogpngdoijplcijdcoeckgm")

    """PROCESS UNINSTALL COCCOC BROWSER VIA CONTROL PANEL"""
    # installation_utils.uninstall_coccoc_by_control_panel(language, is_delete_user_data=False, is_uninstall=True)
    installation_utils.uninstall_coccoc_by_control_panel(
        language, is_delete_user_data=False, is_uninstall=True
    )

    """DOWNLOAD & INSTALL THE TESTING BUILD"""
    # Process install the newer version of browser (the test build gets from FTP server)
    file_to_download_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_to_download_for_test}"
        )
        is False
    ):
        ftp_connection.get_file(
            folder_version=version,
            file_to_download_for_test=file_to_download_for_test,
            platform=platform,
        )
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=setting.coccoc_build_name,
            is_upgraded=True,
            is_close_after_installed=True,
        )

        # Verify the data after upgrade:
        # 1. Verify bookmarks
        assert list_bookmark == get_list_bookmark_from_file_for_default_profile()
        # 2. Verify list extensions
        assert list_extension == get_user_extension_list_for_default_profile()
        # TODO verify history
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    os_utils.get_window_platform_architecture() == "32bit"
    or setting.platform == "32bit",
    reason="Windows is not 64bit operating system",
)
@pytest.mark.ignore_old_build
@pytestrail.case("C1086388")
def xtest_override_coccoc_32bit_by_64bit(
    get_old_browser_build,
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    language=setting.coccoc_language,
    platform="64bit",
):
    """Install coccoc 32 bit (from coccoc.com or from FTP)"""
    try:
        installation.install_coccoc_from_coccoc_com(
            language, version, is_close_after_installed=True, platform="32bit"
        )  # Install from coccoc.com
    finally:
        file_utils.delete_installer_downloaded()

    time.sleep(2)

    """PROCESS SYNCING TO SETUP DATA"""
    turn_on_sync.turn_on_sync_from_setting(
        setting.cc_account_user, setting.cc_account_password
    )

    # Get data for verification (this data should be used to verify after installed newer coccoc version)
    list_bookmark = get_list_bookmark_from_file_for_default_profile()
    list_extension = get_user_extension_list_for_default_profile()
    if (
        browser_utils.get_coccoc_major_build() >= 108
        and "jeoooddfnfogpngdoijplcijdcoeckgm" in list_extension
    ):
        list_extension.remove("jeoooddfnfogpngdoijplcijdcoeckgm")

    """ Install coccoc 64 bit (override 32 bit by 64bit) """
    # Process install the newer version of browser (the test build gets from FTP server)
    file_to_download_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version, build_name=build_name
    )

    if (
        file_utils.check_file_is_exists(
            rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_to_download_for_test}"
        )
        is False
    ):
        ftp_connection.get_file(
            folder_version=version,
            file_to_download_for_test=file_to_download_for_test,
            platform=platform,
        )

    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=setting.coccoc_build_name,
            is_upgraded=True,
            is_close_after_installed=True,
        )
        time.sleep(2)

        # Verify the data after override install:
        # 1. Verify coccoc 64bit is installed
        assert coccoc_version_page.get_coccoc_platform() == "64bit"
        # 2. Verify bookmarks
        assert list_bookmark == get_list_bookmark_from_file_for_default_profile()
        # 3. Verify list extensions
        assert list_extension == get_user_extension_list_for_default_profile()
        # TODO verify history
    finally:
        installation_utils.uninstall_coccoc_silently()
