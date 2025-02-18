import time, random
import pytest
from pytest_pytestrail import pytestrail


from src.pages.menus.main_menu import MainMenu
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import file_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128817")
@pytest.mark.open_tor_window
def test_keep_tor_windows_for_a_long_time(main_menu: MainMenu):
    for i in range(10):
        main_menu.open_new_tor_window_from_tor_window()
        main_menu.minimize_window()
    time.sleep(setting.sleep_n_seconds_for_testing_performance_tor)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128820")
@pytest.mark.open_tor_window
def test_keep_alot_of_tor_tabs_for_a_long_time(toolbar: Toolbar):
    for i in range(30):
        toolbar.open_new_tab()
    time.sleep(setting.sleep_n_seconds_for_testing_performance_tor)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128823")
@pytest.mark.open_tor_window
def test_keep_tor_playing_video_music_for_a_long_time(
    toolbar: Toolbar,
):
    toolbar.make_search_value_with_tor_window(
        search_str="https://www.youtube.com/watch?v=eKFTSSKCzWA&pp=ygUPc291bmQgb2YgbmF0dXJl",
        is_press_enter=True,
    )
    time.sleep(setting.sleep_n_seconds_for_testing_performance_tor)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128826")
@pytest.mark.open_tor_window
def test_keep_tor_downloading_big_size_file(toolbar: Toolbar):
    try:
        toolbar.make_search_value_with_tor_window(
            search_str="https://speed.hetzner.de/1GB.bin",
            is_press_enter=True,
        )
        file_utils.wait_for_file_downloaded2(
            timeout=setting.timeout_for_waiting_download_big_file_size
        )
    finally:
        file_utils.delete_files_by_regress_name_downloads_folder(file_name="GB.bin")


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128829")
@pytest.mark.open_tor_window
def xtest_keep_tor_uploading_big_size_file(toolbar: Toolbar):
    toolbar.make_search_value_with_tor_window(
        search_str="https://speed.hetzner.de/1GB.bin",
        is_press_enter=True,
    )
    file_utils.wait_for_file_downloaded2(
        timeout=setting.timeout_for_waiting_download_big_file_size
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128832")
@pytest.mark.open_tor_window
def test_keep_tor_browsing_a_lot_of_page(toolbar: Toolbar):
    for i in range(30):
        site = random.choice(setting.list_testing_sites)
        toolbar.open_new_tab()
        toolbar.make_search_value_with_tor_window(search_str=site, is_press_enter=True)
        time.sleep(3)
    time.sleep(setting.sleep_n_seconds_for_testing_performance_tor)
