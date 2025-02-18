import ctypes
import filecmp
import glob
import json
import logging
import os
import re
import shutil
import stat
import sys
import time
from typing import List
import zipfile
from datetime import datetime
from pathlib import Path

import win32api
from pymediainfo import MediaInfo
from pywinauto import Application
from pywinauto.keyboard import send_keys

from src.utilities import os_utils, browser_utils
from tests import setting


def remove_dir():
    coccoc_location = f"C:\\Program Files\\CocCoc"
    os.chmod(coccoc_location, 0o777)
    cd_to_local_appdata = r"cd C:\\Program Files"
    remove_coc_coc_folder = "rmdir /S /Q CocCoc"
    os.system(cd_to_local_appdata + remove_coc_coc_folder)


# deletes a directory and all its contents.
def remove_directory(directory):
    if check_folder_is_exists(directory):
        try:
            shutil.rmtree(path=directory)
        except Exception as e:
            raise e


def test_remove_directory():
    remove_directory(directory=str(get_project_root()) + rf"\data\application_upgrade")


# To remove a file with exact name
def remove_file(file_name_with_path):
    if check_file_is_exists(file_name_with_path):
        try:
            os.remove(file_name_with_path)
        except Exception as e:
            raise e


def test_remove_files_re():
    remove_files_re(
        directory=r"C:\Users\Taynq\Documents\automation\test1", filename_re="Copy"
    )


# To remove some files with contain same name
def remove_files_re(directory: str, filename_re: str) -> None:
    list_files = list_all_files_and_folders(directory)
    files = []
    for file in list_files:
        if filename_re.lower() in file.lower():
            files.append(file)

    for file in files:
        if check_file_is_exists(directory + rf"\{file}"):
            try:
                os.remove(directory + rf"\{file}")
            except Exception as e:
                raise e


# To check the folder is existed or not
def check_folder_is_exists(directory_with_path):
    """To check the folder is exited or not

    Args:
        directory_with_path (_type_): full path to the folder/directory

    Returns:
        _type_: _description_
    """
    if os.path.isdir(directory_with_path):
        return True
    else:
        return False


# To check the file is exist or not
def check_file_is_exists(file_name_with_path):
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


# To check the folder is empty
def is_folder_empty(path):
    if any(os.scandir(path)):
        return False


# To compare 2 folders
def compare_dir_layout(dir1, dir2):
    def _compare_dir_layout(dir1, dir2):
        for dir_path, dir_names, filenames in os.walk(dir1):
            for filename in filenames:
                relative_path = dir_path.replace(dir1, "")
                if not os.path.exists(dir2 + relative_path + "\\" + filename):
                    print(relative_path, filename)
        return

    print('files in "' + dir1 + '" but not in "' + dir2 + '"')
    _compare_dir_layout(dir1, dir2)
    print('files in "' + dir2 + '" but not in "' + dir1 + '"')
    _compare_dir_layout(dir2, dir1)


# To get project root directory
def get_project_root() -> Path:
    # print(Path(__file__).parent.parent)
    return Path(__file__).parent.parent.parent


# Rename file python
def rename_file_host():
    os.rename(
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
        "C:\\Windows\\System32\\drivers\\etc\\hosts_",
    )


def revert_file_host():
    os.rename(
        "C:\\Windows\\System32\\drivers\\etc\\hosts_",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
    )


def copy_file_host():
    # shutil.copyfile(Path(get_project_root() + '\\data\\hosts'), 'C:\\Windows\\System32\\drivers\\etc\\')
    temp_str = str(get_project_root()) + r"\data\host_file\hosts"
    source = Path(temp_str)
    destination = "C:\\Windows\\System32\\drivers\\etc\\hosts"
    shutil.copyfile(source, destination)


def remove_file_host():
    os.remove("C:\\Windows\\System32\\drivers\\etc\\hosts")


def test_rename_and_copy_file_host():
    rename_and_copy_file_host()


# To copy file hosts_for_test
def rename_and_copy_file_host():
    # Check file hosts is exist?
    if check_file_is_exists("C:\\Windows\\System32\\drivers\\etc\\hosts"):
        # Rename 'hosts' to 'hosts_'
        try:
            os.rename(
                "C:\\Windows\\System32\\drivers\\etc\\hosts",
                "C:\\Windows\\System32\\drivers\\etc\\hosts_",
            )
        except FileExistsError:
            pass
        time.sleep(1)
        # Copy file 'hosts' for test
        temp_str = str(get_project_root()) + r"\src\data\host_file\hosts"
        source = Path(temp_str)
        destination = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        shutil.copyfile(source, destination)
        time.sleep(1)
    else:
        # Copy file 'hosts' for test
        temp_str = str(get_project_root()) + r"\src\data\host_file\hosts"
        source = Path(temp_str)
        destination = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        shutil.copyfile(source, destination)
        time.sleep(1)


def test_remove_and_revert_file_host():
    remove_and_revert_file_host()


def test_file_hosts():
    rename_and_copy_file_host()
    time.sleep(4)
    remove_and_revert_file_host()


# To remove file hosts_for_test and revert the previous file hosts
def remove_and_revert_file_host():
    # Check file hosts is exist?
    if check_file_is_exists("C:\\Windows\\System32\\drivers\\etc\\hosts_"):
        os.remove("C:\\Windows\\System32\\drivers\\etc\\hosts")
        time.sleep(1)
        os.rename(
            "C:\\Windows\\System32\\drivers\\etc\\hosts_",
            "C:\\Windows\\System32\\drivers\\etc\\hosts",
        )
        time.sleep(1)
    else:
        if check_file_is_exists("C:\\Windows\\System32\\drivers\\etc\\hosts"):
            os.remove("C:\\Windows\\System32\\drivers\\etc\\hosts")
            time.sleep(1)


# To delete the installer files after downloaded
def delete_installer_downloaded(build_name="CocCocSetup"):
    downloaded_folder = f"C:\\Users\\{os_utils.get_username()}\\Downloads"
    os.chmod(downloaded_folder, 0o777)  # Change permission
    for filename in glob.glob(downloaded_folder + "\\" + build_name + "*"):
        os.remove(filename)


# To delete all installer files after testing
def delete_all_installer_downloaded():
    downloaded_folder = f"C:\\Users\\{os_utils.get_username()}\\Downloads"
    os.chmod(downloaded_folder, 0o777)  # Change permission
    for filename in glob.glob(downloaded_folder + "\\" + "CocCocSetup" + "*"):
        os.remove(filename)
    for filename in glob.glob(downloaded_folder + "\\" + "standalone_" + "*"):
        os.remove(filename)
    for filename in glob.glob(downloaded_folder + "\\" + "*" + "coccocsetup" + "*"):
        os.remove(filename)


def test_delete_all_installer_downloaded():
    delete_all_installer_downloaded()


# To delete the installer files after downloaded
def delete_build_by_name(build_name="CocCocSetup"):
    downloaded_folder = f"C:\\Users\\{os_utils.get_username()}\\Downloads"
    os.chmod(downloaded_folder, 0o777)  # Change permission
    for filename in glob.glob(downloaded_folder + "\\" + build_name + "*"):
        os.remove(filename)


def test_delete_build_by_name():
    delete_build_by_name()


def delete_file():
    downloaded_folder = (
        f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
    )
    os.chmod(downloaded_folder, stat.S_IWRITE)
    # shutil.rmtree(downloaded_folder)
    os.remove(downloaded_folder)


def remove_a_file(file_name: str):
    """Check if the file exist, remove it

    Args:
        file_name (star): file name with path
    """
    if check_file_is_exists(file_name):
        os.remove(file_name)


# To remove all files in the folder (Keep the folder existing)
def remove_all_files_in_folder(directory):
    if check_folder_is_exists(directory_with_path=directory):
        shutil.rmtree(path=directory)
        create_folder(directory)


def test_remove_all_files_in_folder():
    remove_all_files_in_folder(
        str(get_project_root()) + rf"\data\application_upgrade\SetupMetrics"
    )


def create_folder(directory):
    if not os.path.exists(directory):
        os.mkdir(path=directory, mode=0o777)


def test_create_folder():
    temp_str = str(get_project_root()) + r"\data\abc"
    source = Path(temp_str)
    create_folder(directory=source)


def create_folder_os_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_application_folder_to_new_folder(
    folder_name, previous_browser_build, is_open_folder_before_copying=False
):
    if check_file_is_exists(setting.coccoc_binary_64bit):
        if is_open_folder_before_copying:
            open_folder_application_directory(
                r"C:\Program Files\CocCoc\Browser\Application", previous_browser_build
            )
        os.chmod(r"C:\Program Files\CocCoc\Browser\Application", 0o777)
        if check_file_is_exists(str(get_project_root()) + rf"\data\{folder_name}"):
            remove_directory(str(get_project_root()) + rf"\data\{folder_name}")
        shutil.copytree(
            src=r"C:\Program Files\CocCoc\Browser\Application",
            dst=str(get_project_root()) + rf"\data\{folder_name}",
            dirs_exist_ok=True,
        )
    elif check_file_is_exists(setting.coccoc_binary_32bit):
        if is_open_folder_before_copying:
            open_folder_application_directory(
                r"C:\Program Files (x86)\CocCoc\Browser\Application",
                previous_browser_build,
            )
        os.chmod(r"C:\Program Files (x86)\CocCoc\Browser\Application", 0o777)
        if check_file_is_exists(str(get_project_root()) + rf"\data\{folder_name}"):
            remove_directory(str(get_project_root()) + rf"\data\{folder_name}")
        shutil.copytree(
            src=r"C:\Program Files (x86)\CocCoc\Browser\Application",
            dst=str(get_project_root()) + rf"\data\{folder_name}",
            dirs_exist_ok=True,
        )
    else:
        print("No coccoc installed")


def test_copy_folder_to_folder():
    copy_application_folder_to_new_folder(folder_name="test")


def check_folder_is_empty(directory):
    if len(os.listdir(directory)) == 0:
        return True
    else:
        return False


def test_check_folder_is_empty():
    print(
        check_folder_is_empty(directory=r"C:\Program Files (x86)\CocCoc\Update\2.9.1.9")
    )


def test_list_all_files_folders():
    # print(list_all_files_and_folders(directory=r"C:\Program Files (x86)\CocCoc\Update"))
    print(
        list_all_files_and_folders(
            directory=rf"C:\\Users\\{os_utils.get_username()}\\Downloads"
        )
    )


# Return as list
def list_all_files_and_folders(directory: str) -> List[str]:
    """To list all files and folder from a directory
    Args:
        directory (str): folder path
    Returns:
        list: list files and folder
    """
    txt_files = []
    if check_folder_is_exists(directory):
        txt_files = os.listdir(directory)
        return txt_files
    else:
        return txt_files


def test_props():
    print(
        get_file_properties(
            r"C:\Program Files (x86)\CocCoc\Update\2.7.1.25\CocCocUpdate.exe",
            property_name="ProductVersion",
        )
    )
    print(
        get_file_properties_by_cmd(
            r"C:\\Program Files (x86)\\CocCoc\\Update\\2.7.1.25\\CocCocUpdate.exe",
            property_name="Version",
        )
    )

    # print(get_file_properties(r'C:\Program Files (x86)\CocCoc\Update\2.7.1.25\CocCocUpdate.exe'))


def get_file_properties(file_name, property_name=None):
    # ==============================================================================
    """
    Read all properties of the given file return them as a dictionary.
    """
    prop_names = (
        "Comments",
        "InternalName",
        "ProductName",
        "CompanyName",
        "LegalCopyright",
        "ProductVersion",
        "FileDescription",
        "LegalTrademarks",
        "PrivateBuild",
        "FileVersion",
        "OriginalFilename",
        "SpecialBuild",
        "Size",
        "Type",
        "DateModified",
    )

    props = {"FixedFileInfo": None, "StringFileInfo": None, "FileVersion": None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixed_info = win32api.GetFileVersionInfo(file_name, "\\")
        props["FixedFileInfo"] = fixed_info
        props["FileVersion"] = "%d.%d.%d.%d" % (
            fixed_info["FileVersionMS"] / 65536,
            fixed_info["FileVersionMS"] % 65536,
            fixed_info["FileVersionLS"] / 65536,
            fixed_info["FileVersionLS"] % 65536,
        )

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(
            file_name, "\\VarFileInfo\\Translation"
        )[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        str_info = {}
        for prop_name in prop_names:
            str_info_path = "\\StringFileInfo\\%04X%04X\\%s" % (
                lang,
                codepage,
                prop_name,
            )
            # print(str_info_path)
            ## print str_info
            str_info[prop_name] = win32api.GetFileVersionInfo(file_name, str_info_path)
        print(str_info)
        return str_info[property_name]

        # print(str_info.get(property_name))
        # props['StringFileInfo'] = str_info
    except:
        pass
    # if property_name is not None:
    #     print(props[property_name])


# support property_name: Description,FileName,FileType,FileSize,Version,Name,Extension
def get_file_properties_by_cmd(file_location, property_name):
    # wmic datafile where Name="C:\\Program Files (x86)\\CocCoc\\Update\\2.7.1.25\\CocCocUpdate.exe" get Description,
    # FileName,FileType,FileSize,Version,Name,Extension
    # property_value = None
    string_command = (
        rf'wmic datafile where Name="{file_location}"' + rf" get {property_name}"
    )
    os.system(string_command + " > output.txt")
    with open("output.txt", "r", encoding="utf-16") as f:
        lines = f.readlines()
        f.close()
        property_value = lines[1]
    os.remove("output.txt")
    return property_value


# def delete_all_files_in_folder


import subprocess


def get_length(filename):
    # result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
    #                          "format=duration", "-of",
    #                          "default=noprint_wrappers=1:nokey=1", filename],
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.STDOUT, shell=True)
    # result = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
    #                          "format=duration", "-of",
    #                          "default=noprint_wrappers=1:nokey=1", filename],
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.STDOUT, shell=True)

    # return result.stdout.splitlines()[-1]

    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
        shell=True,
    ).decode()
    fields = json.loads(result)["streams"][0]

    duration = int(float(fields["duration"]))
    fps = eval(fields["r_frame_rate"])
    # return duration, fps
    hrs, mins, secs = duration // 60 // 60, duration // 60 % 60, duration % 60

    hrs = "0" + str(hrs) if (hrs < 10) else str(hrs)
    mins = "0" + str(mins) if (mins < 10) else str(mins)
    secs = "0" + str(secs) if (secs < 10) else str(secs)
    length = hrs + ":" + mins + ":" + secs
    # return duration, frame_count
    return length


def with_opencv(filename):
    import cv2

    video = cv2.VideoCapture(filename)

    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    hrs, mins, secs = duration // 60 // 60, duration // 60 % 60, duration % 60

    hrs = "0" + str(hrs) if (hrs < 10) else str(hrs)
    mins = "0" + str(mins) if (mins < 10) else str(mins)
    secs = "0" + str(secs) if (secs < 10) else str(secs)
    length = hrs + ":" + mins + ":" + secs
    # return duration, frame_count
    return length


def test_duration():
    # print(get_length(r'C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3'))
    # print(with_opencv(r'C:\\Users\\taynq\\Downloads\\a.mp4'))
    print(
        get_media_duration(
            r"C:\\Users\\taynq\\Downloads\\LÊ HÀ TRÚC -KỂ XẤU- BẠN TRAI VÀ BẬT MÍ -BÍ KÍP GIA TRUYỀN- GIÚP DA CHỐNG LÃO HOÁ.mp4"
        )
    )
    print(
        get_media_duration(
            r"C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3"
        )
    )
    print(get_media_duration(r"C:\\Users\\taynq\\Downloads\\AnhLoChoEmHet.mp3"))


def get_media_duration(file_name):
    clip_info = MediaInfo.parse(file_name)
    duration_ms = clip_info.tracks[0].duration / 1000
    duration_format = convert_seconds_to_hour_minute_second(int(duration_ms))
    # print(clip_info.tracks)
    return duration_format


def convert_seconds_to_hour_minute_second(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def get_extension_of_file(filename):
    file_ext = re.search(r"\.([^.]+)$", filename).group(1)
    # file_ext = filename.rpartition(".")[-1]
    # print(file_ext)
    return file_ext


def test_file_extension():
    get_extension_of_file(
        r"C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3"
    )


def compare_2_folders(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
    """

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if (
        len(dirs_cmp.left_only) > 0
        or len(dirs_cmp.right_only) > 0
        or len(dirs_cmp.funny_files) > 0
    ):
        return False
    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
    if len(mismatch) > 0 or len(errors) > 0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not compare_2_folders(new_dir1, new_dir2):
            return False
    return True


def test_copy_and_compare(
    folder1="application_upgrade", folder2="application_fresh_install"
):
    # copy_application_folder_to_new_folder(folder_name=folder1)
    # copy_application_folder_to_new_folder(folder_name=folder2)
    try:
        assert (
            compare_2_folders(
                dir1=str(get_project_root()) + rf"\data\{folder1}",
                dir2=str(get_project_root()) + rf"\data\{folder2}",
            )
            is True
        )
    finally:
        print("hihi")
        # remove_directory(directory=str(get_project_root()) + rf'\data\{folder1}')
        # remove_directory(directory=str(get_project_root()) + rf'\data\{folder2}')


def open_directory(path, is_closed=True):
    Application(backend="uia").start("explorer.exe " + path, timeout=10)
    time.sleep(3)
    if is_closed:
        send_keys("%{F4}")


def open_folder_application_directory(path, application_version, is_closed=True):
    # Open the folder
    Application(backend="uia").start("explorer.exe " + path, timeout=10)
    # Wait for the application_version is disappeared automatically
    if wait_for_application_version_directory_disappeared(
        application_version=application_version
    ):
        if is_closed:
            send_keys("%{F4}")


def wait_for_application_version_directory_disappeared(
    application_version, timeout=setting.timeout_pywinauto
):
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    is_disappeared = False

    while not is_disappeared:
        if check_file_is_exists(setting.coccoc_binary_64bit):
            list_files_folders_in_application_64 = list_all_files_and_folders(
                r"C:\Program Files\CocCoc\Browser\Application"
            )
            if application_version not in list_files_folders_in_application_64:
                is_disappeared = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for wait for folder {application_version} disappeared")
                break

        # Check for build 32 bit
        else:
            list_files_folders_in_application_32 = list_all_files_and_folders(
                r"C:\Program Files (x86)\CocCoc\Browser\Application"
            )
            if application_version not in list_files_folders_in_application_32:
                is_disappeared = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for wait for folder {application_version} disappeared")
                break
    return is_disappeared


def test_open_directory(path="C:\\Program Files\\CocCoc\\Browser\\Application\\"):
    open_folder_application_directory(path)

    # app.window(title_re='.*Application$').print_control_identifiers()
    # print(process_id_utils.get_window_pid('Application'))
    # app[r'C:\\Program Files\\CocCoc\\Browser\\Application'].print_control_identifiers()
    # interactions_windows.close_explorer_by_its_title(title='*Application')


def wait_for_file_downloaded():
    download_path = rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\"
    max_delay = 300
    interval_delay = 1
    total_delay = 0
    file = ""
    is_download_done = True
    while is_download_done:
        files = [f for f in os.listdir(download_path) if f.endswith(".crdownload")]
        if not files and len(file) > 1:
            is_download_done = False
            break
        if files:
            file = files[0]
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay > max_delay:
            is_download_done = True
            print("Time out while downloading the file")
            break
    if not is_download_done:
        logging.error("File(s) couldn't be downloaded")
    time.sleep(1)
    # print(download_path + '\\' + file.replace(".crdownload", ""))
    return download_path + "\\" + file.replace(".crdownload", "")


def zip_all_files(zip_name, format_file, root_dir, base_dir):
    try:
        shutil.make_archive(
            base_name=zip_name, format=format_file, root_dir=root_dir, base_dir=base_dir
        )
    except Exception as e:
        raise e


def test_zip():
    zip_all_files(
        zip_name=rf'WIN_PERFORMANCE_RESULT_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}',
        format_file="zip",
        root_dir=str(get_project_root()) + r"\tests\performance_test\test_result",
        base_dir=str(get_project_root()) + r"\tests\performance_test\test_result",
    )


def zip_dir(directory):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    zf = zipfile.ZipFile("myzipfile.zip", "w")
    list_files = list_all_files_and_folders(directory)
    for files in list_files:
        zf.write(str(directory + rf"\{files}"))
    zf.close()


def test_zip_dir():
    zip_dir(str(get_project_root()) + r"\tests\performance_test\test_result")


# Zip all file with no path added
def zip_all_file_with_no_path_added(filename, dir_path):
    zipf = zipfile.ZipFile(file=filename, mode="w")
    len_dir_path = len(dir_path)
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path[len_dir_path:])
    zipf.close()


def test_zip_dir2():
    zip_all_file_with_no_path_added(
        filename="sample.zip",
        dir_path=str(get_project_root()) + r"\tests\performance_test\test_result",
    )


def wait_for_file_exist(file_name_with_path: str, timeout: int = 30):
    """
    To wait for the particular file is created OK
    Args:
        file_name_with_path: the absolute path
        timeout: default 30 s
    Returns: bool
    """
    interval_delay = 1
    total_delay = 0
    is_existed = False
    while total_delay < timeout:
        if check_file_is_exists(file_name_with_path):
            is_existed = True
            break
        time.sleep(interval_delay)
        total_delay += interval_delay

    return is_existed


def copy_all_files_of_folder(source_folder: str, destination_folder: str):
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = source_folder + file_name
        destination = destination_folder + file_name
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)


def copy_single_file(src_path: str, dst_path: str):
    if check_file_is_exists(src_path):
        shutil.copy(src_path, dst_path)


def test_remove_all_crash_dump():
    remove_all_crash_dump(
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports"
    )


def is_admin_right() -> bool:
    """
    Checking the admin privilege
    :return:
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_all_crash_dump(directory: str):
    # closing all coccoc crash handler
    browser_utils.kill_all_coccoc_crash_handler()
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    filelist = [f for f in os.listdir(directory) if f.endswith(".dmp")]
    if is_admin_right():
        for f in filelist:
            os.remove(os.path.join(directory, f))
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def check_downloading_file_in_download_directory(
    file_name, directory, timeout=30
) -> bool:
    """
    To Check the file is downloaded or not, by checking its name on downloads' folder
    :param file_name: the name of downloading file
    :param directory: download directory
    :param timeout: 30 seconds, for small file size
    :return: bool
    """
    interval_delay = 1
    total_delay = 0
    is_existed = False
    while total_delay < timeout:
        list_files_name = list_all_files_and_folders(directory)
        try:
            if file_name in list_files_name:
                is_existed = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if total_delay >= timeout:
        print(rf"timeout for waiting download is done after {total_delay} seconds")
    return is_existed


def check_crdownload_existed(
    directory=rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\",
    timeout=setting.timeout_for_waiting_the_download_is_started,
) -> bool:
    """
    To check the file is starting downloading by check the extension '.crdownload' appears on the download folder
    Note: We need to make sure there is no related '.crdownloaded' existed on the checking folder before calling this function
    :param directory: download direactory
    :param timeout:
    :return: True if started and False if timeout comes
    """
    interval_delay = 0.1
    total_delay = 0
    is_started_download = False
    while total_delay < timeout:
        list_files_name = list_all_files_and_folders(directory)
        try:
            for file in list_files_name:
                if file.endswith(".crdownload"):
                    is_started_download = True
                    break  # Break for loop
        except Exception:
            pass
        if is_started_download:
            break  # Break while loop
        time.sleep(interval_delay)
        total_delay += interval_delay
    return is_started_download


def wait_for_file_downloaded2(
    timeout=setting.timeout_for_waiting_download_big_file_size,
    download_path: str = rf"C:\\Users\\{os_utils.get_username()}\\Downloads\\",
):
    is_download_done = False
    file = ""
    if check_crdownload_existed(download_path):
        interval_delay = 1
        total_delay = 0

        while not is_download_done:
            files = [f for f in os.listdir(download_path) if f.endswith(".crdownload")]
            if not files and len(file) > 1:
                is_download_done = True
                break
            if files:
                file = files[0]
                time.sleep(interval_delay)
                total_delay += interval_delay
            if total_delay > timeout:
                print(
                    rf"Timeout while downloading the file after {total_delay} seconds."
                )
                break
    if not is_download_done:
        logging.error("File(s) couldn't be downloaded")
    # print(download_path + '\\' + file.replace(".crdownload", ""))
    if is_download_done:
        return download_path + "\\" + file.replace(".crdownload", "")


def copy_all_folder_to_folder(src, des):
    """To copy all files and sub-folder to a folder

    Args:
        src (str): path to the source folder
        des (str): path to the destination folder
    """
    shutil.copytree(src, des, dirs_exist_ok=True)


def test_delete_folders_by_regress_name():
    delete_folders_by_regress_name(
        directory=r"C:\Users\taynq_coccoc\Documents\automation\coccoc_win\reports",
        folder_name="2023-09-22",
    )


def delete_folders_by_regress_name(directory, folder_name: str):
    list_folders = list_all_files_and_folders(directory)
    if len(list_folders) > 0:
        for folder in list_folders:
            if folder_name in folder:
                remove_directory(directory=directory + "\\" + folder)


def remove_old_reports(directory, exclude_folder_names) -> None:
    list_folders = list_all_files_and_folders(directory)
    list_folders_to_remove = []
    list_string = " ".join(exclude_folder_names)
    if len(list_folders) > 0:
        for folder_name in list_folders:
            if folder_name[10:][:10] not in list_string:
                list_folders_to_remove.append(folder_name)
    if len(list_folders_to_remove) > 0:
        for folder in list_folders_to_remove:
            remove_directory(directory=directory + "\\" + folder)


def delete_files_by_regress_name_downloads_folder(file_name: str):
    downloaded_folder = f"C:\\Users\\{os_utils.get_username()}\\Downloads"
    os.chmod(downloaded_folder, 0o777)  # Change permission
    for filename in glob.glob(downloaded_folder + "\\" + "*" + file_name + "*"):
        os.remove(filename)


def test_delete_all_file_with_extension():
    delete_all_files_with_same_extension(extension=".parts")


def delete_all_files_with_same_extension(extension: str, directory=None):
    """To delete all file with the same extension
        note: default directory is a system Downloads location
    Args:
        extension (str): _description_
        directory (_type_, optional): _description_. Defaults to None.
    """
    if directory is None:
        directory = rf"C:\\Users\\{os_utils.get_username()}\\Downloads"
    if check_folder_is_exists(directory_with_path=directory):
        for file in list_all_files_and_folders(directory):
            if file.endswith(extension):
                os.remove(directory + rf"\\{file}")


def check_any_file_hold_extension(extension_file: str, directory=None) -> bool:
    """This method is for checking any file holds a particular extension then return boolean
    if extension_file is mp4 --> any file at checking directory hold 'mp4' --> return True else False
    Args:
        extension_file (str): file extension
        directory (_type_, optional): Directory to check. Defaults to None.

    Returns:
        bool: _description_
    """
    is_existed = False
    if directory is None:
        directory = rf"C:\\Users\\{os_utils.get_username()}\\Downloads"
    if check_folder_is_exists(directory_with_path=directory):
        for file in list_all_files_and_folders(directory):
            if file.endswith(extension_file):
                is_existed = True
                break
    return is_existed


def open_a_file(filename_with_path: str) -> None:
    """To open any file from system by default app provided by the system

    Args:
        filename_with_path (str): location to the file
    """
    if check_file_is_exists(file_name_with_path=filename_with_path):
        os.startfile(filename_with_path)


def count_total_regex_folder(folder_name: str, file_name: str) -> int:
    """To the total folder by search like
    for eg: we have 2 folder with name: abc and abc (1) --> result in total will be: 2
    Args:
        folder_name (str): The folder to check
        file_name (str): file_name to count

    Returns:
        int: _description_
    """
    total: int = 0
    if check_folder_is_exists(directory_with_path=folder_name):
        all_files_folders = list_all_files_and_folders(directory=folder_name)
        for file in all_files_folders:
            if file_name in file:
                total += 1
    # print(total)
    return total


def test_count_total_regress_folder():
    count_total_regex_folder(
        folder_name=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\",
        file_name="The WIRED CD - Rip. Sample. Mash. Share",
    )


def edit_file(filename_with_path: str, text: str) -> None:
    if check_file_is_exists(file_name_with_path=filename_with_path):
        with open(filename_with_path, "r+") as f:
            old = f.read()
            f.seek(0)
            f.write(f"{text}\n" + old)


def list_files_n_folders_from_directory(directory: str) -> list:
    """Return list files or directory in a list
    Args:
        directory (str): full directory path
    Returns:
        list: list file name and folder name if any
    """
    list_files_dir = []
    if check_folder_is_exists(directory):
        obj = os.scandir(directory)
        for entry in obj:
            if entry.is_dir() or entry.is_file():
                list_files_dir.append(entry.name)
    return list_files_dir


def list_only_folders_from_directory(directory: str) -> list:
    """Return directory in a list only
    Args:
        directory (str): full directory path
    Returns:
        list: list folders name if any
    """
    list_folders = []
    if check_folder_is_exists(directory):
        obj = os.scandir(directory)
        for entry in obj:
            if entry.is_dir():
                list_folders.append(entry.name)
    return list_folders


def move_file(source_file_with_path: str, dest_file_with_path: str) -> None:
    """Move file from path to new path

    Args:
        source_file_with_path (str): source file with path
        dest_file_with_path (str): dest path
    """
    try:
        shutil.move(source_file_with_path, dest_file_with_path)
    except Exception as e:
        raise e


def get_all_major_old_builds() -> list:
    return list(map(lambda x: int(x.split(".")[0]), setting.old_coccoc_version))


def test_delete_unused_build():
    delete_unused_build()


def delete_unused_build(
    directory=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\corom",
):
    """Get list unused builds then delete all of them to free up disk
    Args:
        directory (_type_, optional): _description_. Defaults to.
    """
    major_build = setting.coccoc_test_version.split(".")[0]
    list_applicale_builds_for_test: list = []
    list_applicale_builds_for_test = (
        setting.very_old_coccoc_version
        + setting.old_coccoc_version
        + [element + "_x64" for element in setting.old_coccoc_version]
    )

    # print(list_applicale_builds_for_test)
    list_builds_in_downloaded_folders = list_all_files_and_folders(directory=directory)
    list_remove_current_major_build = list(
        filter(
            lambda x: not x.startswith(major_build), list_builds_in_downloaded_folders
        )
    )
    list_builds_to_delete = [
        element
        for element in list_remove_current_major_build
        if element not in list_applicale_builds_for_test
    ]
    for build in list_builds_to_delete:
        remove_directory(directory=directory + "//" + build)
    # print(list_builds_to_delete)


def test_get_list_applicale_builds_for_test():
    print(get_list_builds_test_from_setting())


def get_list_builds_test_from_setting(add_x64=True) -> list:
    """List builds get from setting.py
    Returns:
        list: _description_
    """
    list_applicale_builds_for_test: list = []
    if add_x64:
        list_applicale_builds_for_test = (
            setting.very_old_coccoc_version
            + setting.old_coccoc_version
            + [element + "_x64" for element in setting.old_coccoc_version]
        )
    else:
        list_applicale_builds_for_test = (
            setting.very_old_coccoc_version + setting.old_coccoc_version
        )
    return list_applicale_builds_for_test


def list_builds_downloaded_already() -> list:
    list_builds_already_downloaded = list_only_folders_from_directory(
        directory=f"C:\\Users\\{os_utils.get_username()}\\Downloads\\corom"
    )
    # remove _x64 then return list
    return list(filter(lambda x: ("_x64" not in x), list_builds_already_downloaded))


def list_missing_builds() -> list:
    return [
        element
        for element in get_list_builds_test_from_setting()
        if element not in list_builds_downloaded_already()
    ]
