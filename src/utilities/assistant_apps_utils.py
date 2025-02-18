import faulthandler
import time

import pyperclip
import pywinauto.mouse
import webbrowser
from pywinauto import application, Application, keyboard, Desktop
from tests import setting
from src.utilities import file_utils, os_utils, string_number_utils


def test_open_url_by_python():
    # open_url_by_python(url="https://google.com")
    open_url_by_python(
        url="http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion/"
    )


def open_url_by_python(url, sleep_n_seconds: int = 0):
    webbrowser.open(url)
    time.sleep(sleep_n_seconds)


def test_check_default_browser_by_open_link():
    # check_default_browser_by_open_link()
    open_url_by_python(url="https://google.com")
    # app2 = application.Application().connect(title_re="Program Manager",
    #                                          timeout=setting.time_out_pywinauto)
    # app2.window().print_control_identifiers()
    # Desktop(backend="uia").window().print_control_identifiers()
    # print(Desktop(backend="uia").windows())
    for window in Desktop(backend="uia").windows():
        print(window.is_dialog())
        # if window.is_dialog():
        #     print(window.window_text())
        #     window.window().print_control_identifiers()


def check_default_browser_by_open_link():
    try:
        open_url_by_python(url="https://google.com")
    finally:
        app2 = application.Application().connect(
            title_re="Google - Cốc Cốc",
            class_name="Chrome_WidgetWin_1",
            timeout=setting.timeout_pywinauto,
        )
        time.sleep(2)
        app2["Google - Cốc Cốc"].close()
        time.sleep(1)


def check_default_browser_by_click_link_from_notepad_plus_plus():
    os_utils.kill_process_by_name("notepad++.exe")
    app = application.Application()
    try:
        # Open notepad++ and connect to it
        if file_utils.check_file_is_exists(setting.notepad_plus_plus_64_bit):
            app.start(
                setting.notepad_plus_plus_64_bit, timeout=setting.timeout_pywinauto
            )
        else:
            app.start(
                setting.notepad_plus_plus_32_bit, timeout=setting.timeout_pywinauto
            )
        app[".* - Notepad$"].menu_select("File --> New")
        dlg = app[".* - Notepad$"]

        # type and double click to check the default browser
        dlg.Edit.type_keys("https://google.com", with_spaces=True, set_foreground=False)
        time.sleep(1)
        pywinauto.mouse.double_click(button="left", coords=(104, 104))
        time.sleep(3)
        # dlg.print_control_identifiers()
        # x, y = win32api.GetCursorPos()
        # print(x, y)

        # time.sleep(1)
        # dlg.child_window(title="https://google.com", class_name="Scintilla").print_control_identifiers()
        # dlg.child_window(title="https://google.com", class_name="Scintilla").click_input(double=True)
        # Connect to cc browser then close it
    finally:
        app2 = application.Application().connect(
            title_re="Google - Cốc Cốc",
            class_name="Chrome_WidgetWin_1",
            timeout=setting.timeout_pywinauto,
        )
        app2["Google - Cốc Cốc"].close()
        # app2 = application.Application().connect(title_re='Google - Google Chrome', class_name='Chrome_WidgetWin_1', timeout=setting.time_out_pywinauto)
        # app2['Google - Google Chrome'].close()
        time.sleep(3)
        # Clean up and close the notepad++
        app[".* - Notepad$"].menu_select("File --> Close")
        app.Save.No.click_input(button="left")
        app[".* - Notepad$"].close()
    time.sleep(2)


def test_check_default_browser_by_click_link_from_notepad_plus_plus():
    check_default_browser_by_click_link_from_notepad_plus_plus()


def test_start_fiddler():
    start_fiddler()


def start_fiddler():
    faulthandler.disable()
    Application(backend="uia").start(
        rf"C:\Users\{os_utils.get_username()}\AppData\Local\Programs\Fiddler\Fiddler.exe",
        timeout=setting.timeout_pywinauto,
    )
    time.sleep(2)
    max_delay = 5
    interval_delay = 1
    total_delay = 0
    fiddler_title = setting.fiddler_title
    app = Application(backend="uia").connect(
        auto_id="frmViewer",
        control_type=50032,
        title_re=fiddler_title,
        timeout=setting.timeout_pywinauto,
    )
    while total_delay < max_delay:
        try:
            app.window().child_window(
                title="Yes", auto_id="btnYes", control_type=50000
            ).wait("visible", timeout=1).click_input()
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    time.sleep(2)


def get_uninstall_log_by_fiddler():
    faulthandler.disable()
    fiddler_title = setting.fiddler_title
    text_traffic_log = None
    max_delay = 10
    interval_delay = 1
    total_delay = 0
    while total_delay < max_delay:
        try:
            app = Application(backend="uia").connect(
                auto_id="frmViewer",
                control_type=50032,
                title_re=fiddler_title,
                timeout=setting.timeout_pywinauto,
            )
            text_traffic_log = (
                app.window()
                .child_window(title_re="/uninstall", control_type="Text")
                .window_text()
            )
            if text_traffic_log is not None:
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    return text_traffic_log


def check_fiddler_log_after_uninstall_coccoc_browser():
    faulthandler.disable()
    fiddler_title = setting.fiddler_title
    app = None
    try:
        app = Application(backend="uia").connect(
            auto_id="frmViewer",
            control_type=50032,
            title_re=fiddler_title,
            timeout=setting.timeout_pywinauto,
        )
        cc_version = string_number_utils.get_string_between_2_str(
            get_uninstall_log_by_fiddler(), "crversion=", "&os"
        )
        assert cc_version == setting.coccoc_test_version
    finally:
        app.window().close()
        time.sleep(1)


def test_get_metrics_log_by_fiddler():
    get_metrics_log_by_fiddler()


def get_metrics_log_by_fiddler():
    faulthandler.disable()
    fiddler_title = setting.fiddler_title
    is_metrics_log_shown = False
    app = None
    log = None
    try:
        app = Application(backend="uia").connect(
            auto_id="frmViewer",
            control_type=50032,
            # title_re='About Version - Google Chrome',
            title_re=fiddler_title,
            timeout=setting.timeout_pywinauto,
        )
        if is_log_show_fiddler(log_title="metrics.coccoc.com"):
            app[fiddler_title].child_window(
                title="metrics.coccoc.com", control_type="Text", found_index=0
            ).click_input(button="right")
            app["Context"].child_window(title="Copy", control_type=50011).click_input()
            # app['Context'].child_window(title="Copy", control_type=50011).print_control_identifiers()
            app[fiddler_title].child_window(
                title="Session	Ctrl+Shift+S", auto_id="432", control_type="MenuItem"
            ).click_input()
            log = pyperclip.paste()
            # print(pyperclip.paste())

        # assert app[fiddler_title].child_window(title_re='/uninstall', control_type="Text").is_visible(timeout=setting.time_out_pywinauto) is True
    finally:
        # print(pyperclip.paste())
        return log
        # return app[fiddler_title].child_window(title_re='/uninstall', control_type="Text").window_text()


def is_log_show_fiddler(log_title, timeout=500):
    faulthandler.disable()
    is_log_show = False
    max_delay = timeout
    interval_delay = 3
    total_delay = 0
    fiddler_title = setting.fiddler_title
    app = Application(backend="uia").connect(
        auto_id="frmViewer",
        control_type=50032,
        title_re=fiddler_title,
        timeout=setting.timeout_pywinauto,
    )
    # print(app.window().window_text())
    # try:

    while not is_log_show:
        try:
            log = (
                app.window()
                .child_window(title=log_title, control_type="Text", found_index=0)
                .wait("visible", timeout=2)
            )
            if log.is_visible():
                is_log_show = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay > max_delay:
            print(f"Timeout for wait for metric log show on Fiddler")
            break
    return is_log_show


def test_is_log_show_fiddler():
    is_log_show_fiddler(log_title="metrics.coccoc.com")


def test_clipboard_text():
    s = pyperclip.paste()
    print(s)


def clear_fiddler_log():
    faulthandler.disable()
    fiddler_title = setting.fiddler_title
    app = Application(backend="uia").connect(
        auto_id="frmViewer",
        control_type=50032,
        title_re=fiddler_title,
        timeout=setting.timeout_pywinauto,
    )
    app[fiddler_title].set_focus()
    app[fiddler_title].child_window(
        auto_id="lvSessions", control_type=50008
    ).click_input()
    keyboard.SendKeys("^x")
    # app[fiddler_title].child._window(title="Copy", control_type=50011).click_input()


def test_clear_fiddler_log():
    clear_fiddler_log()


def close_fiddler():
    fiddler_title = setting.fiddler_title
    app = None
    try:
        app = Application(backend="uia").connect(
            auto_id="frmViewer",
            control_type=50032,
            title_re=fiddler_title,
            timeout=setting.timeout_pywinauto,
        )
    finally:
        app.window().close()


def start_git_bash():
    # if file_utils.check_folder_is_exists(rf'C:\\Program Files\\Git\\'):
    #     command = r'cd C:\\Program Files\\Git\\'
    # else:
    #     command = r"C:\\Program Files {(}x86{)}\\Git"
    # cmd_window = os_utils.open_cmd_as_administrator()
    # time.sleep(1)
    # try:
    #     # pywinauto.keyboard.send_keys(command)
    #     keyboard.send_keys(command, with_spaces=True)
    #     pywinauto.keyboard.send_keys('{ENTER}')
    #     time.sleep(1)
    #     pywinauto.keyboard.send_keys('git-bash.exe')
    #     time.sleep(1)
    #     pywinauto.keyboard.send_keys('{ENTER}')
    #     time.sleep(1)
    # finally:
    #     cmd_window['Administrator'].close()
    git_bash_window = None
    try:
        Application(backend="uia").start(
            r"C:\Program Files\Git\git-bash.exe", timeout=setting.timeout_pywinauto
        )
        git_bash_window = Application(backend="uia").connect(
            control_type=50032,
            title_re="MINGW",
            class_name="mintty",
            timeout=setting.timeout_pywinauto,
        )
        git_bash_window.window().set_focus()
        pywinauto.keyboard.send_keys("cd{ENTER}")
        time.sleep(0.5)
        pywinauto.keyboard.send_keys(
            "cd Documents/automation/coccoc_win{ENTER}", with_spaces=True
        )
        time.sleep(0.5)
        pywinauto.keyboard.send_keys("cd .venv38/Scripts/{ENTER}", with_spaces=True)
        pywinauto.keyboard.send_keys("source activate{ENTER}", with_spaces=True)
        pywinauto.keyboard.send_keys("cd ../..{ENTER}", with_spaces=True)
        pywinauto.keyboard.send_keys(
            "cd src/tests/smoke_test/download/{ENTER}", with_spaces=True
        )
        # pywinauto.keyboard.send_keys('pytest test_download.py{ENTER}', with_spaces=True)

    finally:
        git_bash_window.window().close()


def test_start_git_bash():
    start_git_bash()
