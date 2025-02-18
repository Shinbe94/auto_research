from time import sleep
from random import choices
from typing import List
from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from appium.webdriver.webelement import WebElement

from src.pages.base import BaseAppium, BasePlaywright, BaseSelenium
from src.pages.constant import AWADL, CocCocTitles
from src.utilities import windows_utils
from tests import setting

lang = setting.coccoc_language


class DownloadPage(BasePlaywright):
    @property
    def items_all(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-all")

    @property
    def items_downloading(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-downloading")

    @property
    def items_paused(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-paused")

    @property
    def items_finished(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-finished")

    @property
    def items_torrent(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-torrent")

    @property
    def items_seeding(self) -> Locator:
        return self.page.get_by_test_id("sidebar-item-seeding")

    @property
    def search_textbox(self) -> Locator:
        return self.page.locator('label[data-testid="search-bar"] input')

    @property
    def search_textbox_placeholder(self) -> Locator:
        if "en" in lang:
            return self.page.get_by_placeholder("Search downloads")
        else:
            return self.page.get_by_placeholder("Tìm kiếm tệp đã tải về")

    @property
    def description_text(self) -> Locator:
        if "en" in lang:
            return self.page.get_by_text("Files you download appear here")
        else:
            return self.page.get_by_text("Các tệp bạn tải về sẽ xuất hiện ở đây")

    @property
    def three_dot_btn(self) -> Locator:
        return self.page.locator("#root > div.h0BdT > div:nth-child(4) > div")

    @property
    def three_dot_clear_all_items(self) -> Locator:
        return self.page.get_by_test_id("header-dropdown-item-clearAll")

    @property
    def three_dot_open_download_folder(self) -> Locator:
        return self.page.get_by_test_id("header-dropdown-item-openDownloadsFolder")

    @property
    def three_dot_open_download_settings(self) -> Locator:
        return self.page.get_by_test_id("header-dropdown-item-settings")

    @property
    def btn_add_link(self) -> Locator:
        return self.page.get_by_test_id("add-link")

    @property
    def btn_add_torrent(self) -> Locator:
        return self.page.get_by_test_id("torrent-btn")

    @property
    def search_box(self) -> Locator:
        if lang == "en":
            return self.page.get_by_placeholder("Search downloads")
        else:
            return self.page.get_by_placeholder("Tìm kiếm tệp đã tải về")

    @property
    def no_search_result_found(self) -> Locator:
        if "en" in lang:
            return self.page.get_by_text("No search results found")
        else:
            return self.page.get_by_text("Không tìm thấy kết quả tìm kiếm nào")

    # Interaction methods
    def enter_text_to_search_text_box(self, text) -> None:
        self.search_textbox.fill(text)

    def open_download_page(self) -> None:
        self.page.goto("coccoc://downloads/", timeout=30000)
        if "en" in lang:
            expect(self.page).to_have_title("Downloads")
        else:
            expect(self.page).to_have_title("Tệp đã tải về")

    def verify_download_page_ui(self) -> None:
        expect(self.btn_add_torrent).to_be_visible()
        expect(self.btn_add_link).to_be_visible()
        expect(self.search_textbox_placeholder).to_be_visible()
        expect(self.description_text).to_be_visible()

        expect(self.items_all).to_be_visible()
        expect(self.items_downloading).to_be_visible()
        expect(self.items_paused).to_be_visible()
        expect(self.items_finished).to_be_visible()
        expect(self.items_torrent).to_be_visible()
        expect(self.items_seeding).to_be_visible()

        expect(self.three_dot_btn).to_be_visible()
        self.three_dot_btn.click()
        expect(self.three_dot_clear_all_items).to_be_visible()
        expect(self.three_dot_open_download_folder).to_be_visible()
        expect(self.three_dot_open_download_settings).to_be_visible()

    def click_three_dots_menu(self):
        self.three_dot_btn.click()

    def clear_all_downloads_data(
        self, sleep_n_seconds: int = 1, is_need_open_download_page=True
    ):
        if is_need_open_download_page:
            self.open_download_page()
        self.click_three_dots_menu()
        self.three_dot_clear_all_items.click()
        sleep(sleep_n_seconds)

    def open_downloads_folder(self):
        self.click_three_dots_menu()
        self.three_dot_open_download_folder.click()

    def open_settings(self):
        self.click_three_dots_menu()
        self.three_dot_open_download_settings.click()

    def click_btn_add_link(self):
        self.btn_add_link.click()

    def click_btn_add_torrent(self):
        self.btn_add_torrent.click()

    def get_filename_downloaded(self, item_no: str = 1) -> str:
        locator = rf'div[data-testid="COMPLETE-item-{item_no}"] h6 a'
        return self.get_attribute_value_by_selector(locator, "title")


class DownloadPageSel(BaseSelenium):
    # locator
    if "en" in lang:
        SEARCH_NO_RESULTS_TEXT = (By.XPATH, '//div[text()="No search results found"]')
    else:
        SEARCH_NO_RESULTS_TEXT = (
            By.XPATH,
            '//div[text()="Không tìm thấy kết quả tìm kiếm nào"]',
        )
    SEARCH_TEXT_BOX = (By.CSS_SELECTOR, 'label[data-testid="search-bar"] input')
    BTN_ADD_TORRENT = (By.CSS_SELECTOR, 'div[data-testid="torrent-btn"]')
    BTN_ADD_LINK = (By.CSS_SELECTOR, 'div[data-testid="add-link"]')
    TYPE_URL = (By.CSS_SELECTOR, 'div[data-testid="add-link"] input')
    ADD_LINK_CANCEL_BTN = (
        By.CSS_SELECTOR,
        'div[data-testid="add-link-cancel-btn"]',
    )
    ADD_LINK_OK_BTN = (
        By.CSS_SELECTOR,
        'div[data-testid="add-link-submit-btn"]',
    )
    THREE_DOTS_BTN = (
        By.CSS_SELECTOR,
        'div[data-testid="header-dropdown-item-container"]',
    )
    CLEAR_ALL_DOWNLOAD_BTN = (
        By.CSS_SELECTOR,
        'div[data-testid="header-dropdown-item-clearAll"]',
    )
    OPEN_DOWNLOADS_FOLDER = (
        By.CSS_SELECTOR,
        'div[data-testid="header-dropdown-item-openDownloadsFolder"]',
    )
    BTN_SETTINGS = (By.CSS_SELECTOR, 'div[data-testid="header-dropdown-item-settings"]')
    ITEMS_ALL = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-all"]')
    ITEMS_DOWNLOADING = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-downloading"]')
    ITEMS_PAUSED = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-paused"]')
    ITEMS_FINISHED = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-finished"]')
    ITEMS_TORRENTS = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-torrent"]')
    ITEMS_SEEDING = (By.CSS_SELECTOR, 'div[data-testid="sidebar-item-seeding"]')

    if "en" in lang:
        DESCRIPTION_TEXT = (By.XPATH, '//div[text()="Files you download appear here"]')
    else:
        DESCRIPTION_TEXT = (
            By.XPATH,
            '//div[text()="Các tệp bạn tải về sẽ xuất hiện ở đây"]',
        )
    if "en" in lang:
        BTN_CANCEL = (By.XPATH, '//button[text()="Cancel"]')
    else:
        BTN_CANCEL = (By.XPATH, '//button[text()="Hủy"]')

    if "en" in lang:
        BTN_PLAY = (By.XPATH, '//button[text()="Play"]')
    else:
        BTN_PLAY = (By.XPATH, '//button[text()="Phát"]')

    if "en" in lang:
        BTN_RETRY = (By.XPATH, '//button[text()="Retry"]')
    else:
        BTN_RETRY = (By.XPATH, '//button[text()="Thử lại"]')

    if "en" in lang:
        STATUS_REMOVED = (By.XPATH, '//span[text()="Removed"]')
    else:
        STATUS_REMOVED = (By.XPATH, '//button[text()="Đã xóa"]')

    if "en" in lang:
        STATUS_CANCELED = (By.XPATH, '//span[text()="Canceled"]')
    else:
        STATUS_CANCELED = (By.XPATH, '//button[text()="Đã hủy"]')

    def btn_remove_from_the_list_torrent_item(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'span[data-testid="download-item-{index}-close-btn"]',
        )

    def btn_remove_from_the_list_normal_item(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'span[data-testid="download-item-{index}-close-btn"]',
        )

    def btn_stop_seeding_torrent(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-stopSeeding"]',
        )

    def btn_show_in_folder(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-showInFolder"]',
        )

    def btn_3_dots_of_torrent_item(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'div[data-testid="download-item-{index}-dropdown"]',
        )

    def btn_3_dots_of_item(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'div[data-testid="download-item-{index}-dropdown"]',
        )

    def item_status(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'span[data-testid="download-item-{index}-status"]',
        )

    def item_open_source_page(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'a[data-testid="item-menu-{index}-open-source"]',
        )

    def item_open_when_done(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'li[data-testid="item-menu-{index}-open-when-done"] button',
        )

    def item_download_limit(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'li[data-testid="item-menu-{index}-download-limit"]',
        )

    def item_upload_limit(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'li[data-testid="item-menu-{index}-upload-limit"]',
        )

    def item_remove_from_disk(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'li[data-testid="item-menu-{index}-delete"]',
        )

    def item_copy_link(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'li[data-testid="item-menu-{index}-copy-link"]',
        )

    def item_donot_seed_checkbox(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="item-menu-{index}-no-seed-checkbox"]',
        )

    def item_arrow_down(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'div[data-testid="file-tree-item-{index}-arrow-btn"]',
        )

    def item_file_tree_checkmark(
        self, is_need_open_download_page: bool = True
    ) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="file-tree-item-{index}-checkbox"]',
        )

    def item_btn_pause(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-pause"]',
        )

    def item_btn_resume(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-resume"]',
        )

    def item_btn_cancel(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-cancel"]',
        )

    if "en" in lang:
        FIRST_ITEM_RETRY_BTN_XPATH = (By.XPATH, '//button[text()="Retry"]')
    else:
        FIRST_ITEM_RETRY_BTN_XPATH = (By.XPATH, '//button[text()="Thử lại"]')

    def item_btn_retry(self, is_need_open_download_page: bool = True) -> tuple:
        index = self.get_top_index_download_item(
            is_need_open_download_page=is_need_open_download_page
        )
        return (
            By.CSS_SELECTOR,
            f'button[data-testid="download-item-{index}-control-btn-retryDownload"]',
        )

    FIRST_ITEM_CHILD_DATA_INDEX_0_TORRENT = (
        By.CSS_SELECTOR,
        'div[data-testid="IN_PROGRESS-item-2000000000"] li[data-index="0"] button',
    )
    FIRST_ITEM_CHILD_DATA_INDEX_1_TORRENT = (
        By.CSS_SELECTOR,
        'div[data-testid="IN_PROGRESS-item-2000000000"] li[data-index="1"] button',
    )
    FIRST_ITEM_CHILD_DATA_INDEX_2_TORRENT = (
        By.CSS_SELECTOR,
        'div[data-testid="IN_PROGRESS-item-2000000000"] li[data-index="2"] button',
    )
    LIST_ALL_DATE = (By.CSS_SELECTOR, "#root > div > ul > div")
    LIST_ALL_ITEMS_DATE = (By.CSS_SELECTOR, "#root > div > ul > div > div")

    # Interaction methods

    def open_download_page(self, sleep_n_seconds: int = 1):
        self.open_page(url="coccoc://downloads/")
        sleep(sleep_n_seconds)

    def click_btn_add_torrent(self, is_need_open_download_page=True) -> None:
        if is_need_open_download_page:
            self.open_download_page()

        # Click Btn Add torrent and checking the Window dialog appears
        n: int = 0
        while n < 3:
            try:
                self.click_element(self.BTN_ADD_TORRENT)
                sleep(2)
                if (
                    windows_utils.find_window_by_name(
                        window_name="Open", class_name="#32770"
                    )
                    > 0
                ):
                    break
                else:
                    n += 1
            except Exception:
                pass

    def click_btn_add_link(self, is_need_open_download_page=True) -> None:
        """To click btn addlink to open dialog

        Args:
            is_need_open_download_page (bool, optional): Open download page. Defaults to True.
        """
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.BTN_ADD_LINK)

    def set_magnet_link(
        self,
        magnet_link: str,
        is_need_click_btn_add_link=True,
        is_click_ok_btn=True,
        sleep_n_seconds: int = 0,
    ) -> None:
        """Set magnet link to dialog

        Args:
            magnet_link (str): The magnet link
            is_need_click_btn_add_link (bool, optional): click to open dialog or no needed. Defaults to True.
            is_click_ok_btn (bool, optional): Click Ok to start downloading. Defaults to True.
        """
        if is_need_click_btn_add_link:
            self.click_btn_add_link()
            # sleep(2)
        self.fill_texts(self.TYPE_URL, text=magnet_link)
        if is_click_ok_btn:
            self.click_element(self.ADD_LINK_OK_BTN)
        sleep(sleep_n_seconds)

    def clear_all_downloads_data(
        self, is_need_open_download_page=True, is_need_to_cancel_all_downloading=True
    ):
        """We call this method for clearing the data from download page for easier controling
        Clear all remaining torrent data before and after test
        Args:
            is_need_open_download_page (bool, optional): Opend download page. Defaults to True.
            is_need_to_cancel_all_downloading (bool, optional): Clear all downloading. Defaults to True.
        """
        if is_need_open_download_page:
            self.open_download_page()
        if is_need_to_cancel_all_downloading:
            self.cancel_all_downloading_item_one_by_one()
        self.click_element(self.THREE_DOTS_BTN)
        self.click_element(self.CLEAR_ALL_DOWNLOAD_BTN)

    def get_filename_downloaded(self, item_no: str = 1) -> str:
        locator = (By.CSS_SELECTOR, rf'div[data-testid="COMPLETE-item-{item_no}"] h6 a')
        return self.get_element_attribute_by_its_name_and_locator(locator, "title")

    def wait_for_total_items_appear_in_downloading_part(
        self,
        no_of_item: int = 1,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
        is_need_open_download_page=False,
        sleep_n_seconds: int = 0,
    ) -> bool:
        """This method is for waiting for the number of items starting download by checking
        their appears on Downloading part

        Args:
            no_of_item (int): total item want to check
            timeout (_type_, optional): Timeout. Defaults to None.
            is_need_open_download_page (bool, optional): open download page. Defaults to False.

        Returns:
            bool: _description_
        """
        if is_need_open_download_page:
            self.open_download_page()
        is_downloading_fully_appeared = False
        if timeout is None:
            timeout = setting.timeout_for_waiting_download_medium_file_size

        total_delay = 0
        interval_delay = 5
        while total_delay < timeout:
            if self.get_total_items_downloading(timeout=timeout) == no_of_item:
                is_downloading_fully_appeared = True
                break
            sleep(interval_delay)
            self.reload_page()
            total_delay += interval_delay
            if total_delay >= timeout:
                print(
                    f" Time out after {total_delay} seconds wait for total items downloading"
                )
                break
        sleep(sleep_n_seconds)
        return is_downloading_fully_appeared

    def wait_for_download_items_finished(
        self,
        no_of_item: int = 1,
        timeout=setting.timeout_for_waiting_download_small_file_size,
        is_need_open_download_page=False,
    ) -> bool:
        """This methods is for waiting the total items are downloaded
            by checking the total downloading vs total finished
        Args:
            no_of_item (int): Total items are downloading
            timeout (_type_, optional): timeout, default = setting, else by passing

        Returns:
            bool: _description_
        """
        if is_need_open_download_page:
            self.open_download_page()
        is_download_done = False
        total_delay = 0
        interval_delay = 5
        while total_delay < timeout:
            if self.get_total_items_finished(timeout=timeout) == no_of_item:
                is_download_done = True
                break
            sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                print(
                    f" Time out after {total_delay} seconds wait for downloading is done"
                )
                break
        return is_download_done

    def wait_for_no_of_total_items_appear_in_torrent(
        self,
        total_item: int,
        timeout: int = setting.timeout_for_waiting_download_medium_file_size,
        is_need_open_download_page=False,
    ) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        is_reached = False
        total_delay = 0
        interval_delay = 3
        while total_delay < timeout:
            if self.get_total_items_torrents(timeout) == total_item:
                is_reached = True
                break
            sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                print(
                    f" Time out after {total_delay} seconds wait for all torrent item are downloading"
                )
                break
        return is_reached

    def get_total_items_all(
        self,
        is_need_open_download_page=False,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
    ) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        total_delay = 0
        interval_delay = 1
        while total_delay < timeout:
            try:
                items = self.get_inner_text(self.ITEMS_ALL)
                if "(" in items:
                    return int(items[items.find("(") + 1 : items.find(")")])
                else:
                    sleep(interval_delay)
                    total_delay += interval_delay
                    if total_delay >= timeout:
                        return 0
            except Exception:
                sleep(interval_delay)
                total_delay += interval_delay

    def get_total_items_downloading(
        self,
        is_need_open_download_page=False,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
    ) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        total_delay = 0
        interval_delay = 1
        while total_delay < timeout:
            try:
                items = self.get_inner_text(self.ITEMS_DOWNLOADING)
                if "(" in items:
                    return int(items[items.find("(") + 1 : items.find(")")])
                else:
                    sleep(interval_delay)
                    total_delay += interval_delay
                    if total_delay >= timeout:
                        return 0
            except Exception:
                sleep(interval_delay)
                total_delay += interval_delay

    def get_total_items_paused(
        self,
        is_need_open_download_page=False,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
    ) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        total_delay = 0
        interval_delay = 1
        while total_delay < timeout:
            try:
                items = self.get_inner_text(self.ITEMS_PAUSED)
                if "(" in items:
                    return int(items[items.find("(") + 1 : items.find(")")])
                else:
                    sleep(interval_delay)
                    total_delay += interval_delay
                    if total_delay >= timeout:
                        return 0
            except Exception:
                sleep(interval_delay)
                total_delay += interval_delay

    def wait_for_no_of_total_items_appear_in_paused(
        self,
        total_item: int,
        timeout: int = setting.timeout_for_waiting_download_medium_file_size,
        is_need_open_download_page=False,
    ) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        is_appeared = False
        total_delay = 0
        interval_delay = 3
        while total_delay < timeout:
            if self.get_total_items_paused(timeout=timeout) == total_item:
                is_appeared = True
                break
            sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                print(
                    f"Time out after {total_delay} seconds wait for item appears in Paused part"
                )
                break
        return is_appeared

    def get_total_items_finished(
        self,
        is_need_open_download_page=False,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
    ) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        total_delay = 0
        interval_delay = 1
        while total_delay < timeout:
            try:
                items_text = self.get_inner_text(self.ITEMS_FINISHED)
                # print(f"finish==== : {items_text}")
                if "(" in items_text:
                    return int(
                        items_text[items_text.find("(") + 1 : items_text.find(")")]
                    )
                else:
                    sleep(interval_delay)
                    total_delay += interval_delay
                if total_delay >= timeout:
                    return 0
            except Exception:
                sleep(interval_delay)
                total_delay += interval_delay

    def get_total_items_torrents(self, is_need_open_download_page=False) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        items = self.get_inner_text(self.ITEMS_TORRENTS)
        if "(" in items:
            return int(items[items.find("(") + 1 : items.find(")")])
        else:
            return 0

    def get_total_items_seeding(
        self,
        is_need_open_download_page=False,
        timeout=setting.timeout_for_waiting_download_medium_file_size,
    ) -> int:
        if is_need_open_download_page:
            self.open_download_page()
        total_delay = 0
        interval_delay = 1
        while total_delay < timeout:
            try:
                items = self.get_inner_text(self.ITEMS_SEEDING)
                if "(" in items:
                    return int(items[items.find("(") + 1 : items.find(")")])
                else:
                    sleep(interval_delay)
                    total_delay += interval_delay
                if total_delay >= timeout:
                    return 0
            except Exception:
                sleep(interval_delay)
                total_delay += interval_delay

    def click_items_all(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_ALL)

    def click_items_downloading(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_DOWNLOADING)

    def click_items_paused(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_PAUSED)

    def click_items_finished(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_FINISHED)

    def click_items_torrents(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_TORRENTS)

    def click_items_seeding(self, is_need_open_download_page=False) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.ITEMS_SEEDING)

    def click_btn_cancel(
        self, is_need_open_download_page=False, sleep_n_seconds_before_cancel: int = 0
    ) -> None:
        """To cancel the downloading item

        Args:
            is_need_open_download_page (bool, optional): Open the download page. Defaults to False.
            sleep_n_seconds_before_cancel (int, optional): sleep n seconds before clicking. Defaults to 0.
        """
        if is_need_open_download_page:
            self.open_download_page()
        sleep(sleep_n_seconds_before_cancel)
        self.click_element(self.BTN_CANCEL)

    def cancel_all_downloading_item_one_by_one(self) -> None:
        """Get list downloading items then cancel all"""
        item_downloadings: list = []  # Get list downloading if any
        try:
            item_downloadings = self.get_elements(self.BTN_CANCEL, timeout=3)
        except Exception:
            pass
        if len(item_downloadings) > 0:
            for element in item_downloadings:
                # self.scroll_into_view_element(element)
                self.move_to_element_by_element(element)
                self.click_element_by_js(element)
                sleep(1)
                # element.click()

    def remove_item_from_the_list(self, is_need_open_download_page=False) -> None:
        """Remove the first item from the list
            Note: Item just downloaded
        Args:
            is_need_open_download_page (bool, optional): _description_. Defaults to False.
        """
        if is_need_open_download_page:
            self.open_download_page()

        self.scroll_into_view_element(
            # self.get_element(self.FIRST_ITEM_REMOVE_FROM_DISK_TORRENT)
            self.get_element(
                self.btn_remove_from_the_list_torrent_item(
                    is_need_open_download_page=False
                )
            )
        )
        sleep(5)
        self.click_element(
            self.btn_remove_from_the_list_torrent_item(is_need_open_download_page=False)
        )

    def click_to_stop_seeding_an_item(self) -> None:
        self.click_element(self.btn_stop_seeding_torrent())

    def check_donot_seed_is_checked(self) -> None:
        """To check the checkbox Donot seed is checked
        Mean do not seed the file
        """
        self.click_btn_3dots_of_item()
        assert (
            self.wait_for_attribute_update_value(
                by_locator=self.item_donot_seed_checkbox(),
                attribute_name="class",
                att_value="checkbox checked",
            )
            is True
        )
        assert (
            self.get_element_attribute_by_its_name_and_locator(
                self.item_donot_seed_checkbox(), "class"
            )
            == "checkbox checked"
        )

    def click_to_show_all_child_file_of_first_torrent(self) -> None:
        """To click the Arrow down button to expand (show) all child files"""
        self.click_element(self.item_arrow_down())

    def check_ui_of_child_files_of_the_first_torrent(
        self, is_need_to_click_arrow_down_btn=True
    ) -> None:
        if is_need_to_click_arrow_down_btn:
            self.click_to_show_all_child_file_of_first_torrent()

    def get_all_child_files_of_first_torrent(
        self, by_locator=None, is_need_open_download_page=True
    ) -> List[WebElement]:
        """This method is for getting the all Elements of all child files of the first Torrent is downloading
            Note: This only work for the only first item downloading, we should clear all downloading data, then restart
            browser before testing
        Args:
            by_locator (_type_, optional): _description_. Defaults to None.
            is_need_open_download_page (bool, optional): _description_. Defaults to True.

        Returns:
            List[WebElement]: _description_
        """
        if is_need_open_download_page:
            self.open_download_page()
        self.click_to_show_all_child_file_of_first_torrent()
        if by_locator is None:
            by_locator = (
                By.CSS_SELECTOR,
                'div[data-testid="IN_PROGRESS-item-2000000000"] ul li',
            )
        list_child_torrent_file = [
            ele
            for ele in self.get_elements(by_locator)
            if ele.get_attribute("data-index")
        ]
        return list_child_torrent_file

    def uncheck_some_child_files_of_first_torrent(self) -> List[int]:
        """This methods is for uncheck some child file of the current fist torrent is downloading
            Note: Random select 2 files, This only work for the only first item downloading
        Returns:
            List[int]: Return the list index of selected files for checking not being fully downloaded later
        """
        eles = choices(
            self.get_all_child_files_of_first_torrent(), k=2
        )  # Random select 2 file from list
        indexes = [int(ele.get_attribute("data-index")) for ele in eles]
        for ele in eles:
            self.scroll_into_view_element(ele)
            try:
                ele.click()
            except ElementClickInterceptedException:
                self.scroll_into_bottom_of_page()
                ele.click()
        return indexes

    def uncheck_some_child_files_of_wired_cd_rip_sample_mash_shared_torrent_file(
        self,
    ) -> List[int]:
        """This methods is for uncheck some child file of the current fist torrent is downloading
        Note:
            Random select 2 files, This only work for the only first item downloading
            file "WIRED CD - Rip. Sample. Mash. Share" has 2 last item with small size, need to remove
            them before random choice as they're easily to get full 100%
        Returns:
            List[int]: Return the list index of selected files for checking not being fully downloaded later
        """
        list_child_files = self.get_all_child_files_of_first_torrent()
        eles = choices(
            list_child_files[:-2], k=2
        )  # Remove 2 last items then Random select 2 items from list
        indexes = [int(ele.get_attribute("data-index")) for ele in eles]
        for ele in eles:
            self.scroll_into_view_element(ele)
            try:
                ele.click()
            except ElementClickInterceptedException:
                self.scroll_into_bottom_of_page()
                ele.click()
        return indexes

    def uncheck_all_child_files_of_first_torrent_one_by_one(self) -> None:
        """This methods is for uncheck all child files of the current fist torrent is downloading
        Returns:
            List[int]: Return the list index of selected files for checking not being fully downloaded later
        """
        eles = self.get_all_child_files_of_first_torrent()
        for ele in eles:
            # ele.click()
            try:
                self.scroll_into_view_element(ele)
                self.scroll_down_by_n_pixel(70)
                ele.click()
            except ElementClickInterceptedException:
                self.scroll_down_by_n_pixel(70)
                ele.click()

    def uncheck_all_child_files_of_first_torrent_by_checkmark(self) -> None:
        """This methods is for uncheck all child files of the current fist torrent is downloading,
        by uncheck the top checkmark to unmark all
        Returns:
            List[int]: Return the list index of selected files for checking not being fully downloaded later
        """
        # Check default is checked
        assert self.wait_for_attribute_update_value(
            by_locator=self.item_file_tree_checkmark(),
            attribute_name="class",
            att_value="checkbox checked",
        )
        # Uncheck the checkmark then check it is unchecked
        self.click_element(self.item_file_tree_checkmark())
        assert self.wait_for_attribute_update_value(
            by_locator=self.item_file_tree_checkmark(),
            attribute_name="class",
            att_value="checkbox",
        )

    def check_child_files_of_first_torrent_are_not_fully_downloaded(
        self, list_index_of_file: List[int]
    ):
        """This method is for checking the child files are not downloaded fully (100%) when they're unchecking
        Note: This only work for the only first item downloading
        Args:
            list_index_of_file (List[int]): The list index files are unchecked before
        """
        for i in list_index_of_file:
            percent_downloading = (
                By.CSS_SELECTOR,
                rf'div[data-testid="COMPLETE-item-2000000000"] li[data-index="{i}"] label span span:nth-child(2)',
            )
            self.scroll_into_view_element(self.get_element(percent_downloading))
            assert self.get_element_text(by_locator=percent_downloading) != "100%"

    def check_progress_bar_downloading_is_shown(
        self, by_locator=None, is_need_open_download_page=True
    ) -> bool:
        is_existed = False
        if is_need_open_download_page:
            self.open_download_page()
        if by_locator is None:
            by_locator = (
                By.CSS_SELECTOR,
                'div[data-testid="IN_PROGRESS-item-2000000000"] div',
            )
        list_element_has_style_att = [
            ele
            for ele in self.get_elements(by_locator)
            if (
                ele.get_attribute("style")
                and ele.get_attribute("class") != "download-item-info-icon inProgress"
            )
        ]
        if len(list_element_has_style_att) == 1:
            is_existed = True
        return is_existed

    def check_progress_bar_downloading_is_not_shown(
        self, by_locator=None, is_need_open_download_page=True
    ) -> bool:
        if is_need_open_download_page:
            self.open_download_page()
        if by_locator is None:
            by_locator = (
                By.CSS_SELECTOR,
                'div[data-testid="COMPLETE-item-2000000000"] div',
            )
        list_element_has_style_att = [
            ele
            for ele in self.get_elements(by_locator)
            if (
                ele.get_attribute("style")
                and ele.get_attribute("data-testid") != "download-item-2000000000-icon"
            )
        ]
        if len(list_element_has_style_att) == 0:
            return True
        else:
            return False

    # TORRENT METHODS (For torrent files)

    def click_btn_resume_of_item(self) -> None:
        """To resume downloading of the first item"""
        self.click_element(self.item_btn_resume())

    def click_remove_file_from_disk(self, is_need_open_download_page=True) -> None:
        """To remove the file from disk of the first item"""
        if is_need_open_download_page:
            self.open_download_page()
        self.click_btn_3dots_of_item()
        self.click_element(self.item_remove_from_disk(is_need_open_download_page=False))

    def click_copy_link_of_item(self) -> None:
        """To click Copy link of the first item"""
        self.click_btn_3dots_of_item()
        self.click_element(self.item_copy_link(is_need_open_download_page=False))

    def click_btn_3dots_of_item(self) -> None:
        self.click_element(
            self.btn_3_dots_of_torrent_item(is_need_open_download_page=False)
        )

    def get_torrent_download_item_status_torrent(self) -> str:
        return self.get_element_text(self.item_status())

    def click_remove_first_item_from_the_list_torrent(self) -> None:
        self.click_element(
            self.btn_remove_from_the_list_torrent_item(is_need_open_download_page=False)
        )

    # NORMAL FILE(Not torrent)
    def click_btn_pause_of_item(
        self, is_need_open_download_page=False, sleep_n_seconds: int = 1
    ) -> None:
        """To pause downloading of first item"""
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.item_btn_pause())
        sleep(sleep_n_seconds)

    def click_btn_cancel_of_first_item(self, sleep_n_seconds: int = 0) -> None:
        """To cancel downloading of the first item"""
        btn_cancel = self.scc.find_element_by_css_selector(
            'div[data-testid="IN_PROGRESS-item-1"]div[data-testid="IN_PROGRESS-item-1"] div > button:nth-child(2)'
        )
        self.click_element_by_js(element=btn_cancel)
        # self.click_element(
        #     self.FIRST_ITEM_CANCEL_BTN_NORMAL
        # )  # dont know why it can detect
        # self.click_element_by_js2(self.FIRST_ITEM_CANCEL_BTN_NORMAL)
        # self.click_element_by_js2(self.BTN_CANCEL)
        sleep(sleep_n_seconds)

    def click_open_when_done_of_item(self, is_need_open_download_page=False) -> None:
        """To set open file after done automatically"""
        if is_need_open_download_page:
            self.open_download_page()
        self.click_3dot_of_item(sleep_n_seconds=1)
        self.click_element(self.item_open_when_done(is_need_open_download_page=False))

    def click_open_source_page_of_item(self) -> None:
        """To open source page of first item"""
        self.click_3dot_of_item(sleep_n_seconds=1)
        self.click_element(self.item_open_source_page(is_need_open_download_page=False))

    def click_3dot_of_item(self, sleep_n_seconds: int = 0) -> None:
        # self.click_element(self.btn_3_dots_of_item())
        self.click_element_by_js(self.get_element(self.btn_3_dots_of_item()))
        sleep(sleep_n_seconds)

    def click_show_in_folder_of_item(
        self, is_need_open_download_page=True, sleep_n_seconds: int = 1
    ) -> None:
        if is_need_open_download_page:
            self.open_download_page()
        self.click_element(self.btn_show_in_folder())
        sleep(sleep_n_seconds)

    def get_download_item_status(self) -> None:
        return self.get_element_text(self.item_status())

    def click_remove_item_from_the_list(self) -> None:
        self.click_element(self.btn_remove_from_the_list_normal_item())

    def search_download_item(self, search_text: str) -> None:
        self.fill_texts(self.SEARCH_TEXT_BOX, text=search_text)
        sleep(2)

    def get_total_completed_download_item(self) -> int:
        """To get total downloaded items appear on download page
        Note: support for default and after searching item also
        Returns:
            int: _description_
        """
        locator = (By.CSS_SELECTOR, "ul > div > div")
        total: int = 0
        if self.count_total_elements(by_locator=locator, timeout=5) > 0:
            for element in self.get_elements(locator):
                if "COMPLETE-item" in self.get_attribute_by_its_name_and_element(
                    element=element, attribute_name="data-testid"
                ):
                    total += 1
        return total

    def get_all_index_download_item(
        self, is_need_open_download_page=True, filter_torrent=False, filter_normal=False
    ) -> List[str]:
        """List all index of all download items appear
        Args:
            is_need_open_download_page (bool, optional): _description_. Defaults to True.
            filter_torrent (bool, optional): Filter torrent item only. Defaults to False.
            filter_normal (bool, optional): Filter normal item only. Defaults to False.

        Returns:
            List[str]: List index
        """
        list_index: List = []
        if is_need_open_download_page:
            self.open_download_page()
        list_all_dates: List[WebElement] = self.get_elements(self.LIST_ALL_ITEMS_DATE)
        if len(list_all_dates) > 0:
            for date in list_all_dates:
                att_value = self.get_attribute_by_its_name_and_element(
                    date, "data-testid"
                )
                att_value_num = att_value.split("-")[2]
                list_index.append(att_value_num)
        if filter_torrent:
            return [item for item in list_index if int(item) >= 2000000000]
        if filter_normal:
            return [item for item in list_index if int(item) < 2000000000]
        return list_index

    def get_top_index_download_item(self, is_need_open_download_page=False) -> str:
        """Get the top index item from the list
        Args:
            is_need_open_download_page (bool, optional): _description_. Defaults to False.

        Returns:
            str: _description_
        """
        if is_need_open_download_page:
            self.open_download_page()
        list_all_dates: List[WebElement] = self.get_elements(self.LIST_ALL_ITEMS_DATE)
        if len(list_all_dates) > 0:
            att_value = self.get_attribute_by_its_name_and_element(
                list_all_dates[0], "data-testid"
            )
            return att_value.split("-")[2]
        else:
            return ""

    # TODO fix later
    def get_all_index_download_block_item(
        self, is_need_open_download_page=True, filter_torrent=False, filter_normal=False
    ) -> List[str]:
        """List all index of all download items appear
        Args:
            is_need_open_download_page (bool, optional): _description_. Defaults to True.
            filter_torrent (bool, optional): Filter torrent item only. Defaults to False.
            filter_normal (bool, optional): Filter normal item only. Defaults to False.

        Returns:
            List[str]: List index
        """
        list_index: List = []
        if is_need_open_download_page:
            self.open_download_page()
        list_all_dates: List[WebElement] = self.get_elements(self.LIST_ALL_ITEMS_DATE)
        if len(list_all_dates) > 0:
            for date in list_all_dates:
                att_value = self.get_attribute_by_its_name_and_element(
                    date, "data-testid"
                )
                att_value_num = att_value.split("-")[2]
                list_index.append(att_value_num)
        if filter_torrent:
            return [item for item in list_index if int(item) >= 2000000000]
        if filter_normal:
            return [item for item in list_index if int(item) < 2000000000]
        return list_index

    # TODO fix later
    def get_top_index_download_block_item(
        self, is_need_open_download_page=False
    ) -> str:
        """Get the top index item from the list
        Args:
            is_need_open_download_page (bool, optional): _description_. Defaults to False.

        Returns:
            str: _description_
        """
        if is_need_open_download_page:
            self.open_download_page()
        list_all_dates: List[WebElement] = self.get_elements(self.LIST_ALL_ITEMS_DATE)
        if len(list_all_dates) > 0:
            att_value = self.get_attribute_by_its_name_and_element(
                list_all_dates[0], "data-testid"
            )
            return att_value.split("-")[2]
        else:
            return ""


class DownloadPageAppium(BaseAppium):
    """This class is for Download Page based on appium + winappdriver

    Args:
        BaseAppium (_type_): _description_
    """

    # Locator:
    if "en" in lang:
        BTN_CANCEL = (By.NAME, "Cancel")
    else:
        BTN_CANCEL = (By.NAME, "Hủy")

    if "en" in lang:
        BTN_PAUSE = (By.NAME, "Pause")
    else:
        BTN_PAUSE = (By.NAME, "Tạm dừng")

    if "en" in lang:
        BTN_YES_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]/Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Yes"]',
        )
    else:
        BTN_YES_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]/Pane[@ClassName="Chrome_WidgetWin_1"]//Button[@Name="Có"]',
        )
    if "en" in lang:
        BTN_CLOSE_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]//Button[@Name="Close"]',
        )
    else:
        BTN_CLOSE_XPATH = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="{CocCocTitles.DOWNLOADS_PAGE_TITLE}"]//Button[@Name="Đóng"]',
        )

    if "en" in lang:
        FILE_NAME = (By.NAME, "File name:")
    else:
        FILE_NAME = (By.NAME, "File name:")

    FILE_NAME_TEXT_FILED = (
        By.XPATH,
        '//Window[@ClassName="#32770"][@Name="Open"]/ComboBox[@ClassName="ComboBox"][@Name="File name:"]/Edit[@ClassName="Edit"][@Name="File name:"]',
    )

    # Interaction methods
    def click_cancel_btn(self) -> None:
        self.click_element(self.BTN_CANCEL)

    def click_pause_btn(self) -> None:
        self.click_element(self.BTN_PAUSE)

    def click_close_btn(self) -> None:
        # self.click_element(self.BTN_CLOSE)
        self.click_element(self.BTN_CLOSE_XPATH)
        if self.is_element_appeared(self.BTN_YES_XPATH, timeout=2):
            self.click_element(self.BTN_YES_XPATH)

    def click_yes_btn(self) -> None:
        if self.is_element_appeared(self.BTN_YES_XPATH, timeout=2):
            self.click_element(self.BTN_YES_XPATH)

    def set_value_into_file_name(self, filename_with_path: str) -> None:
        """To enter the filename with path then open
        Args:
            filename_with_path (str): File name to open with its full path to locate
        """
        sleep(1)
        self.fill_texts(
            self.FILE_NAME_TEXT_FILED,
            text=filename_with_path,
            is_press_enter=True,
            set_texts_immediately=True,
        )
