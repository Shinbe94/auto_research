from selenium.webdriver.common.by import By
from src.pages.base import BasePlaywright, BaseSelenium
from src.pages.constant import CocCocText, LocatorJSPath
from tests import setting

lang = setting.coccoc_language


class SettingsOnStartupSel(BaseSelenium):
    # Locators
    URL_INPUT = f'{LocatorJSPath.SETTINGS_STARTUP_DIALOG}.shadowRoot.querySelector("#url").shadowRoot.querySelector("#input")'
    BTN_ADD = f'{LocatorJSPath.SETTINGS_STARTUP_DIALOG}.shadowRoot.querySelector("#actionButton")'
    BTN_CANCEL = (
        f'{LocatorJSPath.SETTINGS_STARTUP_DIALOG}.shadowRoot.querySelector("#cancel")'
    )
    ALL_ADDED_PAGES = f"{LocatorJSPath.SETTINGS_STARTUP_URL_ENTRY_ALL}"
    BTN_3_DOTS = (
        f'{LocatorJSPath.SETTINGS_STARTUP_URL_ENTRY}.shadowRoot.querySelector("#dots")'
    )
    BTN_REMOVE = f'{LocatorJSPath.SETTINGS_STARTUP_URL_ENTRY}.shadowRoot.querySelector("#remove")'
    ICON_LIST = f'{LocatorJSPath.SETTINGS_STARTUP_URL_PAGE}.shadowRoot.querySelector("#container > iron-list")'

    def open_settings_startup(self) -> None:
        self.open_page("coccoc://settings/onStartup")

    def click_open_the_newtab_page(self):
        self.open_settings_startup()
        eles: list = self.get_shadow_elements(
            js_path=LocatorJSPath.SETTINGS_STARTUP_RATIO
        )
        for ele in eles:
            if ele.text == CocCocText.OPEN_NEWTAB_PAGE:
                ele.click()
                assert ele.get_attribute("checked")

    def click_continue_where_you_left_off(self):
        self.open_settings_startup()
        eles: list = self.get_shadow_elements(
            js_path=LocatorJSPath.SETTINGS_STARTUP_RATIO
        )
        for ele in eles:
            if ele.text == CocCocText.CONTINUE_WHERE_YOU_LEFT_OFF:
                ele.click()
                assert ele.get_attribute("checked")

    def click_open_a_specify_page_or_set_of_pages(self):
        self.open_settings_startup()
        eles: list = self.get_shadow_elements(
            js_path=LocatorJSPath.SETTINGS_STARTUP_RATIO
        )
        for ele in eles:
            if ele.text == CocCocText.OPEN_SPECIFIC_OR_SET_OF_PAGES:
                ele.click()
                assert ele.get_attribute("checked")

    def add_new_page(self, text: str, is_need_open_setting_startup_page=False) -> None:
        if is_need_open_setting_startup_page:
            self.open_settings_startup()
        self.click_shadow_element(LocatorJSPath.SETTINGS_STARTUP_BUTTON_ADD_PAGE)
        self.fill_texts_shadow_element(js_path=self.URL_INPUT, text=text)
        self.click_shadow_element(self.BTN_ADD)

    def click_use_current_page(self) -> None:
        self.open_settings_startup()
        self.click_shadow_element(
            LocatorJSPath.SETTINGS_STARTUP_BUTTON_USE_CURRENT_PAGE
        )

    def click_btn_3_dots(self) -> None:
        self.click_shadow_element(self.BTN_3_DOTS)

    def click_btn_remove(self) -> None:
        self.click_shadow_element(self.BTN_REMOVE)

    def remove_all_added_page(self) -> None:
        self.click_open_a_specify_page_or_set_of_pages()
        no_of_item = len(self.get_shadow_elements(self.ALL_ADDED_PAGES))
        if no_of_item > 0:
            for i in range(no_of_item):
                self.click_btn_3_dots()
                self.click_btn_remove()

    def check_favicons(self) -> None:
        self.open_settings_startup()
        ids = self.get_list_id_entry()
        for id in ids:
            favicon_icon = f'{LocatorJSPath.SETTINGS_STARTUP_URL_PAGE}.shadowRoot.querySelector("#{id}").shadowRoot.querySelector("div site-favicon").shadowRoot.querySelector("#favicon")'
            assert self.is_shadow_element_appeared(js_path=favicon_icon)

    def get_list_id_entry(self) -> list:
        if self.get_attribute_value_of_shadow_element(
            js_path=self.ICON_LIST, attribute_name="aria-owns"
        ):
            return self.get_attribute_value_of_shadow_element(
                js_path=self.ICON_LIST, attribute_name="aria-owns"
            ).split(" ")
        else:
            return []


class SettingsOnStartUp(BasePlaywright):
    pass
