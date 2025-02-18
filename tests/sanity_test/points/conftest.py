from time import sleep
import pytest
from src.pages.coccoc_common import open_browser
from src.pages.internal_page.extensions.extensions_page import ExtensionsPage
from src.pages.onboarding.points_onboarding import PointsOnBoarding, PointsOnBoardingSel
from src.pages.turn_on_sync import turn_on_sync
from tests import setting


from tests.conftest import close_win_app_driver_server_by_its_id, p_driver


@pytest.fixture()
def make_points_onboarding_shown() -> None:
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        ep = ExtensionsPage(driver)
        pobs = PointsOnBoardingSel(driver)
        ep.force_points_onboarding_shown()
        ep.turn_off_savior()
        ep.turn_on_savior()
        ep.open_page("https://tinhte.vn")
        pobs.check_point_onboarding_shown()
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()
        sleep(2)


@pytest.fixture()
def login_and_sync() -> None:
    tuple_context = p_driver()  # Start Coccoc by Winappdriver and connect by playwright
    pcc = tuple_context[0]  # get playwright page
    browser = tuple_context[1]
    pw = tuple_context[2]
    winappdriver = tuple_context[3]
    pid = tuple_context[4]  # get winappdriver pid
    turn_on_sync.turn_on_sync_from_setting_by_playwright(
        pcc, email=setting.cc_account_user, password=setting.cc_account_password
    )
    # Close all for cleaning up
    browser.close()
    pw.stop()
    winappdriver.quit()
    close_win_app_driver_server_by_its_id(pid)  # Close current winappdriver instance


@pytest.fixture()
def reset_points_onboarding_state() -> None:
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver = coccoc_instance[0]
    cc_window = coccoc_instance[1]

    try:
        pobs = PointsOnBoardingSel(driver)
        pobs.clear_onboarding_local_storage()
    finally:
        cc_window.window().close()
        if driver is not None:
            driver.quit()
        sleep(2)
