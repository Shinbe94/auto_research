import time

from pytest_pytestrail import pytestrail

from src.pages.coccoc_common import open_browser
from src.pages.onboarding.onboarding import OnBoarding
from src.pages.settings.settings_side_bar import SettingsSidebar
from src.pages.sidebar.sidebar import Sidebar
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474087")
def test_try_now_on_boarding(
    reset_sidebar_on_boarding: None, on_boarding: OnBoarding, sidebar: Sidebar
):
    for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
        on_boarding.open_on_boarding_url(
            url=setting.list_on_boarding_feature_icons.get(icon_name)
        )
        on_boarding.check_on_boarding_is_shown()
        on_boarding.click_try_now_btn()
        if icon_name in setting.list_sidebar_feature_icons:
            sidebar.click_to_hide_sidebar_web_panel()
            sidebar.check_feature_icon_show(icon_name)
        time.sleep(3)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474099")
def test_do_not_show_on_boarding_again(
    reset_sidebar_on_boarding: None, on_boarding: OnBoarding
):
    for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
        on_boarding.open_on_boarding_url(
            url=setting.list_on_boarding_feature_icons.get(icon_name)
        )
        on_boarding.check_on_boarding_is_shown()
        on_boarding.click_close_on_boarding()
        on_boarding.reload_page()
        on_boarding.check_on_boarding_is_hidden()
        time.sleep(3)


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474102")
def test_no_sidebar_on_boarding_when_off_sidebar(
    reset_sidebar_on_boarding: None,
    on_boarding: OnBoarding,
    settings_side_bar: SettingsSidebar,
):
    try:
        settings_side_bar.hide_sidebar()
        for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
            on_boarding.open_on_boarding_url(
                url=setting.list_on_boarding_feature_icons.get(icon_name)
            )
            on_boarding.check_on_boarding_is_hidden()
            time.sleep(3)
    finally:
        settings_side_bar.show_sidebar(is_need_to_open_new_tab=True)
