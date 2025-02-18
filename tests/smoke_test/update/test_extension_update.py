import pytest
from pytest_pytestrail import pytestrail

from src.pages.installations import installation_utils, installation_page
from src.pages.extensions import extensions_page
from tests import setting

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086880")
@pytest.mark.install_coccoc
def test_update_extension(language=setting.coccoc_language):
    try:
        extensions_page.check_extension_version_updated(language)
    finally:
        installation_utils.uninstall_coccoc_silently()
