from pywinauto import ElementNotFoundError, Desktop
from pywinauto.timings import always_wait_until_passes, wait_until_passes

from src.pages.base import BasePage


class FirstTimeRun(BasePage):
    def open_setting_page(self):
        self.goto("coccoc://settings")


def verify_new_tab_coccoc_exist():
    from pywinauto import Desktop

    coccoc_instance = Desktop(backend="uia").Welcome_to_Cốc_Cốc_browser
    # coccoc_instance.print_control_identifiers()
    # common.wait_for_panel_is_exist(coccoc_instance)
    welcome_coccoc_tab = coccoc_instance.child_window(
        title="Welcome to Cốc Cốc browser"
    )
    title_bar = coccoc_instance.child_window(auto_id="TitleBar")
    # new_tab = coccoc_instance.child_window(title_re='New Tab', control_type=50019)
    # common.wait_for_panel_is_exist(welcome_coccoc_tab)
    # common.wait_for_panel_is_exist(new_tab)
    assert welcome_coccoc_tab.exists() is True
    # assert title_bar.exists() is True
    # assert new_tab.exists() is True


#
# @always_wait_until_passes(4, 2)
# def verify_new_coccoc_window_is_open()


def wait_for_coccoc_open_first_time():
    try:
        coccoc_instance = Desktop(backend="uia").Welcome_to_Cốc_Cốc_browser
        # coccoc_instance.print_control_identifiers()
        # common.wait_for_panel_is_exist(coccoc_instance)
        welcome_coccoc_tab = coccoc_instance.child_window(
            title="Welcome to Cốc Cốc browser"
        )
        # wait a maximum of 10.5 seconds for the
        # window to be found in increments of .5 of a second.
        # P.int a message and re-raise the original exception if never found.
        wait_until_passes(10, 1, welcome_coccoc_tab.Exists, ElementNotFoundError)
    except TimeoutError as e:
        print("timed out")
        raise e
