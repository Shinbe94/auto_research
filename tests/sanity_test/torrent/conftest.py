import pytest
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles

from src.pages.installations import installation_page, installation_utils
from src.pages.internal_page.downloads.download_page import DownloadPageSel
from src.pages.support_pages.support_apps import (
    UTorrent,
    start_utorrent,
    utorrent_driver,
)
from src.pages.support_pages.support_pages import WebTorrentSel
from src.utilities import file_utils, os_utils, browser_utils
from tests import setting

installation = installation_page.InstallationPage()


@pytest.fixture(autouse=False)
def uninstall_coccoc_for_torrent():
    installation_utils.uninstall_coccoc_silently()


@pytest.fixture(autouse=False)
def reinstall_coccoc_for_torrent():
    """Execute uninstall the current coccoc if any then reinstall the testing verion"""
    installation_utils.uninstall_coccoc_silently()
    installation.install_coccoc_by_build_name(
        language=setting.coccoc_language, build_name=setting.coccoc_build_name
    )


@pytest.fixture(autouse=True)
def delete_file_before_test():
    file_utils.remove_directory(
        directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Big Buck Bunny"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Tears of Steel"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Cosmos Laundromat"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\100MB.bin"
    )
    yield
    file_utils.remove_directory(
        directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Big Buck Bunny"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Tears of Steel"
    )
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\Cosmos Laundromat"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\100MB.bin"
    )


@pytest.fixture(autouse=True)
def delete_torrent_files_before_test():
    file_utils.remove_a_file(
        file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\sintel.torrent"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\wired-cd.torrent"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\tears-of-steel.torrent"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\big-buck-bunny.torrent"
    )
    file_utils.remove_a_file(
        file_name=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\cosmos-laundromat.torrent"
    )


@pytest.fixture(autouse=False)
def download_torrent_before_test(scc2):
    wts = WebTorrentSel(scc2)
    dlp = DownloadPageSel(scc2)
    try:
        dlp.clear_all_downloads_data()
        wts.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )

        # Wait for torrent is downloaded
        assert (
            dlp.wait_for_total_items_appear_in_downloading_part(
                no_of_item=1, timeout=1200, is_need_open_download_page=True
            )
            is True
        )
    finally:
        # scc2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE
        )


@pytest.fixture(autouse=False)
def delete_torrent_folder():
    # Delete downloaded folder
    file_utils.remove_directory(
        directory=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
    )


@pytest.fixture(autouse=True)
def delete_parts_files():
    """
    To delete the '.parts' file created by torrent if any
    before and after test
    :return:
    """
    file_utils.delete_all_files_with_same_extension(extension=".parts")
    yield
    file_utils.delete_all_files_with_same_extension(extension=".parts")


@pytest.fixture(autouse=True)
def close_win_app_driver():
    yield
    try:
        os_utils.kill_process_by_name("WinAppDriver.exe")
    except Exception as e:
        raise e


@pytest.fixture(autouse=False)
def delete_torrent_folder_of_coccoc():
    """To Delete a torrent folder
    Then execute test
    finally: check torrent folder is created automatically again
    """
    if file_utils.check_folder_is_exists(
        directory_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\torrent"
    ):
        file_utils.remove_directory(
            directory=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\torrent"
        )
    yield
    assert (
        file_utils.check_folder_is_exists(
            directory_with_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\torrent"
        )
        is True
    )


@pytest.fixture(autouse=False)
def create_new_profile_test_torrent():
    browser_utils.create_new_browser_profile()


@pytest.fixture(autouse=False)
def set_utorrent_default():
    """To set UTorrent as default torrent of system

    Raises:
        e: _description_
    """
    utorrent_session = utorrent_driver(sleep_n_seconds=10)  # start urtorrent session
    driver = utorrent_session[0]
    pid = utorrent_session[1]
    ut = UTorrent(driver)
    try:
        ut.set_utorrent_as_default(
            is_need_to_start_utorrent=False, is_kill_utorrent=False
        )
    finally:
        # Kill utorrent and winappdriver
        try:
            os_utils.kill_process_by_its_id(pid)
            os_utils.kill_process_by_name(pid_name="uTorrent.exe")
        except Exception as e:
            raise e
