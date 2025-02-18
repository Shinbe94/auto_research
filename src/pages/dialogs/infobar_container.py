from typing import Tuple
from selenium.webdriver.common.by import By
from src.pages.base import BaseAppium
from tests import setting

lang = setting.coccoc_language


class InfobarContainer(BaseAppium):
    # Locators
    if "en" in lang:
        INFOBAR = (
            By.NAME,
            "Infobar",
        )
    else:
        INFOBAR = (
            By.NAME,
            "Thanh thông tin",
        )

    if "en" in lang:
        BTN_UNDO = (
            By.NAME,
            "Undo",
        )
    else:
        BTN_UNDO = (
            By.NAME,
            "Hoàn tác",
        )

    def text_des(self, theme_name: str) -> tuple:
        if "en" in lang:
            return (
                By.NAME,
                f'Installed theme "{theme_name}"',
            )
        else:
            return (
                By.NAME,
                f'Đã cài đặt chủ đề "{theme_name}"',
            )

    # Interaction methods
    def verify_theme_installed(self, theme_name: str = "Space Catboy") -> None:
        assert self.is_element_appeared(self.INFOBAR, timeout=10)
        assert self.is_element_appeared(self.BTN_UNDO)
        assert self.is_element_appeared(self.text_des(theme_name))
