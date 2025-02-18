import faulthandler
import json
import os
import shutil
import subprocess
import time, random

import logging
from pywinauto import Desktop, Application

from src.pages.coccoc_common import open_browser
from src.pages.installations import first_time_run, base_window
from src.utilities import (
    file_utils,
    os_utils,
    browser_utils,
    ftp_connection,
    string_number_utils,
)
from tests import setting

LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------------------------
def uninstall_coccoc_silently_system_mode():
    version = get_coccoc_version_folder_name_system_mode()
    # print(version)
    # LOGGER.info("Uninstall silently CocCoc system mode, version is: " + version)
    if get_coccoc_installation_location()[1] == "64bit":
        cd_to_installer_folder = f"cd C:\\Program Files\\CocCoc\\Browser\\Application\\{version}\\Installer\\ &&"
        run_uninstaller = "setup.exe --uninstall --multi-install --chrome --system-level --force-uninstall"
        os.system(cd_to_installer_folder + run_uninstaller)
    else:
        cd_to_installer_folder = f"cd C:\\Program Files (x86)\\CocCoc\\Browser\\Application\\{version}\\Installer\\ &&"
        run_uninstaller = "setup.exe --uninstall --multi-install --chrome --system-level --force-uninstall"
        os.system(cd_to_installer_folder + run_uninstaller)

    time.sleep(5)
    # LOGGER.info(f"CocCoc System mode version {version} is uninstalled")


def remove_all_coccoc_data():
    browser_utils.kill_all_coccoc_process()
    remove_coccoc_app_data()


def test_uninstall():
    # uninstall_coccoc_silently_system_mode()
    uninstall_coccoc_silently()


# """To uninstall coccoc via command line"""
# ------------------------------------------------------------------------------------------------------------------
def uninstall_coccoc_silently(is_removed_coccoc_data=True):
    # Close all coccoc process before uninstalling
    browser_utils.kill_all_coccoc_process()
    is_need_delete_registry: bool = False

    # Execute uninstall
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        try:
            subprocess.check_call(
                f'"C:\Program Files\\CocCoc\\Browser\\Application\\{browser_utils.get_coccoc_version_folder_name_system_mode()}\\Installer\\setup.exe" --uninstall --multi-install --chrome --msi --system-level --force-uninstall'
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        try:
            subprocess.check_call(
                f'"C:\\Program Files (x86)\\CocCoc\\Browser\\Application\\{browser_utils.get_coccoc_version_folder_name_system_mode()}\\Installer\\setup.exe" --uninstall --multi-install --chrome --msi --system-level --force-uninstall'
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
    else:
        is_need_delete_registry = True
        # print("No CocCoc is installed, trying to clear user data if any")

    # Clear user data
    if is_removed_coccoc_data:
        browser_utils.kill_all_coccoc_process()
        remove_coccoc_app_data(is_need_delete_registry)
    time.sleep(1)


# ------------------------------------------------------------------------------------------------------------------
# Get version folder of coccoc (first folder under Application folder)
def get_coccoc_version_folder_name_system_mode():
    coccoc_install_location = get_coccoc_installation_location()[0]
    folder_names = []
    for entry_name in os.listdir(coccoc_install_location):
        entry_path = os.path.join(coccoc_install_location, entry_name)
        if os.path.isdir(entry_path):
            folder_names.append(entry_name)
    return str(folder_names[0])


# ------------------------------------------------------------------------------------------------------------------
"""To get the place where coccoc is installed"""


def get_coccoc_installation_location():
    if os.path.isdir(r"C:\\Program Files\\CocCoc\\Browser\\Application"):
        return r"C:\\Program Files\\CocCoc\\Browser\\Application", "64bit"
    elif os.path.isdir(r"C:\\Program Files (x86)\\CocCoc\\Browser\\Application"):
        return r"C:\\Program Files (x86)\\CocCoc\\Browser\\Application", "32bit"
    else:
        return False


# ------------------------------------------------------------------------------------------------------------------
"""To remove coccoc data and its registry"""


def test_remove_coccoc_app_data():
    remove_coccoc_app_data()


def remove_coccoc_app_data(
    is_delete_task_update_schedule=False, is_need_delete_registry=False
):
    # from src.utilities.file_utils import check_folder_is_exists
    # from src.utilities.os_utils import get_username
    local_app_data_path = (
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc"
    )
    app_data_path = f"C:\\Users\\{os_utils.get_username()}\\AppData\\Roaming\\CocCoc"
    program_files_coccoc_application = f"C:\\Program Files\\CocCoc\\Application"
    program_files_coccoc = f"C:\\Program Files\\CocCoc"
    program_files_x86_coccoc_application = (
        f"C:\\Program Files (x86)\\CocCoc\\Application"
    )
    program_files_x86_coccoc = f"C:\\Program Files (x86)\\CocCoc\\"

    # Remove coccoc folder
    if file_utils.check_folder_is_exists(program_files_coccoc_application):
        os.chmod(program_files_coccoc, 0o777)
        shutil.rmtree(program_files_coccoc, ignore_errors=False)
        time.sleep(1)
    if file_utils.check_folder_is_exists(program_files_x86_coccoc_application):
        os.chmod(program_files_x86_coccoc, 0o777)
        shutil.rmtree(program_files_x86_coccoc, ignore_errors=False)
        time.sleep(1)
    if file_utils.check_folder_is_exists(program_files_coccoc):
        os.chmod(program_files_coccoc, 0o777)
        shutil.rmtree(program_files_coccoc, ignore_errors=False)
        time.sleep(1)
    if file_utils.check_folder_is_exists(program_files_x86_coccoc):
        os.chmod(program_files_x86_coccoc, 0o777)
        shutil.rmtree(program_files_x86_coccoc, ignore_errors=False)
        time.sleep(1)
    # REMOVE APPDATA
    if file_utils.check_folder_is_exists(local_app_data_path):
        os.chmod(local_app_data_path, 0o777)
        shutil.rmtree(local_app_data_path, ignore_errors=True)
        time.sleep(1)
    if file_utils.check_folder_is_exists(app_data_path):
        os.chmod(app_data_path, 0o777)
        shutil.rmtree(app_data_path, ignore_errors=False)
        time.sleep(1)

    if is_need_delete_registry:
        remove_coccoc_registry_current_user = (
            "reg delete HKEY_CURRENT_USER\\Software\\CocCoc /f"
        )
        os.system(remove_coccoc_registry_current_user)
        remove_coccoc_registry_local_machine = (
            "reg delete HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\CocCoc /f"
        )
        os.system(remove_coccoc_registry_local_machine)

    # Delete all coccoc task update schedule if any
    if is_delete_task_update_schedule and is_need_delete_registry:
        os_utils.delete_all_coccoc_update_task_schedule()

    # Delete all coccoc update services
    os_utils.delete_all_coccoc_update_services()

    time.sleep(1)


def test_cancel_uninstall_coccoc():
    cancel_uninstall_coccoc()


# ------------------------------------------------------------------------------------------------------------------
"""This method is for testing canceling the uninstall dialog"""


def cancel_uninstall_coccoc(language=setting.coccoc_language):
    # To disable annoying error Windows fatal exception: code 0x8001010d
    faulthandler.disable()

    # To kill all coccoc process is running
    browser_utils.kill_all_coccoc_process()

    # To start program and features
    os.system("appwiz.cpl")

    # To get the current Windows version
    windows_version = os_utils.get_windows_version()

    # Set some needed variable
    program_features = None
    title = None

    # To set the title for each Windows version
    if windows_version == "10":
        title = r"Control Panel\Programs\Programs and Features"
    elif windows_version in ("11", "8", "8.1", "7"):
        title = "Programs and Features"
    try:
        # program_features = Desktop(backend='uia').Control_Panel_Programs_Programs_and_Features
        program_features = Application(backend="uia").connect(
            title_re=".*Programs and Features",
            class_name="CabinetWClass",
            control_type=50032,
            timeout=10,
        )

        program_features[title].child_window(title="Cốc Cốc", control_type=50004).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).click_input(button="left", double=True)
        # time.sleep(2)
        program_features[title].maximize()
        program_features[title].set_focus()

        if language == "en":
            # uninstall_dialog = Desktop(backend='uia').Uninstall_Cốc_Cốc
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            # Hover and check the text
            uninstall_dialog.child_window(
                control_type=50000, title="I'll stay with Cốc Cốc"
            ).set_focus().click_input(button="right", double=True)
            # uninstall_dialog.child_window(control_type=50000, title="I'll stay with Cốc Cốc").click()
            time.sleep(2)
            text = uninstall_dialog.child_window(
                control_type=50020, title="Thank you! you're wonderful!"
            ).window_text()
            assert text == "Thank you! you're wonderful!"
            # To click "I'll stay with Cốc Cốc" and check the uninstall dialog is disappeared
            uninstall_dialog.child_window(
                control_type=50000, title="I'll stay with Cốc Cốc"
            ).click_input(button="left")
            assert uninstall_dialog.exists(timeout=2) is False
        elif language == "vi":
            # uninstall_dialog = Desktop(backend='uia').Gỡ_bỏ_cài_đặt_Cốc_Cốc
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            uninstall_dialog.wait("visible", timeout=setting.timeout_pywinauto)
            # Hover and check the text
            uninstall_dialog.child_window(
                control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
            ).set_focus().click_input(button="right", double=True)
            time.sleep(2)
            text = uninstall_dialog.child_window(
                control_type=50020, title="Cám ơn bạn! bạn thật tuyệt!"
            ).window_text()
            assert text == "Cám ơn bạn! bạn thật tuyệt!"
            # To click "I'll stay with Cốc Cốc" and check the uninstall dialog is disappeared
            uninstall_dialog.child_window(
                control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
            ).click_input(button="left")
            assert uninstall_dialog.exists(timeout=2) is False
        else:
            LOGGER.info("language must be: en or vi")
    finally:
        """To Close Program Files and Features"""
        program_features[title].close()
        faulthandler.enable()


# ------------------------------------------------------------------------------------------------------------------
def uninstall_coccoc_via_control_panel(
    language=setting.coccoc_language, is_delete_user_data=True, is_uninstall=True
):
    # To disable annoying error Windows fatal exception: code 0x8001010d
    faulthandler.disable()
    # To kill all coccoc process is running
    browser_utils.kill_all_coccoc_process()
    # To open control panel
    os.system("appwiz.cpl")
    # To get the Windows version
    windows_version = os_utils.get_windows_version()
    # To set some variable
    title = None
    program_features = None

    # To get the control panel title based on Windows version
    if windows_version == "10":
        title = r"Control Panel\Programs\Programs and Features"
    elif windows_version in ("11", "8", "8.1", "7"):
        title = "Programs and Features"
    else:
        print("Incorrect Windows version")

    # To get the default link after uninstall completely
    opening_url_after_uninstalled = (
        f"https://coccoc.com/uninstall?hl="
        + language
        + "&crversion="
        + browser_utils.get_browser_version_formatted()
        + "&os="
        + os_utils.get_os_version_windows()
        + "&uid="
        + browser_utils.get_uid_formatted()
    )

    # Start uninstalling process
    try:
        # Connect to current program and feature from control panel
        program_features = Application(backend="uia").connect(
            title_re=".*Programs and Features",
            class_name="CabinetWClass",
            control_type=50032,
            timeout=10,
        )

        program_features[title].child_window(title="Cốc Cốc", control_type=50004).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).click_input(button="left", double=True)
        program_features[title].maximize()
        program_features[title].set_focus()
        if language == "en":
            # uninstall_dialog = Desktop(backend='uia').Uninstall_Cốc_Cốc
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            uninstall_dialog.wait("visible", timeout=setting.timeout_pywinauto)
            if is_uninstall:
                if is_delete_user_data:
                    uninstall_dialog.child_window(
                        control_type=50002, title="Delete profile label"
                    ).click()
                    uninstall_dialog.child_window(
                        control_type=50000, title="Uninstall"
                    ).click()
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="Uninstall"
                    ).click()
            else:
                uninstall_dialog.child_window(
                    control_type=50000, title="I'll stay with Cốc Cốc"
                ).click()

        elif language == "vi":
            # uninstall_dialog = Desktop(backend='uia').Gỡ_bỏ_cài_đặt_Cốc_Cốc
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            uninstall_dialog.wait("visible", timeout=setting.timeout_pywinauto)
            if is_uninstall:
                if is_delete_user_data:
                    uninstall_dialog.child_window(
                        control_type=50002, title="Delete profile label"
                    ).click()
                    uninstall_dialog.child_window(
                        control_type=50000, title="Gỡ cài đặt"
                    ).click()
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="Gỡ cài đặt"
                    ).click()
            else:
                uninstall_dialog.child_window(
                    control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
                ).click()

        else:
            LOGGER.info("language must be: en or vi")

    finally:
        # To Close Program Files and Features
        program_features[title].close()
        faulthandler.enable()

        # To close the automatically opening browser window after uninstall successfully
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50032,
            title_re="https",
            timeout=setting.timeout_pywinauto,
        )
        app[opening_url_after_uninstalled].close()
        faulthandler.enable()


# ------------------------------------------------------------------------------------------------------------------
"""
This method is for uninstall the coccoc via control panel
"""


def test_uninstall_coccoc_by_control_panel():
    uninstall_coccoc_by_control_panel(
        language=setting.coccoc_language, is_delete_user_data=True, is_uninstall=True
    )


def uninstall_coccoc_by_control_panel(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
    is_submit_feedback=False,
    wait_for_n_seconds_before_close_the_windows=0,
):
    """
    Uninstall coccoc via control panel
    :param language: 'vi' or 'en'
    :param is_delete_user_data: True --> delete all, False: keep user data
    :param is_uninstall: True --> Uninstall, False --> Stop uninstalling
    :param is_submit_feedback: True --> submit feedback, False --> dont submit feed back
    :param wait_for_n_seconds_before_close_the_windows: delay n seconds before close the opening windows.
    :return:
    """
    # To disable annoying error Windows fatal exception: code 0x8001010d
    faulthandler.disable()

    """To kill all coccoc process is running"""
    browser_utils.kill_all_coccoc_process()
    if file_utils.check_file_is_exists(
        setting.coccoc_binary_64bit
    ) or file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        # language = browser_utils.get_current_coccoc_language()
        # To get the default link after uninstall completely
        # sample opening_url_after_uninstalled = 'https://coccoc.com/uninstall?hl=vi&crversion=97.0.4692.104&os=10.0.19043&uid=2D066388-C17D-4D8D-876D-5A1251516474'
        opening_url_after_uninstalled = (
            f"https://coccoc.com/uninstall?hl="
            + language
            + "&crversion="
            + browser_utils.get_browser_version_formatted()
            + "&os="
            + os_utils.get_os_version_windows()
            + "&uid="
            + browser_utils.get_uid_formatted()
        )

        # Start program and feature page by command line
        # subprocess.call('appwiz.cpl')
        os.system("appwiz.cpl")
        time.sleep(3)
        program_features = None
        windows_version = os_utils.get_windows_version()
        try:
            if windows_version == "10":
                # title = r"Control Panel\Programs\Programs and Features"
                title = r"Programs and Features"
                program_features = Application(backend="uia").connect(
                    title_re=title,
                    class_name="CabinetWClass",
                    control_type=50032,
                    timeout=setting.timeout_pywinauto,
                )
                program_features[title].maximize()
                program_features[title].set_focus()
                program_features[title].child_window(
                    title="Cốc Cốc", control_type=50004
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click_input(
                    button="left", double=True
                )
                time.sleep(1)
            elif windows_version == "11":
                title = "Programs and Features"
                program_features = Application(backend="uia").connect(
                    title_re=title,
                    class_name="CabinetWClass",
                    control_type=50032,
                    timeout=setting.timeout_pywinauto,
                )
                program_features[title].maximize()
                program_features[title].set_focus()
                program_features[title].child_window(
                    title="Cốc Cốc", control_type=50004
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click_input(
                    button="left", double=True
                )
                time.sleep(1)

            if language == "en":
                uninstall_dialog = os_utils.connect_to_window_via_pid(
                    process_name="browser.exe"
                )
                uninstall_dialog.wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=1
                )
                if is_uninstall:
                    if is_delete_user_data:
                        uninstall_dialog.child_window(
                            control_type=50002, title="Delete profile label"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                        time.sleep(0.5)
                        uninstall_dialog.child_window(
                            control_type=50000, title="Uninstall"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                    else:
                        uninstall_dialog.child_window(
                            control_type=50000, title="Uninstall"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                    time.sleep(2)
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="I'll stay with Cốc Cốc"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                time.sleep(1)

            elif language == "vi":
                # uninstall_dialog = Desktop(backend='uia').Gỡ_bỏ_cài_đặt_Cốc_Cốc
                uninstall_dialog = os_utils.connect_to_window_via_pid(
                    process_name="browser.exe"
                )
                uninstall_dialog.wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=1
                )
                if is_uninstall:
                    if is_delete_user_data:
                        uninstall_dialog.child_window(
                            control_type=50002, title="Delete profile label"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                        time.sleep(0.5)
                        uninstall_dialog.child_window(
                            control_type=50000, title="Gỡ cài đặt"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                    else:
                        uninstall_dialog.child_window(
                            control_type=50000, title="Gỡ cài đặt"
                        ).wait(
                            "visible",
                            timeout=setting.timeout_pywinauto,
                            retry_interval=0.5,
                        ).click()
                    time.sleep(2)
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
            else:
                LOGGER.info("language must be: en or vi")
        finally:
            """To Close Program Files and Features"""
            # program_features.close()
            program_features.window().close()
            time.sleep(2)

            """ To close the automatically opening browser window"""
            if is_uninstall:
                if is_submit_feedback:
                    submit_feedback_after_uninstall(language)
                app = Application(backend="uia").connect(
                    class_name="Chrome_WidgetWin_1",
                    control_type=50032,
                    title_re=r"Cốc Cốc đã được gỡ cài đặt",
                    timeout=setting.timeout_pywinauto,
                )
                time.sleep(wait_for_n_seconds_before_close_the_windows)
                app.window().close()
                time.sleep(1)
            faulthandler.enable()
        time.sleep(3)
    else:
        pass


# ------------------------------------------------------------------------------------------------------------------
def install_coccoc(
    language,
    is_default_browser=False,
    is_default_torrent=False,
    is_default_start_up=False,
    is_continue_install=True,
):
    # Start file CocCocSetup.exe
    Application(backend="uia").start(
        f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
    )

    # Connect to coccoc installation dialog
    coccoc_install_dialog = None
    if language == "vi":
        coccoc_install_dialog = Desktop(backend="uia").Đang_chạy_Trình_cài_đặt_Cốc_Cốc
    elif language == "en":
        coccoc_install_dialog = Desktop(backend="uia").Initializing_Cốc_Cốc_Installer
    else:
        LOGGER.info("language must be: vi OR en")
    if is_continue_install:
        if is_default_browser is False:
            coccoc_install_dialog.child_window(auto_id="2025").click()
        if is_default_torrent is False:
            coccoc_install_dialog.child_window(auto_id="2026").click()
        if is_default_start_up is True:
            coccoc_install_dialog.child_window(auto_id="2027").click()
        coccoc_install_dialog.child_window(auto_id="2024").click()
        time.sleep(110)
        first_time_run.verify_new_tab_coccoc_exist()
        time.sleep(10)
    else:
        # To close the installation dialog
        coccoc_install_dialog.child_window(auto_id="1", control_type=50000).click()
        # To cancel installation
        coccoc_install_dialog.child_window(auto_id="2", control_type=50000).click()


# Get browser build for test from FTP
def get_browser_build(
    build_name=setting.coccoc_build_name,
    version=setting.coccoc_test_version,
    platform=setting.platform,
    from_build_name=None,
    to_build_name=None,
):
    build_for_test = base_window.BaseWindow.pre_process_setup_filename(
        version=version,
        build_name=build_name,
        from_build_name=from_build_name,
        to_build_name=to_build_name,
    )
    # print('build for test ' + str(build_for_test))

    if (
        file_utils.check_file_is_exists(
            rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\{build_for_test}"
        )
        is False
    ):
        ftp_connection.get_file(
            folder_version=version,
            file_to_download_for_test=build_for_test,
            platform=platform,
        )

    return build_for_test
    # file_utils.delete_installer_downloaded(build_name=old_browser_build_for_test)


def test_get_browser_build():
    get_browser_build()


def check_folders_after_uninstall():
    assert file_utils.check_folder_is_exists(browser_utils.get_coccoc_folder()) is True
    assert (
        file_utils.check_folder_is_exists(
            f"{browser_utils.get_coccoc_folder()}\\Browser\\Application"
        )
        is False
    )
    assert (
        file_utils.check_folder_is_exists(
            f"{browser_utils.get_coccoc_folder()}\\CrashReports"
        )
        is True
    )
    assert (
        file_utils.check_folder_is_exists(
            f"{browser_utils.get_coccoc_folder()}\\Update"
        )
        is False
    )


def test_check_folders_after_uninstall():
    check_folders_after_uninstall()


def check_user_local_data(is_delete_user_data=False):
    if is_delete_user_data:
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser"
            )
            is False
        )
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data"
            )
            is False
        )
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\CrashReports"
            )
            is True
        )
    else:
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser"
            )
            is True
        )
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data"
            )
            is True
        )
        assert (
            file_utils.check_folder_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\CrashReports"
            )
            is True
        )


def check_uid_exist():
    return file_utils.check_file_is_exists(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Roaming\\CocCoc\\uid"
    )


def test_check_uid_exist():
    assert check_uid_exist() is True


def check_hid3_exist():
    return file_utils.check_file_is_exists(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Roaming\\CocCoc\\hid3"
    )


def test_check_hid3_exist():
    assert check_hid3_exist() is True


def test_check_coccoc_uninstall_dialog():
    check_coccoc_uninstall_dialog(
        language=setting.coccoc_language, is_delete_user_data=True, is_uninstall=False
    )


def check_coccoc_uninstall_dialog(
    language=setting.coccoc_language,
    is_delete_user_data=True,
    is_uninstall=True,
    is_verify_ui=False,
):
    # To disable annoying error Windows fatal exception: code 0x8001010d
    faulthandler.disable()

    """To kill all coccoc process is running"""
    browser_utils.kill_all_coccoc_process()

    # To get the default link after uninstall completely
    # sample opening_url_after_uninstalled = 'https://coccoc.com/uninstall?hl=vi&crversion=97.0.4692.104&os=10.0.19043&uid=2D066388-C17D-4D8D-876D-5A1251516474'
    opening_url_after_uninstalled = (
        f"https://coccoc.com/uninstall?hl="
        + language
        + "&crversion="
        + browser_utils.get_browser_version_formatted()
        + "&os="
        + os_utils.get_os_version_windows()
        + "&uid="
        + browser_utils.get_uid_formatted()
    )

    # Start program and feature page by command line
    os.system("appwiz.cpl")
    time.sleep(2)
    program_features = None
    # program_features = Application(backend='uia')
    windows_version = os_utils.get_windows_version()
    title = None
    try:
        if windows_version == "10":
            # title = r'Control Panel\Programs\Programs and Features'
            title = r"Programs and Features"
            # program_features = Desktop(backend='uia').Control_Panel_Programs_Programs_and_Features
            program_features = Application(backend="uia").connect(
                title_re=title,
                class_name=r"CabinetWClass",
                control_type=50032,
                timeout=10,
            )
            program_features[title].maximize()
            program_features[title].set_focus()
            program_features[title].child_window(
                title=r"Cốc Cốc", control_type=50004
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click_input(
                button="left", double=True
            )
            time.sleep(1)

        elif windows_version == "11":
            title = "Programs and Features"
            program_features = Application(backend="uia").connect(
                title_re=title,
                class_name="CabinetWClass",
                control_type=50032,
                timeout=10,
            )
            program_features[title].maximize()
            program_features[title].set_focus()
            program_features[title].child_window(
                title=r"Cốc Cốc", control_type=50004
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).click_input(
                button="left", double=True
            )
            time.sleep(1)

        """PROCESS TO CHECK THE DIALOG UI"""
        if language == "en":
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            uninstall_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            )

            if is_verify_ui is True:
                # Check UI:
                # Check title "Looks like something went wrong!"
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020, title="Looks like something went wrong!"
                    ).is_visible()
                    is True
                )

                # Check button: "Report problem"
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020,
                        title="Please tell us about your problem and we will help you as soon as posible. Report a problem",
                    ).is_visible()
                    is True
                )
                facebook_fan_page_window = None
                facebook_fan_page_title = "Trình duyệt Cốc Cốc"
                try:
                    uninstall_dialog.child_window(
                        title="Report a problem", control_type=50020
                    ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                    time.sleep(2)
                    facebook_fan_page_window = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=facebook_fan_page_title,
                        timeout=setting.timeout_pywinauto,
                    )
                finally:
                    facebook_fan_page_window.window().set_focus().close()
                time.sleep(2)

                # Check other buttons:
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020,
                        title="Are you sure you want to uninstall Cốc Cốc?",
                    ).is_visible()
                    is True
                )
                uninstall_dialog.child_window(
                    control_type=50000, title="I'll stay with Cốc Cốc"
                ).click_input(button="right")
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020, title="Thank you! you're wonderful!"
                    ).is_visible()
                    is True
                )

                # To check  "I'll stay with Cốc Cốc"
                uninstall_dialog.child_window(
                    control_type=50000, title="Uninstall"
                ).click_input(button="right")
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020,
                        title="We're sorry! please give us a second chance!",
                    ).is_visible()
                    is True
                )
            else:
                pass
            # PROCESS TO UNINSTALL IF ANY
            if is_uninstall:
                if is_delete_user_data:
                    uninstall_dialog.child_window(
                        control_type=50002, title="Delete profile label"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                    uninstall_dialog.child_window(
                        control_type=50000, title="Uninstall"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="Uninstall"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
            else:
                uninstall_dialog.child_window(
                    control_type=50000, title="I'll stay with Cốc Cốc"
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()
            time.sleep(1)

        elif language == "vi":
            uninstall_dialog = os_utils.connect_to_window_via_pid(
                process_name="browser.exe"
            )
            uninstall_dialog.wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            )
            if is_verify_ui is True:
                # Check UI:
                # Check title "Looks like something went wrong!"
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020, title="Có vẻ như bạn đang gặp vấn đề gì đó?"
                    ).is_visible()
                    is True
                )

                # Check button: "Report problem"
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020,
                        title="Hãy cho chúng tôi biết bạn đã gặp phải vấn đề gì. Chúng tôi sẽ giúp bạn sớm nhất có thể.  Báo cáo lỗi",
                    ).is_visible()
                    is True
                )
                facebook_fan_page_window = None
                facebook_fan_page_title = "Trình duyệt Cốc Cốc"
                try:
                    uninstall_dialog.child_window(
                        title="Báo cáo lỗi", control_type=50020
                    ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
                    time.sleep(2)
                    facebook_fan_page_window = Application(backend="uia").connect(
                        class_name="Chrome_WidgetWin_1",
                        control_type=50033,
                        title_re=facebook_fan_page_title,
                        timeout=setting.timeout_pywinauto,
                    )
                finally:
                    facebook_fan_page_window.window().set_focus().close()
                time.sleep(2)

                # Check other buttons:
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020, title="Bạn có chắc chắn muốn gỡ Cốc Cốc?"
                    ).is_visible()
                    is True
                )
                uninstall_dialog.child_window(
                    control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
                ).click_input(button="right")
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020, title="Cám ơn bạn! bạn thật tuyệt!"
                    ).is_visible()
                    is True
                )

                # To check  "I'll stay with Cốc Cốc"
                uninstall_dialog.child_window(
                    control_type=50000, title="Gỡ cài đặt"
                ).click_input(button="right")
                assert (
                    uninstall_dialog.child_window(
                        control_type=50020,
                        title="Chúng tôi rất tiếc! hãy cho chúng tôi thêm 1 cơ hội!",
                    ).is_visible()
                    is True
                )
            else:
                pass
            # PROCESS TO UNINSTALL IF ANY
            if is_uninstall:
                if is_delete_user_data:
                    uninstall_dialog.child_window(
                        control_type=50002, title="Delete profile label"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                    uninstall_dialog.child_window(
                        control_type=50000, title="Gỡ cài đặt"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
                else:
                    uninstall_dialog.child_window(
                        control_type=50000, title="Gỡ cài đặt"
                    ).wait(
                        "visible",
                        timeout=setting.timeout_pywinauto,
                        retry_interval=0.5,
                    ).click()
            else:
                uninstall_dialog.child_window(
                    control_type=50000, title="Tôi vẫn sẽ sử dụng Cốc Cốc"
                ).wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).click()
        else:
            LOGGER.info("language must be: en or vi")
    finally:
        """To Close Program Files and Features"""
        # program_features.close()
        program_features.window().set_focus().close()
        time.sleep(2)

        """ To close the automatically opening browser window"""
        if is_uninstall:
            app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50032,
                title_re="https://coccoc.com/uninstall",
                timeout=setting.timeout_pywinauto,
            )
            app.window().set_focus().close()
        faulthandler.enable()
    time.sleep(2)


def submit_feedback_after_uninstall(language=setting.coccoc_language):
    opening_url_after_uninstalled = r".*coccoc.com/uninstall"
    app = None
    title_feedback = None
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50032,
            title_re=opening_url_after_uninstalled,
            timeout=setting.timeout_pywinauto,
        )
        title_feedback = app.window().window_text()
        # app[title_feedback].print_control_identifiers()
        if language == "en":
            # click "Reinstall coccoc"
            app[title_feedback].child_window(
                title="Tôi muốn cài lại trình duyệt",
                auto_id="reinstall_browser",
                control_type="CheckBox",
            ).click_input()
            app[title_feedback].child_window(
                auto_id="reinstall_browser", control_type="Edit"
            ).set_text("Automation Test")
            i = random.randint(0, 3)
            if i == 0:
                app[title_feedback].child_window(
                    title="Cốc Cốc được cài đặt trên máy nhưng tôi chưa thử bao giờ",
                    auto_id="never_tried",
                    control_type="CheckBox",
                ).click_input(),
            elif i == 1:
                app[title_feedback].child_window(
                    title="Trình duyệt không ổn định hoặc làm nặng máy",
                    auto_id="unstable_slow",
                    control_type="CheckBox",
                ).click_input(),
            elif i == 2:
                app[title_feedback].child_window(
                    title="Không truy cập được các trang web quan trọng",
                    auto_id="access_important",
                    control_type="CheckBox",
                ).click_input(),
            else:
                app[title_feedback].child_window(
                    title="Tính năng trên trình duyệt không như tôi mong đợi",
                    auto_id="unexpected_features",
                    control_type="CheckBox",
                ).click_input()
            # random.choice(list_checkbox)()

            # Submit button
            app[title_feedback].wheel_mouse_input(wheel_dist=-3)
            app[title_feedback].child_window(title="Gửi", control_type="Button").wait(
                "visible", timeout=setting.timeout_pywinauto
            ).click_input()
            assert (
                app[title_feedback]
                .child_window(title="Cảm ơn bạn đã chia sẻ", control_type="Text")
                .is_visible()
                is True
            )

        else:
            # click "Reinstall coccoc"
            app[title_feedback].child_window(
                title="Tôi muốn cài lại trình duyệt",
                auto_id="reinstall_browser",
                control_type="CheckBox",
            ).click_input()
            app[title_feedback].child_window(
                auto_id="reinstall_browser", control_type="Edit"
            ).set_text("Automation Test")
            i = random.randint(0, 3)
            if i == 0:
                app[title_feedback].child_window(
                    title="Cốc Cốc được cài đặt trên máy nhưng tôi chưa thử bao giờ",
                    auto_id="never_tried",
                    control_type="CheckBox",
                ).click_input(),
            elif i == 1:
                app[title_feedback].child_window(
                    title="Trình duyệt không ổn định hoặc làm nặng máy",
                    auto_id="unstable_slow",
                    control_type="CheckBox",
                ).click_input(),
            elif i == 2:
                app[title_feedback].child_window(
                    title="Không truy cập được các trang web quan trọng",
                    auto_id="access_important",
                    control_type="CheckBox",
                ).click_input(),
            else:
                app[title_feedback].child_window(
                    title="Tính năng trên trình duyệt không như tôi mong đợi",
                    auto_id="unexpected_features",
                    control_type="CheckBox",
                ).click_input()
            # random.choice(list_checkbox)()

            # Submit button
            app[title_feedback].wheel_mouse_input(wheel_dist=-3)
            app[title_feedback].child_window(title="Gửi", control_type="Button").wait(
                "visible", timeout=setting.timeout_pywinauto
            ).click_input()
            # app[title_feedback].print_control_identifiers()
            assert (
                app[title_feedback]
                .child_window(title="Cảm ơn bạn đã chia sẻ", control_type="Text")
                .is_visible()
                is True
            )
    finally:
        pass
    time.sleep(2)


def test_submit_feedback_after_uninstall():
    submit_feedback_after_uninstall()


def wait_for_uninstall_request_log_sent(timeout=100) -> bool:
    max_delay = timeout
    interval_delay = 10
    total_delay = 0
    uninstall_log = rf"C:\Users\{os_utils.get_username()}\Documents\uninstall_log.json"
    while total_delay < max_delay:
        try:
            if file_utils.check_file_is_exists(uninstall_log):
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay

    if file_utils.check_file_is_exists(uninstall_log):
        return True
    else:
        print(
            rf"Time out after {timeout} seconds of waiting for the uninstall log sent"
        )
        return False


def check_request_uninstalling_log():
    request_log = read_request_uninstalling_log()
    if request_log is not None:
        cc_version = string_number_utils.get_string_between_2_str(
            request_log["url"], "crversion=", "&os"
        )
        assert cc_version == setting.coccoc_test_version


def read_request_uninstalling_log():
    uninstall_log = rf"C:\Users\{os_utils.get_username()}\Documents\uninstall_log.json"
    if file_utils.check_file_is_exists(uninstall_log):
        with open(uninstall_log, encoding="utf-8") as file:
            parsed_json = json.load(file)
            return parsed_json
    else:
        print(rf"No {uninstall_log} file found")


def test_print():
    browser = open_browser.open_coccoc_by_pywinauto()
    time.sleep(10)
    browser.window().print_control_identifiers()
    # for window in browser.windows():
    #     for item in window.descendants(control_type="ListItem"):
    #         print(item.window_text())
    # for item in window.children(control_type="ListItem"):
    #     print(item.window_text())
    # open_browser.connect_to_coccoc_by_title(title='New Tab - Cốc Cốc')
    # open_browser.close_coccoc_by_window_title(title=r'New Tab - Cốc Cốc')
