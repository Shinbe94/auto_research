from src.pages.base import BaseSelenium


class SettingsHomeSel(BaseSelenium):
    # Locators
    SEARCH_SETTINGS_INPUT = r'document.querySelector("body settings-ui").shadowRoot.querySelector("#toolbar").shadowRoot.querySelector("#search").shadowRoot.querySelector("#searchInput")'

    # Interaction methods

    def enter_value_to_search(self, search_text: str) -> None:
        self.fill_texts_shadow_element(self.SEARCH_SETTINGS_INPUT, search_text)
