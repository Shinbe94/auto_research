import ftplib
import getpass
import os
import platform

import ftputil

from src.utilities import string_number_utils, file_utils
from tests import setting


def get_username():
    return getpass.getuser()


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


def get_files(
    folder_version, platform=setting.platform, ftp_server=setting.ftp_server_local
):
    with ftputil.FTPHost(
        ftp_server, user="anonymous", passwd="", session_factory=ftplib.FTP
    ) as ftp_host:
        if platform == "64bit":
            remote_folder = folder_version + "_x64"
            files = ftp_host.listdir(path=f"/corom/{remote_folder}/installers/")
            local_path = f"C:\\Users\\{get_username()}\\Downloads\\{remote_folder}"
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            for file in files:
                local_file_name = os.path.join(local_path, file)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file}",
                    target=local_file_name,
                )
        else:
            remote_folder = folder_version
            files = ftp_host.listdir(path=f"/corom/{remote_folder}/installers/")
            local_path = f"C:\\Users\\{get_username()}\\Downloads\\{remote_folder}"
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            for file in files:
                local_file_name = os.path.join(local_path, file)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file}",
                    target=local_file_name,
                )
        ftp_host.close()


def get_file(
    folder_version,
    file_to_download_for_test,
    platform=setting.platform,
    ftp_server=setting.ftp_server_local,
):
    with ftputil.FTPHost(
        ftp_server, user="anonymous", passwd="", session_factory=ftplib.FTP
    ) as ftp_host:
        if int(string_number_utils.substring_before_char(folder_version, ".")) < 93:
            remote_folder = folder_version
            local_path = f"C:\\Users\\{get_username()}\\Downloads"
            local_file_name = os.path.join(local_path, file_to_download_for_test)
            ftp_host.download(
                source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                target=local_file_name,
            )
        else:
            if platform == "64bit":
                remote_folder = folder_version + "_x64"
                local_path = f"C:\\Users\\{get_username()}\\Downloads"
                local_file_name = os.path.join(local_path, file_to_download_for_test)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                    target=local_file_name,
                )
            else:
                remote_folder = folder_version
                local_path = f"C:\\Users\\{get_username()}\\Downloads"
                local_file_name = os.path.join(local_path, file_to_download_for_test)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                    target=local_file_name,
                )
        ftp_host.close()


def get_file2(
    folder_version, file_to_download_for_test, ftp_server=setting.ftp_server_local
):
    with ftputil.FTPHost(
        ftp_server, user="anonymous", passwd="", session_factory=ftplib.FTP
    ) as ftp_host:
        if int(string_number_utils.substring_before_char(folder_version, ".")) < 93:
            remote_folder = folder_version
            local_path = rf"C:\Users\{get_username()}\Downloads\corom\{folder_version}\installers"
            local_file_name = os.path.join(local_path, file_to_download_for_test)
            # print(local_file_name)
            ftp_host.download(
                source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                target=local_file_name,
            )
        else:
            if get_window_arch(is_formatted=False) == "64bit":
                remote_folder = folder_version + "_x64"
                local_path = rf"C:\Users\{get_username()}\Downloads\corom\{folder_version}{get_window_arch()}\installers"
                local_file_name = os.path.join(local_path, file_to_download_for_test)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                    target=local_file_name,
                )
            else:
                remote_folder = folder_version
                local_path = rf"C:\Users\{get_username()}\Downloads\corom\{folder_version}{get_window_arch()}\installers"
                local_file_name = os.path.join(local_path, file_to_download_for_test)
                ftp_host.download(
                    source=f"/corom/{remote_folder}/installers/{file_to_download_for_test}",
                    target=local_file_name,
                )
        ftp_host.close()


def get_list_available_incremental_builds(
    folder_version=setting.coccoc_test_version,
    platform=setting.platform,
    ftp_server=setting.ftp_server_local,
):
    list_builds = []
    with ftputil.FTPHost(
        ftp_server, user="anonymous", passwd="", session_factory=ftplib.FTP
    ) as ftp_host:
        if int(string_number_utils.substring_before_char(folder_version, ".")) < 93:
            remote_folder = folder_version
            ftp_host.chdir(f"/corom/{remote_folder}/installers/")
            names = ftp_host.listdir(ftp_host.curdir)
            if len(names) > 0:
                for name in names:
                    if "coccocsetup.exe" in name and "from" in name:
                        list_builds.append(name)
        else:
            if platform == "64bit":
                remote_folder = folder_version + "_x64"
                # local_path = f'C:\\Users\\{get_username()}\\Downloads'
                # local_file_name = os.path.join(local_path, file_to_download_for_test)
                # ftp_host.download(source=f'/corom/{remote_folder}/installers/{file_to_download_for_test}',
                #                   target=local_file_name)
                ftp_host.chdir(f"/corom/{remote_folder}/installers/")
                names = ftp_host.listdir(ftp_host.curdir)
                if len(names) > 0:
                    for name in names:
                        if "coccocsetup.exe" in name and "from" in name:
                            list_builds.append(name)
            else:
                remote_folder = folder_version
                ftp_host.chdir(f"/corom/{remote_folder}/installers/")
                names = ftp_host.listdir(ftp_host.curdir)
                if len(names) > 0:
                    for name in names:
                        if "coccocsetup.exe" in name and "from" in name:
                            list_builds.append(name)
        ftp_host.close()
    # print(list_builds)
    return list_builds


def test_get_list_incremental_build():
    get_list_available_incremental_builds()


def penultimate_build():
    last_part = int(setting.coccoc_test_version.split(".")[-1])
    pen_build = (
        setting.coccoc_test_version.split(".")[0]
        + "."
        + setting.coccoc_test_version.split(".")[1]
        + "."
        + setting.coccoc_test_version.split(".")[2]
        + "."
        + str(last_part - 1)
    )
    previous_of_pen_build = (
        setting.coccoc_test_version.split(".")[0]
        + "."
        + setting.coccoc_test_version.split(".")[1]
        + "."
        + setting.coccoc_test_version.split(".")[2]
        + "."
        + str(last_part - 2)
    )
    # print(penultimate_build)
    return pen_build, previous_of_pen_build


def test_print():
    print(penultimate_build())


def download_file_from_FTP(
    source_file_with_path,
    local_path,
    local_file_name,
    ftp_server=setting.ftp_server_remote,
):
    # local_path = rf"C:\Users\{get_username()}\Downloads\corom\{folder_version}{get_window_arch()}\installers"
    local_file_name_with_path = os.path.join(local_path, local_file_name)
    try:
        with ftputil.FTPHost(
            ftp_server,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        ) as ftp_host:
            ftp_host.download(
                source=source_file_with_path,
                target=local_file_name_with_path,
            )
    except Exception as e:
        raise e


def test_download_coccoc_drivers():
    download_coccoc_drivers()


def download_coccoc_drivers(ftp_server=setting.ftp_server_local):
    """Support to download 3 recents coccoc drivers for testing
    e.g: current test build is 116 --> should check driver for build 116, 115, 114, 113
    """
    list_driver_versions = setting.old_coccoc_version
    list_driver_versions.append(setting.coccoc_test_version)
    list_driver_versions = set(list_driver_versions)
    for version in list_driver_versions:
        if not file_utils.check_folder_is_exists(
            directory_with_path=f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}_x64"
        ):
            file_utils.create_folder_os_make_dir(
                f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}_x64"
            )
            file_utils.create_folder_os_make_dir(
                f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}"
            )
            # Execute copy coccoc_driver win64&32

            download_file_from_FTP(
                source_file_with_path=f"/corom/{version}_x64/chromedriver.exe",
                local_path=f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}_x64",
                local_file_name="chromedriver.exe",
                ftp_server=ftp_server,
            )
            download_file_from_FTP(
                source_file_with_path=f"/corom/{version}/chromedriver.exe",
                local_path=f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}",
                local_file_name="chromedriver.exe",
                ftp_server=ftp_server,
            )
        else:
            if not file_utils.check_file_is_exists(
                f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}_x64\\chromedriver.exe"
            ):
                download_file_from_FTP(
                    source_file_with_path=f"/corom/{version}_x64/chromedriver.exe",
                    local_path=f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}_x64",
                    local_file_name="chromedriver.exe",
                    ftp_server=ftp_server,
                )
            if not file_utils.check_file_is_exists(
                f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}\\chromedriver.exe"
            ):
                download_file_from_FTP(
                    source_file_with_path=f"/corom/{version}/chromedriver.exe",
                    local_path=f"C:\\Users\\{get_username()}\\.wdm\\drivers\\coccocdriver\\{version}",
                    local_file_name="chromedriver.exe",
                    ftp_server=ftp_server,
                )


def download_setup_file_to_local(version: str = setting.coccoc_test_version):
    remote_folders = [version + "_x64", version]
    try:
        with ftputil.FTPHost(
            host=setting.ftp_server_local,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        ) as ftp_host_local:
            if remote_folders[0] in ftp_host_local.listdir(
                path=f"/corom/"
            ) and remote_folders[1] in ftp_host_local.listdir(path=f"/corom/"):
                copy_build(ftp_host_local, remote_folder=remote_folders[0])
                with ftputil.FTPHost(
                    host=setting.ftp_server_local,
                    user="anonymous",
                    passwd="",
                    session_factory=ftplib.FTP,
                ) as other_connection:
                    copy_build(other_connection, remote_folder=remote_folders[1])

            else:
                if ftp_host_local:
                    ftp_host_local.close()

                with ftputil.FTPHost(
                    host=setting.ftp_server_remote,
                    user="anonymous",
                    passwd="",
                    session_factory=ftplib.FTP,
                ) as ftp_host_remote:
                    copy_build(ftp_host_remote, remote_folder=remote_folders[0])
                    ftp_host_remote.close()
                with ftputil.FTPHost(
                    host=setting.ftp_server_remote,
                    user="anonymous",
                    passwd="",
                    session_factory=ftplib.FTP,
                ) as ftp_host_remote:
                    copy_build(ftp_host_remote, remote_folder=remote_folders[1])
                    ftp_host_remote.close()

        if ftp_host_local:
            ftp_host_local.close()
    except Exception:
        with ftputil.FTPHost(
            host=setting.ftp_server_remote,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        ) as ftp_host_remote:
            copy_build(ftp_host_remote, remote_folder=remote_folders[0])
            ftp_host_remote.close()
        with ftputil.FTPHost(
            host=setting.ftp_server_remote,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        ) as ftp_host_remote:
            copy_build(ftp_host_remote, remote_folder=remote_folders[1])
            ftp_host_remote.close()


def copy_build(connection: ftputil.FTPHost, remote_folder):
    files = connection.listdir(path=f"/corom/{remote_folder}/installers/")
    local_path = (
        f"C:\\Users\\{get_username()}\\Downloads\\corom\\{remote_folder}\\installers"
    )
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    for file in files:
        local_file_name = os.path.join(local_path, file)
        if not file_utils.check_file_is_exists(local_file_name):
            connection.download(
                source=f"/corom/{remote_folder}/installers/{file}",
                target=local_file_name,
            )
    connection.close()


def test_download_needed_builds():
    download_needed_builds()


def download_needed_builds():
    list_missing_builds = file_utils.list_missing_builds()
    list_minors = get_list_minor_builds_need_to_download()
    list_need_to_download: list = list_missing_builds + list_minors
    # print(list_need_to_download)
    # for version in list_need_to_download:
    #     copy_build2(connection=connect_ftp_local(), remote_folder=version)


def connect_ftp_remote() -> ftputil.FTPHost:
    try:
        ftp_connection = ftputil.FTPHost(
            host=setting.ftp_server_remote,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        )
    except Exception:
        pass
    else:
        return ftp_connection


def connect_ftp_local() -> ftputil.FTPHost:
    try:
        ftp_connection = ftputil.FTPHost(
            host=setting.ftp_server_local,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        )
    except Exception:
        pass
    else:
        return ftp_connection


def copy_build2(connection: ftputil.FTPHost, remote_folder):
    """Trying to copy from FTP local, if not -> copy from FTP remote
    Args:
        connection (ftputil.FTPHost): FTP connection
        remote_folder (_type_): the folder at FTP site
    """
    if remote_folder in connection.listdir(path="/corom/"):
        try:
            copy_files_from_ftp(connection, remote_folder)
        finally:
            connection.close()
    else:
        connection.close()
        new_connection = connect_ftp_remote()
        if remote_folder in new_connection.listdir(path="/corom/"):
            try:
                copy_files_from_ftp(new_connection, remote_folder)
            finally:
                new_connection.close()
        else:
            new_connection.close()


def test_copy_build2():
    copy_build2(connection=connect_ftp_local(), remote_folder="85.0.4183.146")


def copy_files_from_ftp(connection: ftputil.FTPHost, remote_folder):
    files = connection.listdir(path=f"/corom/{remote_folder}/installers/")
    local_path = (
        f"C:\\Users\\{get_username()}\\Downloads\\corom\\{remote_folder}\\installers"
    )
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    # copy builds
    for file in files:
        local_file_name = os.path.join(local_path, file)
        if not file_utils.check_file_is_exists(local_file_name):
            connection.download(
                source=f"/corom/{remote_folder}/installers/{file}",
                target=local_file_name,
            )
    # if not file_utils.check_file_is_exists(
    #     f"C:\\Users\\{get_username()}\\Downloads\\corom\\{remote_folder}\\chromedriver.exe"
    # ):
    #     connection.download(
    #         source=f"/corom/{remote_folder}/installers/{file}",
    #         target=f"C:\\Users\\{get_username()}\\Downloads\\corom\\{remote_folder}\\chromedriver.exe",
    #     )


def test_get_all_minor_version_of_the_testing_builds_from_ftp():
    get_all_minor_version_of_the_testing_builds_from_ftp()


def get_all_minor_version_of_the_testing_builds_from_ftp(
    build_version=setting.coccoc_test_version,
) -> list:
    list_all = []
    major_build = build_version.split(".")[0]
    with ftputil.FTPHost(
        host=setting.ftp_server_remote,
        user="anonymous",
        passwd="",
        session_factory=ftplib.FTP,
    ) as ftp_host_remote:
        list_all = ftp_host_remote.listdir(path=f"/corom/")
        ftp_host_remote.close()
    list_filter_major = list(filter(lambda x: x.startswith(f"{major_build}"), list_all))
    return list_filter_major


def get_list_minor_builds_need_to_download() -> list:
    major_build = int(setting.coccoc_test_version.split(".")[0])
    if major_build > max(file_utils.get_all_major_old_builds()):
        return get_all_minor_version_of_the_testing_builds_from_ftp()
    else:
        return []


def test_get_all_latest_minor_builds():
    print(get_all_latest_minor_builds())


def get_all_latest_minor_builds() -> list:
    list_all = []
    try:
        with ftputil.FTPHost(
            host=setting.ftp_server_remote,
            user="anonymous",
            passwd="",
            session_factory=ftplib.FTP,
        ) as ftp_host_remote:
            list_all = ftp_host_remote.listdir(path=f"/corom/")
            ftp_host_remote.close()
        list_versions = list(filter(lambda x: "_x64" in x, list_all))
        list_major_versions = list(
            set(list(map(lambda x: int(x.split(".")[0]), list_versions)))
        )
        max_major_version = str(max(list_major_versions))
        return list(filter(lambda x: x.startswith(max_major_version), list_all))
    except Exception:
        return []


def test_get_latest_build_from_ftp():
    print(get_latest_build_from_ftp())


def get_latest_build_from_ftp() -> int:
    list_all = []
    with ftputil.FTPHost(
        host=setting.ftp_server_remote,
        user="anonymous",
        passwd="",
        session_factory=ftplib.FTP,
    ) as ftp_host_remote:
        list_all = ftp_host_remote.listdir(path=f"/corom/")
        ftp_host_remote.close()
    list_versions = list(filter(lambda x: "_x64" in x, list_all))
    list_major_versions = list(
        set(list(map(lambda x: int(x.split(".")[0]), list_versions)))
    )
    return max(list_major_versions)


def delete_unused_build(
    directory=f"C:\\Users\\{get_username()}\\Downloads\\corom",
):
    """Get list unused builds then delete all of them to free up disk
    Note: should ignore all current latest builds
    Args:
        directory (_type_, optional): _description_. Defaults to.
    """
    list_latest_minor_builds: list = get_all_latest_minor_builds()
    if len(list_latest_minor_builds) > 0:
        list_applicale_builds_for_test: list = []
        list_applicale_builds_for_test = (
            setting.very_old_coccoc_version
            + setting.old_coccoc_version
            + [element + "_x64" for element in setting.old_coccoc_version]
            + list_latest_minor_builds
        )

        list_builds_in_downloaded_folders = file_utils.list_all_files_and_folders(
            directory=directory
        )

        list_builds_to_delete = [
            element
            for element in list_builds_in_downloaded_folders
            if element not in list_applicale_builds_for_test
        ]
        for build in list_builds_to_delete:
            file_utils.remove_directory(directory=directory + "//" + build)
