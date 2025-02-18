from time import sleep
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pytest_pytestrail import pytestrail
from src.pages.coccoc_common import open_browser

from src.pages.installations import (
    installation_utils,
    installation_page,
)
from src.pages.settings import first_time_run
from src.utilities import (
    browser_utils,
    encode_decode,
    os_utils,
    network_utils,
)

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086622")
@pytest.mark.skipif(
    os_utils.get_real_system_arch(is_format=False) == "32bit",
    reason="Only support win 64bit",
)
@pytest.mark.install_coccoc
def test_metric_request_when_opening_browser(delete_metrics_file_if_exist):
    driver: WebDriver = open_browser.open_and_connect_coccoc_by_selenium()[0]
    sleep(3)
    driver.quit()
    open_browser.close_coccoc_by_new_tab()
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump
        network_utils.dump_network_log(file_name="mitm_proxy_metrics.py")
        sleep(20)
        # Open coccoc and wait for metrics is sent
        assert first_time_run.wait_for_metrics_is_sent()

        # get metrics log:
        requests_metrics_log_detail = (
            first_time_run.read_metrics_sent_when_open_browser()
        )

        # Assertions
        if requests_metrics_log_detail is not None:
            # Check detail request
            assert "metrics.coccoc.com" in requests_metrics_log_detail["Host"]
            assert "keep-alive" in requests_metrics_log_detail["Connection"]
            assert "Content-Length" in requests_metrics_log_detail.keys()
            assert (
                "application/vnd.chrome.uma"
                in requests_metrics_log_detail["Content-Type"]
            )
            assert "gzip, deflate, br" in requests_metrics_log_detail["Accept-Encoding"]
            assert "Mozilla" in requests_metrics_log_detail["User-Agent"]

            # Check uid & hid3
            assert browser_utils.get_uid() in str(requests_metrics_log_detail)

            assert encode_decode.format_base64_after_decoded(
                encoded_str=browser_utils.get_hid3()
            ) in str(requests_metrics_log_detail)
    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # uninstall coccoc
        installation_utils.uninstall_coccoc_silently()
