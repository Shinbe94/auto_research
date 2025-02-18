import time

from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from tests import setting


class SidebarEditCustomIcon(BaseAppium):
    lang = setting.coccoc_language

    # Locators
    if lang == 'en':
        EDIT_ICON = (By.NAME, 'Edit icon')
    else:
        EDIT_ICON = (By.NAME, 'Chỉnh sửa Icon')

    if lang == 'en':
        TITLE_TEXT = (By.NAME, 'Title')
    else:
        TITLE_TEXT = (By.NAME, 'Tiêu đề')

    if lang == 'en':
        TITLE_EDIT = (By.XPATH,
                      '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit icon"]//Edit[@Name="Title"]')
    else:
        TITLE_EDIT = (By.NAME,
                      '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa Icon"]//Edit[@Name="Title"]')

    if lang == 'en':
        WEBSITE_URL_TEXT = (By.NAME, 'Website URL')
    else:
        WEBSITE_URL_TEXT = (By.NAME, 'Đường dẫn trang web')

    if lang == 'en':
        WEBSITE_URL_EDIT = (By.XPATH, '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Edit icon"]//Edit[@Name="URL"]')
    else:
        WEBSITE_URL_EDIT = (
            By.XPATH, '//Pane[@ClassName="Chrome_WidgetWin_1"][@Name="Chỉnh sửa Icon"]//Edit[@Name="URL"]')

    if lang == 'en':
        OPEN_IN_NEW_SIDEBAR_WINDOW = (By.NAME, 'Open in sidebar window')
    else:
        OPEN_IN_NEW_SIDEBAR_WINDOW = (By.NAME, 'Mở trong cửa sổ thanh bên')

    if lang == 'en':
        BTN_DONE = (By.NAME, 'Done')
    else:
        BTN_DONE = (By.NAME, 'Hoàn tất')

    if lang == 'en':
        BTN_CANCEL = (By.NAME, 'Cancel')
    else:
        BTN_CANCEL = (By.NAME, 'Hủy')

    def verify_ui(self):
        assert self.get_element(self.EDIT_ICON)
        assert self.get_element(self.TITLE_TEXT)
        assert self.get_element(self.TITLE_EDIT)
        assert self.get_element(self.WEBSITE_URL_TEXT)
        assert self.get_element(self.WEBSITE_URL_EDIT)
        assert self.get_element(self.OPEN_IN_NEW_SIDEBAR_WINDOW)

    def click_title_bar(self):
        self.click_element(self.EDIT_ICON)
        print('title bar is clicked')

    def get_current_status_of_open_in_new_sidebar_window(self) -> str:
        """
        This is for getting the checkbox is checked or not
        Returns:
        True -> Checked, False -> not checked
        """
        if self.get_element_attribute_by_its_name_and_its_element(
                element=self.get_element(self.OPEN_IN_NEW_SIDEBAR_WINDOW),
                attribute_name='Toggle.ToggleState') == 1:
            return 'ON'
        else:
            return 'OFF'

    def tick_open_in_new_sidebar_window(self):
        """Just tick on that tick box, don't care its current status or intended status"""
        self.click_element(self.OPEN_IN_NEW_SIDEBAR_WINDOW)

    def tick_on_open_in_new_sidebar_window(self) -> None:
        """
        To check on the option: Open in new sidebar window
        Returns: None
        """
        if not self.get_current_status_of_open_in_new_sidebar_window() == 'ON':
            self.tick_open_in_new_sidebar_window()
            assert self.get_current_status_of_open_in_new_sidebar_window() == 'ON'

    def tick_off_open_in_new_sidebar_window(self) -> None:
        """
        To check off the option: Open in new sidebar window
        Returns: None
        """
        if not self.get_current_status_of_open_in_new_sidebar_window() == 'OFF':
            self.tick_open_in_new_sidebar_window()
            assert self.get_current_status_of_open_in_new_sidebar_window() == 'OFF'

    def click_btn_done(self):
        """ To click done button, don't know why single click does not work, must use double click"""
        # self.click_element(self.BTN_DONE)
        self.double_click_element(self.BTN_DONE)
        time.sleep(1)

    def get_current_icon_title(self) -> str:
        return self.get_element_attribute_by_its_name_and_locator(self.TITLE_EDIT, 'Value.Value')

    def get_current_icon_url(self) -> str:
        return self.get_element_attribute_by_its_name_and_locator(self.WEBSITE_URL_EDIT, 'Value.Value')

    def set_icon_title(self, text: str):
        self.fill_texts(self.TITLE_EDIT, text, is_press_enter=False)

    def set_icon_url(self, url: str):
        self.fill_texts2(self.WEBSITE_URL_EDIT, url, is_press_enter=False)

    def click_dummy_title(self):
        self.click_element(self.TITLE_EDIT)

    def click_and_hold_url(self):
        self.click_and_hold(self.WEBSITE_URL_EDIT)

    def set_icon_title_and_url(self, text: str, url: str):
        self.set_icon_title(text)
        self.set_icon_url(url)

    def set_icon_title_and_url_tick_open_sidebar_window(self, text: str, url: str):
        # self.set_icon_title(text)
        self.set_icon_url(url)
        self.tick_open_in_new_sidebar_window()
        self.click_btn_done()
