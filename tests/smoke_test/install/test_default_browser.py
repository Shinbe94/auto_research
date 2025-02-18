import time

from pytest_pytestrail import pytestrail
from tests import setting
from src.utilities import os_utils
from src.pages.installations import installation_utils
from src.utilities import assistant_apps_utils

from src.pages.installations import installation_page
from src.pages.settings import settings_default_browser
import logging

LOGGER = logging.getLogger(__name__)

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytestrail.case("C1086580")
def test_if_set_default_browser_while_installing(
    language=setting.coccoc_language,
    build_name=setting.coccoc_build_name,
    is_default_browser=True,
):
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=is_default_browser,
        )
        # To verify message default browser:
        settings_default_browser.check_default_browser_text_by_pywinauto()

        # To check the default browser is working correctly by opening the link
        assistant_apps_utils.check_default_browser_by_open_link()
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086583")
def test_if_user_can_set_default_from_settings_page(
    language=setting.coccoc_language,
    build_name=setting.coccoc_build_name,
    is_default_browser=False,
):
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=is_default_browser,
        )
        # Set default browser from setting page then check Coccoc is a default browser
        settings_default_browser.set_default_browser_from_setting_page_pywinauto(
            language=language
        )
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086586")
def test_if_not_set_default_while_installing(
    language=setting.coccoc_language,
    build_name=setting.coccoc_build_name,
    is_default_browser=False,
):
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=is_default_browser,
        )
        # Check coccoc is not a default browser
        settings_default_browser.check_if_not_a_default_browser(language=language)
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086589")
def test_if_set_default_then_change_to_other(
    language=setting.coccoc_language,
    build_name=setting.coccoc_build_name,
    is_default_browser=True,
):
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=is_default_browser,
            is_close_after_installed=True,
        )

        time.sleep(2)
        # To verify message default browser:
        settings_default_browser.check_default_browser_text_by_pywinauto()

        # To set the Google Chrome as a default browser
        settings_default_browser.set_a_browser_to_default()

        # Verify Coccoc default browser page again:
        settings_default_browser.check_if_not_a_default_browser(language=language)
        time.sleep(1)
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086592")
def test_set_default_message_after_installed_a_time(
    language=setting.coccoc_language,
    build_name=setting.coccoc_build_name,
    is_default_browser=False,
):
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=is_default_browser,
            is_close_after_installed=True,
        )
        # Set the system date to 2 months later
        os_utils.change_os_date_to_2_months_later(is_close_cmd_after_changed=True)

        # Verify Coccoc default browser page:
        settings_default_browser.check_if_not_a_default_browser(language=language)

    finally:
        # Change system date to current date
        # os_utils.set_a_date(today)
        # os_utils.sync_datetime()
        os_utils.set_the_time_from_settings_automatically()
        # Uninstall coccoc
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086595")
def test_metric_default_browser(
    language=setting.coccoc_language, build_name=setting.coccoc_build_name
):
    settings_default_browser.set_a_browser_to_default()
    try:
        installation.install_coccoc_by_build_name(
            language=language,
            build_name=build_name,
            is_default_browser=True,
            is_delete_file_offscreen_cashback_extension=True,
        )
        # check the metric "Histogram: DefaultBrowser.State recorded 1 samples"
        settings_default_browser.check_metric_default_browser()
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223874")
def xtest_set_default_pdf_and_default_browser(
    language=setting.coccoc_language, build_name=setting.coccoc_build_name
):
    settings_default_browser.set_a_browser_to_default()
    try:
        installation.install_coccoc_by_build_name(
            language=language, build_name=build_name, is_default_browser=True
        )
        # check the metric "Histogram: DefaultBrowser.State recorded 1 samples"
        settings_default_browser.check_metric_default_browser()
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1223880")
def xtest_set_default_pdf_and_not_default_browser(
    language=setting.coccoc_language, build_name=setting.coccoc_build_name
):
    settings_default_browser.set_a_browser_to_default()
    try:
        installation.install_coccoc_by_build_name(
            language=language, build_name=build_name, is_default_browser=True
        )
        # check the metric "Histogram: DefaultBrowser.State recorded 1 samples"
        settings_default_browser.check_metric_default_browser()
    finally:
        settings_default_browser.set_a_browser_to_default()
        installation_utils.uninstall_coccoc_silently()
