from src.pages.base import BaseAppium, BasePlaywright, BaseSelenium
from src.pages.constant import AWADL


class ExtensionDevtoolApp(BaseAppium):
    CONSOLE_TAB = (AWADL.AUTOMATION_ID, "tab-console")
    ADD_BTN = (AWADL.NAME, "service worker")

    def click_console(self):
        self.click_ele(self.CONSOLE_TAB)

    def click_service_worker(self):
        self.click_ele(self.ADD_BTN)


class ExtensionDevtoolSel(BaseSelenium):
    def open_extension_background(self, extension_id: str) -> None:
        self.open_page(url=f"chrome-extension://{extension_id}/background.html")

    def open_extension_service_worker(self, extension_id: str) -> None:
        self.open_page(url=f"chrome-extension://{extension_id}/background.js")

    def get_extension_log(self) -> None:
        logs = self.scc.get_log("browser")
        for log in logs:
            print(log)


class ExtensionDevtool(BasePlaywright):
    def open_extension_background(self, extension_id: str) -> None:
        self.open_page(url=f"chrome-extension://{extension_id}/background.html")

    def open_extension_service_worker(self, extension_id: str) -> None:
        self.open_page(url=f"chrome-extension://{extension_id}/background.js")
