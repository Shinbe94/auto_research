import faulthandler
import time
from pywinauto.keyboard import send_keys

from pywinauto import Application, Desktop
from pywinauto.timings import always_wait_until_passes
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from src.pages.constant import CocCocTitles

from src.utilities import browser_utils, os_utils, ftp_connection, string_number_utils
from tests import setting
import logging
from selenium.webdriver.support import expected_conditions as EC

LOGGER = logging.getLogger(__name__)


class BaseWindow:

    """This method is for starting the setup file, return the installing dialog"""

    @staticmethod
    def open_coccoc_install_dialog(language, version, file_name="CocCocSetup.exe"):
        # Start file setup
        try:
            if file_name == "CocCocSetup.exe":
                Application(backend="uia").start(
                    f"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_name}",
                    retry_interval=2,
                    timeout=setting.timeout_pywinauto,
                )
            else:
                Application(backend="uia").start(
                    rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{file_name}",
                    retry_interval=2,
                    timeout=setting.timeout_pywinauto,
                )
        except Exception as e:
            print(e)
        # Connect to coccoc installation dialog
        coccoc_install_dialog = None
        if language == "vi":
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Đang_chạy_Trình_cài_đặt_Cốc_Cốc
            coccoc_install_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            )
            # try:
            # coccoc_install_dialog = Application(backend="uia").connect(
            #     class_name="#32770",
            #     control_type=50033,
            #     title=BaseWindow.INSTALLATION_DIALOG_TITLE_VI,
            #     timeout=setting.time_out_pywinauto, retry_interval=0.5)
            # coccoc_install_dialog[BaseWindow.INSTALLATION_DIALOG_TITLE_VI].print_control_identifiers()
            # except Exception as the_exception:
            #     print(the_exception)
            # finally:
            #     if coccoc_install_dialog is not None:
            #         return coccoc_install_dialog
            # return coccoc_install_dialog[BaseWindow.INSTALLATION_DIALOG_TITLE_VI]
        elif language == "en":
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Initializing_Cốc_Cốc_Installer
            coccoc_install_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            )
        else:
            LOGGER.info("language must be: vi OR en")

        return coccoc_install_dialog

    @staticmethod
    def open_coccoc_install_dialog_by_setup_filename(
        file_name, language=setting.coccoc_language
    ):
        # Start file CocCocSetup.exe
        Application(backend="uia").start(
            f"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_name}"
        )

        # Connect to coccoc installation dialog
        coccoc_install_dialog = None
        if language == "vi":
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Đang_chạy_Trình_cài_đặt_Cốc_Cốc
            coccoc_install_dialog.wait("visible")
        elif language == "en":
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Initializing_Cốc_Cốc_Installer
            coccoc_install_dialog.wait("visible")
        else:
            LOGGER.info("language must be: vi OR en")

        return coccoc_install_dialog

    @staticmethod
    def open_setup_file(file_name="CocCocSetup.exe"):
        # Start file setup
        try:
            Application(backend="uia").start(
                f"C:\\Users\\{os_utils.get_username()}\\Downloads\\{file_name}",
                retry_interval=2,
                timeout=setting.timeout_pywinauto,
            )
        finally:
            return os_utils.connect_to_window_via_pid(process_name="CocCocUpdate.exe")

    @staticmethod
    def open_setup_file_by_its_path(file_name_with_path):
        # Start file setup
        try:
            Application(backend="uia").start(
                file_name_with_path,
                retry_interval=2,
                timeout=setting.timeout_pywinauto,
            )
        finally:
            return os_utils.connect_to_window_via_pid(process_name="CocCocUpdate.exe")

    # dialog is installing dialog
    @staticmethod
    def close_install_dialog(dialog):
        try:
            dialog.child_window(auto_id="1", control_type="Button").wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
            dialog.child_window(auto_id="2", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click()
        finally:
            time.sleep(1)
            pass

    """ Pre-process to get the build name (For download the build from FTP server) 
        @version: Testing version 
        @build_name: 
        @from_build_name: from version
        @to_build_name: to version
        @
    """

    @staticmethod
    def pre_process_setup_filename(
        version, build_name, from_build_name=None, to_build_name=None
    ):
        if build_name == "UPGRADE":
            return "{0}_from_{1}_coccocsetup.exe".format(to_build_name, from_build_name)
        elif build_name == "STANDALONE_VERSION":
            return "standalone_{0}.exe".format(version)
        elif build_name == "STANDALONE_VERSION_MACHINE":
            return "standalone_{0}_machine.exe".format(version)
        elif build_name == "STANDALONE_COCCOC_EN":
            return "standalone_coccoc_en.exe"
        elif build_name == "STANDALONE_COCCOC_VI":
            return "standalone_coccoc_vi.exe"
        elif build_name == "STANDALONE_COCCOC_EN_MACHINE":
            return "standalone_coccoc_en_machine.exe"
        elif build_name == "STANDALONE_COCCOC_VI_MACHINE":
            return "standalone_coccoc_vi_machine.exe"
        else:
            LOGGER.info("Incorrect build_name")

    """ This method is for installing the standalone build coccoc browser! """

    @staticmethod
    def open_coccoc_install_dialog_by_build_name(
        build_name,
        version=setting.coccoc_test_version,
        platform=setting.platform,
        from_build_name=None,
        to_build_name=None,
        is_needed_download=False,
    ):
        build_name = BaseWindow.pre_process_setup_filename(
            version,
            build_name,
            from_build_name=from_build_name,
            to_build_name=to_build_name,
        )
        if is_needed_download:
            ftp_connection.get_file(
                folder_version=version,
                file_to_download_for_test=build_name,
                platform=platform,
            )
        # Start file setup file
        # Application(backend='uia').start(f'C:\\Users\\{os_utils.get_username()}\\Downloads\\{build_name}')

        # Version less than 93 has no build 64 bit
        if int(string_number_utils.substring_before_char(version, ".")) < 93:
            Application(backend="uia").start(
                rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}\installers\{build_name}"
            )
        else:
            Application(backend="uia").start(
                # rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{build_name}"
                rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_real_system_arch()}\installers\{build_name}"
            )

        # Connect to coccoc installation dialog
        coccoc_install_dialog = None
        if "vi" in build_name:
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Đang_chạy_Trình_cài_đặt_Cốc_Cốc
            coccoc_install_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            )
        else:
            coccoc_install_dialog = Desktop(
                backend="uia"
            ).Initializing_Cốc_Cốc_Installer
            coccoc_install_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            )
        return coccoc_install_dialog

    @staticmethod
    def open_coccoc_mini_installer(
        version=setting.coccoc_test_version, is_needed_download=False, platform="64bit"
    ):
        setup_file = version + "_coccocsetup.exe"
        if is_needed_download:
            ftp_connection.get_file(
                folder_version=version,
                file_to_download_for_test=setup_file,
                platform=platform,
            )

        Application(backend="uia").start(
            f"C:\\Users\\{os_utils.get_username()}\\Downloads\\{setup_file}"
        )

    @staticmethod
    def open_coccoc(language="vi"):
        # TODO
        # determine location of installed coccoc then open it.
        # Return the current window for further use
        coccoc = Application(backend="uia")
        coccoc.start(
            r"C:\Program Files\CocCoc\Browser\Application\browser.exe", timeout=20
        )
        # coccoc_window = None
        #
        # if language is 'vi':
        #     coccoc_window = Desktop(backend='uia').Thẻ_mới_Cốc_Cốc
        #     coccoc_window.wait('visible', timeout=20)
        #
        # elif language is 'en':
        #     coccoc_window = Desktop(backend='uia').New_tab_Cốc_Cốc
        #     coccoc_window.wait('visible', timeout=20)

        return coccoc

    """ This method is for waiting the installation is done! """

    # Todo Fix F5 the welcome page if it is not loaded automatically
    @staticmethod
    def is_installing_done(
        language: str = setting.coccoc_language,
        is_upgrade: bool = False,
        timeout: int = setting.timeout_for_installing,
    ) -> bool:
        interval_delay: int = 0.5
        total_delay: int = 0
        coccoc_window: Application = None
        is_installed: bool = False

        try:
            if is_upgrade:  # Check new tab is opened
                title = CocCocTitles.NEW_TAB_TITLE
                if language == "en":
                    coccoc_window = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=title,
                        timeout=setting.timeout_pywinauto,
                    )
                    if (
                        coccoc_window[title]
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        )
                        .is_visible()
                    ):
                        is_installed = True

                elif language == "vi":
                    coccoc_window = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=title,
                        timeout=setting.timeout_pywinauto,
                    )
                    if (
                        coccoc_window[title]
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        )
                        .is_visible()
                    ):
                        is_installed = True
            else:
                title = CocCocTitles.WELCOME_PAGE_TITLE
                if "en" in language:
                    # send_keys("{F5}")
                    # Verify welcome tab

                    while total_delay < timeout:
                        try:
                            coccoc_window = Application(backend="uia").connect(
                                class_name="Chrome_WidgetWin_1",
                                control_type=50033,
                                title=title,
                                timeout=0.5,
                            )
                            if coccoc_window.window().exists():
                                # if coccoc_window is not None:
                                # coccoc_window[title].print_control_identifiers()
                                is_installed = True
                                break
                            else:
                                time.sleep(interval_delay)
                                # send_keys("{F5}")
                                total_delay += interval_delay
                            if total_delay > timeout:
                                raise ValueError(
                                    f"Timeout after {total_delay} seconds for installing CocCoc"
                                )
                        except Exception:
                            pass
                    # Check some ui text
                    if browser_utils.get_coccoc_major_build() >= 113:
                        assert (
                            coccoc_window[title]
                            .child_window(
                                title="Let's get your browser ready",
                                control_type="Text",
                            )
                            .exists(timeout=5, retry_interval=0.5)
                        )

                        assert (
                            coccoc_window[title]
                            .child_window(
                                title="Import your data and try Cốc Cốc features in just a few seconds",
                                control_type="Text",
                            )
                            .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                        )
                        assert (
                            coccoc_window[title]
                            .child_window(title="Let's go", control_type="Text")
                            .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                        )
                    else:
                        btn_discover = (
                            coccoc_window[title]
                            .child_window(title="Discover now", control_type=50000)
                            .wait("visible", timeout=setting.timeout_pywinauto)
                        )
                        assert btn_discover

                elif language == "vi":
                    # send_keys("{F5}")
                    # Verify welcome tab
                    while total_delay < timeout:
                        try:
                            coccoc_window = Application(backend="uia").connect(
                                class_name="Chrome_WidgetWin_1",
                                control_type=50033,
                                title=title,
                            )
                            if coccoc_window.window().exists():
                                # coccoc_window[title].print_control_identifiers()
                                is_installed = True
                                break
                            else:
                                time.sleep(interval_delay)
                                # send_keys("{F5}")
                                total_delay += interval_delay
                            if total_delay > timeout:
                                raise ValueError(
                                    f"Timeout after {total_delay} seconds for installing CocCoc"
                                )
                        except Exception:
                            pass
                    # Check some ui text
                    if browser_utils.get_coccoc_major_build() >= 113:
                        assert (
                            coccoc_window[title]
                            .child_window(
                                title="Chuẩn bị cho trình duyệt của bạn",
                                control_type="Text",
                            )
                            .exists(timeout=5, retry_interval=1)
                        )

                        assert (
                            coccoc_window[title]
                            .child_window(
                                title="Dành vài giây nhập dữ liệu và trải nghiệm các tính năng nhé",
                                control_type="Text",
                            )
                            .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                        )
                        assert (
                            coccoc_window[title]
                            .child_window(title="Bắt đầu", control_type="Text")
                            .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                        )
                    else:
                        btn_discover = (
                            coccoc_window[title]
                            .child_window(title="Khám phá ngay", control_type=50000)
                            .wait("visible", timeout=setting.timeout_pywinauto)
                        )
                        assert btn_discover
        finally:
            return is_installed

    """ This is for checking the Welcome tab and New tab after installing the coccoc browser is done! """

    @staticmethod
    def check_coccoc_at_the_first_time_it_run(
        language=setting.coccoc_language, is_close_coccoc=True
    ):
        faulthandler.disable()
        if "en" in language:
            coccoc_window = None
            title = CocCocTitles.WELCOME_PAGE_TITLE
            try:
                coccoc_window = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=50033,
                    title_re=title,
                    timeout=setting.timeout_pywinauto,
                )
                # coccoc_window[title].print_control_identifiers()
                # Verify welcome tab
                if browser_utils.get_coccoc_major_build() >= 113:
                    # assert (
                    #     coccoc_window[title]
                    #     .child_window(
                    #         title="Let's get your browser ready",
                    #         control_type="Text",
                    #     )
                    #     .exists(timeout=setting.time_out_pywinauto, retry_interval=1)
                    # ) is True

                    # assert (
                    #     coccoc_window[title]
                    #     .child_window(
                    #         title="Import your data and try Cốc Cốc features in just a few seconds",
                    #         control_type="Text",
                    #     )
                    #     .exists(timeout=setting.time_out_pywinauto, retry_interval=1)
                    # )
                    # assert (
                    #     coccoc_window[title]
                    #     .child_window(title="Let's go", control_type="Text")
                    #     .exists(timeout=setting.time_out_pywinauto, retry_interval=1)
                    # )
                    pass
                else:
                    welcome_coccoc_tab = coccoc_window[title].wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    )
                    btn_discover = (
                        coccoc_window[title]
                        .child_window(title="Discover now", control_type=50000)
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=1,
                        )
                    )
                    assert welcome_coccoc_tab
                    assert btn_discover
                # Check skip newtab
                if int(setting.coccoc_test_version.split(".")[0]) < 103:
                    # Verify New tab
                    new_tab = (
                        coccoc_window[title]
                        .child_window(title="New Tab", control_type="TabItem")
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=1,
                        )
                    )
                    assert new_tab
                    new_tab_btn = (
                        coccoc_window[title]
                        .child_window(title="New Tab", control_type="TabItem")
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=1,
                        )
                    )
                    new_tab_btn.click_input()
                    search_box = (
                        coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                        .child_window(
                            auto_id="search-string",
                            title="Search with Cốc Cốc",
                            control_type=50004,
                        )
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=1,
                        )
                    )
                    assert search_box
                else:
                    pass
            finally:
                # To close the coccoc if any
                if is_close_coccoc:
                    if int(setting.coccoc_test_version.split(".")[0]) < 103:
                        coccoc_window[CocCocTitles.NEW_TAB_TITLE].close()
                        if (
                            coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                            .child_window(title="Yes", control_type=50000)
                            .wait(
                                "visible",
                                timeout=setting.timeout_pywinauto,
                                retry_interval=1,
                            )
                            .is_visible()
                        ):
                            coccoc_window[CocCocTitles.NEW_TAB_TITLE].child_window(
                                title="Yes", control_type=50000
                            ).wait(
                                "visible",
                                timeout=setting.timeout_pywinauto,
                                retry_interval=1,
                            ).click()
                    else:
                        coccoc_window[CocCocTitles.WELCOME_PAGE_TITLE].close()
        elif language == "vi":
            coccoc_window = None
            try:
                coccoc_window = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=50033,
                    title_re=title,
                    timeout=setting.timeout_pywinauto,
                    retry_interval=1,
                )

                # coccoc_window[title].print_control_identifiers()
                # Verify welcome tab
                if browser_utils.get_coccoc_major_build() >= 113:
                    assert (
                        coccoc_window[title]
                        .child_window(
                            title="Chuẩn bị cho trình duyệt của bạn",
                            control_type="Text",
                        )
                        .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                    ) is True

                    assert (
                        coccoc_window[title]
                        .child_window(
                            title="Dành vài giây nhập dữ liệu và trải nghiệm các tính năng nhé",
                            control_type="Text",
                        )
                        .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                    )
                    assert (
                        coccoc_window[title]
                        .child_window(title="Bắt đầu", control_type="Text")
                        .exists(timeout=setting.timeout_pywinauto, retry_interval=1)
                    )
                else:
                    welcome_coccoc_tab = coccoc_window[title].wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    )
                    btn_discover = (
                        coccoc_window[title]
                        .child_window(title="Khám phá ngay", control_type=50000)
                        .wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=1,
                        )
                    )
                    assert welcome_coccoc_tab
                    assert btn_discover
                # Check skip newtab
                if int(setting.coccoc_test_version.split(".")[0]) < 103:
                    # Verify New tab
                    new_tab = (
                        coccoc_window[title]
                        .child_window(title="Thẻ mới", control_type="TabItem")
                        .wait("visible", timeout=setting.timeout_pywinauto)
                    )
                    assert new_tab
                    new_tab_btn = (
                        coccoc_window[title]
                        .child_window(title="Thẻ mới", control_type="TabItem")
                        .wait("visible", timeout=setting.timeout_pywinauto)
                    )
                    new_tab_btn.click_input()
                    search_box = (
                        coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                        .child_window(
                            auto_id="search-string",
                            title="Tìm kiếm với Cốc Cốc",
                            control_type=50004,
                        )
                        .wait("visible", timeout=setting.timeout_pywinauto)
                    )
                    assert search_box
                else:
                    pass
            finally:
                # To close the coccoc if any
                if is_close_coccoc:
                    if int(setting.coccoc_test_version.split(".")[0]) < 103:
                        coccoc_window[CocCocTitles.NEW_TAB_TITLE].close()
                        if (
                            coccoc_window[CocCocTitles.NEW_TAB_TITLE]
                            .child_window(title="Có", control_type=50000)
                            .wait("visible", timeout=setting.timeout_pywinauto)
                            .is_visible()
                        ):
                            coccoc_window[CocCocTitles.NEW_TAB_TITLE].child_window(
                                title="Có", control_type=50000
                            ).wait("visible", timeout=setting.timeout_pywinauto).click()
                    else:
                        coccoc_window[CocCocTitles.WELCOME_PAGE_TITLE].close()

    """ this method is for connecting and close the coccoc after the installation is done! """

    @staticmethod
    # @always_wait_until_passes(420, 1)
    def close_coccoc_at_the_first_time_it_is_opened(
        language=setting.coccoc_language, is_select_always_close_all_tabs=True
    ):
        title = CocCocTitles.WELCOME_PAGE_TITLE
        if language == "en":
            # send_keys("{F5}")
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_for_installing,
            )
            app[title].close()
            time.sleep(1)
            if app[title].exists():
                if (
                    app[title]
                    .child_window(title="Yes", control_type=50000)
                    .wait("visible", timeout=5)
                    .is_visible()
                ):
                    if is_select_always_close_all_tabs:
                        app[title].child_window(
                            title="Always close all tabs", control_type=50002
                        ).wait("visible", timeout=5).click()
                    app[title].child_window(title="Yes", control_type=50000).wait(
                        "visible", timeout=5
                    ).click()
                else:
                    return True
            else:
                return True
        else:
            if browser_utils.get_coccoc_major_build() >= 100:
                title = "Bắt đầu với Trình duyệt Cốc Cốc - Cốc Cốc"
            # send_keys("{F5}")
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_for_installing,
            )
            app[title].close()
            time.sleep(1)
            if app[title].exists():
                if (
                    app[title]
                    .child_window(title="Có", control_type=50000)
                    .wait("visible", timeout=10)
                    .is_visible()
                ):
                    if is_select_always_close_all_tabs:
                        app[title].child_window(
                            title="Luôn đóng tất cả các thẻ", control_type=50002
                        ).wait("visible", timeout=10).click()
                    app[title].child_window(title="Có", control_type=50000).wait(
                        "visible", timeout=10
                    ).click()
                else:
                    return True
            else:
                return True
        time.sleep(2)

    """ For closing the Coccoc Window after override install! """

    @staticmethod
    @always_wait_until_passes(120, 1)
    def close_coccoc_after_upgraded(language=setting.coccoc_language):
        title = CocCocTitles.NEW_TAB_TITLE
        if language == "en":
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            app[title].close()
            # time.sleep(1)
            # if app[title].child_window(title='Yes', control_type=50000).wait('visible',
            #                                                                  timeout=2).is_visible():
            #     app[title].child_window(title='Yes', control_type=50000).wait('visible').click()
        else:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            app[title].close()
            # time.sleep(1)
            # if app[title].child_window(title='Có', control_type=50000).wait('visible',
            #                                                                 timeout=2).is_visible():
            #     app[title].child_window(title='Có', control_type=50000).wait('visible').click()

    @staticmethod
    def close_coccoc_by_window_title(title, language=setting.coccoc_language):
        try:
            if language == "en":
                app = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=50033,
                    title_re=title,
                    timeout=setting.timeout_pywinauto,
                )
                app[title].close()
                time.sleep(1)
                if app[title].exists():
                    if (
                        app[title]
                        .child_window(title="Yes", control_type=50000)
                        .wait("visible", timeout=10)
                        .is_visible()
                    ):
                        app[title].child_window(title="Yes", control_type=50000).wait(
                            "visible", timeout=10
                        ).click()
                    else:
                        pass
                else:
                    pass
            else:
                app = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=50033,
                    title_re=title,
                    timeout=setting.timeout_pywinauto,
                )
                app[title].close()
                time.sleep(1)
                if app[title].exists():
                    if (
                        app[title]
                        .child_window(title="Có", control_type=50000)
                        .wait("visible", timeout=10)
                        .is_visible()
                    ):
                        app[title].child_window(title="Có", control_type=50000).wait(
                            "visible", timeout=10
                        ).click()
                    else:
                        pass
                else:
                    pass
        except Exception as the_exception:
            print(the_exception)


class BrowserBasePage:
    def __init__(self, driver, app, current_coccoc_language, title):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=30, poll_frequency=0.5)
        self.app = app
        self.current_coccoc_language = current_coccoc_language
        self.title = title

    def close_coccoc_by_window_title(self, title, language=setting.coccoc_language):
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).close()
        except Exception as the_exception:
            print(the_exception)

    # To check is there any video ads appear after some seconds
    def is_pip_ads_appeared(self, language=setting.coccoc_language):
        is_appeared = False
        while not is_appeared:
            if language == "en":
                title_re = "Automatically close after"
                try:
                    self.app = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=title_re,
                        timeout=10,
                    )
                    # self.app[title_re].wait('visible', timeout=setting.time_out_pywinauto, retry_interval=0.5).close()
                    if self.app:
                        is_appeared = True
                except:
                    pass
                finally:
                    break
            else:
                title_re = "Tự động đóng sau"
                try:
                    self.app = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=title_re,
                        timeout=10,
                    )
                    # self.app[title_re].wait('visible', timeout=setting.time_out_pywinauto, retry_interval=0.5).close()
                    if self.app:
                        is_appeared = True
                except:
                    pass
                finally:
                    break
                # if self.app[title_re].child_window(title=title_re, class_name="Chrome_WidgetWin_1",
                #                                 control_type=50033).wait('visible', timeout=15).is_visible():
                #     is_appeared = True
        return is_appeared

    def close_ads_window(self):
        list_windows = self.driver.window_handles
        print("Number of windows: " + str(len(list_windows)))
        print(list_windows)
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            print("ads title is: " + self.driver.title)
            if ("Automatically close after" in self.driver.title) or (
                "Tự động đóng sau" in self.driver.title
            ):
                self.driver.close()
                break
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            print("ads title is: " + self.driver.title)

    def get_current_coccoc_language(self):
        return self.current_coccoc_language

    def get_current_window_title(self):
        return self.title

    def get_driver(self):
        return self.driver

    def get_page_title(self):
        return self.driver.title

    def get_url(self, url, is_wait_for_loaded=True):
        self.driver.get(url)
        if is_wait_for_loaded:
            self.wait_for_page_loaded_completely()

    def reload_page(self):
        self.driver.refresh()

    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    # Click element by its relative (from selenium v4 and onward)
    # def click_element_by_its_relative(self, by_locator, tag, relation_type):
    #     ele = self.get_element(by_locator)
    #     match relation_type:
    #         case 'above':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).above(ele))
    #             self.click(target_ele)
    #         case 'below':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).below(ele))
    #             self.click(target_ele)
    #         case 'to_left_of':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).to_left_of(ele))
    #             self.click(target_ele)
    #         case 'to_right_of':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).to_right_of(ele))
    #             self.click(target_ele)
    #         case 'near':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).near(ele))
    #             self.click(target_ele)
    #         case _:
    #             raise Exception(f'Value of relation_type {relation_type} must be in (above, below, to_left_of, '
    #                             f'to_right_of, near )')

    def click_by_js(self, by_locator):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].click();", ele)

    def click_element_by_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_dummy_ele(self):
        action = ActionChains(self.driver)
        action.move_by_offset(0, 0).click()
        action.perform()

    def send_keys(self, by_locator, value):
        # self.wait.until(EC.element_to_be_clickable(by_locator)).send_keys(value)
        # ele = self.wait.until(EC.presence_of_element_located(by_locator))
        # self.wait.until(EC.presence_of_element_located(by_locator)).clear()
        # self.wait.until(EC.presence_of_element_located(by_locator)).send_keys(value)

        self.wait.until(EC.element_to_be_clickable(by_locator)).clear()
        self.wait.until(EC.element_to_be_clickable(by_locator)).fill_texts(value)

    def send_keys_by_js(self, by_locator, text):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].value='" + text + "';", ele)

    def get_text(self, by_locator):
        return self.wait.until(
            EC.visibility_of_element_located(by_locator)
        ).get_attribute("innerText")

    def get_element(self, by_locator):
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def get_ele(self, by_locator):
        self.wait.until(EC.presence_of_element_located(by_locator))
        return self.driver.find_element(*by_locator)

    def get_elements(self, by_locator):
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def get_value_of_element_attribute(self, by_locator, attribute_name):
        return self.wait.until(
            EC.presence_of_element_located(by_locator)
        ).get_attribute(attribute_name)

    def get_value_of_ele_attribute(self, ele, attribute_name):
        return ele.get_attribute(attribute_name)

    def get_element_by_variable(self, first_string, last_string, value):
        element = first_string + value + last_string
        return self.wait.until(EC.presence_of_element_located(element))

    def clear_text(self, by_locator):
        # ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.wait.until(EC.presence_of_element_located(by_locator)).fill_texts(
            Keys.CONTROL, "a", Keys.DELETE
        )
        # self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        # self.wait.until(EC.presence_of_element_located(by_locator)).clear()

    def wait_for_element_presented(self, by_locator):
        self.wait.until(EC.visibility_of_element_located(by_locator))

    def get_count(self, by_locator):
        return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))

    def get_count2(self, by_locator):
        return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))

    def select_by_text(self, by_locator, option):
        select = Select(self.get_element(by_locator))
        select.select_by_visible_text(option)

    def select_dropdown_element(self):
        Select(self.get_element())

    def drag_and_drop(self, source_element, target_element):
        action = ActionChains(self.driver)
        # action.drag_and_drop(self.get_element(source_element), self.get_element(target_element)).perform()
        action.click_and_hold(self.get_element(source_element)).pause(
            2
        ).move_to_element(self.get_element(target_element)).perform()

    def hover_on_element(self, by_locator, is_click_before_hover=False):
        self.wait.until(EC.presence_of_element_located(by_locator))
        # element = self.driver.find_element(*by_locator)
        element = self.get_element(by_locator)
        action = ActionChains(self.driver)
        # action.move_to_element(element).perform()
        if is_click_before_hover:
            action.click(element).perform()
        action.move_to_element(element)
        action.perform()
        time.sleep(1)
        # print('element hovered')

    def hover_and_hold_element(self, by_locator):
        self.wait.until(EC.presence_of_element_located(by_locator))
        # element = self.driver.find_element(*by_locator)
        element = self.get_element(by_locator)
        action = ActionChains(self.driver)
        # action.move_to_element(element).perform()
        action.click_and_hold(element)
        action.perform()
        time.sleep(2)
        action.release(element).perform()

    def hover_on_element_by_class_name_js(self, by):
        self.driver.execute_script(f"document.getElementsByClassName('{by}').focus()")

    def scroll_to_element(self, by_locator):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)

    def execute_js(self, script):
        self.driver.execute_script(script)

    def switch_to(self, frame):
        self.driver.switch_to.frame(frame)

    def switch_to_frame(self, by_locator):
        # Store iframe web element
        iframe = self.get_element(by_locator)
        # switch to selected iframe
        self.switch_to(iframe)
        # return self.driver

    def leave_frame(self):
        self.driver.switch_to.default_content()

    # def take_screen_shot(self):
    #     allure.attach(self, name="error", attachment_type=allure.attachment_type.PNG)

    def assert_visible(self, by_locator):
        try:
            return self.get_element(by_locator)
        except NoSuchElementException:
            return False

    def is_element_exist(self, by_locator, timeout=0.1):
        self.driver.implicitly_wait(timeout)
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_exist(self, by_locator, timeout):
        wait = WebDriverWait(self.driver, timeout)
        is_exist = False
        while not is_exist:
            try:
                wait.until(
                    EC.visibility_of_element_located(self.get_element(by_locator))
                )
                is_exist = True
                break
            except:
                pass
        return is_exist

    def wait_for_element_disappear(self, by_locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        is_disappear = False
        while not is_disappear:
            try:
                wait.until(EC.invisibility_of_element_located(by_locator))
                is_disappear = True
                break
            except:
                pass
        return is_disappear

    def wait_for_element_disappear2(self, by_locator, short_time=1, long_time=5):
        # self.driver.implicitly_wait(timeout)
        # wait = WebDriverWait(self.driver, short_time)
        try:
            # Wait for element present
            WebDriverWait(self.driver, short_time).until(
                EC.presence_of_element_located(by_locator)
            )
            # Wait for element disappear
            WebDriverWait(self.driver, long_time).until_not(
                EC.presence_of_element_located(by_locator)
            )
            # return True
        except TimeoutException:
            pass
            # return False

    def wait_for_page_loaded_completely(self):
        WebDriverWait(self.driver, setting.timeout_selenium).until(
            lambda wd: self.driver.execute_script("return document.readyState")
            == "complete",
            "Page taking too long to load",
        )
        # print('The page is loaded completely')

    # To get the WebElement from Shadow Element by jsPath
    def get_shadow_element(self, js_path):
        element = None
        max_delay = 5
        interval_delay = 0.5
        total_delay = 0
        is_loaded = False
        while not is_loaded:
            try:
                element = self.driver.execute_script(f"return {js_path};")
                if element is not None:
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    print(f"Timeout for getting element by: {js_path}")
                    break
            except Exception as e:
                print(e)
            finally:
                break
        return element

    # To click the shadow element
    def click_shadow_element_by_js_path(self, js_path):
        ele = self.get_shadow_element(js_path)
        try:
            ele.click()
        except Exception as e:
            print(e)

    def hover_on_element_by_query_selector(self, query_selector):
        scripts = (
            """
         // Targeting video element 
        let clip = document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """)

        clip.addEventListener("mouseover", function () {
            setTimeout(function() {}, 1000);
        })
        /*
        clip.addEventListener("mouseover", function (e) {
            console.log('Event triggered');
        })
        */
        """
        )
        self.execute_js(scripts)

    def hover_on_element_by_query_selector2(self, query_selector):
        scripts = (
            """
        var event = new MouseEvent('mouseover', {
          'view': window,
          'bubbles': true,
          'cancelable': true
        });
        //var element = document.getElementById('name');
        var element = document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """)
        element.addEventListener('mouseover', function() {
          console.log('Event triggered');
        });
        element.dispatchEvent(event);
        """
        )
        self.execute_js(scripts)

    def hover_mouse_center(self, query_selector):
        scripts = (
            """
        document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """).dispatchEvent(new MouseEvent('mouseenter', { 'view': window, 'bubbles': true, 'cancelable': true }));
        """
        )
        self.execute_js(scripts)

    """
        THIS PART IS FOR PYWINAUTO
    """

    def get_shadow_element_by_js(self, js_path):
        element = None
        try:
            element = self.driver.execute_script(f"return {js_path};")
        except Exception as e:
            print(e)
        return element

    def get_shadow_element2(self, js_path):
        timeout = time.time() + 30  # 30 seconds from now
        while True:
            try:
                element = self.driver.execute_script(f"return {js_path};")
                if element or (time.time() > timeout):
                    break
            except Exception as e:
                print(e)
        return element

    # To click the shadow element
    def click_shadow_element(self, js_path):
        ele = self.get_shadow_element(js_path)
        ele.click()

    # To get the attribute's value by shadow element
    def get_attribute_value_by_element(self, ele, attribute_name):
        attribute_value = ele.get_attribute(attribute_name)
        return attribute_value

    # To get the attribute's value by jsPath
    def get_attribute_value_by_js_path(self, js_path, attribute_name):
        ele = self.get_shadow_element(js_path)
        attribute_value = ele.get_attribute(attribute_name)
        return attribute_value

    # def get_element(self, by_locator):
    #     wait = WebDriverWait(self.driver, setting.implicit_wait)
    #     return wait.until(EC.presence_of_element_located(by_locator))

    # def get_text_from_element_by_inner_text(self, by_locator):
    #     return self.get_element(by_locator).get_attribute('innerText')

    # def get_text_from_element_by_inner_text_js_path(driver, js_path):
    #     # wait = WebDriverWait(driver, setting.implicit_wait)
    #     # ele = get_shadow_element(driver, js_path)
    #     # wait.until(EC.visibility_of(get_shadow_element(driver, js_path)))
    #     # return ele.get_attribute('innerText')
    #     # return wait.until(driver.execute_script(f'return {js_path};')).get_attribute('innerText')
    #     ele = WebDriverWait(driver, 30, 3, ignored_exceptions=JavascriptException).until(
    #         lambda lambda_driver: lambda_driver.execute_script(f'''return {js_path};'''))
    #
    #     return ele.get_attribute('innerText')

    # def get_text_from_element(self, by_locator):
    #     return self.get_element(by_locator).text
    #
    # def scroll_to_element(driver, by_locator):
    #     ele = get_element(driver, by_locator)
    #     driver.execute_script("arguments[0].scrollIntoView(true);", ele)

    def scroll_to_element_by_js_path(self, js_path):
        ele = self.get_shadow_element(js_path)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)

    # def wait_for_element_presented(driver, by_locator):
    #     wait = WebDriverWait(driver, setting.implicit_wait)
    #     wait.until(EC.visibility_of_element_located(by_locator))

    def wait_for_element_presented_by_js_path(self, js_path):
        wait = WebDriverWait(self.driver, setting.implicit_wait)
        wait.until(EC.visibility_of(self.get_shadow_element(js_path)))

    def wait_for_text_present_by_js_path(self, js_path, text):
        is_text_presented = True
        while is_text_presented:
            # wait = WebDriverWait(driver, setting.implicit_wait)
            element = self.get_shadow_element(js_path)
            if element.text == text:
                is_text_presented = False
            else:
                is_text_presented = True
