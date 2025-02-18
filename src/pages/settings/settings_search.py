import time
from typing import List

from src.pages.base import BasePlaywright
from playwright.sync_api import Locator, expect, sync_playwright

from src.pages.base import BasePlaywright
from src.pages.coccoc_common import open_browser
from src.utilities import os_utils, file_utils
from tests import setting

lang = setting.coccoc_language


class SettingsSearch(BasePlaywright):
    @property
    def title(self) -> Locator:
        return self.page.locator('div[id="header"] h2')

    @property
    def text_search_engine_use_in_address_bar(self) -> Locator:
        return self.page.locator("#searchExplanation")

    @property
    def text_manage_search_engines_and_site_search(self) -> Locator:
        return self.page.locator("#enginesSubpageTrigger #labelWrapper #label")

    @property
    def drop_down_search_list(self) -> Locator:
        return self.page.locator('#pages select[class="md-select"]')

    @property
    def search_vendors(self) -> Locator:
        return self.page.locator('#pages select[class="md-select"] option')

    @property
    def list_setting_search_engine_entry(self) -> List[Locator]:
        return self.page.locator(
            "#container > div > settings-search-engine-entry"
        ).all()

    @property
    def list_setting_search_engine_entries_name(self) -> List[Locator]:
        return self.page.locator(
            "#container > div > settings-search-engine-entry #name-column > div"
        ).all()

    @property
    def manage_search_engines_and_site_search(self) -> Locator:
        return self.page.locator("#enginesSubpageTrigger")

    # Interaction methods
    def open_page(self):
        self.page.goto("coccoc://settings/search")
        # Verify some UIs
        if "en" in lang:
            expect(
                self.page.get_by_role("heading", name="Search engine")
            ).to_be_visible()
            expect(self.text_search_engine_use_in_address_bar).to_contain_text(
                "Search engine used in the address bar"
            )
            expect(self.text_manage_search_engines_and_site_search).to_contain_text(
                "Manage search engines and site search"
            )
        else:
            expect(
                self.page.get_by_role("heading", name="Công cụ tìm kiếm")
            ).to_be_visible()
            expect(self.text_search_engine_use_in_address_bar).to_contain_text(
                "Công cụ tìm kiếm được sử dụng trên thanh địa chỉ"
            )
            expect(self.text_manage_search_engines_and_site_search).to_contain_text(
                "Quản lý công cụ tìm kiếm và công cụ tìm kiếm trang web"
            )

    def click_manage_search_engines_and_site_search(self):
        self.manage_search_engines_and_site_search.click()

    def get_list_setting_search_engine_entry(self):
        for i in self.list_setting_search_engine_entry:
            print(i)
            # if i.get_attribute('is-default')

        for j in self.list_setting_search_engine_entries_name:
            print(j.text_content())

    def get_list_search_vendor_name(self) -> list:
        list_search_vendor: list = []
        for ele in self.list_setting_search_engine_entries_name:
            name_text = ele.text_content()
            if "Default" in name_text:
                list_search_vendor.append(name_text.split(" (Default)")[0])
            elif "Mặc định" in name_text:
                list_search_vendor.append(name_text.split(" (Mặc định)")[0])
            else:
                list_search_vendor.append(ele.text_content())
        return list_search_vendor

    def check_default_search(self, search_vendor_name: str = "Cốc Cốc"):
        for ele in self.list_setting_search_engine_entries_name:
            if "Mặc định" in ele.text_content() or "Default" in ele.text_content():
                assert search_vendor_name in ele.text_content()

    def get_default_search_engine(self) -> str:
        default_search_name: str = ""
        for ele in self.list_setting_search_engine_entries_name:
            name_text = ele.text_content()
            if "Default" in name_text:
                default_search_name = name_text.split(" (Default)")[0]
            elif "Mặc định" in name_text:
                default_search_name = name_text.split(" (Mặc định)")[0]
        return default_search_name

    def click_btn_more_actions(self, search_vendor_name: str = "Cốc Cốc") -> Locator:
        for entry_search in self.list_setting_search_engine_entry:
            if (
                search_vendor_name
                in entry_search.locator("#name-column > div").text_content()
            ):
                # check button is enable or not
                if (
                    entry_search.locator(
                        'cr-icon-button[class="icon-more-vert"]'
                    ).get_attribute("aria-disabled")
                    == "false"
                ):
                    entry_search.locator(
                        'cr-icon-button[class="icon-more-vert"]'
                    ).click()
                    return entry_search

    def click_btn_edit(self, search_vendor_name: str = "Cốc Cốc"):
        for entry_search in self.list_setting_search_engine_entry:
            if (
                search_vendor_name
                in entry_search.locator("#name-column > div").text_content()
            ):
                entry_search.locator("#editIconButton").click()

    def click_btn_make_default(self, search_vendor_name: str = "Cốc Cốc"):
        entry_search: Locator = self.click_btn_more_actions(search_vendor_name)
        if entry_search:
            entry_search.locator("#makeDefault").click()
            assert search_vendor_name == self.get_default_search_engine()

    def click_btn_make_delete(self, search_vendor_name: str = "Cốc Cốc"):
        entry_search: Locator = self.click_btn_more_actions(search_vendor_name)
        if entry_search:
            entry_search.locator("#deactivate").click()
            expect(entry_search).to_be_hidden()


# Open a coccoc then reload repeatedly and wait for the metrics sent
def wait_for_metric_is_sent_to_cuacua(timeout=60) -> bool:
    interval_delay = 10
    total_delay = 0
    metrics_json = rf"C:\Users\{os_utils.get_username()}\Documents\polite_search.json"
    while total_delay < timeout:
        try:
            if file_utils.check_file_is_exists(metrics_json):
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if file_utils.check_file_is_exists(metrics_json):
        return True
    else:
        print(rf"Time out after {timeout} seconds of waiting for the metrics sent")
        return False
