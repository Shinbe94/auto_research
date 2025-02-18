import time

from pywinauto import Application

from src.pages.constant import CocCocTitles
from tests import setting


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
            if (
                app[title]
                .child_window(title="Yes", control_type=50000)
                .wait("visible", timeout=10)
                .is_visible()
            ):
                app[title].child_window(title="Yes", control_type=50000).wait(
                    "visible"
                ).click()
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
            if (
                app[title]
                .child_window(title="Có", control_type=50000)
                .wait("visible", timeout=10)
                .is_visible()
            ):
                app[title].child_window(title="Có", control_type=50000).wait(
                    "visible"
                ).click()
            else:
                pass
    except Exception as the_exception:
        print(the_exception)
    time.sleep(2)


def close_explorer_by_its_title(title):
    app = Application(backend="uia").connect(
        class_name="CabinetWClass",
        control_type=50032,
        title_re=title,
        timeout=setting.timeout_pywinauto,
    )
    app[title].close()
    # time.sleep(1)
    # if app[title].child_window(title='Yes',
    #                            control_type=50000).wait('visible',
    #                                                     timeout=10).is_visible():
    #     app[title].child_window(title='Yes',
    #                             control_type=50000).wait('visible').click()
    # else:
    #     pass


def close_coccoc_at_new_tab(language=setting.coccoc_language):
    if language == "en":
        close_coccoc_by_window_title(
            title=CocCocTitles.NEW_TAB_TITLE_EN, language=language
        )
    else:
        close_coccoc_by_window_title(
            title=CocCocTitles.NEW_TAB_TITLE_VI, language=language
        )
    time.sleep(2)


def is_default_tor_window_appeared(
    language=setting.coccoc_language, is_closed=False
) -> bool:
    """
    To check the default tor window appear (just start incognito tor)
    Args:
        is_closed: True-> close the window before return the value
        language:
    Returns: bool
    """
    windows_text: list = []

    title = CocCocTitles.DEFAULT_TOR_WINDOW_TITLE

    app: Application = Application(backend="uia").connect(
        class_name="Chrome_WidgetWin_1",
        control_type=50033,
        title=title,
        timeout=setting.timeout_pywinauto,
    )
    for win in app.windows():
        windows_text.append(win.window_text())
    if title in windows_text:
        if is_closed:
            app.window(title=title).set_focus().close()
        return True
    else:
        return False


def click_yes_button_to_accept_close_coccoc_at_new_tab(
    language=setting.coccoc_language,
):
    title = CocCocTitles.DEFAULT_TOR_WINDOW_TITLE

    coccoc_window = Application(backend="uia").connect(
        class_name="Chrome_WidgetWin_1",
        control_type=50033,
        title_re=title,
        timeout=setting.timeout_pywinauto,
    )
    if "en" in language:
        if (
            coccoc_window[title]
            .child_window(title="Yes", control_type=50000)
            .wait("visible", timeout=setting.timeout_pywinauto, retry_interval=1)
            .is_visible()
        ):
            coccoc_window[title].child_window(title="Yes", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=1
            ).click()
    else:
        if (
            coccoc_window[title]
            .child_window(title="Có", control_type=50000)
            .wait("visible", timeout=setting.timeout_pywinauto)
            .is_visible()
        ):
            coccoc_window[title].child_window(title="Có", control_type=50000).wait(
                "visible", timeout=setting.timeout_pywinauto
            ).click()
