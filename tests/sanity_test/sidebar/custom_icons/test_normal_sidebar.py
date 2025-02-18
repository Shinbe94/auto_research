import time

from pytest_pytestrail import pytestrail

from src.pages.sidebar.sidebar import Sidebar
from src.pages.sidebar.sidebar_custom_icon_context_menu import (
    SidebarCustomIconContextMenu,
)
from src.pages.sidebar.sidebar_web_panel import SidebarWebPanel
from src.pages.toolbar.toolbar import Toolbar


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54320")
def test_context_menu_custom_icon(
    get_default_custom_icons,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
    toolbar: Toolbar,
):
    list_custom_icons = get_default_custom_icons(profile_name="Default")
    # Right click and check the context menu of each custom icon
    for icon_name in list_custom_icons:
        sidebar.right_click_custom_icon_by_its_name(icon_name)
        sidebar_custom_icon_context_menu.verify_ui()

        # dummy click to hide the custom icon context menu
        toolbar.click_address_and_search_bar()
        time.sleep(1)

    # click all custom icons
    sidebar.click_all_custom_icons(icon_names=list_custom_icons)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54320")
def test_can_not_create_custom_icon(
    sidebar: Sidebar, sidebar_web_panel: SidebarWebPanel, toolbar: Toolbar
):
    sidebar.click_btn_add_your_favourite_site()
    sidebar.click_add_btn()
    assert sidebar.get_status_add_btn() == "false"
