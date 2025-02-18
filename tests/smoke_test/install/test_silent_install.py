import subprocess

from pytest_pytestrail import pytestrail
from src.utilities import os_utils
from tests import setting
from src.pages.installations import installation_utils
from src.pages.coccoc_common import open_browser
from src.pages.settings import settings_default_browser


# ------------------------------------------------------------------------------------------------------------------
# @pytest.fixture(name='download_file_for_test')
@pytestrail.case("C1086457")
def test_make_coccoc_default(
    setup_file_for_test,
    version=setting.coccoc_test_version,
    language=setting.coccoc_language,
    is_remove_coccoc_after_test=True,
):
    try:
        """INSTALL COCCOC SILENTLY"""
        cmd = rf'cd C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_real_system_arch(is_format=True)}\installers\ && {setup_file_for_test} /silent /forcedcmdline "make-coccoc-default" /install'
        subprocess.check_call(cmd, shell=True)

        # Check browser is installed successfully:
        command_filter_coccoc_pid = (
            "wmic process where " + "'name like '%coccoc%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_coccoc_pid, encoding="utf-8")
        assert "CocCocCrashHandler" in text

        """VERIFY AFTER INSTALL"""
        # Check browser do not launch automatically by check no process name 'browser.exe' is running
        command_filter_browser_exe_pid = (
            "wmic process where " + "'name like '%browser.exe%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_browser_exe_pid, encoding="utf-8")
        assert text != "browser.exe"
        # Start coccoc at least 1 time before checking registry:
        open_browser.open_coccoc_by_pywinauto_then_close_it(is_first_time_opened=True)

        # To verify message default browser:
        settings_default_browser.check_default_browser_text_by_pywinauto(language)

    finally:
        # file_utils.delete_installer_downloaded(build_name=file_to_download_for_test)
        settings_default_browser.set_a_browser_to_default()
        if is_remove_coccoc_after_test:
            installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086460")
def test_with_auto_launch_coccoc(
    setup_file_for_test,
    version=setting.coccoc_test_version,
    is_remove_coccoc_after_test=True,
    language=setting.coccoc_language,
):
    try:
        """INSTALL COCCOC SILENTLY"""
        cmd = rf'cd C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_real_system_arch(is_format=True)}\installers\ && {setup_file_for_test} /silent /forcedcmdline "auto-launch-coccoc" /install'
        subprocess.check_call(cmd, shell=True)

        """VERIFY AFTER INSTALL"""
        # Check browser is installed successfully:
        command_filter_coccoc_pid = (
            "wmic process where " + "'name like '%coccoc%''" + " get Description"
        )
        text_process = subprocess.check_output(
            command_filter_coccoc_pid, encoding="utf-8"
        )
        assert "CocCocCrashHandler" in text_process
        # assert 'CocCocCrashHandler64.exe' in text_process

        # Check browser do not launch automatically by check no process name 'browser.exe' is running
        command_filter_browser_exe_pid = (
            "wmic process where " + "'name like '%browser.exe%''" + " get Description"
        )
        text_browser_exe = subprocess.check_output(
            command_filter_browser_exe_pid, encoding="utf-8"
        )
        assert text_browser_exe != "browser.exe"

        # Check CocCoc is set to run on system startup
        # Start coccoc at least 1 time before checking registry:
        open_browser.open_coccoc_by_pywinauto_then_close_it()
        settings_default_browser.check_start_up_toggle_status_is_on(language)
        assert os_utils.check_coccoc_is_start_up() is True

    finally:
        # pass
        if is_remove_coccoc_after_test:
            installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086466")
def test_combination_params(
    setup_file_for_test,
    version=setting.coccoc_test_version,
    language=setting.coccoc_language,
    is_remove_coccoc_after_test=True,
):
    try:
        """INSTALL COCCOC SILENTLY"""
        cmd = rf'cd C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_real_system_arch(is_format=True)}\installers\ && {setup_file_for_test} /silent /forcedcmdline "do-not-launch-chrome --make-coccoc-default --auto-launch-coccoc" /install'
        subprocess.check_call(cmd, shell=True)

        """VERIFY AFTER INSTALL"""
        # Check browser is installed successfully:
        command_filter_coccoc_pid = (
            "wmic process where " + "'name like '%coccoc%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_coccoc_pid, encoding="utf-8")
        assert "CocCocCrashHandler" in text

        # Check browser do not launch automatically by check no process name 'browser.exe' is running
        command_filter_browser_exe_pid = (
            "wmic process where " + "'name like '%browser.exe%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_browser_exe_pid, encoding="utf-8")
        assert text != "browser.exe"

        # Start coccoc at least 1 time before checking registry:
        open_browser.open_coccoc_by_pywinauto_then_close_it()

        # To verify message default browser:
        settings_default_browser.check_default_browser_text_by_pywinauto(language)

        # Check CocCoc is set to run on system startup
        settings_default_browser.check_start_up_toggle_status_is_on(language)
        assert os_utils.check_coccoc_is_start_up() is True
        # assert os_utils.check_auto_launch_enabled_is_true() is True

    finally:
        # file_utils.delete_installer_downloaded(build_name=file_to_download_for_test)
        settings_default_browser.set_a_browser_to_default()
        if is_remove_coccoc_after_test:
            # installation_utils.uninstall_coccoc_by_control_panel()
            installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086463")
def test_do_not_launch_coccoc_after_installed(
    setup_file_for_test,
    version=setting.coccoc_test_version,
    is_remove_coccoc_after_test=True,
):
    try:
        """INSTALL COCCOC SILENTLY"""
        cmd = rf'cd C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_real_system_arch(is_format=True)}\installers\ && {setup_file_for_test} /silent /forcedcmdline "do-not-launch-chrome" /install'
        subprocess.check_call(cmd, shell=True)

        """VERIFY AFTER INSTALL"""
        command_filter_coccoc_pid = (
            "wmic process where " + "'name like '%coccoc%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_coccoc_pid, encoding="utf-8")
        assert "CocCocCrashHandler" in text
        # assert 'CocCocCrashHandler64.exe' in text

        # Check browser do not launch automatically by check no process name 'browser.exe' is running
        command_filter_browser_exe_pid = (
            "wmic process where " + "'name like '%browser.exe%''" + " get Description"
        )
        text = subprocess.check_output(command_filter_browser_exe_pid, encoding="utf-8")
        assert text != "browser.exe"
    finally:
        if is_remove_coccoc_after_test:
            installation_utils.uninstall_coccoc_silently()
