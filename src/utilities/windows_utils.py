import sys
import time
from win32gui import FindWindow, PostMessage, GetWindowRect
import win32.lib.win32con as win32con
import win32gui
from time import sleep
from tests import setting


class WindowNotFound(Exception):
    ...


def find_window_by_name(window_name: str, class_name=None) -> int:
    """find a window by its name and class_name"""
    handle: int = FindWindow(class_name, window_name)
    if handle == 0:
        raise WindowNotFound(f"'{window_name}' is not found!")
    return handle


def close_window_by_handle(handle: int) -> None:
    PostMessage(handle, win32con.WM_CLOSE, 0, 0)


def close_window_by_its_name(window_name: str, class_name: None) -> None:
    try:
        handle = find_window_by_name(window_name, class_name)
        PostMessage(handle, win32con.WM_CLOSE, 0, 0)
    except WindowNotFound:
        raise (f"'{window_name}' is not found!")


def get_window_size(window_name: str) -> tuple:
    """Return the location and size of the window

    Args:
        window_name (str): _description_

    Raises:
        e: _description_

    Returns:
        tuple: _description_
    """
    try:
        window_handle: list = find_window_handle(
            title=window_name, is_exact_name=False, timeout=4
        )
        window_rect = GetWindowRect(window_handle[0])
        x = window_rect[0]
        y = window_rect[1]
        w = window_rect[2] - x
        h = window_rect[3] - y
        return x, y, w, h
    except Exception as e:
        raise e


def test_get_window_size():
    # print(
    #     get_window_size(
    #         window_name="New Tab - Cốc Cốc", class_name="Chrome_WidgetWin_1"
    #     )
    # )
    print(get_window_size(window_name="Automatically close after"))


def test_find_window_handle():
    assert (
        len(find_window_handle(title="Sourcetree", is_exact_name=True, timeout=2)) == 1
    )


def test_find_window_handle2():
    assert len(find_window_handle(title="Sourcetree")) == 1


def find_window_handle(title: str, is_exact_name=False, timeout: float = 1.0) -> list:
    handleList = []

    def _findit(hwnd, ctx):
        try:
            if is_exact_name:
                if win32gui.GetWindowText(hwnd) == title:
                    handleList.append(hwnd)
            else:
                if title in win32gui.GetWindowText(hwnd):
                    handleList.append(hwnd)
        except Exception as e:
            raise e

    win32gui.EnumWindows(_findit, None)
    return handleList


def get_all_windows(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        # print(hex(hwnd), win32gui.GetWindowText(hwnd))
        # list_window = win32gui.GetWindowText(hwnd)
        print(win32gui.GetWindowText(hwnd))
        # return win32gui.GetWindowText(hwnd)


def test_():
    win32gui.EnumWindows(get_all_windows, None)
