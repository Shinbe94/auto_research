from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from tests import setting

lang = setting.coccoc_language


class ContextMenu(BaseAppium):
    """This class is for interacting with the context menu of the page
        (Interact with option after right click)

    Args:
        BaseAppium (Object): _description_
    """

    # Locators
    if lang == "en":
        OPEN_LINK_IN_NEW_TAB = (
            By.NAME,
            "Open link in new tab",
        )
    else:
        OPEN_LINK_IN_NEW_TAB = (
            By.NAME,
            "Mở đường liên kết trong thẻ mới",
        )
    if lang == "en":
        OPEN_LINK_IN_NEW_WINDOW = (
            By.NAME,
            "Open link in new window",
        )
    else:
        OPEN_LINK_IN_NEW_WINDOW = (
            By.NAME,
            "Mở đường liên kết bằng cửa sổ mới",
        )
    if lang == "en":
        OPEN_LINK_IN_INCOGNITO_WINDOW = (
            By.NAME,
            "Open link in incognito window",
        )
    else:
        OPEN_LINK_IN_INCOGNITO_WINDOW = (
            By.NAME,
            "Mở đường liên kết bằng cửa sổ ẩn danh",
        )
    if lang == "en":
        OPEN_LINK_IN_INCOGNITO_WINDOW_WITH_TOR = (
            By.NAME,
            "Open in Incognito window with Tor",
        )
    else:
        OPEN_LINK_IN_INCOGNITO_WINDOW_WITH_TOR = (
            By.NAME,
            "Mở trong cửa sổ Ẩn danh với Tor",
        )
    if lang == "en":
        COPY_LINK_ADDRESS = (
            By.NAME,
            "Copy link address",
        )
    else:
        COPY_LINK_ADDRESS = (
            By.NAME,
            "Sao chép địa chỉ liên kết",
        )

    def translate_text_locator(self, text) -> str:
        if "en" in lang:
            return f"Translate: {text}"
        else:
            return f"Dịch: {text}"

    if lang == "en":
        BLOCK_ELEMENT = (
            By.NAME,
            "Block element",
        )
    else:
        BLOCK_ELEMENT = (
            By.NAME,
            "Block element",
        )
    if lang == "en":
        REPORT_UNSAFE_CONTENT = (
            By.NAME,
            "Report unsafe content…",
        )
    else:
        REPORT_UNSAFE_CONTENT = (
            By.NAME,
            "Report unsafe content…",
        )

    # Interaction methods

    def click_open_link_in_new_tab(self) -> None:
        self.click_element(self.OPEN_LINK_IN_NEW_TAB)

    def click_open_link_in_new_window(self) -> None:
        self.click_element(self.OPEN_LINK_IN_NEW_WINDOW)

    def click_open_link_in_incognito_window(self) -> None:
        self.click_element(self.OPEN_LINK_IN_INCOGNITO_WINDOW)

    def click_open_link_in_incognito_window_with_tor(self) -> None:
        self.click_element(self.OPEN_LINK_IN_INCOGNITO_WINDOW_WITH_TOR)

    def click_copy_link_address(self) -> None:
        self.click_element(self.COPY_LINK_ADDRESS)

    def translate_text(self, text: str) -> None:
        element = (By.NAME, self.translate_text_locator(text=text))
        self.click_element(element)

    def click_report_unsafe_content(self) -> None:
        self.click_element(self.REPORT_UNSAFE_CONTENT)
