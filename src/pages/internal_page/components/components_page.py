import time

from playwright.sync_api import Locator, expect

from src.pages.base import BasePlaywright
from tests import setting

lang = setting.coccoc_language


class ComponentsPage(BasePlaywright):
    @property
    def component_coccoc_tor_client(self) -> Locator:
        return self.page.locator('span[class="component-name"]').filter(
            has_text="CocCoc Tor Client (Windows)"
        )

    @property
    def component_coccoc_tor_version(self) -> Locator:
        return self.page.locator("#version-gpoepookpekemkncflgccfifoomafdkb")

    @property
    def component_coccoc_tor_status(self) -> Locator:
        return self.page.locator("#status-gpoepookpekemkncflgccfifoomafdkb")

    # Interaction methods
    def open_page(self) -> None:
        self.page.goto("coccoc://components/")

    def check_component_coccoc_tor_client_exist(self) -> bool:
        """to check coccoc tor client component appeared
        Returns:
            bool: True if exist and vice versa
        """
        self.open_page()
        is_exist = False
        if self.component_coccoc_tor_client:
            is_exist = True
        return is_exist

    def get_coccoc_tor_client_version(self) -> str:
        return self.component_coccoc_tor_version.text_content()

    def get_coccoc_tor_client_status(self) -> str:
        return self.component_coccoc_tor_status.text_content()

    def wait_for_coccoc_tor_component_updated(
        self, timeout=setting.timeout_for_update_components
    ) -> bool:
        """Wait for coccoc tor client is updated automatically

        Args:
            timeout (_type_, optional): _description_. Defaults to setting.timeout_for_update_components.

        Returns:
            bool: True if updated, and vice versa
        """
        is_updated = False
        interval_delay = 10
        total_delay = 0
        if "en" in lang:
            text_updated_status = "Component already up to date"
        else:
            text_updated_status = "Thành phần đã được cập nhật"
        while total_delay < timeout:
            if self.get_coccoc_tor_client_status() == text_updated_status:
                is_updated = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
        if total_delay > timeout:
            print(
                rf"Time out for waiting component updated after {total_delay} seconds."
            )
        return is_updated
