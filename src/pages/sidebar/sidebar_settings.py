from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from tests import setting


class SidebarSetting(BaseAppium):
    lang = setting.coccoc_language

    # Locators

    if lang == 'en':
        SIDEBAR_SETTINGS_TITLE_BAR = (By.NAME, 'Sidebar settings')
    else:
        SIDEBAR_SETTINGS_TITLE_BAR = (By.NAME, 'Cài đặt thanh bên')

