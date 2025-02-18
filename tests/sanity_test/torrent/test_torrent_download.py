from time import sleep
import pytest
from pytest_pytestrail import pytestrail
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webdriver import WebDriver
from src.pages.coccoc_common import open_browser

from src.pages.constant import CocCocTitles
from src.pages.dialogs.profiles import Profiles
from src.pages.internal_page.downloads.download_page import (
    DownloadPageAppium,
    DownloadPageSel,
)
from src.pages.menus.context_menu import ContextMenu
from src.pages.support_pages.support_pages import (
    DownloadTestItim,
    WebTorrentSel,
)
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import file_utils, os_utils, windows_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54208")
def test_download_from_torrent_file(
    download_page_sel: DownloadPageSel,
    wad_session: AppiumWebDriver,
):
    download_page_sel.clear_all_downloads_data()

    try:
        # Click btn add torrent and select the file to open for downloading
        download_page_sel.click_btn_add_torrent()

        # attaching the session into the CocCoc window then select the torrent file for downloading
        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        dpa = DownloadPageAppium(session_driver)
        dpa.set_value_into_file_name(
            filename_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\automation\coccoc_win\data\torrent\wired-cd.torrent"
        )
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=600
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54209")
def test_pause_resume_torrent_file(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Download a torrent
        web_torrent_sel.download_sintel_torrent_file()

        # click to pause btn and check that item is appeared on Paused section
        download_page_sel.click_btn_pause_of_item(is_need_open_download_page=True)
        assert download_page_sel.wait_for_no_of_total_items_appear_in_paused(
            total_item=1, timeout=60
        )
        # click to resume btn
        download_page_sel.click_btn_resume_of_item()
        assert download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, timeout=180
        )
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=600
        )

    finally:
        # clear all download data
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54210")
def xtest_from_magnet_link(
    download_page_sel: DownloadPageSel,
    wad_session: AppiumWebDriver,
):
    # TODO Should break and script later
    download_page_sel.clear_all_downloads_data()

    try:
        # Click btn add torrent and select the file to open for downloading
        download_page_sel.click_btn_add_torrent()

        # attaching the session into the CocCoc window then select the torrent file for downloading
        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        dpa = DownloadPageAppium(session_driver)
        dpa.set_value_into_file_name(
            filename_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\automation\coccoc_win\data\torrent\wired-cd.torrent"
        )
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494574")
def test_add_magnet_link_function_well(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
    context_menu: ContextMenu,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Right click then copied the magnet_link then save to variable by using tkinter module
        web_torrent_sel.right_click_magnet_sintel(is_need_to_open_webtorrent=True)
        context_menu.click_copy_link_address()
        magnet_link_copied = os_utils.get_clipboard_text()
        download_page_sel.set_magnet_link(
            magnet_link=magnet_link_copied, sleep_n_seconds=3
        )
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1,
            timeout=setting.timeout_for_waiting_download_small_file_size,
            is_need_open_download_page=True,
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221138")
def test_copy_magnet_link_and_redownload(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    # clear all download data
    download_page_sel.clear_all_downloads_data()
    # try to download a torrent completely
    web_torrent_sel.download_sintel_torrent_file()
    download_page_sel.wait_for_download_items_finished(
        no_of_item=1,
        timeout=setting.timeout_for_waiting_download_small_file_size,
        is_need_open_download_page=True,
    )
    first_window = download_page_sel.get_current_window()
    try:
        # Right click then copied the magnet_link then save to variable by using tkinter module
        download_page_sel.click_copy_link_of_item()
        magnet_link_copied = os_utils.get_clipboard_text()

        # Try to add the magnet link & check duplicate (only 1 item)
        download_page_sel.set_magnet_link(magnet_link=magnet_link_copied)
        download_page_sel.switch_to_window(first_window)
        assert download_page_sel.get_total_items_all() == 1

        # Switch to download page, clear downloaded data and recheck the redownloading is done after Add magnet link again
        download_page_sel.switch_to_window(first_window)
        download_page_sel.clear_all_downloads_data(is_need_open_download_page=True)

        # Remove the downloaded file
        file_utils.remove_directory(
            directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
        )
        # check the redownloading is done after Add magnet link again

        download_page_sel.set_magnet_link(magnet_link=magnet_link_copied)
        download_page_sel.switch_to_window(first_window)  # switch to download page
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=setting.timeout_for_waiting_download_small_file_size
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494577")
def xtest_torrent_download_tree_view(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    # TODO fix later
    # clear all download data
    # download_page_sel.clear_all_downloads_data()
    # # try to download a torrent completely
    # web_torrent_sel.download_wired_cd_rip_sample_mash_shared_torrent_file()
    # try:
    #     download_page_sel.click_to_show_all_child_file_of_first_torrent()
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494580")
def test_context_menu_downloading_file_from_torrent_link(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    # clear all download data
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.download_sintel_torrent_file()
        download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1,
            timeout=setting.timeout_for_waiting_download_small_file_size,
            is_need_open_download_page=True,
        )
        # check during downloading
        download_page_sel.click_btn_3dots_of_item()
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_when_done()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_download_limit()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )
        # Wait for the downloading is done
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=setting.timeout_for_waiting_download_small_file_size
        )
        download_page_sel.reload_page()
        download_page_sel.click_btn_3dots_of_item()

        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_remove_from_disk()
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_when_done(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_download_limit(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )
        assert download_page_sel.is_element_appeared(
            download_page_sel.item_donot_seed_checkbox()
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221267")
def test_context_menu_downloading_file_from_magnet_link(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
):
    # clear all download data
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.download_sintel_magnet_link()
        download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1,
            timeout=setting.timeout_for_waiting_download_small_file_size,
            is_need_open_download_page=True,
        )
        # check during downloading
        download_page_sel.click_btn_3dots_of_item()
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page(
                is_need_open_download_page=False
            )
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_when_done()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_download_limit()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )
        # Wait for the downloading is done
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=setting.timeout_for_waiting_download_small_file_size
        )
        download_page_sel.reload_page()
        download_page_sel.click_btn_3dots_of_item()

        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page()
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_when_done(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_remove_from_disk()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_download_limit(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )
        assert download_page_sel.is_element_appeared(
            download_page_sel.item_donot_seed_checkbox()
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221237")
def test_context_menu_downloading_file_from_torrent_file(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
    wad_session: AppiumWebDriver,
):
    # clear all download data
    download_page_sel.clear_all_downloads_data()
    try:
        # Click btn add torrent and select the file to open for downloading
        download_page_sel.click_btn_add_torrent()

        # attaching the session into the CocCoc window then select the torrent file for downloading
        session_driver: AppiumWebDriver = wad_session(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
            port=4729,
            timeout=5,
            implicitly_wait=5,
        )
        dpa = DownloadPageAppium(session_driver)
        dpa.set_value_into_file_name(
            filename_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\automation\coccoc_win\data\torrent\wired-cd.torrent"
        )
        download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1,
            timeout=setting.timeout_for_waiting_download_small_file_size,
            is_need_open_download_page=True,
        )
        # check during downloading
        download_page_sel.click_btn_3dots_of_item()
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_source_page(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_when_done()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_download_limit()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )

        # Wait for the downloading is done and checking
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=setting.timeout_for_waiting_download_small_file_size
        )
        download_page_sel.reload_page()
        download_page_sel.click_btn_3dots_of_item()

        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_source_page(), timeout=2
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_when_done(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_remove_from_disk()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_download_limit(), timeout=2
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_upload_limit()
        )

        assert download_page_sel.is_element_appeared(
            download_page_sel.item_donot_seed_checkbox()
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221264")
def test_context_menu_downloading_other_file_type(
    download_page_sel: DownloadPageSel,
    download_test_itim: DownloadTestItim,
):
    # clear all download data
    download_page_sel.clear_all_downloads_data()
    try:
        # Download a file
        download_test_itim.download_100mb_file()

        # Wait for the file is appeared at downloading part
        download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1,
            timeout=setting.timeout_for_waiting_download_small_file_size,
            is_need_open_download_page=True,
        )
        # check during downloading
        download_page_sel.click_3dot_of_item()
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_when_done()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )

        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_download_limit(), timeout=2
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_upload_limit(), timeout=2
        )

        # Wait for the downloading is done and checking
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, timeout=setting.timeout_for_waiting_download_small_file_size
        )
        download_page_sel.reload_page()
        download_page_sel.click_3dot_of_item()

        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_open_source_page()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_remove_from_disk()
        )
        assert download_page_sel.is_element_appeared(
            by_locator=download_page_sel.item_copy_link()
        )

        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_open_when_done(), timeout=2
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_download_limit(), timeout=2
        )
        assert download_page_sel.is_element_disappeared(
            by_locator=download_page_sel.item_upload_limit(), timeout=2
        )
        assert download_page_sel.is_element_disappeared(
            download_page_sel.item_donot_seed_checkbox(), timeout=2
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494697")
def xtest_downloading_when_reopening_multiple_profiles(
    download_page_sel: DownloadPageSel,
    download_test_itim: DownloadTestItim,
):
    # TODO fix later
    # clear all download data
    # download_page_sel.clear_all_downloads_data()
    # try:
    #     # Download a file
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C730787")
def test_no_crashes_happened_when_downloading_torrent_from_multiple_profiles(
    create_new_profile_test_torrent,
    sc: WebDriver,
    sc2: WebDriver,
    wad_session: AppiumWebDriver,
    wad_session2: AppiumWebDriver,
):
    wts1 = WebTorrentSel(sc)  # WebTorrentSel with driver_1 (default profile)
    dps1 = DownloadPageSel(sc)  # DownloadPageSel with driver_1 (default profile)
    wts2 = WebTorrentSel(sc2)  # WebTorrentSel with driver_2 (Profile 1)
    dps2 = DownloadPageSel(sc2)  # DownloadPageSel with driver_2 (Profile 1)
    try:
        dps1.clear_all_downloads_data()
        wts1.download_sintel_torrent_file()
        dps2.clear_all_downloads_data()
        wts2.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        dps1.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps1.clear_all_downloads_data()
        dps2.clear_all_downloads_data()
        sc.quit()
        sc2.quit()
        sleep(1)

        # Remove the Profile 1
        open_browser.open_coccoc_by_pywinauto()

        # attaching the session2 into the Manage Profile dialog then remove Profile 2
        session_driver2: AppiumWebDriver = wad_session2(
            title=r"Cốc Cốc",
            port=4730,
            is_exact_name=True,
            timeout=5,
            implicitly_wait=5,
        )
        pd = Profiles(session_driver2)
        pd.click_delete_profile_completely(profile_name="Person 2")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C745585")
def test_no_crashes_when_add_remove_profile(
    create_new_profile_test_torrent,
    sc,
    sc2,
    wad_session: AppiumWebDriver,
    wad_session2: AppiumWebDriver,
):
    wts1 = WebTorrentSel(sc)  # WebTorrentSel with driver_1 (default profile)
    dps1 = DownloadPageSel(sc)  # DownloadPageSel with driver_1 (default profile)
    wts2 = WebTorrentSel(sc2)  # WebTorrentSel with driver_2 (Profile 1)
    dps2 = DownloadPageSel(sc2)  # DownloadPageSel with driver_2 (Profile 1)

    try:
        # Execute download torrent from 2 profiles
        dps1.clear_all_downloads_data()
        wts1.download_sintel_torrent_file()
        dps2.clear_all_downloads_data()
        wts2.download_wired_cd_rip_sample_mash_shared_torrent_file(
            is_need_to_open_webtorrent=True
        )
        assert dps1.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        assert dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )

    finally:
        # clear all download data
        dps1.clear_all_downloads_data()
        dps2.clear_all_downloads_data()

        # Quit all 2 profiles
        sc.quit()
        sc2.quit()
        sleep(2)

        # Remove profile 2
        open_browser.open_coccoc_by_pywinauto()  # Open Default profile

        # attaching the session1 into the CocCoc Default profile then open the Manage Profile dialog
        # session_driver: AppiumWebDriver = wad_session(
        #     title=CocCocTitles.NEW_TAB_TITLE,
        #     port=4729,
        #     timeout=5,
        #     implicitly_wait=5,
        # )
        # tb = Toolbar(session_driver)
        # tb.click_person_1_btn()
        # tb.click_manage_profiles()

        # attaching the session2 into the Manage Profile dialog then remove Profile 2
        session_driver2: AppiumWebDriver = wad_session2(
            title=r"Cốc Cốc",
            port=4730,
            is_exact_name=True,
            timeout=5,
            implicitly_wait=5,
        )
        pd = Profiles(session_driver2)
        pd.click_delete_profile_completely(profile_name="Person 2")

        # Open the Person 1
        pd.click_to_open_coccoc_by_profile_name(person_name="Person 1")
        assert open_browser.is_coccoc_window_appeared(title=CocCocTitles.NEW_TAB_TITLE)

        # TODO should check this case, as currently we got a bug, no torrent item at download page when multiple profiles download https://coccoc.atlassian.net/browse/BR-3701
        # dps1.clear_all_downloads_data()
        # dps2.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1013274")
def test_remove_from_disk_torrent_file(
    download_page_sel: DownloadPageSel, web_torrent_sel: WebTorrentSel, lang
):
    download_page_sel.clear_all_downloads_data()
    try:
        web_torrent_sel.download_sintel_torrent_file()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        # Click to show in folder and check the folder is opened
        download_page_sel.click_show_in_folder_of_item()
        assert os_utils.is_window_explorer_appeared(window_name="Downloads", timeout=10)
        windows_utils.close_window_by_its_name(
            window_name="Downloads", class_name="CabinetWClass"
        )

        # Remove from disk
        download_page_sel.click_remove_file_from_disk()
        download_page_sel.reload_page()
        if "en" in lang:
            assert (
                download_page_sel.get_torrent_download_item_status_torrent()
                == "Removed"
            )
        else:
            assert (
                download_page_sel.get_torrent_download_item_status_torrent() == "Đã xóa"
            )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C833220")
def test_magnet_link_incognito_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_incognito=True
        )[0]
    )
    try:
        wts = WebTorrentSel(driver)  # WebTorrentSel with driver_1 (default profile)
        dps = DownloadPageSel(driver)  # DownloadPageSel with driver_1 (default profile)
        dps.clear_all_downloads_data()
        wts.download_sintel_magnet_link()
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221627")
def test_add_link_incognito_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_incognito=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        dps.clear_all_downloads_data()
        first_window = driver.current_window_handle
        dps.set_magnet_link(magnet_link=setting.MAGNET_SINTEL)
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        driver.switch_to.window(first_window)
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221630")
def test_download_torrent_incognito_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_incognito=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        wts = WebTorrentSel(driver)
        dps.clear_all_downloads_data()
        wts.download_sintel_torrent_file()
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221633")
def test_download_torrent_incognito_window_by_enter_link_url():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_incognito=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        wts = WebTorrentSel(driver)
        dps.clear_all_downloads_data()
        driver.get(setting.MAGNET_SINTEL)
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221636")
def test_magnet_link_tor_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_tor=True
        )[0]
    )
    try:
        wts = WebTorrentSel(driver)  # WebTorrentSel with driver_1 (default profile)
        dps = DownloadPageSel(driver)  # DownloadPageSel with driver_1 (default profile)
        dps.clear_all_downloads_data()
        wts.download_sintel_magnet_link()
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221639")
def test_add_link_tor_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_tor=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        dps.clear_all_downloads_data()
        first_window = driver.current_window_handle
        dps.set_magnet_link(magnet_link=setting.MAGNET_SINTEL)
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        driver.switch_to.window(first_window)
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221642")
def test_download_torrent_tor_window():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_tor=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        wts = WebTorrentSel(driver)
        dps.clear_all_downloads_data()
        wts.download_sintel_torrent_file()
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221645")
def test_download_torrent_tor_window_by_enter_link_url():
    driver: WebDriver = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(
            is_tor=True
        )[0]
    )
    try:
        dps = DownloadPageSel(driver)
        wts = WebTorrentSel(driver)
        dps.clear_all_downloads_data()
        driver.get(setting.MAGNET_SINTEL)
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(10)
    finally:
        driver.quit()  # Quit browser
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )
        sleep(2)
    # reopen coccoc browser and checking
    driver2 = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()[0]
    dps2 = DownloadPageSel(driver2)
    try:
        dps2.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
    finally:
        dps2.clear_all_downloads_data()
        driver2.quit()
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE, is_exact_name=True
        )


@pytest.mark.profile_1
def xtest_multiple_profiles(
    download_page_sel: DownloadPageSel,
    download_page_sel2: DownloadPageSel,
):
    download_page_sel.open_page(url="https://tinhte.vn")
    download_page_sel2.open_page(url="https://google.com")
    sleep(10)


@pytest.mark.profile_1
def xtest_multiple_profiles2(
    sc,
    sc2
    # download_page_sel2: DownloadPageSel,
):
    # download_page_sel.open_page(url="https://tinhte.vn")
    # download_page_sel2.open_page(url="https://google.com")
    sleep(10)
    page_1 = DownloadPageSel(sc)
    page_2 = DownloadPageSel(sc2)
    page_1.open_page(url="https://translate.google.com/")
    page_2.open_page(url="https://google.com")
    sleep(50)


def xtest_window_appeared():
    assert os_utils.is_window_explorer_appeared(window_name="Do3wnloads1", timeout=2)


def xtest_edit_profile(
    # wad_app,
    wad_session: AppiumWebDriver,
):
    # sleep(10)
    # driver = wad_app(port=4731, app_path=open_browser.get_coccoc_executable_path())
    # pd = Profiles(driver)
    # pd.
    open_browser.open_coccoc_by_pywinauto()
    # attaching the session into the CocCoc window then select the torrent file for downloading
    session_driver: AppiumWebDriver = wad_session(
        title=r"Cốc Cốc",
        port=4729,
        timeout=5,
        implicitly_wait=5,
    )
    tb = Toolbar(session_driver)
    tb.click_you_btn()
    tb.click_manage_profiles()
    pd = Profiles(session_driver)
    pd.click_delete_profile_completely(profile_name="Person 2")
