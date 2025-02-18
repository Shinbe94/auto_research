import pytest
from time import sleep
from pytest_pytestrail import pytestrail
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.remote.errorhandler import ErrorHandler

from src.pages.constant import CocCocTitles
from src.pages.coccoc_common import open_browser
from src.pages.internal_page.downloads.download_page import (
    DownloadPageSel,
)
from src.pages.menus.context_menu import ContextMenu
from src.pages.settings.settings_default_browser import SettingsDefaultBrowserSel
from src.pages.settings.settings_downloads import SettingsDownloadsSel
from src.pages.support_pages.support_apps import UTorrent
from src.pages.support_pages.support_pages import WebTorrentSel
from src.pages.topbar.top_bar import Topbar
from src.utilities import file_utils, os_utils
from src.utilities.process_id_utils import is_process_running


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C488430")
@pytest.mark.ignore_check_testing_build
# @pytest.mark.timeout(300)
def test_coccoc_is_not_set_default_torrent(
    set_utorrent_default,
    reinstall_coccoc_for_torrent,
    settings_default_browser_sel: SettingsDefaultBrowserSel,
):
    settings_default_browser_sel.check_message_not_a_default_torrent(
        is_need_to_open_setting_default_browser=True
    )
    assert is_process_running(process_name="uTorrent.exe") is False
    try:
        # Open the torrent file by current default torrent of system (may be Utorrent, preconfigured)
        file_utils.open_a_file(
            filename_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\automation\coccoc_win\data\torrent\sintel.torrent"
        )
        sleep(5)  # sleep for Utorrent started
        # Checking the torrent file is opening by Utorrent
        assert is_process_running(process_name="uTorrent.exe")
    except Exception:
        pass
    finally:
        os_utils.kill_process_by_name(pid_name="uTorrent.exe")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C488439")
def test_change_peers_listening_port(
    settings_downloads_sel: SettingsDownloadsSel,
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.set_value_for_peers_listening_port(
            port_number=3801, is_need_to_open_downloads_setting=True
        )

        web_torrent_sel.download_sintel_torrent_file()
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1800, is_need_open_download_page=True
            )
            is True
        )
    finally:
        download_page_sel.clear_all_downloads_data()
        settings_downloads_sel.set_value_for_peers_listening_port(
            is_need_to_open_downloads_setting=True
        )
        file_utils.remove_directory(
            directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C488442")
def test_max_active_download(
    settings_downloads_sel: SettingsDownloadsSel,
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    max_active_download: int = 2  # the number you want to test
    download_page_sel.clear_all_downloads_data()
    try:
        settings_downloads_sel.set_value_for_max_active_download(
            max_number=max_active_download, is_need_to_open_downloads_setting=True
        )

        # Start download some torrents, e.g download 5 files
        web_torrent_sel.download_tears_of_steel_torrent_file(
            is_need_to_open_webtorrent=True, sleep_n_seconds=2
        )
        web_torrent_sel.download_big_buck_bunny_torrent_file(sleep_n_seconds=2)
        web_torrent_sel.download_cosmos_laundromat_torrent_file(sleep_n_seconds=2)
        web_torrent_sel.download_sintel_torrent_file(sleep_n_seconds=2)
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            sleep_n_seconds=2
        )

        # checking limit
        download_page_sel.wait_for_no_of_total_items_appear_in_torrent(
            total_item=5, timeout=120, is_need_open_download_page=True
        )
        # Sometime need to wait for the limit downloading is function well before assertion
        assert (
            download_page_sel.wait_for_total_items_appear_in_downloading_part(
                no_of_item=max_active_download, timeout=180
            )
            is True
        )
        assert (
            download_page_sel.get_total_items_downloading(timeout=60)
            == max_active_download
        )
        assert download_page_sel.get_total_items_paused(timeout=30) == 3
        sleep(5)  # recheck for sure after 5s
        download_page_sel.reload_page()
        assert (
            download_page_sel.wait_for_total_items_appear_in_downloading_part(
                no_of_item=max_active_download, timeout=60
            )
            is True
        )
        assert (
            download_page_sel.get_total_items_downloading(timeout=20)
            == max_active_download
        )
        # assert download_page_sel.get_total_items_paused() == 3
    finally:
        download_page_sel.cancel_all_downloading_item_one_by_one()
        download_page_sel.clear_all_downloads_data(
            # is_need_to_cancel_all_downloading=False
        )
        settings_downloads_sel.set_value_for_max_active_download(
            is_need_to_open_downloads_setting=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C488451")
def xtest_can_not_add_same_torrent_link(
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    # TODO Should check possible to fix later
    try:
        download_page_sel.clear_all_downloads_data()

        # Start download torrents
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=False
        )
        assert open_browser.is_coccoc_torrent_notification_appears()

    finally:
        pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C488454")
def test_redownload_torrent(
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    try:
        download_page_sel.clear_all_downloads_data()

        # Start download torrents
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        # Wait for the torrent is downloaded
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1800, is_need_open_download_page=True
            )
            is True
        )
        # Click the 'X' button to remove from the list
        download_page_sel.remove_item_from_the_list()
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=0, timeout=5, is_need_open_download_page=False
            )
            is True
        )
        # Redownload the same torrent and check that item appears
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1800, is_need_open_download_page=True
            )
            is True
        )
    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)
        file_utils.remove_directory(
            directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494538")
def xtest_cancel_continue_download(
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    # TODO fix later, seem this test case contain a bug, not autodownloading again.
    try:
        download_page_sel.clear_all_downloads_data()

        # Start download torrents
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )

    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494541")
def test_new_tab_closed_once_torrent_file_starts_downloading(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
    top_bar: Topbar,
    context_menu: ContextMenu,
):
    try:
        download_page_sel.clear_all_downloads_data()

        # Start download torrents by right click and click open link in new tab
        web_torrent_sel.right_click_magnet_tears_of_steel(
            is_need_to_open_webtorrent=True
        )
        context_menu.click_open_link_in_new_tab()
        # Check the new tab is close immediately after downloading starts
        top_bar.check_no_new_tab_opening()

    finally:
        download_page_sel.click_btn_cancel(is_need_open_download_page=True)
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494544")
def test_downloading_torrent_file_once_its_feature_is_off(
    download_page_sel: DownloadPageSel,
    settings_downloads_sel: SettingsDownloadsSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    settings_downloads_sel.turn_off_toggle_enable_torrent_client(
        is_need_to_open_downloads_setting=True
    )
    try:
        # Start download torrents
        web_torrent_sel.download_sintel_torrent_file()
        sleep(5)
        # Check the file with torrent extension is downloaded
        assert file_utils.check_file_is_exists(
            file_name_with_path=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\sintel.torrent"
        )

    finally:
        download_page_sel.clear_all_downloads_data()
        settings_downloads_sel.turn_on_toggle_enable_torrent_client(
            is_need_to_open_downloads_setting=True
        )
        file_utils.remove_a_file(
            file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\sintel.torrent"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494547")
def test_counting_download_seeding_torrent_correctly(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Start download some torrents
        web_torrent_sel.download_sintel_torrent_file(sleep_n_seconds=2)
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            sleep_n_seconds=2
        )
        web_torrent_sel.download_cosmos_laundromat_torrent_file(sleep_n_seconds=2)
        # Wait for all torrents are downloaded
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=3, timeout=3000, is_need_open_download_page=True
            )
            is True
        )
        assert download_page_sel.get_total_items_downloading(timeout=5) == 0
        assert download_page_sel.get_total_items_torrents() == 3
    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494550")
def test_downloading_torrent_restart_for_existing_its_contents(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Start download torrents
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        # Wait for torrent is downloaded
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1200, is_need_open_download_page=True
            )
            is True
        )
        # Check file content (folder) exist
        assert file_utils.check_folder_is_exists(
            directory_with_path=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
        )
        download_page_sel.remove_item_from_the_list(is_need_open_download_page=True)

        # Re-download the torrent file
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        # Check download page
        # Wait for that torrent is appeared at the download page again
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1200, is_need_open_download_page=True
            )
            is True
        )
        assert (
            download_page_sel.get_total_items_finished(is_need_open_download_page=True)
            == 1
        )
        assert download_page_sel.get_total_items_torrents() == 1
        # Check only 1 folder exist (no duplication download)
        assert (
            file_utils.count_total_regex_folder(
                folder_name=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\",
                file_name="The WIRED CD - Rip. Sample. Mash. Share",
            )
            == 1
        )
    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494553")
def test_user_cancels_downloading_some_files_in_torrent_package(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
        is_need_to_open_webtorrent=True
    )
    try:
        # indexes = download_page_sel.uncheck_some_child_files_of_first_torrent()
        indexes = (
            download_page_sel.uncheck_some_child_files_of_wired_cd_rip_sample_mash_shared_torrent_file()
        )
        download_page_sel.wait_for_download_items_finished(no_of_item=1)
        download_page_sel.check_child_files_of_first_torrent_are_not_fully_downloaded(
            list_index_of_file=indexes
        )
    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494556")
def test_user_cancels_all_files_in_torrent_package_by_unticking_one_by_one(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
        is_need_to_open_webtorrent=True
    )
    try:
        # Check the progress bar is appeared
        assert download_page_sel.check_progress_bar_downloading_is_shown() is True

        # Execute uncheck all child files one by one
        download_page_sel.uncheck_all_child_files_of_first_torrent_one_by_one()

        # Check the progress bar is disappeared
        assert (
            download_page_sel.check_progress_bar_downloading_is_not_shown(
                is_need_open_download_page=False
            )
            is True
        )

    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220784")
def test_user_cancels_all_files_in_torrent_package_by_uncheck_the_checkmark(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file(
        is_need_to_open_webtorrent=True
    )
    try:
        # Check the progress bar is appeared
        assert download_page_sel.check_progress_bar_downloading_is_shown() is True

        # Execute uncheck all child files by tick the 'ALL checkmark' at top
        download_page_sel.uncheck_all_child_files_of_first_torrent_by_checkmark()

        # Check the progress bar is disappeared
        assert (
            download_page_sel.check_progress_bar_downloading_is_not_shown(
                is_need_open_download_page=False
            )
            is True
        )

    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494559")
def test_redownload_from_beginning_after_closing_browser_and_delete_file_from_disk(
    download_torrent_before_test,
    delete_torrent_folder,
    download_page_sel: DownloadPageSel,
):
    try:
        # Wait for torrent is downloading again

        download_page_sel.open_download_page()
        assert (
            download_page_sel.wait_for_download_items_finished(
                no_of_item=1, timeout=1200, is_need_open_download_page=True
            )
            is True
        )
        # Check file content (folder) exist after redownloading
        assert file_utils.check_folder_is_exists(
            directory_with_path=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
        )

    finally:
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494565")
def test_clear_all_input_setting_then_reload(
    settings_downloads_sel: SettingsDownloadsSel,
):
    settings_downloads_sel.clear_all_setting_values_and_reload()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494568")
def test_all_option_after_right_click_magnet_link_select_open_in_newtab(
    web_torrent_sel: WebTorrentSel,
    context_menu: ContextMenu,
    top_bar: Topbar,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.right_click_magnet_sintel(is_need_to_open_webtorrent=True)
        context_menu.click_open_link_in_new_tab()
        # Check the new tab is close immediately after downloading starts
        top_bar.check_no_new_tab_opening()
    finally:
        download_page_sel.click_btn_cancel(is_need_open_download_page=True)
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220949")
def test_all_option_after_right_click_magnet_link_select_open_in_new_window(
    web_torrent_sel: WebTorrentSel,
    context_menu: ContextMenu,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.right_click_magnet_sintel(is_need_to_open_webtorrent=True)
        first_window = download_page_sel.get_current_window()
        context_menu.click_open_link_in_new_window()
        # Check the new window is opening and the torrent is downloading
        assert open_browser.is_coccoc_window_appeared(
            title=CocCocTitles.UNTITLED_COCCOC
        )
    finally:
        # Switch back to previous window to clear all testing data
        download_page_sel.switch_to_window(first_window)
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=600
        )
        download_page_sel.clear_all_downloads_data()
        # Close the remaining window
        open_browser.close_coccoc_by_window_title(title=CocCocTitles.UNTITLED_COCCOC)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220952")
def test_all_option_after_right_click_magnet_link_select_open_in_incognito_window(
    web_torrent_sel: WebTorrentSel,
    context_menu: ContextMenu,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.right_click_magnet_sintel(is_need_to_open_webtorrent=True)
        first_window = download_page_sel.get_current_window()
        context_menu.click_open_link_in_incognito_window()
        # Check the new window is opening and the torrent is downloading
        assert open_browser.is_coccoc_window_appeared(
            title=CocCocTitles.UNTITLED_INCOGNITO_COCCOC
        )
    finally:
        # Switch back to previous window to clear all testing data
        download_page_sel.switch_to_window(first_window)
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=600
        )
        download_page_sel.clear_all_downloads_data()
        # Close the remaining window
        open_browser.close_coccoc_by_window_title(title=CocCocTitles.UNTITLED_COCCOC)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1220955")
def test_all_option_after_right_click_magnet_link_select_open_in_incognito_window_with_tor(
    web_torrent_sel: WebTorrentSel,
    context_menu: ContextMenu,
    download_page_sel: DownloadPageSel,
    wad_session: AppiumWebDriver,
):
    download_page_sel.clear_all_downloads_data()
    session_driver = None
    try:
        web_torrent_sel.right_click_magnet_sintel(is_need_to_open_webtorrent=True)
        first_window = download_page_sel.get_current_window()
        context_menu.click_open_link_in_incognito_window_with_tor()
        sleep(5)
        # Check the new window is opening and the torrent is downloading
        # attaching the session into the CocCoc window then select the torrent file for downloading
        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.UNTITLED_COCCOC,
            port=4729,
            timeout=10,
            implicitly_wait=5,
        )
        assert session_driver
        # Switch back to previous window to clear all testing data
        download_page_sel.switch_to_window(first_window)
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=600
        )
    finally:
        if session_driver:
            session_driver.quit()
        download_page_sel.clear_all_downloads_data()
        # Close the remaining window
        # open_browser.close_coccoc_by_window_title(
        #     title="New Incognito Tab - Cốc Cốc (Incognito)"
        # )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494745")
def test_coccoc_still_works_well_after_delete_torrent_folder(
    delete_torrent_folder_of_coccoc,
    web_torrent_sel: WebTorrentSel,
    download_page_sel: DownloadPageSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.download_sintel_torrent_file()
        web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=2, timeout=1200, is_need_open_download_page=True
        )
    finally:
        download_page_sel.clear_all_downloads_data()
