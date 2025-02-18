import json

from src.pages.installations.base_window import BrowserBasePage
from src.utilities import os_utils, file_utils


def get_list_bookmark_from_file_by_profile(profile=1):
    file_name_with_path = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Profile {str(profile)}\Bookmarks"
    list_url = []
    if file_utils.check_file_is_exists(file_name_with_path):
        with open(file_name_with_path, encoding="utf8") as file:
            data = json.load(file)

            # print(data['roots']['bookmark_bar']['children'])
            for i in data["roots"]["bookmark_bar"]["children"]:
                # print(i['url'])
                list_url.append(i["url"])
    return list_url


def get_list_bookmark_from_file_for_default_profile():
    file_name_with_path = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Default\Bookmarks"
    list_bookmarks = []
    if file_utils.check_file_is_exists(file_name_with_path):
        with open(file_name_with_path, encoding="utf8") as file:
            data = json.load(file)
            for i in data["roots"]["bookmark_bar"]["children"]:
                list_bookmarks.append(i["url"])
    return list_bookmarks


def test_json():
    print(get_list_bookmark_from_file_by_profile(61))


class BookmarkPage(BrowserBasePage):
    pass
