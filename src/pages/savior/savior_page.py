from src.pages.savior.savior_base_page import SaviorBasePage


class SaviorPage(SaviorBasePage):
    ID_BTN_DOWNLOAD = 'document.querySelector("html > div").shadowRoot.querySelector("#download-main").getAttribute("id")'
    CLICK_BTN_DOWNLOAD = 'document.querySelector("html > div").shadowRoot.querySelector("#download-main").click()'
    SHOW_SAVIOR_DOCK = "document.querySelector('html > div').shadowRoot.querySelector('.overlay').classList.remove('hidden')"

    def click_btn_download(self):
        self.wait_for_savior_element(self.ID_BTN_DOWNLOAD)
        self.driver.execute_script(self.CLICK_BTN_DOWNLOAD)

    def show_savior_dock(self):
        self.driver.execute_script(self.SHOW_SAVIOR_DOCK)
