from time import sleep
from typing import List
from playwright.sync_api import Locator
from src.pages.base import BasePlaywright, BaseSelenium
from playwright.sync_api import Page, Locator
from selenium.webdriver.common.by import By

from tests import setting


class NewTabPage(BasePlaywright):
    # Locators
    @property
    def newsfeed_ads(self) -> List[Locator]:
        return self.page.locator('a[data-ad-element="AdView"]').all()

    @property
    def video_ads(self) -> Locator:
        return self.page.locator("#animation_container")

    @property
    def icon_ads(self) -> List[Locator]:
        return self.page.locator('li[class="most-visited-tile mv-qc"] a').all()

    @property
    def full_skin_ads(self) -> Locator:
        return self.page.locator("#container")

    @property
    def vast_video(sef) -> Locator:
        return sef.page.locator('iframe[id="ntrb-vast"]')

    @property
    def search_string(sef) -> Locator:
        return sef.page.locator('input[id="search-string"]')

    # Interaction methods
    def open_any_page(self, url: str) -> Page:
        return self.page.goto(url)

    def open_coccoc_homepage(self) -> Page:
        return self.page.goto("https://coccoc.com")

    def click_vast_video_ads(self):
        self.vast_video.click()
        self.page.context.on("page", self.handle_page)

    def get_list_newsfeed_ads(self):
        try:
            if len(self.newsfeed_ads) > 0:
                return self.newsfeed_ads
        except Exception:
            pass

    def get_list_newsfeed_ads_urls(self) -> List[str]:
        """Get list newsfeed ads urls

        Returns:
            List[str]: _description_
        """
        if len(self.get_list_newsfeed_ads()) > 0:
            return [ele.get_attribute("href") for ele in self.get_list_newsfeed_ads()]

    def click_list_newsfeed_ads(self) -> None:
        """Click newsfeed ads from the new tab page"""
        try:
            for ele in self.newsfeed_ads:
                ele.click()
                sleep(1)
                self.page.context.on("page", self.handle_page)
        except Exception as e:
            # pass
            raise e

    def get_video_ads_url(self):
        """Get Video ads

        Returns:
            _type_: _description_
        """
        try:
            if self.video_ads:
                return self.video_ads.get_attribute("href")
        except Exception:
            pass

    def click_video_ads(self) -> None:
        """Try to find any video ads then click it"""
        try:
            self.video_ads.click()
            self.page.context.on("page", self.handle_page)
        except Exception:
            pass

    def get_list_icon_ads_url(self) -> List[str]:
        """Get list icon ads urls

        Returns:
            List[str]: _description_
        """
        list_icon_ads = []
        try:
            list_icon_ads = self.icon_ads
        except Exception:
            pass
        return [ele.get_attribute("href") for ele in list_icon_ads]

    def click_icon_ads(self) -> None:
        """Click newsfeed ads from the new tab page"""
        urls = self.get_list_icon_ads_url()
        if len(urls) > 0:
            for url in urls:
                self.open_any_page(url=url)
                assert self.page.title()
                sleep(1)

    def get_full_skin_ads_url(self):
        try:
            if self.full_skin_ads:
                return self.full_skin_ads.get_attribute("href")
        except Exception:
            pass

    def click_full_skin_ads(self) -> None:
        """Try to find any video ads then click it"""
        try:
            self.full_skin_ads.click()
            self.page.context.on("page", self.handle_page())
        except Exception:
            pass

    def click_ads(self) -> None:
        list_newsfeed_ads_url = self.get_list_newsfeed_ads_urls()

        video_ads_url = self.get_video_ads_url()

        list_icon_ads_urls = self.get_list_icon_ads_url()

        full_skin_ads_url = self.get_full_skin_ads_url()

        list_ads = list_icon_ads_urls + list_newsfeed_ads_url

        if video_ads_url:
            list_ads.append(video_ads_url)
        if full_skin_ads_url:
            list_ads.append(full_skin_ads_url)

        try:
            for url in list_ads:
                self.open_any_page(url)
                sleep(1)
                self.page.context.on("page", self.handle_page)
        except Exception:
            pass

    # def monitor_network(self) -> None:

    def make_search(self, search_string: str, is_press_enter=True) -> None:
        self.open_any_page(url=setting.coccoc_homepage_newtab)
        self.search_string.fill(value=search_string)
        if is_press_enter:
            self.page.keyboard.press("Enter")

    def scroll_to_view_of_last_newfeed_card(self) -> None:
        self.page.evaluate(
            "[...document.querySelectorAll('.nf-card')].at(-1).scrollIntoView({behavior: 'smooth'});"
        )

    def open_n_newtab_at_the_same_time(
        self, n: int, url=setting.coccoc_homepage_newtab
    ) -> None:
        for _ in range(n):
            self.page.evaluate('window.open("{}", "_blank");'.format(url))
            self.page.wait_for_load_state()


class NewTabPageSel(BaseSelenium):
    VAST_VIDEO = (By.CSS_SELECTOR, 'iframe[id="ntrb-vast"]')
    NEWSFEED_ADS = (By.CSS_SELECTOR, 'a[data-ad-element="AdView"]')

    def open_any_page(self, url: str):
        self.open_page(url=url)

    def click_vast_video(self) -> None:
        first_window = self.get_current_window()
        sleep(10)
        self.click_element(self.VAST_VIDEO)
        # self.click_element_by_js(self.get_element(self.VAST_VIDEO))
        try:
            # self.switch_to_window(self.get_all_windows_handle()[1])
            # self.wait_for_page_to_load(load_status="complete", timeout=30)
            for window in self.get_all_windows_handle():
                if window != first_window:
                    self.switch_to_window(window)
                    self.wait_for_page_to_load(load_status="complete", timeout=30)
        finally:
            self.scc.close()
            self.switch_to_window(first_window)

    def click_list_newsfeed_ads(self) -> None:
        """Click newsfeed ads from the new tab page"""

        assert self.get_count(self.NEWSFEED_ADS) > 0
        first_window = self.get_current_window()
        for i, element in enumerate(self.get_elements(self.NEWSFEED_ADS)):
            element.click()
            windows = self.get_all_windows_handle()
            self.switch_to_window(windows[i + 1])
            self.wait_for_page_to_load()
            # assert self.driver.title # some sites block CocCoc's IP address
            self.switch_to_window(first_window)
