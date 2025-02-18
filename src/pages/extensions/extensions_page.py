import json
import os
import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.coccoc_common import interactions, open_browser
from src.utilities import browser_utils, file_utils, os_utils
from tests import setting

COCCOC_EX_TITLE = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#content-wrapper > h2")'
BUTTON_UPDATE = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("extensions-toolbar").shadowRoot.querySelector("#updateNow")'
TOGGLE_DEVELOPER_MODE = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("extensions-toolbar").shadowRoot.querySelector("#devMode")'
ADBLOCK_NAME = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jeoooddfnfogpngdoijplcijdcoeckgm").shadowRoot.querySelector("#name")'
ADBLOCK_BTN_DETAIL = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jeoooddfnfogpngdoijplcijdcoeckgm").shadowRoot.querySelector("#detailsButton")'
ADBLOCK_TOGGLE_ON_OFF = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jeoooddfnfogpngdoijplcijdcoeckgm").shadowRoot.querySelector("#enableToggle")'
ADBLOCK_VERSION = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jeoooddfnfogpngdoijplcijdcoeckgm").shadowRoot.querySelector("#version")'

DICTIONARY_NAME = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#gfgbmghkdjckppeomloefmbphdfmokgd").shadowRoot.querySelector("#name")'
DICTIONARY_BTN_DETAIL = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#gfgbmghkdjckppeomloefmbphdfmokgd").shadowRoot.querySelector("#detailsButton")'
DICTIONARY_TOGGLE_ON_OFF = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#gfgbmghkdjckppeomloefmbphdfmokgd").shadowRoot.querySelector("#enableToggle")'
DICTIONARY_VERSION = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#gfgbmghkdjckppeomloefmbphdfmokgd").shadowRoot.querySelector("#version")'

SAVIOR_NAME = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jdfkmiabjpfjacifcmihfdjhpnjpiick").shadowRoot.querySelector("#name")'
SAVIOR_BTN_DETAIL = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jdfkmiabjpfjacifcmihfdjhpnjpiick").shadowRoot.querySelector("#detailsButton")'
SAVIOR_VERSION = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#jdfkmiabjpfjacifcmihfdjhpnjpiick").shadowRoot.querySelector("#version")'

CASHBACK_NAME = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#afaljjbleihmahhpckngondmgohleljb").shadowRoot.querySelector("#name")'
CASHBACK_BTN_DETAIL = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#afaljjbleihmahhpckngondmgohleljb").shadowRoot.querySelector("#detailsButton")'
CASHBACK_TOGGLE_ON_OFF = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#afaljjbleihmahhpckngondmgohleljb").shadowRoot.querySelector("#enableToggle")'
CASHBACK_VERSION = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("#afaljjbleihmahhpckngondmgohleljb").shadowRoot.querySelector("#version")'

EXTENSION_UPDATE_DONE_MESSAGE = 'document.querySelector("body > extensions-manager").shadowRoot.querySelector("cr-toast-manager").shadowRoot.querySelector("#content")'
EXTENSION_DETAIL_TITLE = (By.CSS_SELECTOR, "head > title")


def get_title(driver):
    element = interactions.get_shadow_element3(driver, COCCOC_EX_TITLE)
    return element.text


def turn_on_developer_mode(driver, toggle_status):
    current_toggle_status = get_toggle_status(driver, js_path=TOGGLE_DEVELOPER_MODE)
    if (toggle_status in ("ON", "OFF")) and (toggle_status == current_toggle_status):
        pass
    elif (toggle_status in ("ON", "OFF")) and (toggle_status != current_toggle_status):
        interactions.get_shadow_element3(driver, TOGGLE_DEVELOPER_MODE).click()
    else:
        print("toggle_status must be ON or OFF")
    time.sleep(2)


def check_extension_updated(driver, timeout=setting.timeout_selenium):
    max_delay = timeout
    interval_delay = 1
    total_delay = 0
    interactions.click_shadow_element(driver, js_path=BUTTON_UPDATE)
    current_coccoc_language = driver.execute_script(
        "return window.navigator.userLanguage || window.navigator.language"
    )
    # interactions.wait_for_element_presented_by_js_path(driver, EXTENSION_UPDATE_DONE_MESSAGE)
    # Wait for extension is updated
    while total_delay < max_delay:
        try:
            update_message = interactions.get_shadow_element3(
                driver, EXTENSION_UPDATE_DONE_MESSAGE
            ).text
            if current_coccoc_language == "vi":
                if update_message == "Đã cập nhật tiện ích":
                    break
            else:
                if update_message == "Extensions updated":
                    break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    time.sleep(2)
    driver.refresh()


def get_adblock_name(driver):
    element = interactions.get_shadow_element3(driver, ADBLOCK_NAME)
    return element.text


def get_adblock_version(driver):
    driver.refresh()
    time.sleep(2)
    element = interactions.get_shadow_element3(driver, ADBLOCK_VERSION)
    return element.text


def click_adblock_detail(driver, language=setting.coccoc_language):
    interactions.get_shadow_element3(driver, ADBLOCK_BTN_DETAIL).click()
    if language == "en":
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Extensions - Adblock"
        )
    else:
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Tiện ích mở rộng - Chặn quảng cáo"
        )


def click_cashback_detail(driver, language=setting.coccoc_language):
    interactions.get_shadow_element3(driver, CASHBACK_BTN_DETAIL).click()
    if language == "en":
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Extensions - Rủng Rỉnh"
        )
    else:
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Tiện ích mở rộng - Rủng Rỉnh"
        )


def click_savior_detail(driver, language=setting.coccoc_language):
    interactions.get_shadow_element3(driver, SAVIOR_BTN_DETAIL).click()
    if language == "en":
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Extensions - Download video & audio"
        )
    else:
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Tiện ích mở rộng - Tải video & audio"
        )


def click_dictionary_detail(driver, language=setting.coccoc_language):
    interactions.get_shadow_element3(driver, DICTIONARY_BTN_DETAIL).click()
    if language == "en":
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Extensions - Dictionary"
        )
    else:
        assert (
            interactions.get_text_from_element_by_inner_text(
                driver, EXTENSION_DETAIL_TITLE
            )
            == "Tiện ích mở rộng - Tra Từ Điển"
        )


def get_toggle_status(driver, js_path):
    toggle_status = interactions.get_attribute_value_by_js_path(
        driver, js_path, "aria-pressed"
    )
    if toggle_status == "true":
        return "ON"
    else:
        return "OFF"


def get_adblock_toggle_status(driver):
    toggle_status = interactions.get_attribute_value_by_js_path(
        driver, ADBLOCK_TOGGLE_ON_OFF, "aria-pressed"
    )
    if toggle_status == "true":
        return "ON"
    else:
        return "OFF"


def get_dictionary_toggle_status(driver):
    toggle_status = interactions.get_attribute_value_by_js_path(
        driver, DICTIONARY_TOGGLE_ON_OFF, "aria-pressed"
    )
    if toggle_status == "true":
        return "ON"
    else:
        return "OFF"


def get_cashback_toggle_status(driver):
    toggle_status = interactions.get_attribute_value_by_js_path(
        driver, CASHBACK_TOGGLE_ON_OFF, "aria-pressed"
    )
    if toggle_status == "true":
        return "ON"
    else:
        return "OFF"


def toggle_adblock(driver, toggle_status):
    current_toggle_status = get_toggle_status(driver, js_path=ADBLOCK_TOGGLE_ON_OFF)
    if (toggle_status in ("ON", "OFF")) and (toggle_status == current_toggle_status):
        pass
    elif (toggle_status in ("ON", "OFF")) and (toggle_status != current_toggle_status):
        interactions.get_shadow_element3(driver, ADBLOCK_TOGGLE_ON_OFF).click()
    else:
        print("toggle_status must be ON or OFF")


def toggle_dictionary(driver, toggle_status):
    current_toggle_status = get_toggle_status(driver, js_path=DICTIONARY_TOGGLE_ON_OFF)
    if (toggle_status in ("ON", "OFF")) and (toggle_status == current_toggle_status):
        pass
    elif (toggle_status in ("ON", "OFF")) and (toggle_status != current_toggle_status):
        interactions.get_shadow_element3(driver, DICTIONARY_TOGGLE_ON_OFF).click()
    else:
        print("toggle_status must be ON or OFF")


def toggle_cashback(driver, toggle_status):
    current_toggle_status = get_toggle_status(driver, js_path=CASHBACK_TOGGLE_ON_OFF)
    if (toggle_status in ("ON", "OFF")) and (toggle_status == current_toggle_status):
        pass
    elif (toggle_status in ("ON", "OFF")) and (toggle_status != current_toggle_status):
        interactions.get_shadow_element3(driver, CASHBACK_TOGGLE_ON_OFF).click()
    else:
        print("toggle_status must be ON or OFF")


def get_dictionary_name(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, DICTIONARY_NAME)
    except Exception as e:
        raise e
    else:
        return str(element.text)


def get_dictionary_version(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, DICTIONARY_VERSION)
    except Exception as e:
        raise e
    else:
        return str(element.text)


def get_savior_name(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, SAVIOR_NAME)
    except Exception as e:
        raise e
    else:
        return str(element.text)


def get_savior_version(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, SAVIOR_VERSION)
    except Exception as e:
        raise e
    else:
        return str(element.text)


def get_cashback_name(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, CASHBACK_NAME)
    except Exception as e:
        raise e
    else:
        return str(element.text)


def get_cashback_version(driver) -> str:
    try:
        element = interactions.get_shadow_element3(driver, CASHBACK_VERSION)
    except Exception as e:
        raise e
    else:
        return str(element.text)


""" Get latest extension version by API"""


def get_extension_version_by_name_via_api(extension_name) -> str:
    # extension_name: savior , en2vi, cache, adblock, rungrinh
    try:
        r = requests.get(f"https://update.coccoc.com/api/{extension_name}")
    except Exception as e:
        raise e
    else:
        data = r.json()
        return str(data["version"])  # Return version


def test_extension():
    get_extension_version_by_name_via_api(extension_name="savior")


def get_extension_version_from_its_folder(extension_id):
    extension_json_file = rf"C:\Program Files\CocCoc\Browser\Application\{browser_utils.get_coccoc_version()}\Extensions\{extension_id}"
    if file_utils.check_file_is_exists(extension_json_file):
        with open(extension_json_file) as json_data:
            data = json.load(json_data)
            extension_version = data["external_version"]
        return extension_version
    else:
        extension_json_file_x86 = rf"C:\Program Files (x86)\CocCoc\Browser\Application\{browser_utils.get_coccoc_version()}\Extensions\{extension_id}"
        with open(extension_json_file_x86) as json_data:
            data = json.load(json_data)
            extension_version = data["external_version"]
        return extension_version


def test_version():
    print(get_extension_version_from_its_folder(setting.savior_extension_json))


def get_user_extension_list(profile=1):
    user_extension_path = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Profile {str(profile)}\Extensions"
    return os.listdir(user_extension_path)


def get_user_extension_list_for_default_profile():
    user_extension_path = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Extensions"
    list_extension = os.listdir(user_extension_path)
    if "Temp" in list_extension:
        list_extension.remove("Temp")
    # print(os.listdir(user_extension_path))
    return list_extension


def open_coccoc_extensions(language=setting.coccoc_language):
    driver = open_browser.open_and_connect_coccoc_by_selenium()[0]
    try:
        driver.get(setting.coccoc_extensions)
        if "en" in language:
            assert get_title(driver) == "Cốc Cốc Extensions"
        else:
            assert get_title(driver) == "Tiện ích mở rộng của Cốc Cốc"
    except Exception:
        browser_utils.kill_all_coccoc_process()
        driver.get(setting.coccoc_extensions)
        if "en" in language:
            assert get_title(driver) == "Cốc Cốc Extensions"
        else:
            assert get_title(driver) == "Tiện ích mở rộng của Cốc Cốc"
    finally:
        return driver


def check_extension_version_updated(language=setting.coccoc_language):
    driver: WebDriver = open_coccoc_extensions(language)
    title = driver.title
    try:
        # Check 4 default extensions appear
        if language == "en":
            if browser_utils.get_coccoc_major_build() <= 107:
                assert get_adblock_name(driver) == "Adblock"
            assert get_cashback_name(driver) == "Rủng Rỉnh"
            assert get_dictionary_name(driver) == "Dictionary"
            assert get_savior_name(driver) == "Download video & audio"
        else:
            if browser_utils.get_coccoc_major_build() <= 107:
                assert get_adblock_name(driver) == "Chặn quảng cáo"
            assert get_cashback_name(driver) == "Rủng Rỉnh"
            assert get_dictionary_name(driver) == "Tra Từ Điển"
            assert get_savior_name(driver) == "Tải video & audio"

        # check 4 default extensions version
        # Turn on developer mode
        turn_on_developer_mode(driver, toggle_status="ON")
        check_extension_updated(driver)
        if browser_utils.get_coccoc_major_build() <= 107:
            assert get_extension_version_by_name_via_api(
                extension_name="adblock"
            ) == get_adblock_version(driver)
        assert get_extension_version_by_name_via_api(
            extension_name="en2vi"
        ) == get_dictionary_version(driver)
        assert get_extension_version_by_name_via_api(
            extension_name="rungrinh"
        ) == get_cashback_version(driver)
        assert int("".join(get_savior_version(driver).split("."))) >= int(
            "".join(
                get_extension_version_by_name_via_api(extension_name="savior").split(
                    "."
                )
            )
        )
        # assert get_extension_version_by_name_via_api(
        #     extension_name="savior"
        # ) == get_savior_version(driver)
    finally:
        open_browser.close_coccoc_by_window_title(title=title)
        if driver is not None:
            driver.quit()
