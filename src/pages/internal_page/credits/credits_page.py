import time

from selenium.webdriver.common.by import By

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.coccoc_common import open_browser, interactions
from tests import setting

lang = setting.coccoc_language


class CreditsPage(BasePlaywright):
    @property
    def tor_client_homepage(self) -> Locator:
        return self.page.locator('a[href="https://gitweb.torproject.org/tor.git"]')

    @property
    def tor_client_label(self) -> Locator:
        """
        Filter to get the parent locator, then from the parent locate the child
        """
        return (
            self.page.locator('div[class="product"]')
            .filter(has=self.tor_client_homepage)
            .locator("label")
        )

    @property
    def tor_client_content(self) -> Locator:
        """
        Filter to get the parent locator, then from the parent locate the child
        """
        return (
            self.page.locator('div[class="product"]')
            .filter(has=self.tor_client_homepage)
            .locator("pre")
        )

    # Libtorrent part
    @property
    def libtorrent(self) -> Locator:
        return self.page.locator('//span[text()="libtorrent"]')

    @property
    def libtorrent_homepage(self) -> Locator:
        return self.page.locator('a[href="https://www.libtorrent.org"]')

    @property
    def libtorrent_label(self) -> Locator:
        """
        Filter to get the parent locator, then from the parent locate the child
        """
        return (
            self.page.locator('div[class="product"]')
            .filter(has=self.libtorrent_homepage)
            .locator("label")
        )

    @property
    def libtorrent_content(self) -> Locator:
        """
        Filter to get the parent locator, then from the parent locate the child
        """
        return (
            self.page.locator('div[class="product"]')
            .filter(has=self.libtorrent_homepage)
            .locator("pre")
        )

    # Interaction methods
    def open_credits_page(self) -> None:
        self.page.goto("coccoc://credits/")

    def click_to_show_tor_client_homepage(self):
        self.tor_client_homepage.scroll_into_view_if_needed()
        self.tor_client_homepage.click()
        expect(self.page).to_have_title("The Tor Project / Core / Tor · GitLab")

    def click_to_show_tor_licences(self) -> None:
        self.tor_client_homepage.scroll_into_view_if_needed()
        self.tor_client_label.click()

    def check_tor_licences_content_is_shown(self) -> None:
        expect(self.tor_client_content).to_be_visible()

    def click_to_show_libtorrent_homepage(self):
        self.libtorrent_homepage.scroll_into_view_if_needed()
        self.libtorrent_homepage.click()
        expect(self.page).to_have_url("https://www.libtorrent.org/")

    def click_to_show_libtorrent_licences(self) -> None:
        self.libtorrent_homepage.scroll_into_view_if_needed()
        self.libtorrent_label.click()

    def check_libtorrent_licences_content_is_shown(self) -> None:
        expect(self.libtorrent_content).to_be_visible()


class CreditsPageSel(BaseSelenium):
    # Locators
    TEXT_CREDITS = (By.XPATH, '//span[text()="Credits"]')

    # Interaction methods
    def open_credits_page(self) -> None:
        self.open_page(url="coccoc://credits/")

    def double_click_text_credits(self) -> None:
        self.open_credits_page()
        self.double_click_element(self.TEXT_CREDITS)
