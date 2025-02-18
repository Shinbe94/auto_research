from time import sleep
from pytest_pytestrail import pytestrail
from selenium.webdriver.remote.webdriver import WebDriver as AppiumWebDriver

from src.pages.constant import CocCocTitles
from src.pages.coccoc_common import open_browser
from src.pages.internal_page.downloads.download_page import DownloadPageAppium
from src.pages.internal_page.task_manager import TaskManagerAppium
from src.pages.menus.main_menu import MainMenu
from src.pages.settings.settings_default_browser import SettingsDefaultBrowserSel
from src.pages.settings.settings_downloads import SettingsDownloadsSel
from src.pages.support_pages.support_apps import UTorrent, start_utorrent
from src.pages.support_pages.support_pages import WebTorrentSel
from src.utilities import file_utils, os_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54205")
def test_default_torrent_by_coccoc(
    set_utorrent_default,
    reinstall_coccoc_for_torrent,
    settings_default_browser_sel: SettingsDefaultBrowserSel,
    wad_session: AppiumWebDriver,
    wad_session2: AppiumWebDriver,
):
    settings_default_browser_sel.make_coccoc_as_default_torrent()
    file_utils.open_a_file(
        filename_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\automation\coccoc_win\data\torrent\sintel.torrent"
    )
    assert open_browser.is_coccoc_window_appeared(
        title=CocCocTitles.DOWNLOADS_PAGE_TITLE
    )

    # attaching the session into the download page
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
        port=4729,
        timeout=5,
        implicitly_wait=5,
    )
    try:
        sc = DownloadPageAppium(session_driver)
        sc.click_cancel_btn()  # Cancel Torrent downloading
    finally:
        open_browser.close_coccoc_by_window_title(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE,
            is_accept_closing_multiple_window=True,
        )
        # Kill utorrent if any error opening it
        os_utils.kill_process_by_name(pid_name="uTorrent.exe")
        sleep(2)
        # Set default Utorrent as default again
        start_utorrent(sleep_n_seconds=4)
        # attaching the session into the Utorrent
        session_driver2: AppiumWebDriver = wad_session2(
            title="μTorrent",
            port=4730,
            timeout=5,
            implicitly_wait=5,
        )
        ut = UTorrent(session_driver2)
        ut.set_utorrent_as_default(is_need_to_start_utorrent=False)
    # pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C473073")
def xtest_torrent_idle_time(
    main_menu: MainMenu,
    web_torrent_sel: WebTorrentSel,
    wad_session: AppiumWebDriver,
    wad_session2: AppiumWebDriver,
):
    # start download Torrent
    web_torrent_sel.download_sintel_torrent_file()
    web_torrent_sel.open_page(url="coccoc://downloads/")

    # attaching the session into the download page
    session_driver: AppiumWebDriver = wad_session(
        title=CocCocTitles.DOWNLOADS_PAGE_TITLE, port=4729
    )

    # Pause the downloading file
    sc = DownloadPageAppium(session_driver)
    sc.click_pause_btn()

    # Open CocCoc task manager
    main_menu.snap_selected_window_to_the_left_half_screen()
    main_menu.open_task_manager()

    # attaching the session into the Coccoc Task Manager
    session_driver2: AppiumWebDriver = wad_session2(
        title=CocCocTitles.COCCOC_TASK_MANAGER_TITLE, port=4730
    )
    tma = TaskManagerAppium(session_driver2)
    tma.snap_selected_window_to_the_right_half_screen()
    try:
        # Sleep for 5 mins
        sleep(310)
        assert tma.is_element_disappeared(tma.TORRENT_PROCESS) is True
    # tma.end_torrent_process()
    finally:
        sc.click_cancel_btn()
        session_driver.quit()
        session_driver2.quit()
        file_utils.remove_directory(
            directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C494571")
def test_default_torrent_settings(
    settings_downloads_sel: SettingsDownloadsSel,
):
    settings_downloads_sel.verify_default_value()
    settings_downloads_sel.verify_search_no_duplication()
