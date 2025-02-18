import json
from time import sleep
import pytest

from src.pages.coccoc_common import open_browser
from src.pages.support_pages.support_pages import ChromeStore
from src.utilities import file_utils, os_utils


@pytest.fixture(autouse=False)
def add_extension_to_coccoc():
    coccoc_instance = open_browser.wad_coccoc_driver()
    appium_driver = coccoc_instance[0]
    try:
        cr = ChromeStore(appium_driver)
        cr.add_extension(
            url="https://chrome.google.com/webstore/detail/volume-master/jghecgabfgfdldnmbfkhmffcabddioke/related?hl=en-US"
        )
    finally:
        open_browser.close_coccoc_by_kill_process(sleep_n_seconds=1)
        try:
            os_utils.kill_process_by_name("WinAppDriver.exe")
        except Exception as e:
            raise e
        sleep(2)


@pytest.fixture(autouse=False)
def save_file_local_state():
    """This fixture is for saving the file Local State with these steps:
    1. Copy current file 'Local State' to the Documents folder
    2. Execute testing, then the test is done so
    3. Remove the file 'Local State' (the tested file)
    4. Copy the file 'Local State' (file save at 1) back to 'User Data'
    5. Clean the file 'Local State' at Documents
    """
    try:
        # copy to safe location
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
            dst_path=rf"C:\Users\{os_utils.get_username()}\Documents",
        )
        yield
    finally:
        # Remove edited files
        file_utils.remove_file(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State"
        )

        # copy back to User Data
        file_utils.copy_single_file(
            src_path=rf"C:\Users\{os_utils.get_username()}\Documents\Local State",
            dst_path=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data",
        )

        # clean for save location
        file_utils.remove_file(
            file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Documents\Local State"
        )


@pytest.fixture(autouse=False)
def sleep_for_test() -> None:
    # sleep for 3 mins
    sleep(60)


@pytest.fixture(autouse=False)
def add_testing_extensionid_to_darklist() -> None:
    """Method is for add the testing extension_id to darklist by:
    - copy current dark list
    - append the testing extension_id to the current dark list
    - execute testing
    - then revert the previous value for darklist
    """
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State"
    current_extensions_darklist: list = []  # current list
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            parsed_json = json.load(file)
            current_extensions_darklist = parsed_json["corom"]["netUnblock"][
                "extensions_darklist"
            ]["extensions"]
            current_extensions_darklist.append(
                "jghecgabfgfdldnmbfkhmffcabddioke"
            )  # add extension_id for test
            # print(current_extensions_darklist)
            try:
                parsed_json["corom"]["netUnblock"]["extensions_darklist"][
                    "extensions"
                ] = current_extensions_darklist
                json.dump(parsed_json, open(json_file, "w"))
            except KeyError:
                pass
            # print(
            #     parsed_json["corom"]["netUnblock"]["extensions_darklist"]["extensions"]
            # )
    else:
        print(f"No {json_file} file found")
    yield
    del current_extensions_darklist[-1]  # remove the added one
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                parsed_json["corom"]["netUnblock"]["extensions_darklist"][
                    "extensions"
                ] = current_extensions_darklist
                json.dump(parsed_json, open(json_file, "w"))
            except KeyError:
                pass
            # print(
            #     parsed_json["corom"]["netUnblock"]["extensions_darklist"]["extensions"]
            # )
    else:
        print(f"No {json_file} file found")


def test_add_testing_extensionid_to_darklist(add_testing_extensionid_to_darklist):
    pass
