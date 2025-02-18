import faulthandler
import time
from pywinauto import Desktop
from pywinauto.timings import always_wait_until_passes

from tests import setting
from src.pages.installations import download_setup_file
from src.pages.installations.base_window import BaseWindow
from src.utilities import browser_utils, network_utils, file_utils, os_utils


class InstallationPage(BaseWindow):
    # ----------------------------------------------------------------------------------------------------------------------
    # Download the CocCocSetUp.exe from coccoc.com then install it
    def install_coccoc_from_coccoc_com(
        self,
        language=setting.coccoc_language,
        version=setting.coccoc_test_version,
        is_default_browser=False,
        is_default_torrent=False,
        is_default_start_up=False,
        is_continue_install=True,
        is_close_after_installed=True,
        headless=True,
        is_select_always_close_all_tabs=True,
        is_delete_file_offscreen_cashback_extension=False,
    ):
        # Download setup file from coccoc.com
        download_setup_file.download_setup_file_automatically(is_headless=False)
        # download_setup_file.download_coccoc_setup_by_selenium(language, platform, headless)

        # Start coccocsetup.exe file to process installing
        # start = time.time()
        dialog = self.open_coccoc_install_dialog(language, version)
        # print(rf"time is: {str(time.time() - start)}")
        if is_continue_install:
            if not is_default_browser:
                time.sleep(1)
                dialog.child_window(
                    auto_id="2025", class_name="Button", control_type=50002
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()

            if not is_default_torrent:
                time.sleep(1)
                dialog.child_window(
                    auto_id="2027", class_name="Button", control_type=50002
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()

            if is_default_start_up:
                time.sleep(1)
                dialog.child_window(
                    auto_id="2026", class_name="Button", control_type=50002
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()

            # To click install button
            time.sleep(1)
            dialog.child_window(auto_id="2024", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # self.wait_for_installation_is_done(language)
            if is_close_after_installed:
                self.close_coccoc_at_the_first_time_it_is_opened(
                    language, is_select_always_close_all_tabs
                )
            time.sleep(1)
            if is_delete_file_offscreen_cashback_extension:
                browser_utils.delete_file_offscreen_cashback_extension()
            return True
        else:
            # To close the installation dialog
            dialog.child_window(auto_id="1", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # To cancel installation
            dialog.child_window(auto_id="2", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            time.sleep(1)
            return False

    def install_coccoc_by_coccocsetup_file(
        self,
        language=setting.coccoc_language,
        is_default_browser=False,
        is_default_torrent=False,
        is_default_start_up=False,
        is_continue_install=True,
        is_close_after_installed=True,
        is_select_always_close_all_tabs=True,
        is_delete_file_offscreen_cashback_extension=False,
    ):
        # Download setup file from coccoc.com
        # download_setup_file.download_coccoc_setup(platform=platform, headless=headless)
        # download_setup_file.download_coccoc_setup_by_selenium(language, platform, headless)

        # Start coccocsetup.exe file to process installing
        # dialog = self.open_coccoc_install_dialog(language)
        # dialog = os_utils.connect_to_window_via_pid(process_name='CocCocUpdate.exe')
        dialog = self.open_setup_file()
        if is_continue_install:
            if language == "en":
                if not is_default_browser:
                    time.sleep(1)
                    dialog.child_window(
                        title="Make Cốc Cốc your default browser",
                        auto_id="2025",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if not is_default_torrent:
                    time.sleep(1)
                    dialog.child_window(
                        title="Make Cốc Cốc your default torrent client",
                        auto_id="2027",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if is_default_start_up:
                    time.sleep(1)
                    dialog.child_window(
                        title="Run browser on system start",
                        auto_id="2026",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
            else:
                if not is_default_browser:
                    time.sleep(1)
                    dialog.child_window(
                        title="Đặt Cốc Cốc làm trình duyệt mặc định",
                        auto_id="2025",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if not is_default_torrent:
                    time.sleep(1)
                    dialog.child_window(
                        title="Đặt Cốc Cốc làm ứng dụng torrent mặc định",
                        auto_id="2027",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if is_default_start_up:
                    time.sleep(1)
                    dialog.child_window(
                        title="Khởi động trình duyệt cùng hệ thống",
                        auto_id="2026",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

            # To click install button
            time.sleep(1)
            dialog.child_window(auto_id="2024", control_type="Button").wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # self.wait_for_installation_is_done(language)
            if is_delete_file_offscreen_cashback_extension:
                browser_utils.delete_file_offscreen_cashback_extension()
            if is_close_after_installed:
                self.close_coccoc_at_the_first_time_it_is_opened(
                    language, is_select_always_close_all_tabs
                )
            time.sleep(1)
            return True
        else:
            # To close the installation dialog
            dialog.child_window(auto_id="1", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # To cancel installation
            dialog.child_window(auto_id="2", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            time.sleep(1)
            return False

    def install_coccoc_from_file_with_path(
        self,
        file_name_with_path,
        language=setting.coccoc_language,
        is_default_browser=False,
        is_default_torrent=False,
        is_default_start_up=False,
        is_continue_install=True,
        is_close_after_installed=True,
        is_select_always_close_all_tabs=True,
        is_delete_file_offscreen_cashback_extension=False,
    ):
        dialog = self.open_setup_file_by_its_path(file_name_with_path)
        if is_continue_install:
            if "en" in language:
                if not is_default_browser:
                    time.sleep(1)
                    dialog.child_window(
                        title="Make Cốc Cốc your default browser",
                        auto_id="2025",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if not is_default_torrent:
                    time.sleep(1)
                    dialog.child_window(
                        title="Make Cốc Cốc your default torrent client",
                        auto_id="2027",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if is_default_start_up:
                    time.sleep(1)
                    dialog.child_window(
                        title="Run browser on system start",
                        auto_id="2026",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
            else:
                if not is_default_browser:
                    time.sleep(1)
                    dialog.child_window(
                        title="Đặt Cốc Cốc làm trình duyệt mặc định",
                        auto_id="2025",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if not is_default_torrent:
                    time.sleep(1)
                    dialog.child_window(
                        title="Đặt Cốc Cốc làm ứng dụng torrent mặc định",
                        auto_id="2027",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                if is_default_start_up:
                    time.sleep(1)
                    dialog.child_window(
                        title="Khởi động trình duyệt cùng hệ thống",
                        auto_id="2026",
                        control_type="CheckBox",
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

            # To click install button
            time.sleep(1)
            dialog.child_window(auto_id="2024", control_type="Button").wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # self.wait_for_installation_is_done(language)
            if is_close_after_installed:
                self.close_coccoc_at_the_first_time_it_is_opened(
                    language, is_select_always_close_all_tabs
                )
            time.sleep(1)
            if is_delete_file_offscreen_cashback_extension:
                browser_utils.delete_file_offscreen_cashback_extension()
            return True
        else:
            # To close the installation dialog
            dialog.child_window(auto_id="1", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            # To cancel installation
            dialog.child_window(auto_id="2", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            time.sleep(1)
            return False

    # ----------------------------------------------------------------------------------------------------------------------
    # To install coccoc via mini installer file (e.g: 98.0.4758.116_coccocsetup.exe)
    def install_coccoc_by_mini_installer(
        self,
        version=setting.coccoc_test_version,
        is_close_after_installed=True,
        is_needed_download=False,
        # platform=setting.platform,
        platform=os_utils.get_real_system_platform(is_format_for_chromium_based=False),
        language=setting.coccoc_language,
        is_select_always_close_all_tabs=True,
    ):
        self.open_coccoc_mini_installer(
            version=version, is_needed_download=is_needed_download, platform=platform
        )
        self.wait_for_installation_is_done(language=language)
        if is_close_after_installed:
            self.close_coccoc_at_the_first_time_it_is_opened(
                language, is_select_always_close_all_tabs
            )

    # To install coccoc by build_name (downloaded from FTP server)
    def install_coccoc_by_build_name(
        self,
        language,
        build_name,
        version=setting.coccoc_test_version,
        # platform=setting.platform,
        platform=os_utils.get_real_system_platform(is_format_for_chromium_based=False),
        is_default_browser=False,
        is_default_torrent=False,
        is_default_start_up=False,
        is_default_pdf=False,
        is_continue_install=True,
        is_needed_download=False,
        is_close_after_installed=True,
        from_build_name=None,
        to_build_name=None,
        is_upgraded=False,
        is_delete_setup_file_after_installed=False,
        is_select_always_close_all_tabs=True,
        is_delete_file_offscreen_cashback_extension=False,  # Delete to prevent RungRinh stuck, selenium cant go ahead
    ):
        try:
            dialog = self.open_coccoc_install_dialog_by_build_name(
                version=version,
                build_name=build_name,
                is_needed_download=is_needed_download,
                platform=platform,
                from_build_name=from_build_name,
                to_build_name=to_build_name,
            )

            if is_continue_install:
                if not is_default_browser:
                    dialog.child_window(
                        auto_id="2025", class_name="Button", control_type=50002
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                if not is_default_torrent:
                    dialog.child_window(
                        auto_id="2027", class_name="Button", control_type=50002
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                if is_default_start_up:
                    dialog.child_window(
                        auto_id="2026", class_name="Button", control_type=50002
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()

                # To click install button
                dialog.child_window(auto_id="2024", control_type=50000).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()

                # To wait for the installation is done
                assert self.wait_for_installation_is_done(
                    language=language, is_upgrade=is_upgraded
                )

                # To close the coccoc window after opening from installation done
                if is_close_after_installed:
                    if is_upgraded:  # after upgrade the window title is 'New tab'
                        self.close_coccoc_after_upgraded()
                    else:
                        self.close_coccoc_at_the_first_time_it_is_opened(
                            language, is_select_always_close_all_tabs
                        )
                else:
                    pass
                return True

            else:  # Stop installing process
                # To close the installation dialog
                dialog.child_window(auto_id="1", control_type=50000).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()

                # To cancel installation (confirm close installing dialog)
                dialog.child_window(auto_id="2", control_type=50000).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()
                return False
        finally:
            if is_delete_file_offscreen_cashback_extension:
                browser_utils.delete_file_offscreen_cashback_extension()
            if is_delete_setup_file_after_installed:
                file_utils.delete_build_by_name(build_name)
            time.sleep(2)

    # ----------------------------------------------------------------------------------------------------------------------
    # To install coccoc then stop network during installation
    def install_interruption_coccoc(self, language=setting.coccoc_language):
        # To disable annoying error Windows fatal exception: code 0x8001010d
        faulthandler.disable()

        # dialog = self.open_coccoc_install_dialog(language)
        dialog = self.open_setup_file()
        dialog.wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
        dialog.child_window(auto_id="2024", control_type=50000).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).click()
        if language == "en":
            dialog.child_window(
                title="Downloading...", control_type="Text", found_index=0
            ).wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.1)
        else:
            dialog.child_window(
                title="Đang tải xuống...", control_type="Text", found_index=0
            ).wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.1)
        try:
            # Block the network
            network_utils.block_network()
            if language == "en":
                assert (
                    dialog.child_window(
                        title="Egads! Download failed. Retrying...",
                        auto_id="2008",
                        control_type="Text",
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        title="Browse the web faster, more securely, more conveniently.",
                        auto_id="2039",
                        control_type="Text",
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        auto_id="2028", control_type="Image"
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        title_re=".*second.*", auto_id="2022", control_type="Text"
                    ).is_visible()
                    is True
                )

                # To Close the installation dialog
                self.close_install_dialog(dialog)
            else:
                assert (
                    dialog.child_window(
                        title="Rất tiếc! Không tải xuống được. Đang thử lại...",
                        auto_id="2008",
                        control_type="Text",
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        title="Lướt web nhanh hơn, an toàn hơn, tiện lợi hơn.",
                        auto_id="2039",
                        control_type="Text",
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        auto_id="2028", control_type="Image"
                    ).is_visible()
                    is True
                )
                assert (
                    dialog.child_window(
                        title_re=".*giây.*", auto_id="2022", control_type="Text"
                    ).is_visible()
                    is True
                )

                # To Close the installation dialog
                self.close_install_dialog(dialog)

        finally:
            network_utils.enable_network()

    # ------------------------------------------------------------------------------------------------------------------
    # @always_wait_until_passes(300, 4)
    def wait_for_installation_is_done(self, language: str, is_upgrade: bool) -> bool:
        """Method wait for the installation is done
        Args:
            language (str): _description_
            is_upgrade (bool): _description_
        Raises:
            ValueError: _description_
        """
        is_done = False
        try:
            if self.is_installing_done(language=language, is_upgrade=is_upgrade):
                is_done = True
            else:
                raise ValueError(
                    "The Coc Coc browse is not opened automatically after installed"
                )
        finally:
            return is_done

    # ------------------------------------------------------------------------------------------------------------------
    # Method to check the UI dialog when start coccoc installer
    def check_ui_of_install_dialog(self, language, version, file_name):
        # To disable annoying error Windows fatal exception: code 0x8001010d
        faulthandler.disable()

        dialog = self.open_coccoc_install_dialog(
            language=language, version=version, file_name=file_name
        )
        try:
            assert dialog.child_window(auto_id="2024", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            )
            # Check image from install dialog
            if int(setting.coccoc_test_version.split(".")[0]) < 105:  # old omaha
                assert dialog.child_window(auto_id="2028", control_type=50006).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                )
            else:  # New omaha
                assert dialog.child_window(auto_id="2035", control_type=50006).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                )
                assert dialog.child_window(auto_id="2036", control_type=50006).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                )

            default_tick_box = dialog.child_window(
                auto_id="2025", control_type=50002
            ).wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            torrent_tick_box = dialog.child_window(
                auto_id="2027", control_type=50002
            ).wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)
            start_up_tick_box = dialog.child_window(
                auto_id="2026", control_type=50002
            ).wait("visible", timeout=setting.timeout_pywinauto, retry_interval=0.5)

            if "vi" in language:
                assert (
                    default_tick_box.window_text()
                    == "Đặt Cốc Cốc làm trình duyệt mặc định"
                )
                assert (
                    torrent_tick_box.window_text()
                    == "Đặt Cốc Cốc làm ứng dụng torrent mặc định"
                )
                assert (
                    start_up_tick_box.window_text()
                    == "Khởi động trình duyệt cùng hệ thống"
                )
            else:
                assert (
                    default_tick_box.window_text()
                    == "Make Cốc Cốc your default browser"
                )
                assert (
                    torrent_tick_box.window_text()
                    == "Make Cốc Cốc your default torrent client"
                )
                assert start_up_tick_box.window_text() == "Run browser on system start"
        finally:
            # To close the installation dialog

            dialog.child_window(auto_id="1", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            dialog.child_window(auto_id="2", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()

    # ----------------------------------------------------------------------------------------------------------------------
    def check_start_up(self, language=setting.coccoc_language):
        coccoc_window = self.open_coccoc(language)
        # coccoc_window.print_control_identifiers()
        if language == "vi":
            address_bar_and_search = (
                coccoc_window["Thẻ mới - Cốc Cốc"]
                .child_window(title="Thanh địa chỉ và tìm kiếm", control_type="Edit")
                .wait("visible", timeout=10)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            title = "Cài đặt - Cốc Cốc"

            default_browser_window = coccoc_window.window(title=title).window(
                title_re="Cài đặt",
                class_name="Chrome_RenderWidgetHostHWND",
                control_type=50030,
            )
            toggle_start_up = default_browser_window.window(
                title_re="Khởi động cùng hệ thống",
                control_type=50000,
                auto_id="control",
            ).wait("visible", timeout=10, retry_interval=1)
            # print(toggle_start_up.get_toggle_state())
            toggle_start_up.click()
            toggle_start_up_after_clicked = default_browser_window.window(
                title_re="Khởi động cùng hệ thống",
                control_type=50000,
                auto_id="control",
            ).wait("visible", timeout=10, retry_interval=1)
            # print(toggle_start_up_after_clicked.get_toggle_state())
        else:
            address_bar_and_search = (
                coccoc_window["New Tab - Cốc Cốc"]
                .child_window(
                    title="Address and execute_search bar", control_type="Edit"
                )
                .wait("visible", timeout=10)
            )
            address_bar_and_search.type_keys("coccoc://settings/defaultBrowser{ENTER}")
            title = "Settings - Cốc Cốc"

            default_browser_window = coccoc_window.window(title=title).window(
                title_re="Settings",
                class_name="Chrome_RenderWidgetHostHWND",
                control_type=50030,
            )
            toggle_start_up = default_browser_window.window(
                title_re="Run automatically on system startup",
                control_type=50000,
                auto_id="control",
            ).wait("visible", timeout=10, retry_interval=1)
            # print(toggle_start_up.get_toggle_state())
            toggle_start_up.click()
            toggle_start_up_after_clicked = default_browser_window.window(
                title_re="Run automatically on system startup",
                control_type=50000,
                auto_id="control",
            ).wait("visible", timeout=10, retry_interval=1)
            # print(toggle_start_up_after_clicked.get_toggle_state())

    # ------------------------------------------------------------------------------------------------------------------
    def check_side_bar(self, language=setting.coccoc_language):
        coccoc_window = self.open_coccoc(language)
        # coccoc_window.print_control_identifiers()
        if language == "vi":
            address_bar_and_search = (
                coccoc_window["Thẻ mới - Cốc Cốc"]
                .child_window(title="Thanh địa chỉ và tìm kiếm", control_type="Edit")
                .wait("visible", timeout=10, retry_interval=1)
            )
            address_bar_and_search.type_keys("coccoc://settings{ENTER}")
            # title = u'Cài đặt - Cốc Cốc'
            # side_bar_screen = coccoc_window.window(title=title).window(title_re='Cài đặt',
            #                                                            class_name='Chrome_RenderWidgetHostHWND',
            #                                                            control_type=50030)
            # side_bar_screen.child_window(auto_id='container', control_type=50026).print_control_identifiers()

            # toggle_show_side_bar = side_bar_screen.window(title_re='Hiển thị thanh bên', control_type=50000,
            #                                               auto_id='control')
            # print(toggle_show_side_bar.get_toggle_state())
            # toggle_show_side_bar.click()

            # side_bar_screen_group = coccoc_window.window(title=title).window(auto_id='container', control_type=50026)
            # side_bar_screen_group.print_control_identifiers()
            # coccoc_window[u'Cài đặt - Cốc Cốc'].print_control_identifiers()
            # tick_box_settings = coccoc_window[u'Cài đặt - Cốc Cốc'].child_window(title="Cốc Cốc", control_type="Pane").child_window(title_re="Cài đặt", control_type=50026, auto_id='control')
            # tick_box_settings.click()
            setting_page = Desktop(backend="uia").Cài_đặt_Cốc_Cốc
            setting_page.print_control_identifiers()
        else:
            address_bar_and_search = (
                coccoc_window["New Tab - Cốc Cốc"]
                .child_window(
                    title="Address and execute_search bar", control_type="Edit"
                )
                .wait("visible", timeout=10, retry_interval=1)
            )
            address_bar_and_search.type_keys("coccoc://settings{ENTER}")
            title = "Settings - Cốc Cốc"
            # side_bar_screen = coccoc_window.window(title=title).window(title_re='Cài đặt',
            #                                                            class_name='Chrome_RenderWidgetHostHWND',
            #                                                            control_type=50030)
            # side_bar_screen.child_window(auto_id='container', control_type=50026).print_control_identifiers()

            # toggle_show_side_bar = side_bar_screen.window(title_re='Hiển thị thanh bên', control_type=50000,
            #                                               auto_id='control')
            # print(toggle_show_side_bar.get_toggle_state())
            # toggle_show_side_bar.click()

            # side_bar_screen_group = coccoc_window.window(title=title).window(auto_id='container', control_type=50026)
            # side_bar_screen_group.print_control_identifiers()
            # coccoc_window[u'Cài đặt - Cốc Cốc'].print_control_identifiers()
            # tick_box_settings = coccoc_window[u'Cài đặt - Cốc Cốc'].child_window(title="Cốc Cốc", control_type="Pane").child_window(title_re="Cài đặt", control_type=50026, auto_id='control')
            # tick_box_settings.click()
            # setting_page = Desktop(backend='uia').Settings_Cốc_Cốc
            # first_screen = setting_page.w
            # setting_page.print_control_identifiers()
            settings_screen = (
                coccoc_window[title]
                .child_window(
                    title_re="Settings",
                    class_name="Chrome_RenderWidgetHostHWND",
                    control_type=50030,
                )
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
            )
            # settings_screen.GroupBox2.Menu.dump_tree()
            settings_screen.GroupBox2.Menu.child_window(
                title="Sidebar", control_type="MenuItem"
            ).dump_tree()
            side_bar = settings_screen.GroupBox2.Menu.child_window(
                title="Sidebar", control_type="MenuItem"
            )
            side_bar.invoke()
            coccoc_window[title]["GroupBox", "SidebarGroupBox"].dump_tree()
            abc = coccoc_window[title]["GroupBox", "SidebarGroupBox"]
            abc.child_window(title="Sidebar", control_type="Text").click()
            # coccoc_window[title]['SidebarGroupBox'].dump_tree()
            # coccoc_window[title]['SidebarGroupBox']['SidebarCheckBox2', 'CheckBox2'].dump_tree()
            # setting_check_box = coccoc_window[title]['SidebarGroupBox']['SidebarCheckBox2', 'CheckBox2']

    # ----------------------------------------------------------------------------------------------------------------------
    # Download setup file from coccoc.com then install
    def install_general_from_site(
        self, language=setting.coccoc_language, source="site"
    ):
        try:
            file_utils.rename_and_copy_file_host()
            download_setup_file.download_coccoc_setup()
            self.install_coccoc_from_coccoc_com(
                language, is_default_browser=False, is_default_start_up=False
            )

        finally:
            file_utils.remove_and_revert_file_host()
            file_utils.delete_installer_downloaded()

    # ----------------------------------------------------------------------------------------------------------------------
    # Download setup file from FTP server then install
    def install_general_from_ftp(
        self,
        language=setting.coccoc_language,
    ):
        try:
            download_setup_file.download_coccoc_setup()
            self.install_coccoc_from_coccoc_com(
                language, is_default_browser=False, is_default_start_up=False
            )

        finally:
            file_utils.delete_installer_downloaded()


installation = InstallationPage()


def test_install_from_file_with_path():
    installation.install_coccoc_from_file_with_path(
        file_name_with_path=rf"C:\Users\{os_utils.get_username()}\Downloads\corom\108.0.5359.100_x64\installers\standalone_108.0.5359.102_machine.exe"
    )
    # installation.open_setup_file()
