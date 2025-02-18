from time import sleep
import pytest
from pywinauto import Application
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocDialog, CocCocTitles
from src.pages.internal_page.downloads.download_page import DownloadPageSel
from src.pages.support_pages.support_pages import DownloadTestItim
from src.utilities import file_utils, os_utils


@pytest.fixture(autouse=True)
def delete_download_files():
    """
    To delete file before and after test
    :return:
    """
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
    )
    file_utils.remove_directory(
        directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
    )
    file_utils.delete_files_by_regress_name_downloads_folder(file_name="sample")
    file_utils.delete_files_by_regress_name_downloads_folder(
        file_name="Microsoft_Press_eBook_Programming"
    )
    file_utils.delete_files_by_regress_name_downloads_folder(
        file_name="người Tình mùa đông"
    )
    file_utils.delete_files_by_regress_name_downloads_folder(file_name="100MB")
    file_utils.delete_all_files_with_same_extension(".crdownload")
    file_utils.delete_all_files_with_same_extension(".webm")
    file_utils.delete_all_files_with_same_extension(".bin")
    # file_utils.delete_all_files_with_same_extension(".mp4")
    yield
    file_utils.remove_directory(
        directory=rf"C:\\Users\\{os_utils.get_username()}\Downloads\\The WIRED CD - Rip. Sample. Mash. Share"
    )
    file_utils.remove_directory(
        directory=rf"C:\Users\{os_utils.get_username()}\Downloads\Sintel"
    )
    file_utils.delete_files_by_regress_name_downloads_folder(file_name="sample")
    file_utils.delete_files_by_regress_name_downloads_folder(
        file_name="Microsoft_Press_eBook_Programming"
    )
    file_utils.delete_files_by_regress_name_downloads_folder(
        file_name="người Tình mùa đông"
    )

    file_utils.delete_files_by_regress_name_downloads_folder(file_name="100MB")
    file_utils.delete_all_files_with_same_extension(".crdownload")
    file_utils.delete_all_files_with_same_extension(".webm")
    file_utils.delete_all_files_with_same_extension(".bin")
    # file_utils.delete_all_files_with_same_extension(".mp4")


@pytest.fixture(autouse=False)
def download_some_files_for_test():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = coccoc_instance[0]
    coccoc_window: Application = coccoc_instance[1]

    dti = DownloadTestItim(driver)
    dps = DownloadPageSel(driver)
    dps.clear_all_downloads_data()
    try:
        dti.download_100mb_file()
        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=1, is_need_open_download_page=True
        )
        sleep(3)
    finally:
        coccoc_window.window().close()
        sleep(3)
        coccoc_window.window().child_window(
            title=CocCocDialog.BTN_EXIT, control_type=50000
        ).wait("visible", timeout=3).double_click_input(button="left")
        if driver is not None:
            driver.quit()
    sleep(3)


@pytest.fixture(autouse=False)
def setup_for_close_while_testing():
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = coccoc_instance[0]
    coccoc_window: Application = coccoc_instance[1]

    dti = DownloadTestItim(driver)
    dps = DownloadPageSel(driver)
    dps.clear_all_downloads_data()
    try:
        dti.download_100mb_file()
        dti.download_1_GB()

        dps.wait_for_total_items_appear_in_downloading_part(
            no_of_item=2, is_need_open_download_page=True
        )
        sleep(3)
        dti.open_download_test_item_page()  # Prepare for test after click continue downloading
        # Click close and click btn continue downloading
        coccoc_window.window().close()
        sleep(3)
        coccoc_window.window().child_window(
            title=CocCocDialog.BTN_CONTINUE_DOWNLOADING, control_type=50000
        ).wait("visible", timeout=3).double_click_input(button="left")
        # check the redirection to the download page after click continue downloading
        assert open_browser.is_coccoc_window_appeared(
            title=CocCocTitles.DOWNLOADS_PAGE_TITLE
        )

    finally:
        # Click to close then click Exit btn
        coccoc_window.window().close()
        sleep(3)
        coccoc_window.window().child_window(title="Exit", control_type=50000).wait(
            "visible", timeout=3
        ).click_input()
        if driver is not None:
            driver.quit()
    sleep(2)
