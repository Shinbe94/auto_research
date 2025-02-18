from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from tests import setting


class SidebarWebPanel(BaseAppium):
    lang = setting.coccoc_language

    # Locators

    if lang == 'en':
        SIDEBAR_WEB_PANEL = (By.NAME, 'Sidebar webpanel')
    else:
        SIDEBAR_WEB_PANEL = (By.NAME, 'Sidebar webpanel')

    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_MORE = (By.NAME, 'More options')
    else:
        SIDEBAR_WEB_PANEL_BTN_MORE = (By.NAME, 'More options')

    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_GO_BACK = (By.NAME, 'Click to go back')
    else:
        SIDEBAR_WEB_PANEL_BTN_GO_BACK = (By.NAME, 'Click to go back')
    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_GO_FORWARD = (By.NAME, 'Click to go forward')
    else:
        SIDEBAR_WEB_PANEL_BTN_GO_FORWARD = (By.NAME, 'Click to go forward')

    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_RELOAD_PAGE = (By.NAME, 'Reload this page')
    else:
        SIDEBAR_WEB_PANEL_BTN_RELOAD_PAGE = (By.NAME, 'Reload this page')

    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_PIN_WEB_PANEL = (By.NAME, 'Pin web panel')
    else:
        SIDEBAR_WEB_PANEL_BTN_PIN_WEB_PANEL = (By.NAME, 'Pin web panel')

    if lang == 'en':
        SIDEBAR_WEB_PANEL_BTN_HIDE = (By.NAME, 'Hide')
    else:
        SIDEBAR_WEB_PANEL_BTN_HIDE = (By.NAME, 'Hide')

    def click_hide(self):
        self.click_element(self.SIDEBAR_WEB_PANEL_BTN_HIDE)
