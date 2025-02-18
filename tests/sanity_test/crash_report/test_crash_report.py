import time

from pytest_pytestrail import pytestrail
from playwright.sync_api import Locator, expect
from src.pages.internal_page.crashes.crash_page import CrashPage
from src.pages.internal_page.crashes.crashes_page import CrashesPage
from src.pages.support_pages.support_pages import GooglePage

from src.utilities import file_utils, os_utils, network_utils, read_write_data_by
from tests import setting
from src.pages.internal_page.crashes import crashes_page as cp


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C54309")
def test_crash_report_page_is_displayed(crash_page: CrashPage, google_page: GooglePage):
    try:
        google_page.open_google_homepage()
        crash_page.open_crash_page()
        crash_page.click_reload_btn()
        assert google_page.get_current_url() == "https://www.google.com/"
    finally:
        # handle permission error if any, some time the permission error occurs but don't know why
        try:
            file_utils.remove_all_crash_dump(
                rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports"
            )
        except PermissionError:
            pass


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502911")
def xtest_detail_crash_report_sent_to_server(
    uninstall_coccoc: None, crash_page: CrashPage, crashes_page: CrashesPage, lang: str
):
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump with file capture network
        network_utils.dump_network_log(file_name="crash_report.py")

        crash_page.open_google_homepage()
        crash_page.click_reload_btn()

        crash_page.open_google_homepage()
        crash_page.click_reload_btn()

        new_page = crashes_page.page.context.new_page()
        new_page.goto("coccoc://crashes/")
        new_page.locator("#crashList > div:nth-child(3) > button").click()
        new_page.reload()
        expect(
            new_page.locator("#crashList > div:nth-child(3) > button")
        ).to_be_hidden()
        crash_page.open_google_homepage()
        crash_page.click_reload_btn()

        new_page2 = crashes_page.page.context.new_page()
        new_page2.goto("coccoc://crashes/")

        # Wait for the request log sent and be captured!
        assert cp.wait_for_crash_report_is_sent()
        if "en" in lang:
            expect(
                new_page2.locator(
                    "#crashList > div:nth-child(3) > table > tbody > tr.status > td.value"
                )
            ).to_contain_text("Uploaded")
        else:
            expect(
                new_page2.locator(
                    "#crashList > div:nth-child(3) > table > tbody > tr.status > td.value"
                )
            ).to_contain_text("Đã tải lên")
        request_data = read_write_data_by.read_json_file(file_name="crash_report_log")
        # print(request_data)
        if request_data is not None:
            assert "cr.browser.coccoc.com" in request_data["Host"]
            assert "keep-alive" in request_data["Connection"]
            assert "Content-Length" in request_data.keys()
            assert "text/html; charset=utf-8" in request_data["Content-Type"]
            assert "Breakpad/1.0 (Windows)" in request_data["User-Agent"]
            # assert vid in request_data.get('Cookie')
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\crash_report_log.json"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502914")
def xtest_no_crash_sent_within_1_hour_after_previous_report_sent(
    uninstall_coccoc: None, crash_page: CrashPage, crashes_page: CrashesPage, lang: str
):
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump with file capture network
        network_utils.dump_network_log(file_name="crash_report.py")

        crash_page.open_google_homepage()
        crash_page.click_reload_btn()

        crash_page.open_google_homepage()
        crash_page.click_reload_btn()

        new_page = crashes_page.page.context.new_page()
        new_page.goto("coccoc://crashes/")
        new_page.locator("#crashList > div:nth-child(3) > button").click()
        new_page.reload()
        expect(
            new_page.locator("#crashList > div:nth-child(3) > button")
        ).to_be_hidden()

        # Wait for the request log sent and be captured!
        assert cp.wait_for_crash_report_is_sent()
        if "en" in lang:
            expect(
                new_page.locator(
                    "#crashList > div:nth-child(3) > table > tbody > tr.status > td.value"
                )
            ).to_contain_text("Not uploaded")
        else:
            expect(
                new_page.locator(
                    "#crashList > div:nth-child(3) > table > tbody > tr.status > td.value"
                )
            ).to_contain_text("Chưa tải lên")
        request_data = read_write_data_by.read_json_file(file_name="crash_report_log")
        # print(request_data)
        if request_data is not None:
            assert "cr.browser.coccoc.com" in request_data["Host"]
            assert "keep-alive" in request_data["Connection"]
            assert "Content-Length" in request_data.keys()
            assert "text/html; charset=utf-8" in request_data["Content-Type"]
            assert "Breakpad/1.0 (Windows)" in request_data["User-Agent"]
            # assert vid in request_data.get('Cookie')
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\crash_report_log.json"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502917")
def test_information_crash_report_saved_in_local_folder(crash_page: CrashPage):
    crash_page.open_crash_page()
    crash_page.click_reload_btn()
    crash_page.open_crash_page()
    assert (
        len(
            file_utils.list_all_files_and_folders(
                directory=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports"
            )
        )
        > 1
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502920")
def xtest_crash_report_send_to_server_or_not(
    uninstall_coccoc: None, crash_page: CrashPage
):
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump with file capture network
        network_utils.dump_network_log(file_name="crash_report.py")

        crash_page.open_google_homepage()
        crash_page.click_reload_btn()
        # Wait for the request log sent and be captured!
        assert cp.wait_for_crash_report_is_sent()
        request_data = read_write_data_by.read_json_file(file_name="crash_report_log")
        if request_data is not None:
            assert "cr.browser.coccoc.com" in request_data["Host"]
            assert "keep-alive" in request_data["Connection"]
            assert "Content-Length" in request_data.keys()
            assert "text/html; charset=utf-8" in request_data["Content-Type"]
            assert "Breakpad/1.0 (Windows)" in request_data["User-Agent"]
            # assert vid in request_data.get('Cookie')
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\crash_report_log.json"
        )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C502923")
def test_no_provide_additional_detail_btn_show(
    crash_page: CrashPage, crashes_page: CrashesPage
):
    lang = setting.coccoc_language
    crash_page.open_crash_page()
    crash_page.click_reload_btn()
    new_page = crashes_page.page.context.new_page()
    new_page.goto("coccoc://crashes/")
    time.sleep(2)

    if lang == "en":
        element: Locator = new_page.get_by_text(
            "Provide additional details", exact=True
        )
    else:
        element: Locator = new_page.get_by_text("Cung cấp chi tiết bổ sung", exact=True)
    expect(element).not_to_be_visible()
