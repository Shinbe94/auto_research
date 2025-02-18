import ctypes
from pathlib import Path
import tkinter as tk
import datetime
import faulthandler
import getpass
import os
import platform
import subprocess
import sys
import time
from datetime import date

import pywinauto
from pywinauto import Application, keyboard

from src.utilities import time_utils, process_id_utils
from tests import setting


# from pywinauto.application import Application


def get_username():
    return getpass.getuser()


def get_username1():
    return os.environ["COMPUTERNAME"]


def test_get_username():
    print(os.environ["COMPUTERNAME"])


def is_leap_year(year) -> bool:
    if (year % 400 == 0) and (year % 100 == 0):
        return True

    # not divided by 100 means not a century year
    # year divided by 4 is a leap year
    elif (year % 4 == 0) and (year % 100 != 0):
        return True

    # if not divided by both 400 (century year) and 4 (not century year)
    # year is not leap year
    else:
        return False


def get_next_2_month_from_today():
    today = datetime.date.today()
    format_month = 12 if (today.month + 2) % 12 == 0 else (today.month + 2) % 12
    calculated_year = int(today.year) + ((int(today.month) + 1) // 12)

    if is_leap_year(calculated_year) and format_month == 2 and int(today.day) >= 29:
        calculated_today_after_2_month = 29
    elif format_month == 2 and int(today.day) >= 28:
        calculated_today_after_2_month = 28
    else:
        calculated_today_after_2_month = int(today.day)

    # print(int(today.day))
    if get_windows_version() == "11":
        next_2_month = date(
            calculated_year, format_month, calculated_today_after_2_month
        ).strftime("%d/%m/%Y")
    else:
        next_2_month = date(
            calculated_year, format_month, calculated_today_after_2_month
        ).strftime("%m/%d/%Y")
    return next_2_month, today.strftime("%m/%d/%Y")


def test_get_next_2_month_from_today():
    print(get_next_2_month_from_today())


def get_today():
    today = datetime.date.today()
    if get_windows_version() == "11":
        return str(today.strftime("%d/%m/%Y"))
    else:
        return str(today.strftime("%m/%d/%Y"))


def test_get_today():
    print(get_today())


def get_tomorrow():
    tmr = datetime.date.today() + datetime.timedelta(days=1)
    if get_windows_version() == "11":
        return str(tmr.strftime("%d/%m/%Y"))
    else:
        return str(tmr.strftime("%m/%d/%Y"))


def test_get_tomorrow():
    print(get_tomorrow())


def get_the_day_after_tomorrow():
    tmr = datetime.date.today() + datetime.timedelta(days=2)
    if get_windows_version() == "11":
        return str(tmr.strftime("%d/%m/%Y"))
    else:
        return str(tmr.strftime("%m/%d/%Y"))


def kill_process_by_name(pid_name: str):
    """
    To kill process by its name, also disable console log by added stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT
    Args:
        pid_name: process name, e.g: WinAppDriver.exe, notepad++.exe ...
    Returns: None
    """
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if is_admin():
        if process_id_utils.is_process_running(pid_name):
            subprocess.run(
                rf"taskkill /im {pid_name} /f",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )

            time.sleep(1)
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def test_kill_process_by_name():
    kill_process_by_name("WinAppDriver.exe")
    # kill_process_by_name('notepad++.exe')
    # kill_process_by_name('browser.exe')


def test_kill_process_by_its_id():
    kill_process_by_its_id(process_id=20296)


def kill_process_by_its_id(process_id: int):
    """
    To kill process by its id
    :param process_id:
    :return:
    """
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if is_admin():
        if process_id_utils.check_process_is_running_by_its_id(process_id):
            subprocess.run(
                rf"taskkill /im {process_id} /f",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )

            time.sleep(1)
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def open_cmd_as_administrator():
    kill_process_by_name("cmd.exe")
    # To get the current Windows version
    windows_version = get_windows_version()

    time.sleep(1)
    pywinauto.keyboard.send_keys("{LWIN}")
    time.sleep(1)
    pywinauto.keyboard.send_keys("c")
    time.sleep(0.1)
    pywinauto.keyboard.send_keys("m")
    time.sleep(0.1)
    pywinauto.keyboard.send_keys("d")
    time.sleep(0.1)
    pywinauto.keyboard.send_keys(".exe")
    time.sleep(3)
    if windows_version == "10":
        search = Application(backend="uia").connect(
            class_name="Windows.UI.Core.CoreWindow",
            control_type=50032,
            title_re="Search",
            timeout=20,
        )
        # search['Search'].child_window(title="Command Prompt, App, Press right to switch preview",
        #                               auto_id="PPCommand Prompt", control_type="ListItem").wait('visible').click_input(
        #     button='right')
        search["Search"].child_window(
            title="Run as administrator", auto_id="pp_RunAs", control_type=50007
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
        cmd_window = Application(backend="uia").connect(
            title_re="Administrator: Command Prompt", timeout=20
        )
        return cmd_window

    elif windows_version == "11":
        search = Application(backend="uia").connect(
            class_name="Windows.UI.Core.CoreWindow",
            control_type=50032,
            title_re="Search",
            timeout=20,
        )
        # search['Search'].child_window(title="Command Prompt, App, Press right to switch preview",
        #                               auto_id="PPCommand Prompt", control_type="ListItem").wait('visible').click_input(
        #     button='right')
        search["Search"].child_window(
            title="Run as administrator", auto_id="pp_RunAs", control_type=50007
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
        cmd_window = Application(backend="uia").connect(
            title_re="Administrator: Command Prompt", timeout=20
        )
        return cmd_window
    elif windows_version == "7":
        search = Application(backend="uia").connect(
            class_name="DV2ControlHost",
            control_type=50033,
            title_re="Start menu",
            timeout=20,
        )

        search["Start menu"].child_window(
            title="Name", auto_id="System.ItemNameDisplay", control_type=50004
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="right"
        )

        search["Start menu"].child_window(
            title="Run as administrator", auto_id=31074, control_type=50011
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
        cmd_window = Application(backend="uia").connect(
            title_re="Administrator", timeout=20
        )
        return cmd_window
    elif windows_version == "8":
        search = Application(backend="uia").connect(
            class_name="SearchPane",
            control_type=50032,
            title_re="Search Pane",
            timeout=20,
        )

        search["Search Pane"].child_window(
            title="Command Prompt", auto_id="Suggestion_Rich_2", control_type=50007
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="right"
        )

        search["Search Pane"].child_window(
            title="Run as administrator",
            auto_id="MenuFlyoutItemText",
            control_type=50020,
        ).wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=1
        ).click_input(
            button="left"
        )
        cmd_window = Application(backend="uia").connect(
            title_re="Administrator", timeout=20
        )
        return cmd_window

    time.sleep(2)


def change_os_date_to_2_months_later(is_close_cmd_after_changed=False):
    data = None
    try:
        # To open CMD as administrator
        open_cmd_pywinauto()
        # Change the date to 2 month later
        pywinauto.keyboard.send_keys("date{ENTER}")
        time.sleep(1)
        data = get_next_2_month_from_today()
        time.sleep(1)
        pywinauto.keyboard.send_keys(data[0])
        time.sleep(1)
        pywinauto.keyboard.send_keys("{ENTER}")
        time.sleep(2)
    # return the actual current date
    finally:
        if is_close_cmd_after_changed:
            kill_process_by_name("cmd.exe")
        return data[1]


def change_os_date(date: str, is_close_cmd_after_changed=False):
    """Change the system date to a new date
    Args:
        date (str): Formnat with be: "%m/%d/%Y"
        is_close_cmd_after_changed (bool, optional): Close the cmd. Defaults to False.
    Returns:
        _type_: _description_
    """
    # To open CMD as administrator
    try:
        open_cmd_pywinauto()
        # Change the date to 2 month later
        pywinauto.keyboard.send_keys("date{ENTER}")
        time.sleep(1)
        pywinauto.keyboard.send_keys(date)
        time.sleep(1)
        pywinauto.keyboard.send_keys("{ENTER}")
        time.sleep(2)
    finally:
        if is_close_cmd_after_changed:
            kill_process_by_name("cmd.exe")
        return date


def test_sync_datetime():
    sync_datetime(is_need_start_cmd=True)


# To sync the time again
def sync_datetime(is_need_start_cmd=False):
    cmd_window = None
    try:
        # connect to CMD windows
        if is_need_start_cmd:
            open_cmd_pywinauto()
            cmd_window = Application(backend="uia").connect(
                title_re="Administrator: C:", timeout=setting.timeout_pywinauto
            )
            cmd_window.window().set_focus()
            pywinauto.keyboard.send_keys("w32tm /resync{ENTER}")
            time.sleep(3)
        else:
            cmd_window = Application(backend="uia").connect(
                title_re="Administrator: C:", timeout=setting.timeout_pywinauto
            )
            cmd_window.window().set_focus()
            pywinauto.keyboard.send_keys("w32tm /resync{ENTER}")
            time.sleep(3)

    finally:
        kill_process_by_name("cmd.exe")
        time.sleep(1)


def test_set_time_from_settings():
    set_the_time_from_settings_automatically()


def set_the_time_from_settings_automatically():
    faulthandler.disable()
    windows_version = get_windows_version()
    if windows_version == "10":
        settings_window_10 = None
        try:
            # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
            start_windows_settings()
            settings_window_10 = Application(backend="uia").connect(
                class_name="ApplicationFrameWindow",
                control_type=50032,
                title="Settings",
                timeout=setting.timeout_pywinauto,
            )
            # settings_window_10['Settings'].print_control_identifiers()
            settings_window_10["Settings"].maximize()
            settings_window_10["Settings"].set_focus()
            settings_window_10["Settings"].child_window(
                auto_id="SettingsPageGroupTimeRegion", control_type="ListItem"
            ).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            ).click_input()
            time.sleep(1)
            # settings_window_10['Settings'].print_control_identifiers()
            toggle_time = (
                settings_window_10["Settings"]
                .child_window(
                    auto_id="SystemSettings_DateTime_IsTimeSetAutomaticallyEnabled_ToggleSwitch",
                    control_type="Button",
                )
                .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
            )
            if toggle_time.get_toggle_state() == 1:
                toggle_time.click_input()
                time.sleep(3)
                toggle_time.click_input()
                time.sleep(2)
            else:
                toggle_time.click_input()
                time.sleep(3)
        finally:
            settings_window_10["Settings"].close()
            time.sleep(1)

    elif windows_version == "11":
        settings_window = None
        try:
            # pywinauto.keyboard.send_keys("{VK_LWIN down}i{VK_LWIN up}")
            start_windows_settings()

            settings_window = Application(backend="uia").connect(
                class_name="ApplicationFrameWindow",
                control_type=50032,
                title="Settings",
                timeout=setting.timeout_pywinauto,
            )
            # settings_window['Settings'].print_control_identifiers()
            settings_window["Settings"].maximize()
            settings_window["Settings"].set_focus()
            settings_window["Settings"].child_window(
                title="Time & language", control_type="ListItem"
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(1)
            settings_window["Settings"].child_window(
                title="Date & time", control_type="ListItem"
            ).wait("visible", timeout=setting.timeout_pywinauto).click_input()
            time.sleep(1)
            # settings_window['Settings'].print_control_identifiers()
            toggle_time = (
                settings_window["Settings"]
                .child_window(
                    auto_id="SystemSettings_DateTime_IsTimeSetAutomaticallyEnabled_ToggleSwitch",
                    control_type="Button",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
            )
            if toggle_time.get_toggle_state() == 1:
                toggle_time.click_input()
                time.sleep(3)
                toggle_time.click_input()
                time.sleep(2)
            else:
                toggle_time.click_input()
                time.sleep(3)
        finally:
            settings_window["Settings"].close()
    time.sleep(1)


def test_get_platform_architecture():
    print(get_platform_architecture())


def get_platform_architecture():
    if sys.platform.startswith("linux") and sys.maxsize > 2**32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        architecture = "64"
    elif sys.platform.startswith("win"):
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError(
            "Could not determine chromedriver download URL for this platform."
        )
    return platform, architecture


def get_window_platform_architecture(is_format_for_chromium_based=True):
    if setting.platform:
        platform_architecture = setting.platform
    else:
        platform_architecture = platform.architecture()[0]

    if is_format_for_chromium_based:
        platform_architecture1 = (
            platform_architecture[:2] + "-" + platform_architecture[2:]
        )
        return platform_architecture1
    else:
        return platform_architecture


def test_get_real_system_platform():
    print(get_real_system_platform())


def get_real_system_platform(is_format_for_chromium_based=True):
    """
    to get real system arch (not from setting config)
    Args:
        is_format_for_chromium_based:
    Returns:
    """
    platform_architecture = platform.architecture()[0]
    if is_format_for_chromium_based:
        platform_architecture1 = (
            platform_architecture[:2] + "-" + platform_architecture[2:]
        )
        return platform_architecture1
    else:
        return platform_architecture


def test_platform_architecture():
    print(get_window_platform_architecture(is_format_for_chromium_based=True))


def test_get_window_arch():
    print(get_window_arch().strip("_"))


def get_window_arch(is_formatted=True):
    # If platform is specified use it, if not get automatically from os
    if setting.platform == "64bit":
        return "_x64"
    elif setting.platform == "32bit":
        return ""
    else:
        if is_formatted:
            if platform.architecture()[0] == "64bit":
                return "_x64"
            else:
                return ""
        return platform.architecture()[0]


def test_get_os_version_windows():
    print(get_os_version_windows())


# To get Windows version
def get_os_version_windows(windows_ver=10):
    os.system(f"ver" + " > output.txt")
    os_version = None
    if os.path.exists("output.txt"):
        # fp = open('output.txt', "r")
        # output = fp.read()
        with open("output.txt") as f:
            lines = f.readlines()
            f.close()
            output_text = lines[
                1
            ]  # Microsoft Windows [Version 10.0.19043.1526] or Microsoft Windows [Version 6.1.7601]
            temp = output_text.split("Microsoft Windows [Version ", 1)[1]
            if windows_ver == 10:
                temp2 = temp[0:9]
            else:
                temp2 = temp[0:7]

            # Replace "." by "_"
            # os_version_formatted = temp2.replace('.', '_')
    os.remove("output.txt")
    return temp2


# To check is the coccoc being set as start up along with Windows
def check_coccoc_is_start_up():
    command_start_up_coccoc = rf"wmic startup get caption,command"
    text = subprocess.check_output(command_start_up_coccoc, encoding="utf-8")
    # print(text)
    if r"CocCoc\Browser\Application\browser.exe" in text:
        return True
    else:
        return False


# To check autolaunch_enabled is true at LocalState
def check_auto_launch_enabled_is_true():
    faulthandler.disable()
    str_auto_launch = r'"autolaunch_enabled":true'
    if is_file_exists(
        rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State"
    ):
        # with open(fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State') as f:
        #     content = f.read()
        #     f.close()
        #     if str_auto_launch in content:
        #         return True
        #     else:
        #         return False
        if is_admin():
            # check = subprocess.check_output(
            #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', encoding='utf-8')
            # check = subprocess.check_output(
            #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', shell=True,
            #     stderr=subprocess.STDOUT)
            # out_put = subprocess.Popen([sys.executable, fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State'], stdout=subprocess.PIPE)
            # check = out_put.communicate()
            # print(check)
            # assert str_auto_launch in str(check)
            os.chmod(
                rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
                0o777,
            )
            with open(
                rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
                encoding="utf-8",
            ) as f:
                content = f.read()
                # assert str_auto_launch in str(content)
                # print(content)
                f.close()

                if str_auto_launch in str(content):
                    return True
                else:
                    return False
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )

            # check = subprocess.check_output(
            #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', encoding='utf-8')
            # check = subprocess.check_output(
            #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', shell=True,
            #     stderr=subprocess.STDOUT)
            # out_put = subprocess.Popen([sys.executable, fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State'], stdout=subprocess.PIPE)
            # check = out_put.communicate()
            # print(check)
            # assert str_auto_launch in str(check)
            #
            os.chmod(
                rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
                0o777,
            )
            with open(
                rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State",
                encoding="utf-8",
            ) as f:
                content = f.read()
                # assert str_auto_launch in str(content)
                # print(content)
                f.close()

                if str_auto_launch in str(content):
                    return True
                else:
                    return False


def check_auto_launch_enabled_is_true2():
    str_auto_launch = r'"autolaunch_enabled":true'
    if is_file_exists(
        rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State"
    ):
        # check = subprocess.check_output(
        #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', encoding='utf-8')

        # check = subprocess.check_output(
        #     fr'C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State', shell=True,
        #     stderr=subprocess.STDOUT)
        command = rf"C:\Users\{get_username()}\AppData\Local\CocCoc\Browser\User Data\Local State"
        open_cmd_as_administrator()
        pywinauto.keyboard.send_keys("import subprocess{ENTER}")
        pywinauto.keyboard.send_keys(
            rf"out_put = subprocess.Popen([sys.executable, {command}],stdout=subprocess.PIPE)"
            + "{ENTER}"
        )
        # out_put = subprocess.Popen(
        #     [sys.executable, command],
        #     stdout=subprocess.PIPE)
        # check = out_put.communicate()
        # # print(check)
        # assert str_auto_launch in str(check)


def test_():
    check_auto_launch_enabled_is_true()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_windows_version() -> str:
    version = sys.getwindowsversion()
    if int(sys.getwindowsversion().build) > 20000:
        return str(11)
    else:
        return str(platform.release())


def test_winver():
    print("platform is: " + platform.platform())
    print("OS is: " + platform.system())
    print("OS version: " + platform.release())
    print("OS version full: " + platform.version())
    print(platform.version().split(".")[2])
    print(platform.machine())
    version = sys.getwindowsversion()

    print(version)
    print(version[2])  # You can directly reference the build element by index number
    print(version.build)  # Or by name
    print(version[0])
    print(get_windows_version())


def get_folder_size(start_path="."):
    total_size = 0
    for dir_path, dir_names, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dir_path, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def test_size():
    print(get_folder_size(r"C:\Program Files\CocCoc\Browser\Application\a"), "bytes")


def create_coccoc_update_task_schedule():
    command = (
        r'SCHTASKS /CREATE /SC DAILY /TN "CocCocTask\autoUpdate" /TR "C:\Program Files {(}x86{)}\CocCoc\Update\CocCocUpdate.exe" /ua /installsource scheduler /ST '
        + str(time_utils.n_minutes_after_current(2))[11:16]
    )
    cmd_windows = open_cmd_as_administrator()
    # pywinauto.keyboard.send_keys(command)
    time.sleep(3)
    try:
        keyboard.send_keys(command, with_spaces=True)
        pywinauto.keyboard.send_keys("{ENTER}")
    finally:
        cmd_windows["Administrator"].close()


def test_create_coccoc_update_task_schedule():
    create_coccoc_update_task_schedule()


def delete_coccoc_update_task_schedule():
    command = rf'SCHTASKS /DELETE /TN "CocCocTask\autoUpdate'
    cmd_window = open_cmd_as_administrator()
    time.sleep(3)
    try:
        # pywinauto.keyboard.send_keys(command)
        keyboard.send_keys(command, with_spaces=True)
        pywinauto.keyboard.send_keys("{ENTER}")
        time.sleep(1)
        pywinauto.keyboard.send_keys("y")
        time.sleep(1)
        pywinauto.keyboard.send_keys("{ENTER}")
    finally:
        cmd_window["Administrator"].close()


def test_delete_coccoc_update_task_schedule():
    delete_coccoc_update_task_schedule()


def edit_coccoc_update_task_schedule():
    command = (
        r'SCHTASKS /CHANGE /TN "CocCocUpdateTaskMachineUA" /ST '
        + str(time_utils.n_minutes_after_current(2))[11:16]
    )
    command_core = (
        r'SCHTASKS /CHANGE /TN "CocCocUpdateTaskMachineCore" /ST '
        + str(time_utils.n_minutes_after_current(2))[11:16]
    )
    cmd_window = open_cmd_pywinauto()
    try:
        cmd_window.type_keys(command, with_spaces=True)
        cmd_window.type_keys("{ENTER}", with_spaces=True)
        time.sleep(0.5)
        cmd_window.type_keys(command_core, with_spaces=True)
        cmd_window.type_keys("{ENTER}", with_spaces=True)
        time.sleep(0.5)
    finally:
        kill_process_by_name("cmd.exe")
        # cmd_window['Administrator'].close()


def test_edit_coccoc_update_task_schedule():
    edit_coccoc_update_task_schedule()


def check_coccoc_browser_task_scheduler():
    list_coccoc_task_scheduler_cmd = "schtasks /query"
    list_coccoc_task_scheduler = subprocess.check_output(
        list_coccoc_task_scheduler_cmd, encoding="utf-8"
    )
    assert "CocCocUpdateTaskMachineCore" in list_coccoc_task_scheduler
    assert "CocCocUpdateTaskMachineUA" in list_coccoc_task_scheduler


def test_check_coccoc_browser_task_scheduler():
    check_coccoc_browser_task_scheduler()


def check_no_coccoc_browser_task_scheduler():
    list_coccoc_task_scheduler_cmd = "schtasks /query"
    list_coccoc_task_scheduler = subprocess.check_output(
        list_coccoc_task_scheduler_cmd, encoding="utf-8"
    )
    assert "CocCocUpdateTaskMachineCore" not in list_coccoc_task_scheduler
    assert "CocCocUpdateTaskMachineUA" not in list_coccoc_task_scheduler


def wait_for_coccoc_task_scheduler_is_disappeared(timeout=120):
    is_disappeared = False
    max_delay = timeout
    interval_delay = 1
    total_delay = 0
    while not is_disappeared:
        list_coccoc_task_scheduler_cmd = "schtasks /query"
        list_coccoc_task_scheduler = subprocess.check_output(
            list_coccoc_task_scheduler_cmd, encoding="utf-8"
        )
        if (
            "CocCocUpdateTaskMachineCore" not in list_coccoc_task_scheduler
            and "CocCocUpdateTaskMachineUA" not in list_coccoc_task_scheduler
        ):
            is_disappeared = True
            break
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay > max_delay:
            print(rf"Timeout for wait for coccoc task scheduler disappeared ")
            break
    return is_disappeared


def test_check_no_coccoc_browser_task_scheduler():
    check_no_coccoc_browser_task_scheduler()


def connect_to_window_via_pid(process_name):
    # use Pid to connect
    app: Application = None
    list_pid = process_id_utils.get_running_process_ids(process_name)
    for pid in list_pid:
        try:
            app = Application(backend="uia").connect(
                process=pid, timeout=setting.timeout_pywinauto, retry_interval=1
            )

        except pywinauto.ElementNotFoundError:
            pass
        if app.window().exists():
            break
    return app.window()


def connect_pid(pid):
    total_delay = 0
    interval_delay = 2
    max_delay = 30
    app: Application = None
    while total_delay < max_delay:
        try:
            app = Application(backend="uia").connect(
                process=pid, timeout=1, retry_interval=0.5
            )
            # if app.window().exists():
            #     return app.window()
        except pywinauto.ElementNotFoundError:
            time.sleep(interval_delay)
            total_delay += interval_delay
            pass
        else:
            if app.window().exists():
                return app.window()
            else:
                time.sleep(interval_delay)
                total_delay += interval_delay
                continue
        if total_delay >= max_delay:
            break
    return app.window()


def test_connect_to_window_via_pid():
    connect_to_window_via_pid(process_name="browser.exe").child_window(
        title="I'll stay with Cốc Cốc", control_type="Button"
    ).click()


def test_connect_to_window_via_pid2():
    connect_to_window_via_pid(
        process_name="CocCocUpdate.exe"
    ).print_control_identifiers()


def test_print():
    version = "104.1.1.1"
    print(version.split(".")[0])


def enter_command_cmd(command: str, sleep_n_seconds: int =1) -> None:
    open_cmd_pywinauto()
    keyboard.send_keys(command, with_spaces=True)
    keyboard.send_keys("{ENTER}")
    time.sleep(sleep_n_seconds)


def open_cmd_pywinauto():
    app: Application = None
    try:
        kill_process_by_name("cmd.exe")
        app = Application().start(
            r"C:\Windows\System32\cmd.exe /k",
            create_new_console=True,
            wait_for_idle=False,
            timeout=setting.timeout_pywinauto,
            retry_interval=1,
        )
        time.sleep(2)
    finally:
        return app.window().set_focus()


def test_open_cmd_pywinauto():
    cmd = open_cmd_pywinauto()

    cmd.type_keys("coccoc://settings/defaultBrowser{ENTER}")
    # close_cmd()


def test_close_cmd():
    close_cmd(title_re="Administrator")


def close_cmd(title_re, timeout=setting.timeout_pywinauto):
    try:
        cmd_window = Application(backend="uia").connect(
            class_name="ConsoleWindowClass", title_re=title_re, timeout=timeout
        )
        cmd_window.window().close()
    except Exception as e:
        # cmd_window.window().set_focus().close()
        raise e


def delete_all_coccoc_update_task_schedule():
    faulthandler.disable()
    command1 = rf'SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineCore'
    command2 = rf'SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineUA'
    cmd = open_cmd_pywinauto()
    try:
        """Using send_keys method"""
        # pywinauto.keyboard.send_keys(command)
        # keyboard.send_keys(command1, with_spaces=True)
        # pywinauto.keyboard.send_keys('{ENTER}')
        # time.sleep(1)
        # pywinauto.keyboard.send_keys('y')
        # time.sleep(1)
        # pywinauto.keyboard.send_keys('{ENTER}')

        """Using type_keys method for faster"""
        cmd.type_keys(command1, with_spaces=True)
        cmd.type_keys("{ENTER}", with_spaces=True)
        time.sleep(0.3)
        cmd.type_keys("y{ENTER}", with_spaces=True)
        time.sleep(0.3)

        """Using send_keys method"""
        # keyboard.send_keys(command2, with_spaces=True)
        # pywinauto.keyboard.send_keys('{ENTER}')
        # time.sleep(1)
        # pywinauto.keyboard.send_keys('y')
        # time.sleep(1)
        # pywinauto.keyboard.send_keys('{ENTER}')

        """Using type_keys method for faster"""
        cmd.type_keys(command2, with_spaces=True)
        cmd.type_keys("{ENTER}", with_spaces=True)
        time.sleep(0.3)
        cmd.type_keys("y{ENTER}", with_spaces=True)
        time.sleep(0.3)

    finally:
        # close_cmd()
        kill_process_by_name("cmd.exe")


def test_delete_all_coccoc_update_task_schedule():
    delete_all_coccoc_update_task_schedule()


def delete_all_coccoc_update_task_schedule2():
    faulthandler.disable()
    command1 = r'SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineCore'
    command2 = r'SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineUA'

    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if is_admin():
        # subprocess.run(['SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineCore'], capture_output=True, text=True, input="y")
        #
        # subprocess.run(['SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineUA'], capture_output=True, text=True, input="y")
        foo_proc = subprocess.Popen(
            [r'SCHTASKS /DELETE /TN "CocCocUpdateTaskMachineCore'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        foo_proc.communicate("y\n")

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def test_delete_all_coccoc_update_task_schedule2():
    delete_all_coccoc_update_task_schedule2()


def delete_all_coccoc_update_services():
    faulthandler.disable()
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if is_admin():
        subprocess.run(
            "sc stop coccoc", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        subprocess.run(
            "sc delete coccoc", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        subprocess.run(
            "sc stop coccocm", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        subprocess.run(
            "sc delete coccocm", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        subprocess.run(
            "sc stop CocCocElevationService",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        subprocess.run(
            "sc delete CocCocElevationService",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def test_delete_all_coccoc_update_services():
    delete_all_coccoc_update_services()


# To close Settings
def close_windows_settings():
    try:
        kill_process_by_name("SystemSettings.exe")
    except Exception:
        pass
    time.sleep(1)


def test_start_windows_settings():
    start_windows_settings()


def start_windows_settings(is_close_after_started_again=True):
    if is_close_after_started_again:
        close_windows_settings()
    os.system("start ms-settings:")
    time.sleep(2)


def turn_proxy_on():
    cmd_windows = open_cmd_pywinauto()
    try:
        enable_proxy = rf'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1'
        # set_proxy = "netsh winhttp import proxy source=ie"
        set_proxy = "netsh winhttp set proxy 127.0.0.1:9090"

        cmd_windows.type_keys(enable_proxy, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        cmd_windows.type_keys("y{ENTER}", with_spaces=True)
        time.sleep(2)

        cmd_windows.type_keys(set_proxy, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        time.sleep(3)
    finally:
        kill_process_by_name("cmd.exe")
    time.sleep(1)


def turn_proxy_off():
    cmd_windows = open_cmd_pywinauto()
    clear_all = "netsh winhttp reset proxy"
    try:
        disable_proxy = rf'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0'
        cmd_windows.type_keys(disable_proxy, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        cmd_windows.type_keys("y{ENTER}", with_spaces=True)
        time.sleep(2)
        cmd_windows.type_keys(clear_all, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        time.sleep(3)
    finally:
        kill_process_by_name("cmd.exe")
    time.sleep(1)


def test_on_off_proxy():
    turn_proxy_on()
    time.sleep(10)
    turn_proxy_off()


def check_registry_exist(query: str) -> bool:
    # 'reg query HKEY_CURRENT_USER\Software\CocCoc'
    out_put = None
    try:
        out_put = subprocess.check_output(query, encoding="utf-8", timeout=2)
    except Exception:
        pass
    if out_put is not None:
        if "ERROR" in out_put:
            return False
        else:
            return True
    else:
        return True


def test_check_registry_exist():
    print(check_registry_exist(query="reg query HKEY_CURRENT_USER\Software\CocCoc"))


def get_real_arch():
    return platform.architecture()[0]


def test_get_real_arch():
    print(get_real_arch())


def test_get_clipboard_text():
    print(get_clipboard_text())


def get_clipboard_text() -> str:
    """To get the content of current lastest clipboard

    Returns:
        str: value
    """
    root = tk.Tk()
    text = root.clipboard_get()
    root.withdraw()
    root.update()
    root.destroy()
    return text


def is_window_explorer_appeared(
    window_name: str, timeout=setting.timeout, is_close_after_found=False
) -> bool:
    is_appeared = False
    interval_delay = 0.5
    total_delay = 0
    app = None
    while total_delay < timeout:
        try:
            app = Application(backend="uia").connect(
                class_name="CabinetWClass",
                control_type=50032,
                title=window_name,
                timeout=0.5,
                found_index=0,
            )
            if app is not None:
                is_appeared = True
                if is_close_after_found:
                    app.window().child_window(
                        title="Close", auto_id="Close", control_type=5000
                    ).wait("visible").double_click_input(button="left")
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            break
    if total_delay >= timeout:
        print(
            f"Timeout for waiting the Windows Explorer appear after {total_delay} seconds"
        )
    return is_appeared


def restart_background_intellignet_transfer():
    cmd_windows = open_cmd_pywinauto()
    try:
        # stop_service = r'sc stop BITS'
        # start_service = r'sc start BITS'
        stop_service = r'net stop "Background Intelligent Transfer Service"'
        start_service = r'net start "Background Intelligent Transfer Service"'
        cmd_windows.type_keys(stop_service, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        time.sleep(6)
        cmd_windows.type_keys(start_service, with_spaces=True)
        cmd_windows.type_keys("{ENTER}", with_spaces=True)
        time.sleep(6)
    finally:
        kill_process_by_name("cmd.exe")
        time.sleep(1)


def check_the_proxy_setting_show():
    try:
        app = Application(backend="uia").connect(
            class_name="ApplicationFrameWindow",
            control_type=50032,
            title="Settings",
            timeout=setting.timeout_pywinauto,
            found_index=0,
        )
    except Exception as e:
        raise e
    else:
        if get_windows_version() == "10":
            assert (
                app.window()
                .child_window(
                    title="Automatic proxy setup",
                    control_type=50020,
                    class_name="TextBlock",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
        else:
            assert (
                app.window()
                .child_window(
                    title="Proxy",
                    control_type=50000,
                    class_name="Microsoft.UI.Xaml.Controls.BreadcrumbBarItem",
                )
                .wait("visible", timeout=setting.timeout_pywinauto)
                .is_visible()
                is True
            )
    finally:
        app.window().wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).set_focus().close()


# To check the file is exist or not
def is_file_exists(file_name_with_path):
    """To check the file is existed or not
    Args:
        file_name_with_path (_type_): full path to the file with its name
    Returns:
        _type_: _description_
    """
    my_file = Path(file_name_with_path)
    if my_file.is_file():
        return True
    else:
        return False


def get_real_system_arch(is_format=True):
    """
    to get real system arch (not from setting config)
    Args:
        is_format: return '_x64' or '' else return '64bit' or '32bit'
    Returns:
    """
    platform_architecture = platform.architecture()[0]
    if is_format:
        if platform_architecture == "64bit":
            return "_x64"
        else:
            return ""
    else:
        return platform_architecture
