from pytest_pytestrail import pytestrail
from src.pages.internal_page.components.components_page import ComponentsPage

from src.pages.menus.main_menu import MainMenu
from src.pages.toolbar.toolbar import Toolbar
from src.utilities import file_utils, os_utils


# ------------------------------------------------------------------------------------------------------------------
@pytestrail.case("C1128808")
# @pytest.mark.open_tor_window
def test_tor_components_update(
    uninstall_coccoc,
    install_coccoc,
    main_menu: MainMenu,
    toolbar: Toolbar,
    components_page: ComponentsPage,
):
    main_menu.open_new_tor_window_from_normal_window()
    main_menu.snap_selected_window_to_the_right_half_screen()
    # set active the normal window and open the 2nd tor window
    toolbar.click_address_and_search_bar()

    # check the coccoc tor client is updated correctly
    assert components_page.check_component_coccoc_tor_client_exist() is True
    assert components_page.wait_for_coccoc_tor_component_updated()
    # check folder version
    assert components_page.get_coccoc_tor_client_version() in file_utils.list_all_files_and_folders(
        directory=rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\CocCocTorClient"
    )
