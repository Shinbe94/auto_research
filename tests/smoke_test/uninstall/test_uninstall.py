import pytest
from src.pages.installations import installation_utils, installation_page
from tests import setting
from src.pages.settings import settings_default_browser
from src.utilities import (
    browser_utils,
    file_utils,
    os_utils,
    assistant_apps_utils,
    process_id_utils,
    network_utils,
)
from pytest_pytestrail import pytestrail

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytestrail.case("C1088593")
@pytest.mark.install_coccoc
def test_uninstall_dialog_ui(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=False,
):
    try:
        installation_utils.check_coccoc_uninstall_dialog(
            language, is_delete_user_data, is_uninstall, is_verify_ui=True
        )
    finally:
        # installation_utils.check_coccoc_uninstall_dialog(language, is_delete_user_data, is_uninstall=True)
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088608")
@pytest.mark.install_coccoc
def test_coccoc_rule_is_removed_from_firewall_setting(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
):
    # To check Rules are here
    browser_utils.check_coccoc_firewall_rules()
    try:
        # Uninstall coccoc
        installation_utils.uninstall_coccoc_by_control_panel(
            language, is_delete_user_data, is_uninstall
        )

        # To check the Rules are removed
        browser_utils.check_no_coccoc_firewall_rules()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088599")
@pytest.mark.install_coccoc
def test_user_cancel_uninstall():
    try:
        installation_utils.cancel_uninstall_coccoc()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088590")
@pytest.mark.install_coccoc
def test_uninstall_with_out_delete_user_data(
    language=setting.coccoc_language,
    is_delete_user_data=False,
    is_uninstall=True,
):
    try:
        installation_utils.uninstall_coccoc_by_control_panel(
            language, is_delete_user_data, is_uninstall
        )
        """CHECK FOLDERS AFTER UNINSTALL COCCOC"""
        installation_utils.check_folders_after_uninstall()

        """all user local data folders"""
        installation_utils.check_user_local_data(
            is_delete_user_data=is_delete_user_data
        )

        """CHECK UID FILE EXISTS"""
        assert installation_utils.check_uid_exist() is True

        """CHECK COCCOC WINDOWS TASK SCHEDULE IS REMOVED"""
        if os_utils.wait_for_coccoc_task_scheduler_is_disappeared():
            os_utils.check_no_coccoc_browser_task_scheduler()

        """CHECK NO CocCocUpdate.exe"""
        assert (
            process_id_utils.is_process_running_by_subprocess("CocCocUpdate.exe")
            is False
        )
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088686")
@pytest.mark.install_coccoc
def test_uninstall_coccoc_is_not_default_and_delete_user_data(
    set_chrome_as_default_browser,
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
):
    platform_installed = (
        "64bit"
        if file_utils.check_file_is_exists(setting.coccoc_binary_64bit)
        else "32bit"
    )
    try:
        installation_utils.uninstall_coccoc_by_control_panel(
            language, is_delete_user_data, is_uninstall
        )
        """CHECK FOLDERS AFTER UNINSTALL COCCOC"""
        installation_utils.check_folders_after_uninstall()

        """all user local data folders"""
        installation_utils.check_user_local_data(
            is_delete_user_data=is_delete_user_data
        )

        """CHECK UID FILE EXISTS"""
        assert installation_utils.check_uid_exist() is True
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088605")
@pytest.mark.install_coccoc
@pytest.mark.skipif(
    os_utils.get_real_system_arch(is_format=False) == "32bit",
    reason="Only support win 64bit",
)
def test_requests_send_when_uninstall_browser(
    remove_dummy_data_for_request_uninstall,
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
):
    # assistant_apps_utils.start_fiddler()
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump
        network_utils.dump_network_log(file_name="mitm_proxy_uninstall.py")

        # Execute uninstall coccoc
        installation_utils.uninstall_coccoc_by_control_panel(
            language,
            is_delete_user_data,
            is_uninstall,
            wait_for_n_seconds_before_close_the_windows=10,
        )
        # Wait for the request log sent
        assert installation_utils.wait_for_uninstall_request_log_sent()

        # Check request log sent after uninstalled
        installation_utils.check_request_uninstalling_log()
        # assistant_apps_utils.check_fiddler_log_after_uninstall_coccoc_browser()
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\uninstall_log.json"
        )

        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skip
@pytest.mark.install_coccoc
def test_uninstall_coccoc_silent():
    try:
        installation_utils.uninstall_coccoc_silently()
    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.install_as_default_browser
@pytestrail.case("C1088683")
def test_uninstall_coccoc_browser_successfully(
    language=setting.coccoc_language,
    is_delete_user_data=False,
    is_uninstall=True,
):
    try:
        installation_utils.uninstall_coccoc_by_control_panel(
            language, is_delete_user_data, is_uninstall
        )
    finally:
        """CHECK FOLDERS AFTER UNINSTALL COCCOC"""
        installation_utils.check_folders_after_uninstall()

        """all user local data folders"""
        installation_utils.check_user_local_data(
            is_delete_user_data=is_delete_user_data
        )

        """CHECK UID FILE EXISTS"""
        assert installation_utils.check_uid_exist() is True

        """CHECK COCCOC WINDOWS TASK SCHEDULE IS REMOVED"""
        if os_utils.wait_for_coccoc_task_scheduler_is_disappeared():
            os_utils.check_no_coccoc_browser_task_scheduler()

    """INSTALL COCCOC AGAIN THEN RECHECK DEFAULT BROWSER"""
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=setting.coccoc_build_name,
            is_close_after_installed=True,
            is_upgraded=True,
            is_delete_file_offscreen_cashback_extension=True,
        )
        # To verify message default browser:
        settings_default_browser.check_default_browser_text_by_pywinauto(language)
        # To check the default browser is working correctly by opening the link
        assistant_apps_utils.check_default_browser_by_open_link()
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088905")
@pytest.mark.install_coccoc
def test_coccoc_browser_task_scheduler_are_removed(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
):
    try:
        os_utils.check_coccoc_browser_task_scheduler()

        # Uninstall coccoc
        installation_utils.uninstall_coccoc_by_control_panel(
            language, is_delete_user_data, is_uninstall
        )
        if os_utils.wait_for_coccoc_task_scheduler_is_disappeared():
            os_utils.check_no_coccoc_browser_task_scheduler()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1088596")
@pytest.mark.install_coccoc
def test_uninstall_page(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
):
    try:
        installation_utils.uninstall_coccoc_by_control_panel(
            language=language,
            is_delete_user_data=is_delete_user_data,
            is_uninstall=is_uninstall,
            is_submit_feedback=False,
        )
    finally:
        installation_utils.uninstall_coccoc_silently()
