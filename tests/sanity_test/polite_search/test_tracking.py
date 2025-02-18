import time

from pytest_pytestrail import pytestrail

from src.pages.settings import settings_search as setSearch
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import file_utils, os_utils, network_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1013303")
def test_crash_report_send_to_server_or_not(
    settings_search: setSearch.SettingsSearch, toolbar: Toolbar
):
    try:
        # Turn ON proxy
        os_utils.turn_proxy_on()

        # Start mitmdump with file capture network
        network_utils.dump_network_log(file_name="polite_search.py")

        settings_search.open_page()
        settings_search.click_manage_search_engines_and_site_search()
        settings_search.click_btn_make_default(search_vendor_name="Google")
        time.sleep(2)
        settings_search.reload_page()
        toolbar.make_search_value(search_str=rf"váy hoa", is_press_enter=True)

        # Wait for the request log sent and be captured!
        assert setSearch.wait_for_metric_is_sent_to_cuacua() is False

    finally:
        # Turn OFF proxy
        os_utils.turn_proxy_off()

        # Turn OFF dump_network_log
        os_utils.kill_process_by_name("cmd.exe")
        os_utils.close_cmd(title_re="Administrator")

        # remove metrics log
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\Documents\polite_search.json"
        )

        # Change default to CocCoc search
        settings_search.open_page()
        settings_search.click_manage_search_engines_and_site_search()
        settings_search.click_btn_make_default(search_vendor_name="Cốc Cốc")
