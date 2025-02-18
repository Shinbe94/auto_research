import pytest

from src.pages.installations import installation_utils


@pytest.fixture(autouse=False)
def uninstall_coccoc_for_polite_search():
    installation_utils.uninstall_coccoc_silently()
