from time import sleep
from selenium.webdriver.common.by import By
from src.pages.base import BaseSelenium
from src.pages.constant import CocCocSettingTitle, LocatorJSPath


class DictionarySel(BaseSelenium):
    # Locator
    JS_PATH_STYLE = f'{LocatorJSPath.DICT_PRE}.querySelector("style")'
    JS_PATH_DICT_TOOLTIPS = f'{LocatorJSPath.DICT_PRE}.querySelector("div.corom-trigger.coccoc-triangle-bottom")'
    JS_PATH_DICT_TOOLTIPS_ICON = f'{LocatorJSPath.DICT_PRE}.querySelector("div.corom-trigger.coccoc-triangle-bottom > div.coccoc-tt-icon")'
    JS_PATH_DICT_TOOLTIPS_TEXT = f'{LocatorJSPath.DICT_PRE}.querySelector("div.corom-trigger.coccoc-triangle-bottom > div.coccoc-tt-text")'
    JS_PATH_DICT_POPUP = f'{LocatorJSPath.DICT_PRE}.querySelector("div.corom-popup")'
    JS_PATH_DICT_POPUP_WORD = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("div.coccoc-word")'
    )
    JS_PATH_DICT_POPUP_BTN_SPEAKER = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("#btn_speaker")'
    )
    JS_PATH_DICT_POPUP_BTN_SETTING = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("#btn_setting")'
    )
    JS_PATH_DICT_POPUP_BTN_MORE = f'{LocatorJSPath.DICT_PRE}.querySelector("#btn_more")'
    JS_PATH_DICT_POPUP_BTN_CLOSE = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("#btn_close")'
    )

    JS_PATH_DICT_POPUP_PRONUNCIATION = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("div.coccoc-pronunciation")'
    )
    JS_PATH_DICT_POPUP_PRONUNCIATION_TEXT = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("div.coccoc-pronun-text")'
    )
    JS_PATH_DICT_POPUP_PRONUNCIATION_TYPE = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("div.coccoc-pronun-type")'
    )
    JS_PATH_DICT_POPUP_TRANSLATIONS = (
        f'{LocatorJSPath.DICT_PRE}.querySelector("div.coccoc-translations")'
    )

    def enter_text_in_textarea_then_double_click(self, text: str) -> None:
        TEXT_AREA = (By.ID, "w3review")
        self.open_page(
            url="https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_textarea"
        )
        self.switch_to_iframe(frame_reference="iframeResult")
        self.clear_text_of_element(TEXT_AREA)
        self.fill_texts(TEXT_AREA, text=text)
        sleep(1)
        self.double_click_element(TEXT_AREA)
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP).is_displayed()

    def check_dict_tooltip_shown(self) -> None:
        assert self.get_shadow_element(self.JS_PATH_DICT_TOOLTIPS).is_displayed()

    def check_dict_tooltip_never_shown_yet(self) -> None:
        """
        Using for the check when tooltips have never shown yet!
        """
        assert (
            self.is_shadow_element_disappeared(self.JS_PATH_DICT_TOOLTIPS, timeout=5)
            is True
        )

    def check_tooltip_is_hidden(self) -> None:
        """Check the tooltip has attribute 'hidden'"""
        assert self.get_shadow_element(self.JS_PATH_DICT_TOOLTIPS).get_attribute(
            "hidden"
        )

    def click_dict_tooltips(self) -> None:
        self.click_shadow_element(self.JS_PATH_DICT_TOOLTIPS)
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP).is_displayed()

    def check_dict_popup_shown(self) -> None:
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP).is_displayed()

    def check_dict_popup_never_shown_yet(self) -> None:
        """
        Using for the check when tooltips have never shown yet!
        """
        assert (
            self.is_shadow_element_disappeared(self.JS_PATH_DICT_POPUP, timeout=5)
            is True
        )

    def check_dict_popup_ui(self) -> None:
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP_WORD).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_BTN_SPEAKER
        ).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_BTN_SETTING
        ).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP_BTN_MORE).is_displayed()
        assert self.get_shadow_element(self.JS_PATH_DICT_POPUP_BTN_CLOSE).is_displayed()

        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_PRONUNCIATION
        ).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_PRONUNCIATION_TEXT
        ).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_PRONUNCIATION_TYPE
        ).is_displayed()
        assert self.get_shadow_element(
            self.JS_PATH_DICT_POPUP_TRANSLATIONS
        ).is_displayed()

    def click_btn_more(self, text: str) -> None:
        current_window = self.get_current_window()
        try:
            self.click_shadow_element(js_path=self.JS_PATH_DICT_POPUP_BTN_MORE)
            list_url = []
            for window in self.get_all_windows_handle():
                if window != current_window:
                    self.switch_to_window(window)
                    sleep(1)
                    list_url.append(self.get_current_url())
                    # self.wait_for_title(title_text="Cốc Cốc")
                    # assert (
                    #     f"coccoc.com/search?query={text.lower()}+meaning"
                    #     in self.get_current_url()
                    # )
            assert f"https://coccoc.com/search?query={text.lower()}+meaning" in list_url
        finally:
            self.scc.close()

    def click_btn_setting(self) -> None:
        current_window = self.get_current_window()
        try:
            self.click_shadow_element(js_path=self.JS_PATH_DICT_POPUP_BTN_SETTING)
            list_url = []
            for window in self.get_all_windows_handle():
                if window != current_window:
                    self.switch_to_window(window)
                    sleep(1)
                    list_url.append(self.get_current_url())
                    # self.wait_for_title(title_text=CocCocSettingTitle.DICTIONARY_TITLE)
                    # assert (
                    #     f"chrome-extension://gfgbmghkdjckppeomloefmbphdfmokgd/options.html"
                    #     in self.get_current_url()
                    # )
            assert (
                f"chrome-extension://gfgbmghkdjckppeomloefmbphdfmokgd/options.html"
                in self.get_current_url()
            )
        finally:
            self.scc.close()
