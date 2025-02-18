import time
from time import sleep

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright, BaseSelenium
from tests import setting

lang = setting.coccoc_language


class PointsOnBoarding(BasePlaywright):
    @property
    def on_boarding_dialog(self) -> Locator:
        # return self.page.locator('div[class="body"] div[class="container"]')
        # return self.page.locator(
        #     'div[style="position: absolute; top: 0px; display: block !important;"] div[class="body"] div[class="container"]')
        return self.page.locator("html > div div > div.container")

    @property
    def logo(self) -> Locator:
        return self.page.locator('div[class="logo"]')

    @property
    def onboarding_title(self) -> Locator:
        return self.page.locator('div[class="container"] div[class="title"]')

    @property
    def btn_close(self) -> Locator:
        return self.page.locator('div[class="close_button"]')

    @property
    def feature_image(self) -> Locator:
        return self.page.locator('div[class="feature-img"] img')

    @property
    def feature_image_en(self) -> Locator:
        return self.page.locator(
            'img[src="chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/images/pointImage_en.png"]'
        )

    @property
    def feature_image_vi(self) -> Locator:
        return self.page.locator(
            'img[src="chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/images/pointImage_vi.png"]'
        )

    @property
    def description_text(self) -> Locator:
        return self.page.locator('div[class="desc "]')

    @property
    def btn_skip(self) -> Locator:
        return self.page.locator('button[class="cancel-btn"]')

    @property
    def btn_login_now(self) -> Locator:
        return self.page.locator('button[class="onboarding-btn"]')

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
        self.btn_login_now.click()
        time.sleep(1)
        expect(self.on_boarding_dialog).to_be_hidden(timeout=1)

    def click_close_on_boarding(self):
        self.btn_close.click()
        time.sleep(1)

    def close_on_boarding_by_pressing_esc_btn(self):
        self.page.keyboard.press("Escape")

    def verify_points_onboarding_ui_non_logged_in(self) -> None:
        sleep(15)  # sleep 15 seconds for onboarding shown
        expect(self.logo).to_be_visible()
        if "en" in lang:
            expect(self.onboarding_title).to_contain_text(
                "Are you ready to Surf web – Earn points – Get rewards?"
            )
        else:
            expect(self.onboarding_title).to_contain_text(
                "Bạn đã sẵn sàng Lướt web - Tích điểm - Đổi quà?"
            )
        expect(self.feature_image).to_be_visible()
        if "en" in lang:
            expect(self.feature_image_en).to_be_visible()
        else:
            expect(self.feature_image_vi).to_be_visible()
        if "en" in lang:
            expect(self.description_text).to_contain_text(
                "All you need to do is log in to Cốc Cốc Account and earn 100 points instantly. Redeem your points for valuable gifts."
            )
        else:
            expect(self.description_text).to_contain_text(
                "Tất cả những gì bạn cần làm là đăng nhập Tài khoản Cốc Cốc và nhận ngay 100 điểm thưởng. Tích điểm ngay hôm nay và nhanh tay đổi lấy những phần quà hấp dẫn!"
            )
        if "en" in lang:
            expect(self.btn_skip).to_contain_text("Skip")
        else:
            expect(self.btn_skip).to_contain_text("Bỏ qua")
        if "en" in lang:
            expect(self.btn_login_now).to_contain_text("Try now")
        else:
            expect(self.btn_login_now).to_contain_text("Đăng nhập ngay")

    def verify_points_onboarding_ui_logged_in(self) -> None:
        sleep(15)  # sleep 15 seconds for onboarding shown
        expect(self.logo).to_be_visible()
        if "en" in lang:
            expect(self.onboarding_title).to_contain_text(
                "Lots of rewards are awaiting you on Cốc Cốc Points"
            )
        else:
            expect(self.onboarding_title).to_contain_text(
                "Rất nhiều quà tặng đang chờ bạn trên Cốc Cốc Points"
            )
        expect(self.feature_image).to_be_visible()
        if "en" in lang:
            expect(self.feature_image_en).to_be_visible()
        else:
            expect(self.feature_image_vi).to_be_visible()
        if "en" in lang:
            expect(self.description_text).to_contain_text(
                "Once you log in to your Cốc Cốc Account, you will automatically become a member of Cốc Cốc Points and receive points when using our browser. Access Cốc Cốc Points on sidebar now to redeem your points for rewards."
            )
        else:
            expect(self.description_text).to_contain_text(
                "Khi đăng nhập Tài khoản Cốc Cốc, bạn tự động trở thành thành viên Cốc Cốc Points và nhận điểm thưởng khi sử dụng trình duyệt. Truy cập ngay Cốc Cốc Points trên thanh truy cập nhanh và sử dụng điểm thưởng đã tích lũy được bằng cách quy đổi thành quà tặng."
            )
        if "en" in lang:
            expect(self.btn_skip).to_contain_text("Skip")
        else:
            expect(self.btn_skip).to_contain_text("Bỏ qua")
        if "en" in lang:
            expect(self.btn_login_now).to_contain_text("Log in now")
        else:
            expect(self.btn_login_now).to_contain_text("Thử ngay")

    def check_onboarding_is_not_shown(self) -> bool:
        sleep(15)  # sleep 15 seconds for onboarding shown
        # expect(self.logo).to_be_hidden()
        if "en" in lang:
            expect(self.onboarding_title).not_to_contain_text(
                "Are you ready to Surf web – Earn points – Get rewards?"
            )
        else:
            expect(self.onboarding_title).not_to_contain_text(
                "Bạn đã sẵn sàng Lướt web - Tích điểm - Đổi quà?"
            )

    def check_points_onboarding_is_shown_by_console(self) -> str:
        self.open_page("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        return self.evaluate_js(
            """async () => {async function hasPoints() {
                    return new Promise((resolve) => {
                        chrome.storage.local.get(result => {
                            if (result.onboardTrack.point) {
                                return resolve(true);
                            }
                            resolve(false);
                        })
                    });
                }
                return await hasPoints()}"""
        )

    def clear_onboarding_local_storage(self) -> None:
        self.open_page("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        self.evaluate_js("await chrome.storage.local.clear()")


class PointsOnBoardingSel(BaseSelenium):
    # Locators
    JS_PATH_ONBOARDING = r'document.querySelector("html > div").shadowRoot.querySelector("div > div.container")'
    # Interaction methods

    def check_point_onboarding_shown(self) -> None:
        sleep(15)  # sleep 15 seconds for onboarding shown
        assert self.get_shadow_element(self.JS_PATH_ONBOARDING)

    def clear_onboarding_local_storage(self) -> None:
        self.open_page("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        self.execute_js("await chrome.storage.local.clear()")
