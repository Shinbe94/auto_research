from pytest_pytestrail import pytestrail

from src.pages.internal_page.credits.credits_page import CreditsPage


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C542877")
def test_show_licences(credits_page: CreditsPage):
    credits_page.open_credits_page()
    credits_page.click_to_show_libtorrent_licences()
    credits_page.check_libtorrent_licences_content_is_shown()
    credits_page.click_to_show_libtorrent_licences()
    credits_page.click_to_show_libtorrent_homepage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C542880")
def test_show_homepage(credits_page: CreditsPage):
    credits_page.open_credits_page()
    credits_page.click_to_show_libtorrent_homepage()
