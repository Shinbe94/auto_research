# Get version folder of coccoc (first folder under Application folder)
import ctypes
import ftplib
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pywinauto import Application

import chromedriver_autoinstaller
import ftputil
from packaging import version
from selenium import webdriver

# Chrome
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOptions

from tests import setting
from src.utilities import file_utils, process_id_utils, os_utils
from src.pages.coccoc_common import open_browser, interactions_windows


def test_get_coccoc_version_folder_name_system_mode():
    print(get_coccoc_version_folder_name_system_mode())


def get_coccoc_version_folder_name_system_mode():
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        coccoc_install_location = "C:\\Program Files\\CocCoc\\Browser\\Application"
    else:
        coccoc_install_location = (
            "C:\\Program Files (x86)\\CocCoc\\Browser\\Application"
        )
    folder_names = []
    versions = []
    for entry_name in os.listdir(coccoc_install_location):
        entry_path = os.path.join(coccoc_install_location, entry_name)
        if os.path.isdir(entry_path):
            folder_names.append(entry_name)
    for i in folder_names:
        version_format = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", i)
        if len(version_format) > 0:
            versions.append(i)
    for n, i in enumerate(versions):
        versions[n] = version.parse(i)
    return str(max(versions))
    # return str(folder_names[0])
    # return versions


def get_os_arch():
    return platform.architecture()[0]


def get_coccoc_installation_location():
    if os.path.isdir(r"C:\\Program Files\\CocCoc\\Browser\\Application"):
        return r"C:\\Program Files\\CocCoc\\Browser\\Application", "64bit"
    elif os.path.isdir(r"C:\\Program Files (x86)\\CocCoc\\Browser\\Application"):
        return r"C:\\Program Files (x86)\\CocCoc\\Browser\\Application", "32bit"
    else:
        return False


def get_browser_version_formatted():
    temp1 = get_coccoc_version_folder_name_system_mode()
    # temp2 = temp1.replace('.', '_')
    return temp1


def get_uid_formatted():
    shutil.copy(
        f"C:\\ProgramData\\CocCoc\\uid", f"C:\\ProgramData\\CocCoc\\uid" + ".txt"
    )
    file_path = f"C:\\ProgramData\\CocCoc\\uid.txt"
    with open(file_path) as f:
        lines = f.readlines()
        output_text = lines[0]
        # uid_formatted = output_text.replace('-', '_')
    os.remove(f"C:\\ProgramData\\CocCoc\\uid.txt")
    return output_text


def get_coccoc_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = os_utils.get_platform_architecture()
    if platform == "linux":
        path = get_linux_executable_path()
        with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
            version = (
                proc.stdout.read()
                .decode("utf-8")
                .replace("Chromium", "")
                .replace("Google Chrome", "")
                .strip()
            )
    elif platform == "mac":
        process = subprocess.Popen(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--version",
            ],
            stdout=subprocess.PIPE,
        )
        version = (
            process.communicate()[0]
            .decode("UTF-8")
            .replace("Google Chrome", "")
            .strip()
        )
    elif platform == "win":
        process = subprocess.Popen(
            # ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            [
                "reg",
                "query",
                "HKEY_CURRENT_USER\\Software\\CocCoc\\Browser\\BLBeacon",
                "/v",
                "version",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        output = process.communicate()
        if output:
            version = output[0].decode("UTF-8").strip().split()[-1]
        else:
            process = subprocess.Popen(
                [
                    "powershell",
                    "-command",
                    "$(Get-ItemProperty -Path Registry::HKEY_CURRENT_USER\\Software\\CocCoc\\Browser\\BLBeacon).version",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            version = process.communicate()[0].decode("UTF-8").strip()
    else:
        return
    return version


def get_version_of_coccoc():
    if (
        file_utils.check_file_is_exists(setting.coccoc_binary_64bit)
        or file_utils.check_file_is_exists(setting.coccoc_binary_32bit)
        or file_utils.check_file_is_exists(
            f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
        )
    ):
        process = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\CocCoc\Browser\BLBeacon" /v version',
            encoding="utf-8",
        )
        # print(process.strip().split()[-1])
        return process.strip().split()[-1]
    else:
        return None


def test_coccoc_ver():
    print(get_version_of_coccoc())


def get_linux_executable_path():
    """
    Look through a list of candidates for Google Chrome executables that might
    exist, and return the full path to first one that does. Raise a ValueError
    if none do.

    :return: the full path to a Chrome executable on the system
    """
    for executable in (
        "google-chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-dev",
        "chromium-browser",
        "chromium",
    ):
        path = shutil.which(executable)
        if path is not None:
            return path
    raise ValueError("No chrome executable found on PATH")


def get_chrome_executable_path():
    if file_utils.check_file_is_exists(setting.chrome_binary_64bit):
        return setting.chrome_binary_64bit
    else:
        return setting.chrome_binary_32bit


def kill_all_coccoc_crash_handler():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if os_utils.is_admin():
        if process_id_utils.is_process_running("CocCocCrashHandler.exe"):
            # subprocess.check_output('taskkill /im CocCocCrashHandler.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocCrashHandler.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocCrashHandler.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running("CocCocCrashHandler64.exe"):
            # subprocess.check_output('taskkill /im CocCocCrashHandler64.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocCrashHandler64.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocCrashHandler64.exe")
            time.sleep(0.5)

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def kill_all_coccoc_process():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if os_utils.is_admin():
        if process_id_utils.is_process_running("CocCocUpdate.exe"):
            # subprocess.check_output('taskkill /im CocCocUpdate.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocUpdate.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocUpdate.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running("CocCocCrashHandler.exe"):
            # subprocess.check_output('taskkill /im CocCocCrashHandler.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocCrashHandler.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocCrashHandler.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running("CocCocCrashHandler64.exe"):
            # subprocess.check_output('taskkill /im CocCocCrashHandler64.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocCrashHandler64.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocCrashHandler64.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running("CocCocTorrentUpdate.exe"):
            # subprocess.check_output('taskkill /im CocCocTorrentUpdate.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocTorrentUpdate.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("CocCocTorrentUpdate.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running("browser.exe"):
            # subprocess.check_output('taskkill /im browser.exe /f')
            # subprocess.check_output('taskkill /f /im browser.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("browser.exe")
            time.sleep(0.5)
        if process_id_utils.is_process_running(process_name="setup.exe"):
            # subprocess.check_output('taskkill /im setup.exe /f')
            # subprocess.check_output('taskkill /f /im setup.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("setup.exe")
            time.sleep(0.5)
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def test_kill_all_coccoc_process():
    kill_all_coccoc_process()


def kill_chrome_process():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if os_utils.is_admin():
        if process_id_utils.is_process_running("chrome.exe"):
            # subprocess.check_output('taskkill /im CocCocUpdate.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocUpdate.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("chrome.exe")

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def kill_brave_process():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    if os_utils.is_admin():
        if process_id_utils.is_process_running("brave.exe"):
            # subprocess.check_output('taskkill /im CocCocUpdate.exe /f')
            # subprocess.check_output('taskkill /f /im CocCocUpdate.exe 2>&1 | exit /B 0')
            os_utils.kill_process_by_name("brave.exe")

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def test_check_coccoc_firewall_rules():
    check_coccoc_firewall_rules()


# To check all firewall rules for coccoc are here!
def check_coccoc_firewall_rules():
    firewall_rules_coccoc_cmd = "netsh advfirewall firewall show Rule Name=all"
    try:
        list_rules = subprocess.check_output(
            firewall_rules_coccoc_cmd, encoding="utf-8", errors="ignore"
        )
    except UnicodeDecodeError:
        try:
            list_rules = subprocess.check_output(
                firewall_rules_coccoc_cmd, encoding="latin-1"
            )
        except UnicodeDecodeError:
            list_rules = subprocess.check_output(
                firewall_rules_coccoc_cmd, encoding="ISO-8859-1"
            )
    assert "C?c C?c (TCP-Out)" in list_rules
    assert "C?c C?c (UDP-Out)" in list_rules
    assert "C?c C?c (TCP-In)" in list_rules
    assert "C?c C?c (UDP-In)" in list_rules
    assert "C?c C?c (mDNS-In)" in list_rules
    # assert 'C?c C?c Torrent Update (UDP-In)' in list_rules
    # assert 'C?c C?c Torrent Update (TCP-In)' in list_rules
    # assert 'C?c C?c Torrent Update (UDP-Out)' in list_rules
    # assert 'C?c C?c Torrent Update (TCP-Out)' in list_rules


def test_check_no_coccoc_firewall_rules():
    check_no_coccoc_firewall_rules()


# To check all firewall rules for coccoc is removed
def check_no_coccoc_firewall_rules():
    firewall_rules_coccoc_cmd = r"netsh advfirewall firewall show Rule Name=all"
    try:
        list_rules = subprocess.check_output(
            firewall_rules_coccoc_cmd, encoding="utf-8", errors="ignore"
        )
    except UnicodeDecodeError:
        try:
            list_rules = subprocess.check_output(
                firewall_rules_coccoc_cmd, encoding="latin-1"
            )
        except UnicodeDecodeError:
            list_rules = subprocess.check_output(
                firewall_rules_coccoc_cmd, encoding="ISO-8859-1"
            )
    # print(list_rules)
    assert "C?c C?c (TCP-Out)" not in list_rules
    assert "C?c C?c (UDP-Out)" not in list_rules
    assert "C?c C?c (TCP-In)" not in list_rules
    assert "C?c C?c (UDP-In)" not in list_rules
    assert "C?c C?c (mDNS-In)" not in list_rules
    # assert 'C?c C?c Torrent Update (UDP-In)' in list_rules
    # assert 'C?c C?c Torrent Update (TCP-In)' in list_rules
    # assert 'C?c C?c Torrent Update (UDP-Out)' in list_rules
    # assert 'C?c C?c Torrent Update (TCP-Out)' in list_rules


def test_check_no_coccoc_firewall_rules():
    check_no_coccoc_firewall_rules()


# To convert from chromium-build to coccoc-build
# e.g: 104.0.5112.84 --> 110.0.84


def chromium_version_to_coccoc_version(chromium_version=setting.coccoc_test_version):
    # text = string_number_utils.substring_before_char('104.0.5112.84', '.')
    result = re.split("\\.", chromium_version)
    coccoc_version = str(int(result[0]) + 6) + "." + result[1] + "." + result[3]
    return coccoc_version


def test_substr():
    print(chromium_version_to_coccoc_version())


def get_coccoc_update_folder() -> str:
    if file_utils.check_folder_is_exists("C:\\Program Files (x86)\\CocCoc\\Update"):
        return "C:\\Program Files (x86)\\CocCoc\\Update"
    else:
        return "C:\\Program Files\\CocCoc\\Update"


def get_coccoc_folder() -> str:
    if file_utils.check_folder_is_exists("C:\\Program Files (x86)\\CocCoc"):
        return "C:\\Program Files (x86)\\CocCoc"
    else:
        return "C:\\Program Files\\CocCoc"


def get_current_browser_and_current_omaha_version():
    current_coccoc_version = get_coccoc_version()
    current_omaha_version = file_utils.list_all_files_and_folders(
        get_coccoc_update_folder()
    )[0]
    return current_coccoc_version, current_omaha_version


def get_active_omaha_version():
    version_list = []
    text_list = file_utils.list_all_files_and_folders(get_coccoc_update_folder())
    for text in text_list:
        version_format = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", text)

        if len(version_format) > 0:
            version_list.append(version_format[0])
    for n, i in enumerate(version_list):
        version_list[n] = version.parse(i)
    return str(max(version_list))


def test_active_omaha_version():
    print(get_active_omaha_version())


def test_get_latest_omaha_from_ftp():
    get_latest_omaha_from_ftp()


def get_latest_omaha_from_ftp():
    with ftputil.FTPHost(
        setting.ftp_server_remote,
        user="anonymous",
        passwd="",
        session_factory=ftplib.FTP,
    ) as ftp_host:
        version_list = []
        ftp_host.chdir(f"/corom/omaha/")
        text_list = ftp_host.listdir(ftp_host.curdir)
        for text in text_list:
            version_format = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", text)
            if len(version_format) > 0:
                version_list.append(version_format[0])

        # print(version_list)
        for n, i in enumerate(version_list):
            version_list[n] = version.parse(i)
        # print(str(max(version_list)))
        return str(max(version_list))


def get_uid():
    file_path = f"C:\\Users\\{os_utils.get_username()}\\AppData\\Roaming\\CocCoc\\uid"
    with open(file_path) as f:
        lines = f.readlines()
        output_text = lines[0]
    return output_text


def test_get_uid():
    print(get_uid())


def get_hid3():
    file_path = f"C:\\Users\\{os_utils.get_username()}\\AppData\\Roaming\\CocCoc\\hid3"
    with open(file_path) as f:
        lines = f.readlines()
        output_text = lines[0]
    return output_text


def test_get_hid3():
    print(get_hid3())


def get_current_coccoc_language() -> str:
    driver: WebDriver = None
    current_coccoc_language: str = None
    try:
        coccoc = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium()
        driver = coccoc[0]
        current_coccoc_language = coccoc[2]
    except Exception as e:
        raise e
    else:
        # To remove/format for 'en-US'...
        if "en" in current_coccoc_language:
            current_coccoc_language = "en"
    finally:
        interactions_windows.close_coccoc_at_new_tab(language=current_coccoc_language)
        if driver is not None:
            driver.quit()
    return current_coccoc_language


def test_get_current_coccoc_language():
    print(get_current_coccoc_language())


def kill_all_coccoc_process2():
    if process_id_utils.is_process_running("CocCocUpdate.exe"):
        subprocess.check_call("taskkill /im CocCocUpdate.exe /f")
        time.sleep(0.5)
    if process_id_utils.is_process_running("CocCocCrashHandler.exe"):
        subprocess.check_call("taskkill /im CocCocCrashHandler.exe /f")
        time.sleep(0.5)
    if process_id_utils.is_process_running("CocCocCrashHandler64.exe"):
        subprocess.check_call("taskkill /im CocCocCrashHandler64.exe /f")
        time.sleep(0.5)
    if process_id_utils.is_process_running("CocCocTorrentUpdate.exe"):
        subprocess.check_call("taskkill /im CocCocTorrentUpdate.exe /f")
        time.sleep(0.5)
    if process_id_utils.is_process_running("browser.exe"):
        subprocess.check_call("taskkill /im browser.exe /f")
        time.sleep(0.5)
    if process_id_utils.is_process_running("setup.exe"):
        subprocess.check_call("taskkill /im setup.exe /f")
        time.sleep(0.5)


def get_coccoc_major_build() -> int:
    major_build = setting.coccoc_test_version.split(".")[0]
    return int(major_build)


def test_get_coccoc_major_build():
    print(get_coccoc_major_build())


def get_coccoc_executable_path() -> str:
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        return setting.coccoc_binary_64bit
    elif file_utils.check_file_is_exists(setting.coccoc_binary_32bit):
        return setting.coccoc_binary_32bit
    elif file_utils.check_file_is_exists(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
    ):
        return f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\Application\\browser.exe"
    else:
        raise ValueError("No CocCoc Installted")


def get_winappdriver_executable_path() -> str:
    if file_utils.check_file_is_exists(
        "C:\\Program Files (x86)\\Windows Application Driver\\WinAppDriver.exe"
    ):
        return "C:\\Program Files (x86)\\Windows Application Driver\\WinAppDriver.exe"
    elif file_utils.check_file_is_exists(
        "C:\\Program Files\\Windows Application Driver\\WinAppDriver.exe"
    ):
        return "C:\\Program Files\\Windows Application Driver\\WinAppDriver.exe"
    else:
        raise ValueError("No winappdriver installed")


def test_create_new_browser_profile():
    create_new_browser_profile()


def create_new_browser_profile(
    profile_name: str = "Profile 1", is_close_then=True
) -> None:
    """To create a new profile by command line
    Args:
        profile_name (str, optional): Name of the profile. Defaults to "Profile 1". convention name: 'Profile 1', 'Profile 2'
        is_close_then (bool, optional): Close the Window after create. Defaults to True.
    Raises:s
        e: Any exception
    """
    try:
        # subprocess.run(
        #     rf"{get_coccoc_executable_path()}"
        #     + rf' --profile-directory="{profile_name}"'
        # )
        app = Application(backend="uia").start(
            get_coccoc_executable_path() + rf' --profile-directory="{profile_name}"',
            timeout=setting.timeout_pywinauto,
        )
        time.sleep(2)
        app.window().wait(
            "exists enabled visible ready",
            timeout=setting.timeout_pywinauto,
            retry_interval=1,
        ).maximize()
        if is_close_then:
            app.window().close()
    except Exception as e:
        raise e


def get_coccoc_driver_executable_path() -> str:
    """Return the path of coccoc driver by current installed coccoc version

    Returns:
        str: Full file name with path
    """
    current_cc_major_version = get_version_of_coccoc().split(".")[0]
    if int(current_cc_major_version) <= 114:
        return f"C:\\Users\\{os_utils.get_username()}\\.wdm\\drivers\\coccocdriver\\{get_version_of_coccoc()}\\chromedriver.exe"
    else:
        # if setting.platform == "64bit":
        if os_utils.get_real_system_arch(is_format=False) == "64bit":
            return f"C:\\Users\\{os_utils.get_username()}\\.wdm\\drivers\\coccocdriver\\{get_version_of_coccoc()}_x64\\chromedriver.exe"
        else:
            return f"C:\\Users\\{os_utils.get_username()}\\.wdm\\drivers\\coccocdriver\\{get_version_of_coccoc()}\\chromedriver.exe"


def test_delete_file_offscreen_cashback_extension():
    delete_file_offscreen_cashback_extension()


def delete_file_offscreen_cashback_extension() -> None:
    """This method is for deleting the file 'offscreen.html' of Cashback extension
    to prevent it affect to playwright
    from V116 we have problem while open cc = playwright
    this page: chrome-extension://afaljjbleihmahhpckngondmgohleljb/offscreen.html leads to error
    """
    list_file_dir = file_utils.list_files_n_folders_from_directory(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb"
    )

    if len(list_file_dir) > 0:
        # Move file offscreen.html to Documents
        if file_utils.check_file_is_exists(
            f"C:\\Users\\{os_utils.get_username()}\\Documents\\offscreen.html"
        ):
            file_utils.remove_a_file(
                f"C:\\Users\\{os_utils.get_username()}\\Documents\\offscreen.html"
            )
        file_utils.move_file(
            source_file_with_path=f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb\\{list_file_dir[0]}\\offscreen.html",
            dest_file_with_path=f"C:\\Users\\{os_utils.get_username()}\\Documents",
        )
        # Remove all file offscreen.html if any
        for dir in list_file_dir:
            if file_utils.check_file_is_exists(
                f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb\\{dir}\\offscreen.html"
            ):
                file_utils.remove_a_file(
                    f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb\\{dir}\\offscreen.html"
                )


def copy_back_file_offscreen_cashback_extension() -> None:
    """This method is for revert the file 'offscreen.html' of Cashback extension
    to prevent it affect to playwright
    from V116 we have problem while open cc = playwright
    this page: chrome-extension://afaljjbleihmahhpckngondmgohleljb/offscreen.html leads to error
    """
    list_file_dir = file_utils.list_files_n_folders_from_directory(
        f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb"
    )
    # copy back and delete offscreen.html at Documents
    if len(list_file_dir) > 0:
        try:
            for dir in list_file_dir:
                if not file_utils.check_file_is_exists(
                    f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb\\{dir}\\offscreen.html"
                ):
                    file_utils.copy_single_file(
                        src_path=f"C:\\Users\\{os_utils.get_username()}\\Documents\\offscreen.html",
                        dst_path=f"C:\\Users\\{os_utils.get_username()}\\AppData\\Local\\CocCoc\\Browser\\User Data\\Default\\Extensions\\afaljjbleihmahhpckngondmgohleljb\\{dir}\\offscreen.html",
                    )
        finally:
            file_utils.remove_a_file(
                f"C:\\Users\\{os_utils.get_username()}\\Documents\\offscreen.html"
            )
