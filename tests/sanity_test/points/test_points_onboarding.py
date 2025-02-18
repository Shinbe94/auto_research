from time import sleep
from pytest_pytestrail import pytestrail
from src.pages.internal_page.extensions.extensions_page import ExtensionsPage
from src.pages.onboarding.points_onboarding import PointsOnBoarding
from tests import setting


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763528")
def test_points_onboarding_ui(
    points_on_boarding: PointsOnBoarding, extensions_page: ExtensionsPage
):
    extensions_page.force_points_onboarding_shown()
    extensions_page.turn_off_savior()
    extensions_page.turn_on_savior()
    extensions_page.open_page("https://tinhte.vn")
    points_on_boarding.verify_points_onboarding_ui_non_logged_in()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763531")
def test_points_onboarding_shows_if_not_logged_in(points_on_boarding: PointsOnBoarding):
    points_on_boarding.clear_onboarding_local_storage()
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.verify_points_onboarding_ui_non_logged_in()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763537")
def test_points_onboarding_shows_only_1_time_if_not_logged_in(
    make_points_onboarding_shown,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763558")
def test_points_onboarding_shows_if_logged_in(
    login_and_sync, points_on_boarding: PointsOnBoarding
):
    points_on_boarding.clear_onboarding_local_storage()
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.verify_points_onboarding_ui_logged_in()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C771206")
def test_points_onboarding_shows_only_1_time_if_logged_in(
    login_and_sync,
    make_points_onboarding_shown,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763534")
def test_points_onboarding_does_not_show_on_working_time(
    reset_points_onboarding_state,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


def test_onboarding(points_on_boarding: PointsOnBoarding):
    assert points_on_boarding.check_points_onboarding_is_shown_by_console()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763540")
def test_points_onboarding_does_not_show_for_internal_pages(
    reset_points_onboarding_state,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="coccoc://extensions/")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()

    points_on_boarding.open_page(url=setting.coccoc_homepage_newtab)
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763543")
def test_just_only_1_onboarding_show_at_the_same_time(
    uninstall_coccoc,
    install_coccoc,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://www.messenger.com/")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763549")
def test_points_onboarding_does_not_show_if_restart_browser(
    reset_points_onboarding_state,
    make_points_onboarding_shown,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763552")
def test_points_onboarding_does_not_show_if_user_at_points_page(
    reset_points_onboarding_state,
    make_points_onboarding_shown,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://points.coccoc.com/")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C763561")
def test_no_onboarding_for_browser_less_than_89(
    install_very_old_coccoc,
    points_on_boarding: PointsOnBoarding,
):
    points_on_boarding.open_page(url="https://tinhte.vn")
    for _ in range(181):  # Sleep in 30 mins, reload while sleeping each 10 seconds
        points_on_boarding.reload_page()
        sleep(10)
    points_on_boarding.check_onboarding_is_not_shown()


# def test_onboarding(points_on_boarding: PointsOnBoarding):
#     assert points_on_boarding.check_points_onboarding_is_shown_by_console()
