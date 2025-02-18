from time import sleep
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.coccoc_common import open_browser
from src.pages.constant import CocCocTitles
from src.pages.internal_page.flags.flags_page import FlagsPageSel


@pytest.fixture(autouse=False)
def enable_coccoc_ai_feature():
    """To enable the coccoc AI sidebar feature"""
    coccoc_instance = (
        open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium3()
    )
    driver: WebDriver = coccoc_instance[0]
    fps = FlagsPageSel(driver)
    try:
        fps.change_flag_status(flag_id="coccoc-sidebar-ai", status="Enabled")
    finally:
        open_browser.close_coccoc_by_window_title(title=CocCocTitles.EXPERIMENTS_TITLE)
        if driver is not None:
            driver.quit()
            sleep(1)
