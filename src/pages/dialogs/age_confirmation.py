from time import sleep
from playwright.sync_api import Locator, expect
from selenium.webdriver.common.by import By

from src.pages.base import BasePlaywright, BaseSelenium
from tests import setting

lang = setting.coccoc_language


class AgeConfirmationSel(BaseSelenium):
    # Locator
    if "en" in lang:
        AGE_CONFIRMATION_TITLE = (By.XPATH, '//div[text()="Confirm your age"]')
    else:
        AGE_CONFIRMATION_TITLE = (By.XPATH, '//div[text()="Xác nhận tuổi của bạn"]')

    if "en" in lang:
        CONFIRMATION_DES = (
            By.XPATH,
            '//div[text()="We need to verify your age to show approriate content, Please confirm that you are 18 or higher"]',
        )
    else:
        CONFIRMATION_DES = (
            By.XPATH,
            '//div[text()="Chúng tôi cần xác nhận tuổi của bạn nhằm mục đích hiển thị các nội dung phù hợp. Xin vui lòng xác nhận nếu bạn đã đủ 18 tuổi."]',
        )
    if "en" in lang:
        BTN_NO = (By.XPATH, '//div[text()="NO, I\'M UNDER 18"]')
    else:
        BTN_NO = (By.XPATH, '//div[text()="Tôi dưới 18 tuổi"]')

    if "en" in lang:
        BTN_YES = (By.XPATH, '//div[text()="YES, CONFIRM"]')
    else:
        BTN_YES = (By.XPATH, '//div[text()="Tôi đã đủ 18 tuổi"]')

    # Interaction methods

    def verify_popup_appears(self) -> None:
        assert self.get_element(self.AGE_CONFIRMATION_TITLE)
        assert self.get_element(self.CONFIRMATION_DES)
        assert self.get_element(self.BTN_NO)
        assert self.get_element(self.BTN_YES)

    def verify_popup_does_not_appears(self) -> None:
        sleep(5)  # Sleep 5 seconds for waiting if any Age confirmation popup shown
        assert self.is_element_disappeared(self.AGE_CONFIRMATION_TITLE)
        assert self.is_element_disappeared(self.CONFIRMATION_DES)
        assert self.is_element_disappeared(self.BTN_NO)
        assert self.is_element_disappeared(self.BTN_YES)

    def click_btn_yes(self) -> None:
        self.click_element(self.BTN_YES)
        self.verify_popup_does_not_appears()

    def click_btn_no(self) -> None:
        self.click_element(self.BTN_NO)
        self.verify_popup_does_not_appears()


class AgeConfirmationPlay(BasePlaywright):
    # Locator
    @property
    def age_confirmation_title(self) -> Locator:
        if "en" in lang:
            return self.page.locator('//div[text()="Confirm your age"]')
        else:
            return self.page.locator('//div[text()="Xác nhận tuổi của bạn"]')

    @property
    def age_confirmation_des(self) -> Locator:
        if "en" in lang:
            return self.page.locator(
                '//div[text()="We need to verify your age to show approriate content, Please confirm that you are 18 or higher"]'
            )
        else:
            return self.page.locator(
                '//div[text()="Chúng tôi cần xác nhận tuổi của bạn nhằm mục đích hiển thị các nội dung phù hợp. Xin vui lòng xác nhận nếu bạn đã đủ 18 tuổi."]'
            )

    @property
    def btn_no(self) -> Locator:
        if "en" in lang:
            return self.page.locator('//div[text()="NO, I\'M UNDER 18"]')
        else:
            return self.page.locator('//div[text()="Tôi dưới 18 tuổi"]')

    @property
    def btn_yes(self) -> Locator:
        if "en" in lang:
            return self.page.locator('//div[text()="YES, CONFIRM"]')
        else:
            return self.page.locator('//div[text()="Tôi đã đủ 18 tuổi"]')

    # Interaction methods

    def verify_popup_appears(self) -> None:
        expect(self.age_confirmation_title).to_be_visible()
        expect(self.age_confirmation_des).to_be_visible()
        expect(self.btn_no).to_be_visible()
        expect(self.btn_yes).to_be_visible()

    def verify_popup_does_not_appears(self) -> None:
        sleep(5)  # Sleep 5 seconds for waiting if any Age confirmation popup shown
        expect(self.age_confirmation_title).to_be_hidden()
        expect(self.age_confirmation_des).to_be_hidden()
        expect(self.btn_no).to_be_hidden()
        expect(self.btn_yes).to_be_hidden()

    def click_btn_yes(self) -> None:
        self.btn_yes.click()
        self.verify_popup_does_not_appears()

    def click_btn_no(self) -> None:
        self.btn_no.click()
        self.verify_popup_does_not_appears()
