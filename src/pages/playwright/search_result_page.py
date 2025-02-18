from src.pages.base import BasePage


class SearchResultsPage(BasePage):

    def is_results_found(self):
        selector = '#result-stats'
        content = self.page.locator(
            selector).text_content()
        return content is not None
