import time

from pytest_pytestrail import pytestrail
from src.pages.internal_page.histograms.histograms import Histograms
from src.pages.onboarding.onboarding import OnBoarding
from src.pages.sidebar.sidebar import Sidebar

from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474105")
def test_event_tracking_shown_at_first_time(
    reset_sidebar_on_boarding: None, on_boarding: OnBoarding, histograms: Histograms
):
    for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
        on_boarding.open_on_boarding_url(
            url=setting.list_on_boarding_feature_icons.get(icon_name)
        )
        on_boarding.check_on_boarding_is_shown()
        on_boarding.click_close_on_boarding()
    histograms.check_metric_savior_onboard_shown(count=1)
    assert histograms.get_total_samples_of_metric_savior_onboard_shown() == len(
        setting.list_on_boarding_feature_icons
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474114")
def test_event_tracking_after_click_try_now(
    reset_sidebar_on_boarding: None,
    on_boarding: OnBoarding,
    histograms: Histograms,
    sidebar: Sidebar,
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
    histograms.check_metric_savior_onboard_try_now_click(count=1)
    assert histograms.get_total_samples_of_metric_savior_onboard_try_now_click() == len(
        setting.list_on_boarding_feature_icons
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C474123")
def test_event_tracking_after_close_onboard(
    reset_sidebar_on_boarding: None, on_boarding: OnBoarding, histograms: Histograms
):
    for icon_name in list(setting.list_on_boarding_feature_icons.keys()):
        on_boarding.open_on_boarding_url(
            url=setting.list_on_boarding_feature_icons.get(icon_name)
        )
        on_boarding.check_on_boarding_is_shown()
        # on_boarding.close_on_boarding_by_pressing_esc_btn()
        # https://coccoc.atlassian.net/browse/PE-8573
        on_boarding.click_close_on_boarding()
        time.sleep(2)
    histograms.check_metric_savior_close_onboard_popup(count=1)
    assert histograms.get_total_samples_of_metric_savior_close_onboard_popup() == len(
        setting.list_on_boarding_feature_icons
    )
