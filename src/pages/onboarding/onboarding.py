import time

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright
from tests import setting

lang = setting.coccoc_language


class OnBoarding(BasePlaywright):
    @property
    def on_boarding_dialog(self) -> Locator:
        # return self.page.locator('div[class="body"] div[class="container"]')
        # return self.page.locator(
        #     'div[style="position: absolute; top: 0px; display: block !important;"] div[class="body"] div[class="container"]')
        return self.page.locator("html > div div > div.container")

    @property
    def btn_try_now(self) -> Locator:
        return self.page.locator('button[class="onboarding-btn"]')

    @property
    def btn_skip(self) -> Locator:
        return self.page.locator('button[class="cancel-btn"]')

    @property
    def btn_close(self) -> Locator:
        return self.page.locator('div[class="close_button"]')

    @property
    def icon_messenger(self) -> Locator:
        return self.page.locator('div[class="icon messenger "]')

    @property
    def icon_zalo(self) -> Locator:
        return self.page.locator('div[class="icon zalo "]')

    @property
    def icon_tele(self) -> Locator:
        return self.page.locator('div[class="icon tele "]')

    @property
    def icon_skype(self) -> Locator:
        return self.page.locator('div[class="icon skype active"]')

    @property
    def description_text(self) -> Locator:
        return self.page.locator('div[class="desc"]')

    @property
    def on_boarding_title(self) -> Locator:
        return self.page.locator('div[class="container"] div[class="title"]')

    # Interaction methods

    def open_savior_background(self):
        self.page.goto("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")

    def open_on_boarding_url(self, url: str):
        self.page.goto(url)
        time.sleep(2)

    def open_web_skype(self):
        self.page.goto("https://web.skype.com")

    def open_telegram(self):
        self.page.goto("https://web.telegram.org")

    def check_on_boarding_is_shown(self):
        expect(self.on_boarding_dialog).to_be_visible(timeout=30000)

    def check_on_boarding_is_hidden(self):
        expect(self.on_boarding_dialog).to_be_hidden(timeout=1)

    def click_try_now_btn(self):
        self.btn_try_now.click()
        time.sleep(1)
        expect(self.on_boarding_dialog).to_be_hidden(timeout=1)

    def click_close_on_boarding(self):
        self.btn_close.click()
        time.sleep(1)

    def close_on_boarding_by_pressing_esc_btn(self):
        self.page.keyboard.press("Escape")
