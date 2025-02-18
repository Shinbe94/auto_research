import json

from src.utilities import os_utils, file_utils


def test_get_show_close_all_tabs_confirmation():
    print(get_show_close_all_tabs_confirmation())


def get_show_close_all_tabs_confirmation() -> bool:
    """
    Get status of setting for confirmation warning close multiple tabs
    Return the status of 'Warn you when closing multiple tabs' from 'coccoc://settings/appearance'
    Returns: True as default, False means disable
    """
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Preferences"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                return parsed_json["show_close_all_tabs_confirmation"]
            except KeyError:
                return True
    else:
        print(rf"No {json_file} file found")


def test_disable_show_close_all_tabs_confirmation():
    disable_show_close_all_tabs_confirmation()


def disable_show_close_all_tabs_confirmation():
    """
    To disable confirmation warning close multiple tabs
    Note: Every time we reopen the browser, chromium will set it back to the default value 'Normal'
    Returns:None
    """
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Preferences"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                parsed_json["show_close_all_tabs_confirmation"] = False
                json.dump(parsed_json, open(json_file, "w"))
            except KeyError:
                pass
                # parsed_json["show_close_all_tabs_confirmation"] = False
                # json.dump(parsed_json, open(json_file, "w+"))
                # with open(json_file, 'w') as file:
                #     json.dump(parsed_json, file)
    else:
        print(rf"No {json_file} file found")


def get_value_by_key(key: str):
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Preferences"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                return parsed_json[key]
            except KeyError:
                return None
    else:
        print(rf"No {json_file} file found")


def test_get_value_by_key():
    print(get_value_by_key(key="show_close_all_tabs_confirmation"))


def test_disable_restore_popup():
    disable_restore_popup()


def disable_restore_popup():
    """
    Disabling restore popup that comes when chrome process is killed
    Returns:
    """
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Preferences"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                parsed_json["profile"]["exit_type"] = "none"
                json.dump(parsed_json, open(json_file, "w"))
            except KeyError:
                pass
                # parsed_json["show_close_all_tabs_confirmation"] = False
                # json.dump(parsed_json, open(json_file, "w+"))
                # with open(json_file, 'w') as file:
                #     json.dump(parsed_json, file)
    else:
        print(rf"No {json_file} file found")


def test_hide_bookmark_bar():
    hide_bookmark_bar()


def hide_bookmark_bar():
    """
    To hide bookmark_bar on browser
    Returns:None
    """
    json_file = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Preferences"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            parsed_json = json.load(file)
            try:
                parsed_json["bookmark_bar"]["show_on_all_tabs"] = False
                json.dump(parsed_json, open(json_file, "w"))
            except KeyError:
                pass
                # parsed_json["show_close_all_tabs_confirmation"] = False
                # json.dump(parsed_json, open(json_file, "w+"))
                # with open(json_file, 'w') as file:
                #     json.dump(parsed_json, file)
    else:
        print(rf"No {json_file} file found")
