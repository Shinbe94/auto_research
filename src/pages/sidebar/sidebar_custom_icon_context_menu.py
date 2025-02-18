from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from src.pages.sidebar.sidebar_edit_custom_icon import SidebarEditCustomIcon
from tests import setting


class SidebarCustomIconContextMenu(BaseAppium):
    lang = setting.coccoc_language

    # Locators
    if lang == 'en':
        OPEN_IN_SIDEBAR_WINDOW = (By.NAME, 'Open in sidebar window')
    else:
        OPEN_IN_SIDEBAR_WINDOW = (By.NAME, 'Mở trong cửa sổ thanh bên')

    if lang == 'en':
        OPEN_IN_NEW_TAB = (By.NAME, 'Open in new tab')
    else:
        OPEN_IN_NEW_TAB = (By.NAME, 'Mở trong thẻ mới')

    if lang == 'en':
        BTN_EDIT = (By.NAME, 'Edit')
    else:
        BTN_EDIT = (By.NAME, 'Chỉnh sửa')

    if lang == 'en':
        REMOVE_FROM_SIDEBAR = (By.NAME, 'Remove from Sidebar')
    else:
        REMOVE_FROM_SIDEBAR = (By.NAME, 'Xóa khỏi thanh bên')

    if lang == 'en':
        ALWAYS_OPEN_IN_SIDEBAR_WINDOW = (By.NAME, 'Always open in sidebar window')
    else:
        ALWAYS_OPEN_IN_SIDEBAR_WINDOW = (By.NAME, 'Luôn mở ở cửa sổ thanh bên')

    def click_to_edit_custom_icon(self) -> SidebarEditCustomIcon:
        # sidebar_edit_custom_icon_view = SidebarEditCustomIcon(self.wad)
        self.click_element(self.BTN_EDIT)
        # sidebar_edit_custom_icon_view.verify_ui()
        return SidebarEditCustomIcon(self)

    def click_remove_from_sidebar(self):
        self.click_element(self.REMOVE_FROM_SIDEBAR)

    def click_open_in_new_tab(self):
        self.click_element(self.OPEN_IN_NEW_TAB)

    def click_open_in_sidebar_window(self):
        self.click_element(self.OPEN_IN_SIDEBAR_WINDOW)

    def click_always_open_in_sidebar_window(self):
        self.click_element(self.ALWAYS_OPEN_IN_SIDEBAR_WINDOW)

    def get_state_of_always_open_in_sidebar_window(self):
        return self.get_element_attribute_by_its_name_and_locator(self.ALWAYS_OPEN_IN_SIDEBAR_WINDOW,
                                                                  'Toggle.ToggleState')

    def verify_ui(self):
        assert self.get_element(self.OPEN_IN_SIDEBAR_WINDOW)
        assert self.get_element(self.OPEN_IN_NEW_TAB)
        assert self.get_element(self.BTN_EDIT)
        assert self.get_element(self.REMOVE_FROM_SIDEBAR)
        assert self.get_element(self.ALWAYS_OPEN_IN_SIDEBAR_WINDOW)
