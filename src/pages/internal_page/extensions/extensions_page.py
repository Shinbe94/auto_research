import time

from playwright.sync_api import Locator
from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium, BasePlaywright, BaseSelenium
from appium.webdriver.webelement import WebElement
from src.pages.constant import LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class ExtensionsPage(BasePlaywright):
    @property
    def developer_mode(self) -> Locator:
        return self.page.locator("#devMode")

    @property
    def savior_background(self) -> Locator:
        return self.page.locator(
            'extensions-item[id="jdfkmiabjpfjacifcmihfdjhpnjpiick"] a[class="clippable-flex-text"]'
        )

    @property
    def savior_toggle_btn(self) -> Locator:
        return self.page.locator(
            'extensions-item[id="jdfkmiabjpfjacifcmihfdjhpnjpiick"] #enableToggle'
        )

    # Interaction methods
    def open_page_extension_page(self):
        self.page.goto("coccoc://extensions/")

    def get_developer_mode_state(self) -> str:
        return self.get_attribute_value_by_locator(self.developer_mode, "aria-pressed")

    def get_status_extension(self, locator: Locator) -> str:
        return self.get_attribute_value_by_locator(locator, "aria-pressed")

    def turn_on_developer_mode(self):
        if self.get_developer_mode_state() != "true":
            self.developer_mode.click()
            assert self.get_developer_mode_state() == "true"

    def turn_off_developer_mode(self):
        if self.get_developer_mode_state() != "false":
            self.developer_mode.click()
            assert self.get_developer_mode_state() == "false"

    def click_savior_background(self):
        self.savior_background.click()

    def open_savior_background(self):
        self.open_page_extension_page()
        self.turn_on_developer_mode()
        # self.click_savior_background()
        # with self.page.expect_popup() as popup_info:
        #     # self.click_savior_background()
        #     self.savior_background.click()
        # popup = popup_info.value
        # popup.wait_for_load_state()
        # # new_window = self.page.context.wait_for_event('page', self.click_savior_background())
        # # new_window = self.page.context.expect_page(self.click_savior_background())
        # print('title' + popup.title())
        # return popup
        # with self.page.context.expect_page() as new_page:
        #     self.savior_background.click()
        #
        # pages = new_page.value.context.pages
        # for new_page in pages:
        #     new_page.wait_for_load_state()
        #     print(new_page.title())
        # with self.page.expect_event('page') as new_page:
        #     self.savior_background.click()
        #
        # pages = new_page.value
        # print(pages.url)
        # return pages
        # for new_page in pages:
        #     new_page.wait_for_load_state()
        #     print(new_page.title())
        # page2 = self.page.context.new_page()
        # page2.goto('chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html')
        # return page2

    def handle_new_window(self):
        self.page.goto("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        self.page.evaluate("chrome.storage.local.set({ onboardTrack: {} });")
        self.page.evaluate(
            r"""
                Object.keys(chrome.metricsPrivate).forEach(function (key) {
                var method = chrome.metricsPrivate[key];
                if (typeof method !== 'function' || key.indexOf('record') !== 0) {
                return;
                }
                chrome.metricsPrivate['__' + key] = method;
                chrome.metricsPrivate[key] = function () {
                if (key === 'recordCustomData' && arguments[0] && arguments[0].length === 1) {
                console.info(
                'recordCustomData %c%s', 'color: lime',
                arguments[0][0].key,
                JSON.parse(arguments[0][0].value)
                );
                return;
                }
                console.info.bind(console, key).apply(console, arguments);
                return chrome.metricsPrivate['__' + key].apply(chrome.metricsPrivate, arguments);
                };
                });
                """
        )
        return self.page

    def force_points_onboarding_shown(self) -> None:
        self.open_page("chrome-extension://jdfkmiabjpfjacifcmihfdjhpnjpiick/popup.html")
        self.evaluate_js(
            'chrome.storage.local.set({ onboardTrack: {"point": {"forceShow": true}} })'
        )

    def turn_on_savior(self):
        self.open_page_extension_page()
        if not self.get_status_extension(self.savior_toggle_btn) == "true":
            self.savior_toggle_btn.click()
            assert self.get_status_extension(self.savior_toggle_btn) == "true"

    def turn_off_savior(self):
        self.open_page_extension_page()
        if not self.get_status_extension(self.savior_toggle_btn) == "false":
            self.savior_toggle_btn.click()
            assert self.get_status_extension(self.savior_toggle_btn) == "false"


class ExtensionsPageSel(BaseSelenium):
    # Locators

    def js_path_extension_name(self, extension_id: str) -> str:
        return f'{LocatorJSPath.EXTENTIONS_PRE}{extension_id}").shadowRoot.querySelector("#name")'

    def js_path_remove_btn(self, extension_id: str) -> str:
        return f'{LocatorJSPath.EXTENTIONS_PRE}{extension_id}").shadowRoot.querySelector("#removeButton")'

    def js_path_detail_btn(self, extension_id: str) -> str:
        return f'{LocatorJSPath.EXTENTIONS_PRE}{extension_id}").shadowRoot.querySelector("#detailsButton")'

    def js_path_toggle_status(self, extension_id: str) -> str:
        return f'{LocatorJSPath.EXTENTIONS_PRE}{extension_id}").shadowRoot.querySelector("#enableToggle")'

    def js_path_darklist(self, extension_id: str) -> str:
        return f'{LocatorJSPath.EXTENTIONS_PRE}{extension_id}").shadowRoot.querySelector("#blacklisted-warning")'

    COCCOC_EXTENSIONS_ITEM_CONTAINER = f'{LocatorJSPath.EXTENTIONS_ITEM_LIST}.shadowRoot.querySelectorAll("#content-wrapper div.items-container")'

    # interaction methods

    def open_extension_page(self) -> None:
        self.open_page(url="coccoc://extensions/")

    def open_extension_detail(self, extension_id: str) -> None:
        self.open_page(url=f"coccoc://extensions/?id={extension_id}")

    def get_extension_name_by_id(
        self, extension_id: str, is_need_open_extension_page=True
    ) -> str:
        if is_need_open_extension_page:
            self.open_extension_page()
        return self.get_text_shadow_element(
            js_path=self.js_path_extension_name(extension_id)
        )

    def check_extension_darklist(
        self, extension_id: str, is_need_open_extension_page=True, timeout=120
    ) -> None:
        """Wait for the extension becomes to darklist and the warning shown

        Args:
            extension_id (str): _description_
            is_need_open_extension_page (bool, optional): _description_. Defaults to True.
            timeout (int, optional): _description_. Defaults to 120.

        Raises:
            ValueError: _description_
        """
        warning_info_element: WebElement = None
        total_delay: int = 0
        interval_delay: int = 5
        if is_need_open_extension_page:
            self.open_extension_page()
        while total_delay < timeout:
            try:
                warning_info_element = self.get_shadow_element(
                    js_path=self.js_path_darklist(extension_id), timeout=5
                )
            except Exception:
                time.sleep(interval_delay)
                total_delay += interval_delay
            else:
                if "en" in lang:
                    if (
                        warning_info_element.text
                        == "Disabled by Cốc Cốc. This extension may be unsafe."
                    ):
                        break

                else:
                    if (
                        warning_info_element.text
                        == "Đã bị Cốc Cốc vô hiệu hóa. Tiện ích này có thể không an toàn."
                    ):
                        break

            if total_delay > timeout:
                raise ValueError(
                    f"Timeout after waiting {total_delay} seconds for checking dark list"
                )

    def remove_extension(
        self,
        extension_id: str,
        is_need_open_extension_page=True,
        sleep_n_seconds: int = 1,
    ) -> None:
        """click btn remove extension

        Args:
            extension_id (str): _description_
            is_need_open_extension_page (bool, optional): _description_. Defaults to True.
            sleep_n_seconds (int, optional): _description_. Defaults to 1.
        """
        if is_need_open_extension_page:
            self.open_extension_page()
        self.click_shadow_element(js_path=self.js_path_remove_btn(extension_id))
        time.sleep(sleep_n_seconds)

    def click_detail_btn(
        self,
        extension_id: str,
        is_need_open_extension_page=True,
    ) -> None:
        """This method helps to open extension detail page by its id

        Args:
            extension_id (str): _description_
            is_need_open_extension_page (bool, optional): _description_. Defaults to True.
        """
        if is_need_open_extension_page:
            self.open_extension_page()
        self.click_shadow_element(js_path=self.js_path_detail_btn(extension_id))

    def click_toggle_status(self, extension_id: str) -> None:
        self.click_shadow_element(self.js_path_toggle_status(extension_id=extension_id))

    def get_extension_toggle_status(
        self, extension_id: str, is_need_open_extension_page: bool = True
    ) -> str:
        if is_need_open_extension_page:
            self.open_extension_page()
        return self.get_attribute_value_of_shadow_element(
            js_path=self.js_path_toggle_status(extension_id=extension_id),
            attribute_name="aria-pressed",
        )

    def turning_on_extension_toggle_status(self, extension_id: str) -> None:
        if self.get_extension_toggle_status(extension_id=extension_id) != "true":
            self.click_toggle_status(extension_id=extension_id)
            self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_toggle_status(extension_id=extension_id),
                attribute_name="aria-pressed",
                att_value="true",
            )

    def turning_off_extension_toggle_status(self, extension_id: str) -> None:
        if self.get_extension_toggle_status(extension_id=extension_id) != "false":
            self.click_toggle_status(extension_id=extension_id)
            self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_toggle_status(extension_id=extension_id),
                attribute_name="aria-pressed",
                att_value="false",
            )

    def check_list_coccoc_extensions_are_in_a_group(self) -> None:
        self.open_extension_page()
        list_item_containers = self.get_shadow_elements(
            self.COCCOC_EXTENSIONS_ITEM_CONTAINER
        )
        for ele in list_item_containers:
            if len(ele.find_elements_by_tag_name("extensions-item")) > 0:
                assert ele.find_element_by_id(setting.dictionary_extension_id)
                assert ele.find_element_by_id(setting.cashback_extension_id)
                assert ele.find_element_by_id(setting.savior_extension_id)


class ExtensionsPageApp(BaseAppium):
    # Locators
    # if lang == "en":
    #     BTN_CONFIRM_REMOVE = (By.NAME, "Remove")
    # else:
    #     BTN_CONFIRM_REMOVE = (By.NAME, "Xóa")

    # BTN_CONFIRM_REMOVE = (
    #     By.XPATH,
    #     '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name=\'Remove "Volume Master"?\']//Button[@Name="Remove"]',
    # )

    # Interaction methods:

    def click_btn_confirm_remove_extension(self, extension_name: str) -> None:
        BTN_CONFIRM_REMOVE = (
            By.XPATH,
            f'//Pane[@ClassName="Chrome_WidgetWin_1"][@Name=\'Remove "{extension_name}"?\']//Button[@Name="Remove"]',
        )
        self.double_click_element(BTN_CONFIRM_REMOVE)
