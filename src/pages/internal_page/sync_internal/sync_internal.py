import time

from selenium.webdriver.common.by import By
from src.pages.installations.base_window import BrowserBasePage


class SyncInternal(BrowserBasePage):
    LIST_COMMIT = (By.CSS_SELECTOR, 'div[class="traffic-event-entry"]')
    LIST_COMMIT_RESPONSE = (By.CSS_SELECTOR, 'div[class="traffic-event-entry"]')

    def check_if_list_commit_response(self):
        self.get_url("coccoc://sync-internals/")
        list_commit = self.get_elements(self.LIST_COMMIT)
        list_commit_response = []
        list_commit_response2 = []
        if len(list_commit) > 0:
            for element in list_commit:
                if "type" in element.get_attribute("class").split():
                    list_commit_response.append(element)

        if len(list_commit_response) > 0:
            for element in list_commit_response:
                if element.text == "Commit Response":
                    list_commit_response2.append(element)

        if len(list_commit_response2) > 0:
            last_element = list_commit_response2[-1]
            last_text_element = last_element.find_element_by_cssselector(
                'pre[class="details"]'
            )
            text_appeared = False
            max_delay = 60
            interval_delay = 0.5
            total_delay = 0
            while not False:
                try:
                    text = last_text_element.text
                    if "Result: SYNCER_OK" == text:
                        text_appeared = True
                    time.sleep(interval_delay)
                    total_delay += interval_delay
                    if total_delay > max_delay:
                        print("Timeout for wait for getting syncing status")
                        break
                finally:
                    break
            if text_appeared:
                title = self.get_current_window_title() + " - Cốc Cốc"
                self.close_coccoc_by_window_title(title)
                # return True

    def is_synced_done(self):
        self.get_url("coccoc://sync-internals/")

        return True
