from pytest_pytestrail import pytestrail
from src.pages.installations import download_setup_file
from tests import setting
from src.pages.installations import installation_utils, installation_page
from src.utilities import file_utils

installation = installation_page.InstallationPage()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.skip
@pytestrail.case("C1086412")
def test_installing_fresh_package_successfully(language=setting.coccoc_language):
    try:
        installation.install_coccoc_by_build_name(
            language, build_name=setting.coccoc_build_name
        )
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086433")
def test_install_package_while_interruption(language=setting.coccoc_language):
    try:
        file_utils.rename_and_copy_file_host()
        download_setup_file.download_setup_file_automatically(is_headless=False)
        installation.install_interruption_coccoc(language=language)
    finally:
        file_utils.remove_and_revert_file_host()


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086418")
def test_pop_up_installer_confirm_during_installation(
    setup_file_for_test,
    language=setting.coccoc_language,
    version=setting.coccoc_test_version,
):
    installation.check_ui_of_install_dialog(
        language=language, version=version, file_name=setup_file_for_test
    )


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1086421")
def test_do_not_show_installation_dialog_after_installing_successfully(
    language=setting.coccoc_language,
):
    try:
        installation.install_coccoc_by_build_name(
            language, build_name=setting.coccoc_build_name
        )
    finally:
        installation_utils.uninstall_coccoc_silently()


# ------------------------------------------------------------------------------------------------------------------
# @pytest.mark.build_standalone
@pytestrail.case("C1086430")
def test_installing_from_standalone_package(language=setting.coccoc_language):
    try:
        installation.install_coccoc_by_build_name(
            language, build_name=setting.coccoc_build_name
        )
    finally:
        installation_utils.uninstall_coccoc_silently()
