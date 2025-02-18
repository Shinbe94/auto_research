from time import sleep
from selenium.webdriver.common.by import By
from appium.webdriver.webelement import WebElement
from src.pages.constant import CocCocSettingTitle, LocatorJSPath
from src.pages.internal_page.extensions.extensions_page import ExtensionsPageSel
from tests import setting

lang = setting.coccoc_language


class ExtensionDetailPageSel(ExtensionsPageSel):
    # Locators
    def js_path_detail_permissions(self) -> str:
        return (
            f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#permissions-list")'
        )

    def js_path_list_detail_inspect_view(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#inspectable-views").querySelector("#inspect-views")'

    def js_path_list_detail_permissions(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#permissions-list > li")'

    def js_path_detail_toggle(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#enableToggle")'

    def js_path_detail_extenstion_status(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#enable-section > span")'

    def js_path_detail_extension_options(self) -> str:
        return (
            f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#extensionsOptions")'
        )

    def js_path_section_hr(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelectorAll("#container div.section.hr")'

    def js_path_allow_incognito_toggle(self) -> str:
        return f'{LocatorJSPath.EXTENTIONS_DETAIL_PRE}.querySelector("#allow-incognito").shadowRoot.querySelector("#crToggle")'

    LABEL_CHECK_BOX_DOUBLE_CLICK = (
        By.CSS_SELECTOR,
        'label[for="double-click-translate"]',
    )
    LABEL_CHECK_BOX_SHOW_TOOLTIP = (By.CSS_SELECTOR, 'label[for="show-tooltip"]')
    LABEL_CHECK_BOX_TEXTAREA = (By.CSS_SELECTOR, 'label[for="input-translate"]')
    LABEL_CHECK_BOX_UNIT_CONVERTER = (
        By.CSS_SELECTOR,
        'label[for="currency-converter"]',
    )
    CHECK_BOX_DOUBLE_CLICK_TRANSLATE = (By.CSS_SELECTOR, "#double-click-translate")
    CHECK_BOX_SHOW_TOOLTIP = (By.CSS_SELECTOR, "#show-tooltip")
    CHECK_BOX_TEXTAREA = (By.CSS_SELECTOR, "#input-translate")
    CHECK_BOX_CURRENCY_CONVERTER = (By.CSS_SELECTOR, "#currency-converter")

    if "en" in lang:
        DOUBLE_CLICK_TEXT = (
            By.XPATH,
            '//span[text()="Double click on a word to translate into Vietnamese"]',
        )
    else:
        DOUBLE_CLICK_TEXT = (
            By.XPATH,
            '//span[text()="Nhấp đúp chuột vào từ để dịch sang tiếng Việt"]',
        )
    if "en" in lang:
        SHOW_TOOLTIP_TEXT = (
            By.XPATH,
            '//span[text()="Show tooltip when highlighting a word"]',
        )
    else:
        SHOW_TOOLTIP_TEXT = (
            By.XPATH,
            '//span[text()="Hiển thị chú thích tính năng khi bôi đen từ"]',
        )
    if "en" in lang:
        ENABLE_DICTIONAY_AREA_TEXT = (
            By.XPATH,
            '//span[text()="Enable Dictionary in text input area"]',
        )
    else:
        ENABLE_DICTIONAY_AREA_TEXT = (
            By.XPATH,
            '//span[text()="Bật tính năng Tra từ điển trong khung soạn thảo"]',
        )
    if "en" in lang:
        ENABLE_UNIT_CONVERTER_TEXT = (
            By.XPATH,
            '//span[text()="Enable Unit converter feature"]',
        )
    else:
        ENABLE_UNIT_CONVERTER_TEXT = (
            By.XPATH,
            '//span[text()="Bật tính năng Chuyển đổi ngoại tệ"]',
        )

    # Interaction Methods
    def get_list_permissions_ele(self) -> list:
        list_ele: list[WebElement] = []
        try:
            parent_ele: WebElement = self.get_shadow_element(
                self.js_path_detail_permissions()
            )

        except Exception:
            raise ValueError("No element found!")
        else:
            list_ele = parent_ele.find_elements(By.TAG_NAME, "li")
            if len(list_ele) >= 1:
                return list_ele[:-1]  # remove last element
            else:
                return list_ele

    def open_dictionary_extention_options(self) -> None:
        self.click_shadow_element(self.js_path_detail_extension_options())
        first_window = self.get_current_window()
        try:
            for window in self.get_all_windows_handle():
                if window != first_window:
                    self.switch_to_window(window)
                    self.wait_for_title(title_text=CocCocSettingTitle.DICTIONARY_TITLE)
        finally:
            self.scc.close()

    def open_dictionary_extention_options_directly(self) -> None:
        self.open_page(
            url="chrome-extension://gfgbmghkdjckppeomloefmbphdfmokgd/options.html"
        )
        self.wait_for_title(title_text=CocCocSettingTitle.DICTIONARY_TITLE)

    def get_status_checkbox_double_click_on_word(self) -> bool:
        if (
            self.get_element_attribute_by_its_name_and_locator(
                self.CHECK_BOX_DOUBLE_CLICK_TRANSLATE, "checked"
            )
            is None
        ):
            return False
        else:
            return True

    def get_status_checkbox_enable_dictionary_text_area(self) -> bool:
        sleep(2)
        if (
            self.get_element_attribute_by_its_name_and_locator(
                self.CHECK_BOX_TEXTAREA, "checked"
            )
            is None
        ):
            return False
        else:
            return True

    def get_status_checkbox_show_tooltip(self) -> bool:
        if (
            self.get_element_attribute_by_its_name_and_locator(
                self.CHECK_BOX_SHOW_TOOLTIP, "checked"
            )
            is None
        ):
            return False
        else:
            return True

    def get_status_checkbox_unit_converter(self) -> bool:
        if (
            self.get_element_attribute_by_its_name_and_locator(
                self.CHECK_BOX_CURRENCY_CONVERTER, "checked"
            )
            is None
        ):
            return False
        else:
            return True

    def check_enable_double_click_translate_to_vietnamese(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_double_click_on_word() is not True:
            self.click_element(self.LABEL_CHECK_BOX_DOUBLE_CLICK)
            assert self.get_status_checkbox_double_click_on_word() is True

    def check_disable_double_click_translate_to_vietnamese(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_double_click_on_word() is not False:
            self.click_element(self.LABEL_CHECK_BOX_DOUBLE_CLICK)
            assert self.get_status_checkbox_double_click_on_word() is False

    def check_enable_show_tooltip(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_show_tooltip() is not True:
            self.click_element(self.LABEL_CHECK_BOX_SHOW_TOOLTIP)
            assert self.get_status_checkbox_show_tooltip() is True

    def check_disable_show_tooltip(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_show_tooltip() is not False:
            self.click_element(self.LABEL_CHECK_BOX_SHOW_TOOLTIP)
            assert self.get_status_checkbox_show_tooltip() is False

    def check_enable_dictionary_text_area(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_enable_dictionary_text_area() is not True:
            self.click_element(self.LABEL_CHECK_BOX_TEXTAREA)
            assert self.get_status_checkbox_enable_dictionary_text_area() is True

    def check_disable_dictionary_text_area(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_enable_dictionary_text_area() is not False:
            self.click_element(self.LABEL_CHECK_BOX_TEXTAREA)
            assert self.get_status_checkbox_enable_dictionary_text_area() is False

    def check_enable_unix_converter(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_unit_converter() is not True:
            self.click_element(self.LABEL_CHECK_BOX_UNIT_CONVERTER)
            assert self.get_status_checkbox_unit_converter() is True

    def check_disable_unix_converter(
        self, is_open_dictionary_extention_options_directly: bool = True
    ) -> None:
        if is_open_dictionary_extention_options_directly:
            self.open_dictionary_extention_options_directly()
        if self.get_status_checkbox_unit_converter() is not False:
            self.click_element(self.LABEL_CHECK_BOX_UNIT_CONVERTER)
            assert self.get_status_checkbox_unit_converter() is False

    def extension_toggle_status(self) -> str:
        return self.get_attribute_value_of_shadow_element(
            js_path=self.js_path_detail_toggle(), attribute_name="aria-pressed"
        )

    def turn_on_dictionary(self) -> None:
        self.open_extension_detail(extension_id="gfgbmghkdjckppeomloefmbphdfmokgd")
        if self.extension_toggle_status() != "true":
            self.click_shadow_element(self.js_path_detail_toggle())
            assert self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_detail_toggle(),
                attribute_name="aria-pressed",
                att_value="true",
            )

    def turn_off_dictionary(self) -> None:
        self.open_extension_detail(extension_id="gfgbmghkdjckppeomloefmbphdfmokgd")
        if self.extension_toggle_status() != "false":
            self.click_shadow_element(self.js_path_detail_toggle())
            assert self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_detail_toggle(),
                attribute_name="aria-pressed",
                att_value="false",
            )

    def get_extension_version(self) -> str:
        elements: list[WebElement] = self.get_shadow_elements(
            js_path=self.js_path_section_hr()
        )
        for element in elements:
            if self.get_element_text_by_element(
                element.find_element(by=By.CSS_SELECTOR, value="div.section-title")
            ) in [
                "Version",
                "Phiên bản",
            ]:
                return self.get_element_text_by_element(
                    element.find_element(
                        by=By.CSS_SELECTOR, value="div.section-content"
                    )
                )

    def get_allow_incognito_toggle_status(self) -> str:
        return self.get_attribute_value_of_shadow_element(
            js_path=self.js_path_allow_incognito_toggle(),
            attribute_name="aria-pressed",
        )

    def verify_ui_dictionary_options(self) -> None:
        assert self.get_element(self.DOUBLE_CLICK_TEXT).is_displayed()
        assert self.get_element(self.SHOW_TOOLTIP_TEXT).is_displayed()
        assert self.get_element(self.ENABLE_DICTIONAY_AREA_TEXT).is_displayed()
        assert self.get_element(self.ENABLE_UNIT_CONVERTER_TEXT).is_displayed()

    def verify_status_dictionary_options(self) -> None:
        assert self.get_status_checkbox_double_click_on_word()
        assert self.get_status_checkbox_show_tooltip()
        assert self.get_status_checkbox_enable_dictionary_text_area() is False
        assert self.get_status_checkbox_unit_converter()

    def turning_on_allow_incognito_mode(self) -> None:
        self.open_extension_detail(extension_id="gfgbmghkdjckppeomloefmbphdfmokgd")
        if self.get_allow_incognito_toggle_status() != "true":
            self.click_shadow_element(self.js_path_allow_incognito_toggle())
            assert self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_allow_incognito_toggle(),
                attribute_name="aria-pressed",
                att_value="true",
            )

    def turning_off_allow_incognito_mode(self) -> None:
        self.open_extension_detail(extension_id="gfgbmghkdjckppeomloefmbphdfmokgd")
        if self.get_allow_incognito_toggle_status() != "false":
            self.click_shadow_element(self.js_path_allow_incognito_toggle())
            assert self.wait_for_attribute_update_value_shadow_element(
                js_path=self.js_path_allow_incognito_toggle(),
                attribute_name="aria-pressed",
                att_value="false",
            )

    def open_extension_bg(self) -> None:
        current_window = self.get_current_window()
        self.click_shadow_element(self.js_path_list_detail_inspect_view())
        for window in self.get_all_windows_handle():
            if window != current_window:
                self.switch_to_window(window)
                print(f"Window is: {self.get_current_url()}")
