from time import sleep
from pywinauto.keyboard import send_keys
from src.pages.base import BaseAppium, BasePlaywright, BaseSelenium
from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pywinauto import keyboard, Application
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import os_utils
from tests import setting

lang = setting.coccoc_language


class GooglePage(BasePlaywright):
    """Access google using playwright

    Args:
        BasePlaywright (_type_): _description_
    """

    def open_google_homepage(self):
        self.page.goto("https://google.com")

    def open_page(self, url):
        self.page.goto(url)


class GooglePageSel(BaseSelenium):
    # Locators
    BODY = (By.XPATH, "//body")

    # Interaction methods
    def open_google_page(self) -> None:
        self.open_page(url="https://google.com")

    def right_click_google_page(self) -> None:
        self.right_click_element(self.BODY)


class InfoByIp(BasePlaywright):
    """Get my IP using playwright

    Args:
        BasePlaywright (_type_): _description_

    Returns:
        _type_: _description_
    """

    @property
    def ip_address(self) -> Locator:
        return self.page.locator(".yourip > h1")

    def open_page_info_by_ip(self):
        self.page.goto("https://www.infobyip.com/")

    def get_my_ip_address(self) -> str:
        self.open_page_info_by_ip()
        your_client_ip = self.ip_address.text_content()
        return your_client_ip.split(": ")[1]


class InfoByIpSel(BaseSelenium):
    """Get my IP using selenium

    Args:
        BaseSelenium (_type_): _description_

    Returns:
        _type_: _description_
    """

    # locator
    # Todo this should be updated later
    IP_ADDRESS = (By.CSS_SELECTOR, ".yourip > h1")

    # Interaction methods

    def open_infor_by_ip_page(self):
        self.open_page(url="https://www.infobyip.com/")

    def get_my_ip_address(self) -> str:
        self.open_infor_by_ip_page()
        your_client_ip = self.get_element_text(self.IP_ADDRESS)
        return your_client_ip.split(": ")[1]


class WebTorrentSel(BaseSelenium):
    """Get WebTorrent using selenium

    Args:
        BaseSelenium (_type_): _description_

    Returns:
        _type_: _description_
    """

    # locator
    # Todo this should be updated later

    SINTEL_TORRENT_FILE = (
        By.CSS_SELECTOR,
        'a[href="https://webtorrent.io/torrents/sintel.torrent"]',
    )
    SINTEL_MAGNET_LINK = (
        By.CSS_SELECTOR,
        r'a[href="magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fsintel.torrent"]',
    )
    WIRED_CD_RIP_SAMPLE_MASH_SHARE_TORRENT_FILE = (
        By.CSS_SELECTOR,
        'a[href="https://webtorrent.io/torrents/wired-cd.torrent"]',
    )
    WIRED_CD_RIP_SAMPLE_MASH_SHARE_MAGNET_LINK = (
        By.CSS_SELECTOR,
        r'a[href="magnet:?xt=urn:btih:a88fda5954e89178c372716a6a78b8180ed4dad3&dn=The+WIRED+CD+-+Rip.+Sample.+Mash.+Share&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fwired-cd.torrent"]',
    )
    BIG_BUG_BUNNY_TORRENT_FILE = (
        By.CSS_SELECTOR,
        'a[href="https://webtorrent.io/torrents/big-buck-bunny.torrent"]',
    )
    BIG_BUG_BUNNY_MAGNET_LINK = (
        By.CSS_SELECTOR,
        r'a[href="magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big+Buck+Bunny&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fbig-buck-bunny.torrent"]',
    )
    TEARS_OF_STEEL_TORRENT_FILE = (
        By.CSS_SELECTOR,
        'a[href="https://webtorrent.io/torrents/tears-of-steel.torrent"]',
    )
    TEARS_OF_STEEL_MAGNET_LINK = (
        By.CSS_SELECTOR,
        r'a[href="magnet:?xt=urn:btih:209c8226b299b308beaf2b9cd3fb49212dbd13ec&dn=Tears+of+Steel&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Ftears-of-steel.torrent"]',
    )
    COSMOS_LAUDROMAT_TORRENT_FILE = (
        By.CSS_SELECTOR,
        'a[href="https://webtorrent.io/torrents/cosmos-laundromat.torrent"]',
    )
    COSMOS_LAUDROMAT_MAGNET_LINK = (
        By.CSS_SELECTOR,
        r'a[href="magnet:?xt=urn:btih:c9e15763f722f23e98a29decdfae341b98d53056&dn=Cosmos+Laundromat&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fcosmos-laundromat.torrent"]',
    )
    # Interaction methods

    def open_webtorrent(self):
        self.open_page(url="https://webtorrent.io/free-torrents")

    def download_sintel_torrent_file(
        self, is_need_to_open_webtorrent=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.SINTEL_TORRENT_FILE)
        sleep(sleep_n_seconds)

    def download_sintel_magnet_link(
        self, is_need_to_open_webtorrent=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.SINTEL_MAGNET_LINK)
        sleep(sleep_n_seconds)

    def download_wired_cd_rip_sample_mash_shared_torrent_file(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.WIRED_CD_RIP_SAMPLE_MASH_SHARE_TORRENT_FILE)
        sleep(sleep_n_seconds)

    def download_wired_cd_rip_sample_mash_shared_magnet_link(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.WIRED_CD_RIP_SAMPLE_MASH_SHARE_MAGNET_LINK)
        sleep(sleep_n_seconds)

    def download_big_buck_bunny_torrent_file(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.BIG_BUG_BUNNY_TORRENT_FILE)
        sleep(sleep_n_seconds)

    def download_big_buck_bunny_magnet_link(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.BIG_BUG_BUNNY_MAGNET_LINK)
        sleep(sleep_n_seconds)

    def download_tears_of_steel_torrent_file(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.TEARS_OF_STEEL_TORRENT_FILE)
        sleep(sleep_n_seconds)

    def download_tears_of_steel_magnet_link(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.TEARS_OF_STEEL_MAGNET_LINK)
        sleep(sleep_n_seconds)

    def download_cosmos_laundromat_torrent_file(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.COSMOS_LAUDROMAT_TORRENT_FILE)
        sleep(sleep_n_seconds)

    def download_cosmos_laundromat_magnet_link(
        self, is_need_to_open_webtorrent=False, sleep_n_seconds: int = 0
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.click_element(self.COSMOS_LAUDROMAT_MAGNET_LINK)
        sleep(sleep_n_seconds)

    def right_click_magnet_sintel(self, is_need_to_open_webtorrent=False) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.right_click_element(self.SINTEL_MAGNET_LINK)

    def right_click_magnet_tears_of_steel(
        self, is_need_to_open_webtorrent=False
    ) -> None:
        if is_need_to_open_webtorrent:
            self.open_webtorrent()
        self.right_click_element(self.TEARS_OF_STEEL_MAGNET_LINK)


class ThePirateBaySel(BaseSelenium):
    """Interact with element from ThePirateBay using selenium

    Args:
        BaseSelenium (_type_): _description_

    Returns:
        _type_: _description_
    """

    # locator
    MAGNET_ICON_FROM_SEARCH_LIST = (
        By.CSS_SELECTOR,
        '#torrents #st:nth-child(2) span[class="item-icons"] a',
    )

    # Interaction methods
    def making_search(self, search_str) -> None:
        self.open_page(url=rf"https://thepiratebay.org/search.php?q={search_str}")

    def right_click_magnet_icon(self) -> None:
        self.right_click_element(self.MAGNET_ICON_FROM_SEARCH_LIST)


class DownloadTestItim(BaseSelenium):
    """Interact with element from DownloadTestItim using selenium
    https://download-tests.itim.vn/
    Args:
        BaseSelenium (_type_): _description_

    Returns:
        _type_: _description_
    """

    # locator
    RATIO_100_MB = (
        By.CSS_SELECTOR,
        'input[value="100MB.bin"]',
    )
    RATIO_1GB = (
        By.CSS_SELECTOR,
        'input[value="1GB_(1fb3c3e4-ffea-45c5-9362-baaac6c32b0d).bin"]',
    )

    FILE_EXAMPLE_WEBM = (
        By.CSS_SELECTOR,
        'input[value="file example WEBM 1920_3_7MB.webm"]',
    )
    RATIO_TEAR_OF_STEEL = (By.CSS_SELECTOR, 'input[value="Tear_of_Steel_(2012).mp4"]')
    RUNNING_ON_EMPTY = (
        By.CSS_SELECTOR,
        'input[value="Jackson Browne - Running on Empty w- lyrics.mp4"]',
    )

    MICROSOFT_PRESS = (
        By.CSS_SELECTOR,
        'input[value="Microsoft_Press_eBook_Programming_Windows_8_Apps_HTML_CSS_JavaScript_2E_PDF.pdf"]',
    )
    NGUOI_TINH_MUA_DONE = (
        By.CSS_SELECTOR,
        'input[value="người Tình mùa đông &%$& - (Như Quỳnh).mp3"]',
    )
    BTN_UPLOAD = (By.CSS_SELECTOR, 'input[value="Upload"]')
    BTN_DOWNLOAD = (By.CSS_SELECTOR, "button.btn.btn-primary")
    SAMPLE_2 = (By.CSS_SELECTOR, 'input[value="sample2.xlsx"]')
    SAMPLE_3 = (By.CSS_SELECTOR, 'input[value="sample3.docx"]')
    SAMPLE_4 = (By.CSS_SELECTOR, 'input[value="sample4.csv"]')
    SAMPLE_6 = (By.CSS_SELECTOR, 'input[value="sample 6.txt"]')
    SAMPLE_PPTX = (By.CSS_SELECTOR, 'input[value="samplepptx.pptx"]')
    SAMPLE_TEXT_LARGE = (By.CSS_SELECTOR, 'input[value="sample text large.txt"]')

    # Interaction methods
    def open_download_test_item_page(self) -> None:
        self.open_page(url="https://download-tests.itim.vn/")

    def click_btn_download(self) -> None:
        self.move_to_element(self.BTN_DOWNLOAD)
        self.click_element(self.BTN_DOWNLOAD)

    def download_100mb_file(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.RATIO_100_MB)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_1_GB(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.RATIO_1GB)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_file_example_webm(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.FILE_EXAMPLE_WEBM)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_running_on_empty(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.RUNNING_ON_EMPTY)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_microsoft_press(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.MICROSOFT_PRESS)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_nguoi_tinh_mua_dong(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.NGUOI_TINH_MUA_DONE)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_sample2(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_2)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_sample3(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_3)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_sample4(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_4)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_sample6(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_6)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_samplepptx(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_PPTX)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_sample_text_large(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.SAMPLE_TEXT_LARGE)
        self.click_btn_download()
        sleep(sleep_n_seconds)

    def download_tear_of_steel(
        self, is_open_download_test_item_page=True, sleep_n_seconds: int = 0
    ) -> None:
        if is_open_download_test_item_page:
            self.open_download_test_item_page()
        self.move_to_element(self.BTN_UPLOAD)
        self.click_element(self.RATIO_TEAR_OF_STEEL)
        self.click_btn_download()
        sleep(sleep_n_seconds)


class ChromeStore(Toolbar):
    """Install theme via Chrome Themes Store
    Args:
        Toolbar (_type_): _description_
    """

    # Locator
    BTN_ADD_TO_CHROME = (By.NAME, "Add to Chrome")
    BTN_ADD_EXTENSION = (By.NAME, "Add extension")

    # Interaction methods

    def add_extension(self, url: str) -> None:
        self.make_search_value(search_str=url, is_press_enter=True)
        sleep(2)
        self.click_element(self.BTN_ADD_TO_CHROME)
        self.double_click_element(self.BTN_ADD_EXTENSION)
        sleep(15)  # Sleep for sure the installation is done

    def add_theme(self, url: str) -> None:
        self.make_search_value(search_str=url, is_press_enter=True)
        sleep(10)
        self.click_element(self.BTN_ADD_TO_CHROME)
        sleep(2)


class WarningPageSel(BaseSelenium):
    # Locators

    MAIN_MESSAGE = (By.CSS_SELECTOR, "#main-message > h1")
    BODY = (By.CSS_SELECTOR, 'body[id="body"]')

    def open_site(self, url: str) -> None:
        self.open_page(url=url)

    def check_main_message(self) -> None:
        if "en" in lang:
            assert (
                self.get_element_text(self.MAIN_MESSAGE)
                == "The site ahead contains malware"
            )
        else:
            assert (
                self.get_element_text(self.MAIN_MESSAGE)
                == "Trang web bạn sắp truy cập chứa phần mềm độc hại"
            )

    def check_bg_color(self) -> None:
        """Check Red bg color"""
        assert "rgba(217, 48, 37" in self.get_element_css_value_by_its_name_and_locator(
            self.BODY, "background-color"
        )


class DeveloperMozillaSel(BaseSelenium):
    # Locator
    JS_PATH_TEXTAREA = r'document.querySelector("#story")'

    def clear_and_set_text_in_textarea(self, text: str) -> None:
        self.open_page(
            url="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea"
        )
        self.clear_text_of_shadow_element(js_path=self.JS_PATH_TEXTAREA)
        self.fill_texts_shadow_element(js_path=self.JS_PATH_TEXTAREA, text=text)
        sleep(1)
        self.double_click_shadow_element(js_path=self.JS_PATH_TEXTAREA)


class W3SchoolSel(BaseSelenium):
    # Locator

    TEXT_AREA = (By.ID, "w3review")
    FRAME_CONTAINER = (By.ID, "iframecontainer")
    ENABLE_DICTIONAY_AREA_TEXT = (
        By.XPATH,
        '//span[text()="Oh, we still are looking for the right word. Would you help?"]',
    )

    def enter_text_in_textarea_then_double_click(self, text: str) -> None:
        self.open_page(
            url="https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_textarea"
        )
        first_window = self.get_current_window()
        try:
            self.switch_to_iframe(frame_reference="iframeResult")
            self.clear_text_of_element(self.TEXT_AREA)
            self.fill_texts(self.TEXT_AREA, text=text)
            sleep(1)
            self.double_click_element(self.TEXT_AREA)

        finally:
            self.switch_to_window(first_window)

    def click_text_in_textarea(self) -> None:
        first_window = self.get_current_window()

        self.click_mouse_by_offset(1919, 500)
        self.double_click_mouse_by_offset(1919, 500)
        sleep(2)
        try:
            self.switch_to_iframe(frame_reference="iframeResult")
            self.move_to_element_with_offset(self.TEXT_AREA, 0, 0)
            sleep(1)
            self.click_element(self.TEXT_AREA)
            sleep(2)
            self.click_element(self.TEXT_AREA)
            sleep(3)

        finally:
            self.switch_to_window(first_window)


class XeSel(BaseSelenium):
    # Locator

    POPUP = (By.CSS_SELECTOR, "yld-tag-host-campaign")
    POPUP_CLOSE_BTN = 'document.querySelector("yld-tag-host-campaign").shadow.querySelector(\'button[y-type="custom-close-button"]\')'
    TEXT_1USD = (
        By.CSS_SELECTOR,
        'a[href="/currencyconverter/convert/?Amount=1&From=USD&To=EUR"]',
    )
    TEXT_1EUR = (
        By.CSS_SELECTOR,
        'a[href="/currencyconverter/convert/?Amount=1&From=EUR&To=USD"]',
    )
    TEXT_5USD = (
        By.CSS_SELECTOR,
        'a[href="/currencyconverter/convert/?Amount=5&From=USD&To=EUR"]',
    )
    TEXT_5EUR = (
        By.CSS_SELECTOR,
        'a[href="/currencyconverter/convert/?Amount=5&From=EUR&To=USD"]',
    )

    def open_xe_page(self, sleep_n_seconds: int = 10) -> None:
        self.open_page(
            url="https://www.xe.com/currencyconverter/convert/?Amount=100&From=USD&To=EUR"
        )
        sleep(sleep_n_seconds)
        self.wait_then_close_popup_if_any()

    def wait_then_close_popup_if_any(self) -> None:
        self.scroll_to_top_page_by_js()  # trick to active show the pop-up if any
        if self.is_shadow_element_appeared(js_path=self.POPUP_CLOSE_BTN):
            self.click_shadow_element(js_path=self.POPUP_CLOSE_BTN)
        # if self.is_element_appeared(self.POPUP, timeout=10):
        #     self.press_keyboard_element(self.POPUP, keys=Keys.ESCAPE)

    def blacken_1_usd(self, is_open_xe_page=True, sleep_n_seconds: int = 10) -> None:
        if is_open_xe_page:
            self.open_xe_page(sleep_n_seconds=sleep_n_seconds)
        self.fullscreen_window()
        if self.is_shadow_element_appeared(js_path=self.POPUP_CLOSE_BTN, timeout=5):
            self.click_shadow_element(js_path=self.POPUP_CLOSE_BTN)
        # if self.is_element_appeared(self.POPUP):
        #     self.press_keyboard_element(self.POPUP, keys=Keys.ESCAPE)
        self.blacken_text2(self.TEXT_1USD)
        sleep(1)

    def blacken_5_usd(self, is_open_xe_page=True) -> None:
        if is_open_xe_page:
            self.open_xe_page()
        if self.is_shadow_element_appeared(js_path=self.POPUP_CLOSE_BTN, timeout=3):
            self.click_shadow_element(js_path=self.POPUP_CLOSE_BTN)
        self.blacken_text2(self.TEXT_5USD, is_need_full_screen=False)
        sleep(1)

    def blacken_1_eur(self, is_open_xe_page=True) -> None:
        if is_open_xe_page:
            self.open_xe_page()
        if self.is_shadow_element_appeared(js_path=self.POPUP_CLOSE_BTN, timeout=3):
            self.click_shadow_element(js_path=self.POPUP_CLOSE_BTN)
        self.blacken_text2(self.TEXT_1EUR)
        sleep(1)

    def blacken_5_eur(self, is_open_xe_page=True) -> None:
        if is_open_xe_page:
            self.open_xe_page()
        if self.is_shadow_element_appeared(js_path=self.POPUP_CLOSE_BTN, timeout=3):
            self.click_shadow_element(js_path=self.POPUP_CLOSE_BTN)
        self.blacken_text2(self.TEXT_5EUR)
        sleep(1)


class XePlayright(BasePlaywright):
    # Locator

    text_1usd = 'a[href="/currencyconverter/convert/?Amount=1&From=USD&To=EUR"]'

    def open_xe_page(self, url: str, sleep_n_seconds: int = 10) -> None:
        # self.page.on("popup", lambda popup: print("jhihi" + popup.text_content()))
        # self.page.on("dialog", lambda dialog: print("hihi" + dialog.message()))
        self.page.goto(url)
        try:
            self.page.wait_for_selector("yld-tag-host-campaign", timeout=20_000)
        except Exception:
            pass
        else:
            self.page.locator("yld-tag-host-campaign").press("Escape")

    def blacken_1_usd(self, url: str) -> None:
        self.open_xe_page(url)
        self.blacken_text2(self.text_1usd, is_need_full_screen=True)
        sleep(1)


class VirusTotalApp(Toolbar):
    # Locator
    BTN_CHOOSE_FILE = (By.NAME, "Choose file")
    BTN_CONFIRM_UPLOAD = (By.NAME, "Confirm upload")
    RESULT_OK = (
        By.NAME,
        "No security vendors and no sandboxes flagged this file as malicious",
    )

    # Interaction method
    def select_file_to_upload(self, version, file_name: str):
        self.click_element(self.BTN_CHOOSE_FILE)
        sleep(2)
        keyboard.send_keys(
            rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{file_name}"
        )
        keyboard.send_keys("{ENTER}")
        sleep(3)
        if file_name == "CocCocSetup.exe":
            pass
        else:
            if self.is_element_appeared(self.BTN_CONFIRM_UPLOAD, timeout=30):
                self.click_element(self.BTN_CONFIRM_UPLOAD)

        assert self.is_element_appeared(self.RESULT_OK, timeout=600)
        sleep(1)


class FacebookSel(BaseSelenium):
    # Locators
    USERNAME = (By.CSS_SELECTOR, "#email")
    PASSWORD = (By.CSS_SELECTOR, "#pass")
    EYE_ICON = (By.CSS_SELECTOR, "#passContainer a div>div")

    #
    def open_facebook_home(self) -> None:
        self.open_page("https://www.facebook.com/")

    def set_username(self, text: str, is_need_open_facebook=False) -> None:
        if is_need_open_facebook:
            self.open_facebook_home()
        self.fill_texts(self.USERNAME, text)

    def set_password(self, text: str, is_need_open_facebook=False) -> None:
        if is_need_open_facebook:
            self.open_facebook_home()
        self.fill_texts(self.PASSWORD, text)

    def double_click_username(self, text: str, is_need_open_facebook=False) -> None:
        if is_need_open_facebook:
            self.open_facebook_home()
        self.set_username(text)
        self.double_click_element(self.USERNAME)
        sleep(2)

    def double_click_password(self, text: str, is_need_open_facebook=False) -> None:
        if is_need_open_facebook:
            self.open_facebook_home()
        self.set_password(text)
        self.click_element(self.EYE_ICON)
        self.double_click_element(self.PASSWORD)
        sleep(2)


class SafeBrowsingSel(BaseSelenium):
    # Locators
    DOMAIN_WEBSITE_URL = (
        By.CSS_SELECTOR,
        '#safeForm div[class="w-full mt-4"]:nth-child(3) div input',
    )
    DOMAIN_WEBSITE_URL_LABEL = (
        By.CSS_SELECTOR,
        '#safeForm div[class="w-full mt-4"]:nth-child(3) label',
    )
    DOMAIN_WEBSITE_URL_ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        '#safeForm div[class="w-full mt-4"]:nth-child(3) p',
    )
    TYPE_OF_VIOLATION_LABEL = (
        By.CSS_SELECTOR,
        '#safeForm div[class="w-full mt-4"]:nth-child(4) label',
    )
    TYPE_OF_VIOLATION_ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        '#safeForm div[class="w-full mt-4"]:nth-child(4) p',
    )
    CAPTCHA_WARNING = (By.CSS_SELECTOR, '#safeForm div[class="pt-4 sm:m-auto"] p')
    BTN_SUBMIT = (By.XPATH, '//span[text()="Gửi báo cáo"]')
    DROP_DOWN = (By.CSS_SELECTOR, "#mui-component-select-type")
    DROP_DOWN_UI = (By.CSS_SELECTOR, "#menu-type ul")
    DROP_DOWN_VALUE_BLANK = (By.CSS_SELECTOR, "#menu-type > div ul li:nth-child(1)")
    DROP_DOWN_VALUE_0 = (By.CSS_SELECTOR, '#menu-type > div ul li[data-value="0"]')
    DROP_DOWN_VALUE_1 = (By.CSS_SELECTOR, '#menu-type > div ul li[data-value="1"]')
    DROP_DOWN_VALUE_2 = (By.CSS_SELECTOR, '#menu-type > div ul li[data-value="2"]')
    DROP_DOWN_VALUE_3 = (By.CSS_SELECTOR, '#menu-type > div ul li[data-value="3"]')
    DROP_DOWN_VALUE_4 = (By.CSS_SELECTOR, '#menu-type > div ul li[data-value="4"]')

    # Interaction Methods
    def open_safe_browsing_page(self) -> None:
        self.open_page(url="https://safe.coccoc.com/")

    def check_no_domain_site_url_added_as_default(self) -> None:
        self.open_safe_browsing_page()
        self.scroll_into_view_element_by_locator(self.DOMAIN_WEBSITE_URL)
        assert (
            self.get_element_attribute_by_its_name_and_locator(
                self.DOMAIN_WEBSITE_URL, "value"
            )
            == ""
        )

    def get_domain_site_url(self) -> str:
        print(self.scc.ser)
        return self.get_element_attribute_by_its_name_and_locator(
            self.DOMAIN_WEBSITE_URL, "value"
        )

    def verify_error_when_submiting_with_no_input(self) -> None:
        self.open_safe_browsing_page()
        self.scroll_into_view_element_by_locator(self.DOMAIN_WEBSITE_URL)
        self.click_element(self.BTN_SUBMIT)
        assert (
            self.get_element_text(self.DOMAIN_WEBSITE_URL_LABEL)
            == "Nhập địa chỉ Domain/Website/Url"
        )
        assert (
            self.get_element_text(self.DOMAIN_WEBSITE_URL_ERROR_MESSAGE)
            == "Định dạng Domain/Website/Url chưa đúng."
        )
        assert self.get_element_text(self.TYPE_OF_VIOLATION_LABEL) == "Kiểu vi phạm"
        assert (
            self.get_element_text(self.TYPE_OF_VIOLATION_ERROR_MESSAGE)
            == "Vui lòng lựa chọn kiểu vi phạm."
        )
        assert (
            self.get_element_text(self.CAPTCHA_WARNING) == "Bạn vui lòng nhập captcha."
        )

    def verify_type_of_violations(self) -> None:
        self.open_safe_browsing_page()
        self.scroll_into_view_element_by_locator(self.DOMAIN_WEBSITE_URL)
        try:
            self.click_element(self.DROP_DOWN)
            assert self.get_element_text(self.DROP_DOWN_VALUE_BLANK) == "--"
            assert (
                self.get_element_text(self.DROP_DOWN_VALUE_0) == "Chứa phần mềm độc hại"
            )
            assert self.get_element_text(self.DROP_DOWN_VALUE_1) == "Trang web lừa đảo"
            assert self.get_element_text(self.DROP_DOWN_VALUE_2) == "Tin tức giả mạo"
            assert self.get_element_text(self.DROP_DOWN_VALUE_3) == "Nội dung phản cảm"
            assert self.get_element_text(self.DROP_DOWN_VALUE_4) == "Khác"
        finally:
            self.click_element(self.DROP_DOWN_VALUE_BLANK)

    def click_dropdown(self) -> None:
        self.click_element(self.DROP_DOWN)
        self.is_element_appeared(self.DROP_DOWN_UI)

    def select_all_options(self) -> None:
        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_BLANK)
        assert self.get_element_text(self.DROP_DOWN) == ""

        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_0)
        self.wait_for_text_is_present(self.DROP_DOWN, "Chứa phần mềm độc hại")
        # assert self.get_element_text(self.DROP_DOWN) == "Chứa phần mềm độc hại"

        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_1)
        self.wait_for_text_is_present(self.DROP_DOWN, "Trang web lừa đảo")
        # assert self.get_element_text(self.DROP_DOWN) == "Trang web lừa đảo"

        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_2)
        self.wait_for_text_is_present(self.DROP_DOWN, "Tin tức giả mạo")
        # assert self.get_element_text(self.DROP_DOWN) == "Tin tức giả mạo"

        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_3)
        self.wait_for_text_is_present(self.DROP_DOWN, "Nội dung phản cảm")
        # assert self.get_element_text(self.DROP_DOWN) == "Nội dung phản cảm"

        self.click_dropdown()
        self.click_element(self.DROP_DOWN_VALUE_4)
        self.wait_for_text_is_present(self.DROP_DOWN, "Khác")
        # assert self.get_element_text(self.DROP_DOWN) == "Khác"


class SafeBrowsingApp(BaseAppium):
    # Locators
    DOMAIN_WEBSITE_URL = (
        By.XPATH,
        '//Edit[@AutomationId="domainsiteurl"]',
    )

    def get_current_domain_site_url(self) -> str:
        return self.get_element_attribute_by_its_name_and_locator(
            self.DOMAIN_WEBSITE_URL, "Value.Value"
        )
