from typing import Tuple
from selenium.webdriver.common.by import By
from src.pages.base import BaseAppium
from tests import setting

lang = setting.coccoc_language


class GoogleTranslatePopUp(BaseAppium):
    """This class is for interacting with the Google Translate dialog
        Remove/edit/add profile via UI

    Args:
        BaseAppium (Object): _description_
    """

    # Locators
    if "en" in lang:
        TRANSLATE_POPUP = (By.NAME, "Translate this page?")
    else:
        TRANSLATE_POPUP = (By.NAME, "Translate this page?")

    def check_translate_popup_shown(self) -> None:
        assert self.is_element_appeared(self.TRANSLATE_POPUP)

    def check_translate_popup_not_shown(self) -> None:
        assert self.is_element_disappeared(self.TRANSLATE_POPUP)
