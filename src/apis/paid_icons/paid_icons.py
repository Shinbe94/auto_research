from src.apis.base_api import BaseApi
from src.utilities.api.request import APIRequest
from tests import setting


class PaidIcons(BaseApi):
    def __init__(self):
        super().__init__()
        self.request = APIRequest()

    def get_paid_icons(self):
        paid_icons = self.request.get(url=setting.PAID_ICONS_API, headers=self.headers)
        return paid_icons

    def get_list_paid_icons_name(self):
        icons = self.request.get(
            url=setting.PAID_ICONS_API, headers=self.headers
        ).as_dict
        icon_names = [icon.get("title") for icon in icons]  # type: ignore
        return icon_names
