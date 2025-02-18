from pytest_pytestrail import pytestrail

from src.pages.sidebar.sidebar import Sidebar
from src.pages.sidebar.sidebar_custom_icon_context_menu import (
    SidebarCustomIconContextMenu,
)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C154564")
def test_add_recommended_sites_checked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    icon_name = random_recommend_icon[0]
    icon_url = random_recommend_icon[1]
    # print(icon_url)
    sidebar.add_recommended_icon(icon_name)
    # Icon after added, we locate them by their url
    sidebar.right_click_custom_icon_by_its_name(icon_name=icon_url)
    sidebar_custom_icon_context_menu.verify_ui()
    assert (
        sidebar_custom_icon_context_menu.get_state_of_always_open_in_sidebar_window()
        == "1"
    )
    sidebar.click_custom_icon(icon_name=icon_url)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C202924")
def xtest_add_recommended_sites_unchecked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    # Todo https://coccoc.atlassian.net/browse/BR-3604?focusedCommentId=382759
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    icon_name = random_recommend_icon[0]
    icon_url = random_recommend_icon[1]
    sidebar.add_recommended_icon(icon_name, is_checked_on_open_in_sidebar_window=False)
    # Icon after added, we locate them by their url
    sidebar.right_click_custom_icon_by_its_name(icon_name=icon_url)
    sidebar_custom_icon_context_menu.verify_ui()
    assert (
        sidebar_custom_icon_context_menu.get_state_of_always_open_in_sidebar_window()
        == "0"
    )
    sidebar.click_custom_icon(icon_name=icon_url)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C224500")
def xtest_add_url_sites_unchecked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    # TODO fix later after https://coccoc.atlassian.net/browse/BR-3604


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C224533")
def xtest_add_url_sites_checked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    # TODO fix later after https://coccoc.atlassian.net/browse/BR-3604


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C161815")
def xtest_add_sites_checked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    # TODO fix later after https://coccoc.atlassian.net/browse/BR-3604


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C224521")
def xtest_add_sites_unchecked_open_in_sidebar_window(
    copy_sidebar_icon_files: None,
    sidebar: Sidebar,
    sidebar_custom_icon_context_menu: SidebarCustomIconContextMenu,
):
    random_recommend_icon: tuple = sidebar.get_random_recommended_icon()
    # TODO fix later after https://coccoc.atlassian.net/browse/BR-3604


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C224524")
def test_can_edit_sidebar_custom_icon(
    copy_sidebar_icon_files,
    get_default_custom_icons,
    sidebar,
    sidebar_custom_icon_context_menu,
    sidebar_edit_custom_icon,
):
    # TODO fix later after https://coccoc.atlassian.net/browse/BR-3604
    list_custom_icons = get_default_custom_icons(profile_name="Default")
    sidebar.click_to_edit_custom_icon(icon_name=list_custom_icons[0])
    status_open_sidebar_window_before = (
        sidebar_edit_custom_icon.get_current_status_of_open_in_new_sidebar_window()
    )
    sidebar_edit_custom_icon.set_icon_title(text="Test title")

    sidebar_edit_custom_icon.set_icon_url(url="https://google.com/")
    sidebar_edit_custom_icon.click_btn_done()

    # sidebar_edit_custom_icon.set_icon_title_and_url_tick_open_sidebar_window(text='Test title',
    #                                                                          url='https://google.com')
    sidebar.click_to_edit_custom_icon(icon_name="Test title")
    assert sidebar_edit_custom_icon.get_current_icon_title() == "Test title"
    assert sidebar_edit_custom_icon.get_current_icon_url() == "https://google.com/"
    # assert status_open_sidebar_window_before != sidebar_edit_custom_icon.get_current_status_of_open_in_new_sidebar_window()
    # sidebar_edit_custom_icon.click_btn_done()
