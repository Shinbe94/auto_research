from src.pages.base import BasePage


class SearchPage(BasePage):

    @property
    def input_text(self):
        return self.page.wait_for_selector('input[name="q"]')

    INPUT_TEXT_SEARCH = 'input[name="q"]'
    BTN_SEARCH = 'input[name="btnK"]'
    BTN_SEARCH2 = '//form/div[1]/div[1]/div[2]/div[2]/div[5]//input[@name="btnK"]'

    def load_search_page(self, url):
        self.goto(url)

    def is_title_matches(self):
        return "Google" in self.page.title()

    def execute_search(self, text):
        self.page.fill(self.INPUT_TEXT_SEARCH, text)
        # self.page.press(self.BTN_SEARCH, "Enter")
        self.page.click(self.BTN_SEARCH2)
