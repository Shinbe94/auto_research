from time import sleep
from pytest_pytestrail import pytestrail
from src.pages.internal_page.downloads.download_page import (
    DownloadPageSel,
)
from src.pages.support_pages.support_apps import check_notepad_is_opening
from src.utilities import file_utils, os_utils, windows_utils
from src.pages.support_pages.support_pages import (
    DownloadTestItim,
    WebTorrentSel,
)
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54224")
def test_pause_item(
    download_page_sel: DownloadPageSel,
    download_test_itim: DownloadTestItim,
    toolbar: Toolbar,
):
    try:
        download_page_sel.clear_all_downloads_data()
        download_test_itim.download_100mb_file()
        first_window = download_page_sel.get_current_window()
        toolbar.open_download_page()
        download_page_sel.switch_to_window(first_window)
        download_page_sel.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, timeout=30, is_need_open_download_page=True, sleep_n_seconds=2
        )
        download_page_sel.click_btn_pause_of_item()
        assert download_page_sel.is_element_appeared(
            download_page_sel.item_btn_resume()
        )
        assert download_page_sel.get_total_items_paused() == 1
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54226")
def test_show_in_folder(
    download_page_sel: DownloadPageSel,
    download_test_itim: DownloadTestItim,
):
    try:
        download_page_sel.clear_all_downloads_data()
        download_test_itim.download_100mb_file()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )

        # Click to show in folder and check the folder is opened
        download_page_sel.click_show_in_folder_of_item(sleep_n_seconds=2)
        assert os_utils.is_window_explorer_appeared(window_name="Downloads", timeout=10)
        windows_utils.close_window_by_its_name(
            window_name="Downloads", class_name="CabinetWClass"
        )
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\100MB.bin"
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1221687")
def xtest_cancel_downloading_file(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()
        # Download a file
        download_test_itim.download_100mb_file()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        sleep(4)
        # Click to cancel downloading item then check, item status, btn retry
        download_page_sel.click_btn_cancel(sleep_n_seconds_before_cancel=1)
        # download_page_sel.cancel_all_downloading_item_one_by_one()
        if "en" in lang:
            assert download_page_sel.get_download_item_status() == "Canceled"
        else:
            assert download_page_sel.get_download_item_status() == "Đã hủy"

        assert download_page_sel.is_element_appeared(
            download_page_sel.FIRST_ITEM_RETRY_BTN_XPATH
        )

        # check no file with '.crdownload' exists
        assert (
            file_utils.check_any_file_hold_extension(
                extension_file="crdownload",
                directory=rf"C:\Users\{os_utils.get_username()}\Downloads",
            )
            is False
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54229")
def xtest_retry_download(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim
):
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54230")
def test_open_source_page(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()
        # Download a file
        download_test_itim.download_sample2()
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        current_window = download_page_sel.scc.current_window_handle
        # download_page_sel.click_3dot_first_item(sleep_n_seconds=2)
        download_page_sel.click_open_source_page_of_item()
        for window in download_page_sel.scc.window_handles:
            if window != current_window:
                download_page_sel.scc.switch_to.window(window)
        assert download_page_sel.scc.current_url == "https://download-tests.itim.vn/"

    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494607")
def test_remove_from_list(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()
        # Download a file
        download_test_itim.download_sample2()
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )

        # click the 'X' button to remove from the list
        download_page_sel.click_remove_item_from_the_list()
        assert download_page_sel.get_total_items_all(timeout=2) == 0

        # Check the file is still existed on the disk
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\sample2.xlsx"
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494592")
def test_remove_from_disk(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()
        # Download a file
        download_test_itim.download_sample2()
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )

        # click the 'X' button to remove from the list
        download_page_sel.click_remove_file_from_disk()
        assert download_page_sel.get_total_items_all() == 1

        # check download item status and the Retry btn shows
        if "en" in lang:
            assert download_page_sel.get_download_item_status() == "Removed"
        else:
            assert download_page_sel.get_download_item_status() == "Đã xóa"
        assert download_page_sel.is_element_appeared(download_page_sel.item_btn_retry())
        # Check the file is not existed on the disk
        assert (
            file_utils.check_file_is_exists(
                file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\sample2.xlsx"
            )
            is False
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C127794")
def test_clear_all_downloader(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()

        # Download some files
        download_test_itim.download_1_GB(
            is_open_download_test_item_page=True, sleep_n_seconds=2
        )
        download_test_itim.download_tear_of_steel(sleep_n_seconds=2)
        download_test_itim.download_sample2()
        download_test_itim.download_sample3()

        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=2, is_need_open_download_page=True, timeout=1200
        )

        # click the click 'clear all'
        download_page_sel.clear_all_downloads_data(
            is_need_to_cancel_all_downloading=False
        )
        assert download_page_sel.get_total_items_all() == 2  # remaining items
        # Check downloaded files are still existed
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\sample2.xlsx"
        )
        assert file_utils.check_file_is_exists(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\sample3.docx"
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494595")
def test_download_page_after_delete_file_from_disk(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()

        # Download file
        download_test_itim.download_sample2(is_open_download_test_item_page=True)

        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )

        # Delete file from hard disk
        file_utils.remove_a_file(
            file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\sample2.xlsx"
        )
        assert (
            download_page_sel.get_total_items_all(is_need_open_download_page=True) == 1
        )  # remaining items

        # Check the download item status after deleting from hard disk
        # Also check the 'Retry' btn shows
        if "en" in lang:
            assert download_page_sel.get_download_item_status() == "Removed"
        else:
            assert download_page_sel.get_download_item_status() == "Đã xóa"
        assert download_page_sel.is_element_appeared(download_page_sel.item_btn_retry())
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494598")
def test_open_when_done(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()

        # Download file
        download_test_itim.download_sample_text_large(
            is_open_download_test_item_page=True
        )

        # click 'Open when done'
        download_page_sel.click_open_when_done_of_item(is_need_open_download_page=True)

        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=1, is_need_open_download_page=True, timeout=1200
        )
        # Check the file is opened automatically then close it after that
        assert check_notepad_is_opening(
            window_name="sample text large - Notepad", timeout=120
        )
        # windows_utils.close_window_by_its_name(
        #     window_name="sample text large - Notepad", class_name="Notepad"
        # )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494610")
def test_play_btn_does_not_show(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()

        # Download some files not in Video format
        download_test_itim.download_sample2()
        download_test_itim.download_sample3()
        download_test_itim.download_sample6()
        download_test_itim.download_samplepptx()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=4, is_need_open_download_page=True, timeout=1200
        )

        # Check no btn 'Play' shown (By count total = 0)
        assert (
            download_page_sel.count_total_elements(
                download_page_sel.BTN_PLAY, timeout=5
            )
            == 0
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1222029")
def test_play_btn_show(
    download_page_sel: DownloadPageSel, download_test_itim: DownloadTestItim, lang
):
    try:
        # clean download data
        download_page_sel.clear_all_downloads_data()

        # Download some files in Video format and wait for finished
        download_test_itim.download_running_on_empty()
        download_test_itim.download_file_example_webm()
        download_page_sel.wait_for_download_items_finished(
            no_of_item=2, is_need_open_download_page=True, timeout=1200
        )

        # Check btn 'Play' shown (By count total play btn show)
        assert (
            download_page_sel.count_total_elements(
                download_page_sel.BTN_PLAY, timeout=5
            )
            == 2
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494619")
def test_do_not_continue_download_if_reopen_browser(
    download_some_files_for_test,
    download_page_sel: DownloadPageSel,
):
    try:
        assert (
            download_page_sel.get_total_items_all(is_need_open_download_page=True) == 1
        )
        assert download_page_sel.get_total_items_downloading(timeout=5) == 0
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494628")
def test_progress_bar_when_download_unknown_size(
    download_page_sel: DownloadPageSel,
):
    # TODO fix later after https://coccoc.atlassian.net/browse/PE-7684 fixed
    pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494634")
def test_ui_when_removing_downloaded_file_on_disk(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
    download_test_itim: DownloadTestItim,
):
    download_page_sel.clear_all_downloads_data()
    try:
        # Download torrent and a file and wait for download is done
        web_torrent_sel.download_sintel_torrent_file(
            is_need_to_open_webtorrent=True, sleep_n_seconds=2
        )
        download_test_itim.download_sample2()
        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=2, is_need_open_download_page=True, timeout=1200
        )

        # Delete files
        file_utils.remove_a_file(
            file_name=rf"C:\Users\{os_utils.get_username()}\Downloads\sample2.xlsx"
        )
        file_utils.remove_directory(
            directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
        )
        sleep(2)
        # Check file status is removed and the btn retry shown
        download_page_sel.reload_page()
        assert download_page_sel.count_total_elements(download_page_sel.BTN_RETRY) == 2
        assert (
            download_page_sel.count_total_elements(download_page_sel.STATUS_REMOVED)
            == 2
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494637")
def test_search_function_in_download_page(
    download_page_sel: DownloadPageSel,
    web_torrent_sel: WebTorrentSel,
    download_test_itim: DownloadTestItim,
):
    download_page_sel.clear_all_downloads_data()
    try:
        download_test_itim.download_microsoft_press()
        download_test_itim.download_nguoi_tinh_mua_dong()
        download_test_itim.download_sample2()
        download_test_itim.download_sample4()
        download_test_itim.download_sample6()
        web_torrent_sel.download_sintel_torrent_file(is_need_to_open_webtorrent=True)

        assert download_page_sel.wait_for_download_items_finished(
            no_of_item=6, is_need_open_download_page=True, timeout=1200
        )

        # check search no result
        download_page_sel.search_download_item(search_text="ahihi css")
        assert download_page_sel.get_total_completed_download_item() == 0
        assert download_page_sel.is_element_appeared(
            download_page_sel.SEARCH_NO_RESULTS_TEXT
        )
        download_page_sel.search_download_item(search_text="Thử lại")
        assert download_page_sel.get_total_completed_download_item() == 0
        assert download_page_sel.is_element_appeared(
            download_page_sel.SEARCH_NO_RESULTS_TEXT
        )

        # Check search have 1 result
        download_page_sel.search_download_item(search_text="sample4.csv")
        assert download_page_sel.get_total_completed_download_item() == 1

        download_page_sel.search_download_item(search_text="Sintel")
        assert download_page_sel.get_total_completed_download_item() == 1
        download_page_sel.search_download_item(
            search_text="người Tình mùa đông _ - (Như Quỳnh)"
        )
        assert download_page_sel.get_total_completed_download_item() == 1

        # Check search have more result
        download_page_sel.search_download_item(search_text="sample")
        assert download_page_sel.get_total_completed_download_item() == 3
    finally:
        download_page_sel.clear_all_downloads_data()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1164285")
def test_close_browser_while_file_downloading(
    setup_for_close_while_testing,
    download_page_sel: DownloadPageSel,
):
    try:
        # Check total item at All part
        assert (
            download_page_sel.get_total_items_all(is_need_open_download_page=True) == 2
        )
        # Check total item at Downloading is 0
        assert download_page_sel.get_total_items_downloading(timeout=5) == 0

        # Check BTN retry show 2
        assert download_page_sel.count_total_elements(download_page_sel.BTN_RETRY) == 2
        # Check BTN Canceled show 2
        assert (
            download_page_sel.count_total_elements(download_page_sel.STATUS_CANCELED)
            == 2
        )
    finally:
        download_page_sel.clear_all_downloads_data()


# def test_youtube_page_appium(youtube_page_appium: YoutubeAppium):
#     youtube_page_appium.open_youtube_url(
#         url="https://www.youtube.com/watch?v=7ICKkagL3xA"
#     )
#     youtube_page_appium.hover_mouse_on_movie_player()
#     youtube_page_appium.click_btn_download()
