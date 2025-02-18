from time import sleep
from selenium.webdriver.common.by import By
from src.pages.base import BaseSelenium
from src.pages.constant import LocatorJSPath
from src.utilities import os_utils


class UnitConverterSel(BaseSelenium):
    # Locator
    JS_PATH_UNIT_EX = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-money-main.coccoc-dark-theme")'
    JS_PATH_UNIT_EX_HIDDEN = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-money-main.coccoc-dark-theme.hidden")'
    JS_PATH_UNIT_EX_MORE_CURRENCY = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-btn-currencies")'
    )
    JS_PATH_UNIT_EX_MORE_CURRENCY_BACK = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-more-back")'
    )
    JS_PATH_UNIT_EX_MORE_CURRENCY_ADD = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-more-add")'
    )
    JS_PATH_UNIT_EX_MORE_CURRENCY_LIST = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelectorAll("div.coccoc-currency-short")'
    )
    JS_PATH_UNIT_EX_MORE_CURRENCY_VALUE = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelectorAll("div.coccoc-currency-value")'
    )
    JS_PATH_UNIT_EX_MORE_CURRENCY_SIGN = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelectorAll("div.coccoc-currency-sign")'
    )
    JS_PATH_UNIT_EX_ARROW = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-arrow")'
    )
    JS_PATH_UNIT_EX_INFO = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-btn-info")'
    )
    JS_PATH_UNIT_EX_INFO_TEXT = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-info-text")'
    )
    JS_PATH_UNIT_EX_INFO_SOURCE = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-info-text > span")'
    )
    JS_PATH_UNIT_EX_COPY = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-btn-copy")'
    )
    JS_PATH_UNIT_EX_CLOSE = (
        f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-btn-close")'
    )
    JS_PATH_UNIT_EX_FROM_VALUE = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-value-from div.coccoc-value")'
    JS_PATH_UNIT_EX_FROM_VALUE_COPIED = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-value-from div.coccoc-value.copied")'

    JS_PATH_UNIT_EX_TO_VALUE = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-value-to div.coccoc-value")'
    JS_PATH_UNIT_EX_TO_VALUE_COPIED = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-value-to div.coccoc-value.copied")'

    JS_PATH_ADD_MORE_CURRENCY_NOTI_TEXT = f'{LocatorJSPath.UNIT_EX_PRE}.querySelector("div.coccoc-add-currencies.coccoc-dark-theme")'

    def check_exchange_1_usd(self) -> None:
        try:
            # Check basic UI
            self.check_ui_unit_exchange()
            # Check 1 USD
            assert (
                self.get_text_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
                == "USD 1.00"
            )
            assert self.get_text_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE) != ""
        finally:
            sleep(1)
            self.click_shadow_element(self.JS_PATH_UNIT_EX_CLOSE)

    def check_exchange_5_usd(self) -> None:
        try:
            # Check basic UI
            self.check_ui_unit_exchange()
            # Check 5 USD
            assert (
                self.get_text_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
                == "USD 5.00"
            )
            assert self.get_text_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE) != ""
        finally:
            sleep(1)
            self.click_shadow_element(self.JS_PATH_UNIT_EX_CLOSE)

    def check_exchange_1_eur(self) -> None:
        try:
            # Check basic UI
            self.check_ui_unit_exchange()
            # Check 1 EUR
            assert (
                self.get_text_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
                == "EUR 1.00"
            )
            assert self.get_text_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE) != ""
        finally:
            sleep(1)
            self.click_shadow_element(self.JS_PATH_UNIT_EX_CLOSE)

    def check_exchange_5_eur(self) -> None:
        try:
            # Check basic UI
            self.check_ui_unit_exchange()
            # Check 5 EUR
            assert (
                self.get_text_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
                == "EUR 5.00"
            )
            assert self.get_text_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE) != ""
        finally:
            sleep(1)
            self.click_shadow_element(self.JS_PATH_UNIT_EX_CLOSE)

    def check_ui_unit_exchange(self) -> None:
        sleep(1)
        # Dialog unit exchange shown
        assert self.get_shadow_element(self.JS_PATH_UNIT_EX).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_UNIT_EX_MORE_CURRENCY
        ).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_UNIT_EX_ARROW).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_UNIT_EX_INFO).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_UNIT_EX_COPY).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_UNIT_EX_CLOSE).is_displayed()

    def check_unit_exchange_not_shown(self) -> bool:
        return self.is_shadow_element_disappeared(self.JS_PATH_UNIT_EX, timeout=5)

    def check_unit_exchange_is_hidden(self) -> None:
        sleep(1)
        assert self.is_shadow_element_appeared(js_path=self.JS_PATH_UNIT_EX_HIDDEN)

    def click_btn_info(self) -> None:
        self.click_shadow_element(js_path=self.JS_PATH_UNIT_EX_INFO)
        assert "Tỷ giá bởi" in self.get_text_shadow_element(
            js_path=self.JS_PATH_UNIT_EX_INFO_TEXT
        )
        assert (
            self.get_text_shadow_element(js_path=self.JS_PATH_UNIT_EX_INFO_SOURCE)
            == "www.vietcombank.com.vn"
        )

    def copy_value_from(self) -> None:
        actual_text = self.get_text_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
        self.click_shadow_element(self.JS_PATH_UNIT_EX_FROM_VALUE)
        text_from_clipboard = os_utils.get_clipboard_text()
        assert actual_text == text_from_clipboard

    def copy_value_to(self) -> None:
        actual_text = self.get_text_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE)
        self.click_shadow_element(self.JS_PATH_UNIT_EX_TO_VALUE)
        text_from_clipboard = os_utils.get_clipboard_text()
        assert actual_text == text_from_clipboard

    def click_btn_copy(self, text: str) -> None:
        self.click_shadow_element(self.JS_PATH_UNIT_EX_COPY)
        text_from_clipboard = os_utils.get_clipboard_text()
        assert text == text_from_clipboard

    def click_btn_more(self) -> None:
        self.click_shadow_element(self.JS_PATH_UNIT_EX_MORE_CURRENCY)

    def check_ui_after_click_btn_more(self) -> None:
        assert self.is_shadow_element_appeared(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_BACK
        )
        assert self.is_shadow_element_appeared(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_ADD
        )
        assert "Thêm ngoại tệ khác" in self.get_text_shadow_element(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_ADD
        )
        assert ["USD", "EUR", "JPY", "CNY"] == self.get_list_more_corrency()
        assert len(self.get_list_more_corrency_value()) == 4
        assert ["$", "€", "￥", "¥"] == self.get_list_more_corrency_sign()

    def get_list_more_corrency(self) -> list:
        elements = self.get_shadow_elements(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_LIST
        )
        return [ele.text for ele in elements]

    def get_list_more_corrency_value(self) -> list:
        elements = self.get_shadow_elements(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_VALUE
        )
        return [ele.text for ele in elements]

    def get_list_more_corrency_sign(self) -> list:
        elements = self.get_shadow_elements(
            js_path=self.JS_PATH_UNIT_EX_MORE_CURRENCY_SIGN
        )
        return [ele.text for ele in elements]

    def click_btn_add_more_currency(self) -> None:
        self.click_btn_more()
        self.click_shadow_element(self.JS_PATH_UNIT_EX_MORE_CURRENCY_ADD)
        sleep(1)
        assert (
            "Chức năng này sẽ tiếp tục cập nhật bạn nhé, hy vọng bạn cảm thấy hài lòng"
            in self.get_text_shadow_element(self.JS_PATH_ADD_MORE_CURRENCY_NOTI_TEXT)
        )
