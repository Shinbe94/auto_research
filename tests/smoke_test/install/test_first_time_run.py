from time import sleep

import pytest
from pytest_pytestrail import pytestrail
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from src.pages.coccoc_common import open_browser
from src.pages.settings import first_time_run
from src.pages.support_pages.support_pages import VirusTotalApp
from src.pages.toolbar.toolbar import Toolbar
from tests import setting
from src.pages.installations import installation_utils, installation_page
from src.utilities import os_utils, browser_utils

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.is_test_first_time_run
@pytestrail.case("C1086487")
def test_first_time_run():
    try:
        installation.check_coccoc_at_the_first_time_it_run()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytest.mark.install_coccoc
@pytestrail.case("C1086490")
def test_components():
    try:
        browser_utils.kill_all_coccoc_process()
        assert first_time_run.check_components_after_installed()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086493")
@pytest.mark.install_coccoc
def test_task_manager():
    try:
        first_time_run.check_task_manager(language=setting.coccoc_language)
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086496")
@pytest.mark.install_coccoc
def test_extension():
    try:
        first_time_run.check_extension_version_after_installed(
            language=setting.coccoc_language
        )
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086499")
@pytest.mark.install_coccoc
def test_folders_of_coccoc():
    try:
        first_time_run.check_folders_after_installed()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086502")
@pytest.mark.install_coccoc
def test_dictionaries_extension_data_file():
    try:
        first_time_run.check_dictionaries()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skip
@pytest.mark.install_coccoc
@pytestrail.case("C1086508")
def test_no_chromium_or_google_registry():
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skip
@pytest.mark.install_coccoc
@pytestrail.case("C1086511")
def test_browser_logos():
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086514")
@pytest.mark.install_coccoc
def test_browser_version_and_omaha():
    try:
        first_time_run.check_browser_and_omaha_version()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytestrail.case("C1086517")
@pytest.mark.install_coccoc
def test_signatures_for_dll_and_exe_files():
    try:
        first_time_run.check_signatures_for_dll_exe_file()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086520")
@pytest.mark.install_coccoc
def test_task_scheduler_after_installed():
    try:
        first_time_run.check_task_scheduler()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(
    os_utils.get_windows_version() != "11", reason="Windows version is not 11"
)
@pytestrail.case("C1086535")
@pytest.mark.install_coccoc
def test_registry():
    # Reg Query "HKEY_CURRENT_USER\SOFTWARE\Clients\StartMenuInternet"
    # Reg Query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node"
    try:
        first_time_run.check_registry_win11()
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skip
@pytest.mark.install_coccoc
@pytestrail.case("C1086523")
def test_firewall_rule_when_user_allows():
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytest.mark.skip
@pytest.mark.install_coccoc
@pytestrail.case("C1086526")
def test_firewall_rule_when_user_cancel():
    pass


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytest.mark.do_not_install_coccoc
@pytestrail.case("C1086505")
def test_no_warning_by_total_virus(
    setup_file_for_test,
    wad_session: AppiumWebDriver,
    version=setting.coccoc_test_version,
):
    open_browser.close_chrome_by_kill_process()
    try:
        open_browser.open_chrome()
        sleep(3)
        # attaching the session into the CocCoc window then select the torrent file for downloading
        session_driver: AppiumWebDriver = wad_session(
            title="New Tab - Google Chrome",
            port=4729,
            timeout=10,
            implicitly_wait=5,
        )
        tb = Toolbar(session_driver)
        tb.make_search_value(
            search_str="https://virustotal.com/gui/home/upload",
            is_press_enter=True,
            sleep_n_seconds=5,
        )
        vta = VirusTotalApp(session_driver)
        vta.select_file_to_upload(version=version, file_name=setup_file_for_test)

    finally:
        open_browser.close_chrome_by_kill_process()
        installation_utils.uninstall_coccoc_silently()
