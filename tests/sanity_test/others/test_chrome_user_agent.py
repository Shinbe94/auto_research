import pytest

from pytest_pytestrail import pytestrail
from src.pages.new_tab.new_tab_page import NewTabPageSel
from src.utilities import browser_utils
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C794761")
def test_navigator_user_agent_api_when_enable_cococ_use_chrome_user_agent(
    new_tab_page_sel: NewTabPageSel,
):
    assert "coc_coc_browser" in new_tab_page_sel.execute_js(
        "return navigator.userAgent;"
    )
    for url in setting.list_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert "coc_coc_browser" in new_tab_page_sel.execute_js(
            "return navigator.userAgent;"
        )
    for url in setting.list_non_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert "coc_coc_browser" not in new_tab_page_sel.execute_js(
            "return navigator.userAgent;"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C797958")
@pytest.mark.DisableCocCocUseChromeUserAgent
def test_navigator_user_agent_api_when_disable_cococ_use_chrome_user_agent(
    new_tab_page_sel: NewTabPageSel,
):
    assert "coc_coc_browser" in new_tab_page_sel.execute_js(
        "return navigator.userAgent;"
    )
    for url in setting.list_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert "coc_coc_browser" in new_tab_page_sel.execute_js(
            "return navigator.userAgent;"
        )
    for url in setting.list_non_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert "coc_coc_browser" not in new_tab_page_sel.execute_js(
            "return navigator.userAgent;"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1071886")
def test_navigator_user_agent_data_api_when_enable_cococ_use_chrome_user_agent(
    new_tab_page_sel: NewTabPageSel,
):
    major_build = browser_utils.get_coccoc_major_build()

    assert f"'brand': 'CocCoc', 'version': '{str(major_build + 6 )}'" in str(
        new_tab_page_sel.execute_js("return navigator.userAgentData;")
    )

    for url in setting.list_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert f"'brand': 'CocCoc', 'version': '{str(major_build + 6 )}'" in str(
            new_tab_page_sel.execute_js("return navigator.userAgentData;")
        )
    for url in setting.list_non_cc_sites:
        new_tab_page_sel.open_page(url=url)
        assert f"'brand': 'Google Chrome', 'version': '{str(major_build)}'" in str(
            new_tab_page_sel.execute_js("return navigator.userAgentData;")
        )
        assert f"'brand': 'CocCoc', 'version': '{str(major_build + 6 )}'" not in str(
            new_tab_page_sel.execute_js("return navigator.userAgentData;")
        )
