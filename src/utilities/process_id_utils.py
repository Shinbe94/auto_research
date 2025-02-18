import subprocess
import time

import psutil
import win32gui
import win32process


def test_is_process_running():
    print(is_process_running(process_name="setup.exe"))


def is_process_running(process_name: str) -> bool:
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# def test_process():
#     print(is_process_running('cmd.exe'))


def pid_by_name(process_name):
    list_of_process_objects = []
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=["pid", "name"])
            if process_name.lower() in process_info["name"].lower():
                list_of_process_objects.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_process_objects


# if is_process_running("Excel"):
#     listOfProcessIds = pid_by_name("Excel")
#     if len(listOfProcessIds) > 0:
#         for i in listOfProcessIds:
#             processID = i["pid"]
#             # print(processID)


def is_process_running_by_subprocess(process_name: str) -> bool:
    results = subprocess.check_output(["tasklist"], universal_newlines=True)

    if any(line.startswith(process_name) for line in results.splitlines()):
        return True
    else:
        return False


def test_is_process_running_by_subprocess():
    print(is_process_running_by_subprocess(process_name="browser.exe"))


def get_running_process(process_name):
    list_of_process_objects = []
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=["pid", "name"])
            if process_name.lower() in process_info["name"].lower():
                list_of_process_objects.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if len(list_of_process_objects) > 0:
        for process in list_of_process_objects:
            process_id = process["pid"]
            return process_id
    # return list_of_process_objects


def get_running_processes(process_name):
    list_of_process_objects = []
    list_pids = []
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=["pid", "name"])
            if process_name.lower() in process_info["name"].lower():
                list_of_process_objects.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # if len(list_of_process_objects) > 0:
    #     for process in list_of_process_objects:
    #         # process_id = process['pid']
    #         list_pids.append(process['pid'])
    #         # return process_id
    return list_of_process_objects


def test_get_running_processes():
    print(get_running_process("chrome.exe"))


def get_window_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def get_running_process_ids(
    process_name, timeout=20, is_need_wait_process_started=True
):
    if is_need_wait_process_started:
        is_process_started = False
        max_delay = timeout
        interval_delay = 1
        total_delay = 0
        # start_time = time.time()
        while not is_process_started:
            if is_process_running_by_subprocess(process_name):
                is_process_started = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for wait for process get started")
                break
        # print('time elapse = ' + str(time.time() - start_time))
    list_of_process_objects = []
    list_of_process_ids = []
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=["pid", "name"])
            if process_name.lower() in process_info["name"].lower():
                list_of_process_objects.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if len(list_of_process_objects) > 0:
        for process in list_of_process_objects:
            list_of_process_ids.append(process["pid"])

    return list_of_process_ids


def test_get_running_process_ids():
    print(get_running_process_ids(process_name="browser.exe"))


def get_process_ids_by_name(process_name: str):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    list_of_process_objects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if process_name.lower() in pinfo["name"].lower():
                list_of_process_objects.append(pinfo["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_process_objects


def test_get_process_ids_by_name():
    print(get_process_ids_by_name("cmd.exe"))
    print(get_process_ids_by_name("browser.exe"))


def check_process_is_running_by_its_id(pid: int) -> bool:
    """
    To check is the process running by given id
    :param pid:
    :return:
    """
    if psutil.pid_exists(pid):
        return True
    else:
        return False
