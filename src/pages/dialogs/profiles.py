from time import sleep
from typing import Tuple
from selenium.webdriver.common.by import By

from src.pages.base import BaseAppium
from src.pages.coccoc_common import open_browser
from tests import setting

lang = setting.coccoc_language


class Profiles(BaseAppium):
    """This class is for interacting with the Profiles dialog
        Remove/edit/add profile via UI

    Args:
        BaseAppium (Object): _description_
    """

    # Locators

    def more_actions_btn(self, profile_name: str) -> Tuple:
        if "en" in lang:
            return (
                By.XPATH,
                rf'//Button[@Name="More actions for {profile_name}"][@AutomationId="moreActionsButton"]',
            )
        else:
            return (
                By.XPATH,
                rf'//Button[@Name="Thêm thao tác khác cho {profile_name}"][@AutomationId="moreActionsButton"]',
            )

    if "en" in lang:
        MORE_ACTIONS_DELETE = (
            By.XPATH,
            '//Window[@AutomationId="dialog"]/Menu[@AutomationId="wrapper"]/MenuItem[@Name="Delete"]',
        )
    else:
        MORE_ACTIONS_DELETE = (
            By.XPATH,
            '//Window[@AutomationId="dialog"]/Menu[@AutomationId="wrapper"]/MenuItem[@Name="Xóa"]',
        )

    if "en" in lang:
        MORE_ACTIONS_EDIT = (
            By.XPATH,
            '//Window[@AutomationId="dialog"]/Menu[@AutomationId="wrapper"]/MenuItem[@Name="Edit"]',
        )
    else:
        MORE_ACTIONS_EDIT = (
            By.XPATH,
            '//Window[@AutomationId="dialog"]/Menu[@AutomationId="wrapper"]/MenuItem[@Name="Chỉnh sửa"]',
        )
    COMFIRM_DELETE_BTN = (
        By.XPATH,
        '//Button[@AutomationId="removeConfirmationButton"]',
    )
    if "en" in lang:
        COMFIRM_CANCEL_BTN = (
            By.NAME,
            "Cancel",
        )
    else:
        COMFIRM_CANCEL_BTN = (
            By.NAME,
            "Hủy",
        )

    def profile_xpath_locator(self, person_name: str = "Person 1") -> Tuple:
        if "en" in lang:
            return (
                By.XPATH,
                rf'//Button[@Name="Open {person_name} profile"]',
            )
        else:
            return (
                By.XPATH,
                rf'//Button[@Name="Mở hồ sơ {person_name}"]',
            )

    # Interaction methods

    def click_open_link_in_new_tab(self) -> None:
        self.click_element(self.OPEN_LINK_IN_NEW_TAB)

        self.click_element(self.COPY_LINK_ADDRESS)

    @staticmethod
    def open_profiles_dialog() -> None:
        """We should make sure that we have multipe profile here"""
        open_browser.open_coccoc_by_pywinauto()

    def click_more_actions_btn(self, profile_name: str) -> None:
        # self.open_profiles_dialog()
        self.click_element(by_locator=self.more_actions_btn(profile_name=profile_name))

    def click_more_action_delete(self) -> None:
        self.click_element(self.MORE_ACTIONS_DELETE)

    def click_more_action_edit(self) -> None:
        self.click_element(self.MORE_ACTIONS_EDIT)

    def click_confirm_delete_btn(self, sleep_n_seconds: int = 1) -> None:
        self.move_to_element(self.COMFIRM_DELETE_BTN)
        self.click_and_hold(self.COMFIRM_DELETE_BTN)
        self.release_element(self.COMFIRM_DELETE_BTN)
        # self.click_element(self.COMFIRM_DELETE_BTN)
        sleep(sleep_n_seconds)

    def click_confirm_cancel_btn(self) -> None:
        self.click_element(self.COMFIRM_CANCEL_BTN)

    def click_delete_profile_completely(self, profile_name: str) -> None:
        self.click_more_actions_btn(profile_name)
        self.click_more_action_delete()
        self.click_confirm_delete_btn(sleep_n_seconds=2)
        sleep(2)

    def click_edit_profile(self, profile_name: str) -> None:
        # self.
        pass

    def open_profile_window(self, profile_name: str) -> None:
        pass

    def click_to_open_coccoc_by_profile_name(self, person_name: str) -> None:
        """We should make sure that we have multipe profiles already"""
        self.click_element(
            by_locator=self.profile_xpath_locator(person_name=person_name)
        )
