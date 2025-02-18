import time

from pytest_pytestrail import pytestrail
from selenium.webdriver.common.by import By
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.sidebar.sidebar import Sidebar
from src.pages.toolbar.toolbar import Toolbar

from src.utilities import encode_decode


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54319")
def test_paid_icons(
    get_paid_icons, sidebar: Sidebar, toolbar: Toolbar, histograms: Histograms
):
    # fetch api paid icons then get urls and icon titles
    icon_names = [icon.get("title") for icon in get_paid_icons]
    icon_urls = [icon.get("url") for icon in get_paid_icons]
    urls: list = []

    # Open paid icons one by one then get the opening urls
    for icon_name in icon_names:
        paid_icon_locator = (By.NAME, f"{icon_name}")
        sidebar.click_element(paid_icon_locator)
        time.sleep(3)
        urls.append(toolbar.get_opening_url())

    # Assert the opening url vs url from sidebar
    for i in range(len(urls)):
        assert urls[i] in encode_decode.url_decode(icon_urls[i])

    # Check metrics sent
    histograms.check_paid_icons_read()
    histograms.check_paid_icon_clicked(no_of_clicked=len(icon_urls))


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1129684")
def test_list_valid_paid_icons(sidebar: Sidebar):
    sidebar.check_paid_icons()
