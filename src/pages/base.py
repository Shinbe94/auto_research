import time
from typing import Any, List, Tuple
import pywinauto.mouse

import pywinauto
from pywinauto.keyboard import send_keys
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.select import Select
from appium.webdriver.webelement import WebElement as AppiumElement
from func_timeout import FunctionTimedOut, func_set_timeout
from playwright.sync_api import sync_playwright, Page, Locator, expect
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    InvalidSelectorException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from tests import setting


class BasePage:
    def __init__(self, page):
        self.page = page
        # pass

    def goto(self, url):
        self.page.goto(url)

    def get_element(self, locator):
        return self.page.wait_for_selector(locator)

    def fill_text(self, ele, text):
        self.page.fill(ele, text)

    @staticmethod
    def open_coccoc(self, request):
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                executable_path=setting.coccoc_binary_64bit,
                # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Profile 1',
                user_data_dir=setting.coccoc_default_profile,
                headless=False,
            )
            # browser = p.chromium.launch(
            #     # executable_path=settings.coccoc_binary,
            #     # user_data_dir=r'C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data\\Profile 1',
            #     headless=False
            # )
            page = browser.new_page()
            # page.goto(url)
            request.cls.page = page
            yield page
            browser.close()


class BasePlaywright(object):
    """
    playwright page after connect to current CocCoc browser which opening by WinAppDriver + Appium
    """

    def __init__(self, page: Page):
        self.page = page

    def open_page(self, url: str) -> Page:
        return self.page.goto(url)

    def get_current_url(self) -> str:
        return self.page.url

    def reload_page(self):
        """Reload the current page"""
        self.page.reload()

    def open_new_tab(self):
        context = self.page.context
        new_tab: Page = context.new_page()
        return new_tab

    # def open_new_tab_with_har(self):
    #     context = self.page.con
    #     new_tab: Page = context.new_page()
    #     return new_tab

    def get_cookies(self, urls: list = None) -> List:
        return self.page.context.cookies(urls)

    def clear_cookies(self) -> None:
        self.page.context.clear_cookies()

    def get_vid(self) -> str:
        list_cookies: list = self.page.context.cookies()
        for i in list_cookies:
            if i.get("domain") == ".coccoc.com" and i.get("name") == "vid":
                return i.get("value")

    def get_console_logs(self) -> str:
        with self.page.expect_console_message() as msg_info:
            new_tab = self.open_new_tab()
            new_tab.goto("https://en.wikipedia.org/wiki/Main_Page")
            self.page.evaluate(
                "str => str", self.page.on("console", lambda msg: msg.text)
            )

        logs = msg_info.value
        return logs

    def print_args(self, msg):
        for arg in msg.args:
            print(arg.json_value())

    def get_console_logs_text(self) -> List:
        logs: list = []

        def _get_log() -> List:
            # self.page.on("console", lambda msg: logs.append(msg.args))
            # self.page.on(
            #     "console", lambda msg: print([arg.json_value() for arg in msg.args])
            # )
            self.page.on("console", lambda msg: logs.append(msg.text))
            # self.page
            return logs

        return _get_log

    def get_msg(self, msg):
        for arg in msg.args:
            print(arg.json_value())

    def get_console_logs_as_text(self) -> list:
        logs = list()
        self.page.on("console", lambda msg: logs.append(msg.text))
        # self.page.goto(
        #     url,
        #     timeout=60000,
        # )
        # self.page.wait_for_timeout(5_000)
        return logs

    def record_har_file(self, path: str, file_name: str) -> None:
        page = self.open_new_tab()

    @staticmethod
    def get_attribute_value_by_locator(locator: Locator, attribute_name: str):
        """
        To return the value of attribute of element
        Args:
            locator: Locator
            attribute_name: attribute's name
        Returns:
        """
        return locator.get_attribute(attribute_name)

    def get_attribute_value_by_selector(self, selector: str, attribute_name: str):
        """
        To return the value of attribute of element
        Args:
            selector: selector
            attribute_name: attribute's name
        Returns:

        """
        return self.page.get_attribute(selector, attribute_name)

    def check_text_is_not_appeared(self, text: str):
        element: Locator = self.page.get_by_text(text, exact=True)
        expect(element).not_to_be_visible()

    def accept_dialog(self):
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button").click()

    def dismiss_dialog(self):
        self.page.on("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("button").click()

    # def get_console_log(self):
    #     self.page.on("console", lambda message: message.)

    def snap_selected_window_to_the_right_half_screen(self):
        """
        Snap the active windows to the right half of the screen
        Returns:
        """
        self.page.keyboard.press("Control+ArrowRight")
        # self.page.keyboard.down("Control")
        # self.page.keyboard.press("ArrowRight")
        # self.page.keyboard.down("Control")
        # self.page.keyboard.down("ArrowRight")

    def snap_selected_window_to_the_left_half_screen(self):
        """
        Snap the active windows to the left half of the screen
        Returns:
        """
        self.page.keyboard.down("Control")
        self.page.keyboard.press("ArrowLeft")

    def handle_page(self, new_page: Page):
        new_page.wait_for_load_state()
        # print(new_page.title())
        assert new_page.title()

        # context.on("page", handle_page)

    def evaluate_js(self, js_command) -> str:
        try:
            return self.page.evaluate(js_command)
        except Exception as e:
            raise e

    def blacken_text2(self, by_locator: str, is_need_full_screen=True) -> None:
        """Blacken the text by using playwright + pywinauto drag mouse and drop
        Args:
            by_locator (tuple): _description_
        """
        if is_need_full_screen:
            send_keys("{F11}")  # this tip help to get correct element coordinates
            time.sleep(4)
        else:
            time.sleep(2)
        box = self.page.locator(by_locator).bounding_box()

        # get element coordinates
        frame_x = round(box["x"])
        frame_y = round(box["y"])

        # get the width of the element
        width_element: int = round(box["width"])

        pywinauto.mouse.move(
            coords=(frame_x - 3, frame_y + 3)
        )  # Minus 3 for sure blacken all text
        time.sleep(0.2)
        pywinauto.mouse.press(button="left", coords=(frame_x - 3, frame_y + 3))
        pywinauto.mouse.release(button="left", coords=(frame_x - 3, frame_y + 3))
        pywinauto.mouse.press(button="left", coords=(frame_x - 3, frame_y + 3))
        time.sleep(0.5)
        pywinauto.mouse.move(
            coords=(frame_x + width_element + 2, frame_y + 3)
        )  # Plus 2 for sure blacken all text

        pywinauto.mouse.release(
            button="left", coords=(frame_x + width_element + 2, frame_y + 3)
        )


class BaseAppium(object):
    """
    Using driver from:
    WinAppDriver + Appium
    """

    def __init__(
        self,
        wad,
        timeout=setting.timeout,
    ):
        self.wad: WebDriver = wad
        self.timeout = timeout
        self.wait = WebDriverWait(
            self.wad,
            timeout=self.timeout,
            poll_frequency=1,
            ignored_exceptions=[WebDriverException],
        )

    def get_ele(self, by_locator: Tuple[str, str]) -> AppiumElement:
        interval_delay = 1
        total_delay = 0
        ele: AppiumElement
        while total_delay < 10:
            try:
                if by_locator[0] == "AUTOMATION_ID":
                    ele = self.wad.find_element_by_accessibility_id(by_locator[1])
                elif by_locator[0] == "CLASS_NAME":
                    ele = self.wad.find_element_by_class_name(by_locator[1])
                else:
                    ele = self.wad.find_element_by_name(by_locator[1])
                if ele is not None:
                    return ele
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay

    def click_ele(self, by_locator: Tuple[str, str]):
        self.get_ele(by_locator).click()

    def send_keys_ele(
        self, by_locator: Tuple[str, str], text: str, is_press_enter=False
    ):
        ele = self.get_ele(by_locator)
        ele.clear()
        ele.click()
        if is_press_enter:
            ele.send_keys(text + Keys.RETURN)
        else:
            ele.send_keys(text)

    def press_enter_to_element(self, by_locator: tuple) -> None:
        ele = self.get_ele(by_locator)
        ele.send_keys(Keys.RETURN)

    def get_ele_attribute_by_its_name_and_locator(
        self, by_locator: tuple, attribute_name: str
    ) -> str:
        ele = self.get_ele(by_locator)
        attribute_value = ele.get_attribute(attribute_name)
        return attribute_value

    def get_element(self, by_locator: tuple) -> AppiumElement:
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def get_elements(self, by_locator: tuple) -> List[AppiumElement]:
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def click_element(self, by_locator: tuple, is_wait_for_clickable=True) -> None:
        # self.get_element(by_locator).click()
        if is_wait_for_clickable:
            self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        else:
            self.get_element(by_locator).click()
        # self.wait.until(EC.presence_of_element_located(by_locator)).click()

    def double_click_element(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.double_click(self.get_element(by_locator)).perform()

    def right_click_element(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.context_click(self.get_element(by_locator)).perform()

    def clear_text_of_element(self, by_locator: tuple) -> None:
        element = self.get_element(by_locator)
        element.click()
        element.clear()

    def fill_texts(
        self,
        by_locator: tuple,
        text: str,
        is_press_enter=False,
        set_texts_immediately=False,
    ) -> None:
        """
        Enter text to the element
        Args:
            by_locator:
            text:
            is_press_enter: True: press enter after send the text, False: just send the text only
        Returns:
        """
        element = self.get_element(by_locator)
        element.click()
        if not set_texts_immediately:
            element.clear()
        if is_press_enter:
            element.send_keys(text + Keys.RETURN)
        else:
            element.send_keys(text)

    def fill_texts2(self, by_locator: tuple, text: str, is_press_enter=False) -> None:
        """
        For some unknown reason the dialog is close after the first text, so we need to click and hold the next input
        text, so we should using workaround like these
        Args:
            by_locator:
            text:
            is_press_enter:
        Returns:
        """
        element = self.get_element(by_locator)
        # element.click()
        self.move_to_element(by_locator)
        self.click_and_hold(by_locator)
        element.clear()
        # print(self.get_element_attribute_by_its_name_and_its_element(element, 'Value.Value'))
        # element.send_keys(Keys.COMMAND + 'a')
        if is_press_enter:
            element.send_keys(text + Keys.RETURN)
        else:
            element.send_keys(text)

    def set_texts(self, by_locator: tuple, text: str, is_press_enter=False) -> None:
        element = self.get_element(by_locator)
        element.click()
        element.clear()
        if is_press_enter:
            element.set_text(text + Keys.RETURN)
        else:
            element.set_text(text)

    def is_displayed(self, by_locator: tuple) -> bool:
        # wait = WebDriverWait(self.appium_driver, 20)
        element = self.get_element(by_locator)
        if element is not None:
            return True
        else:
            return False

    def get_element_attribute_by_its_name_and_locator(
        self, by_locator: tuple, attribute_name: str
    ) -> str:
        element = self.get_element(by_locator)
        attribute_value = element.get_attribute(attribute_name)
        return attribute_value

    @staticmethod
    def get_element_attribute_by_its_name_and_its_element(
        element: AppiumElement, attribute_name: str
    ) -> str:
        attribute_value = element.get_attribute(attribute_name)
        return attribute_value

    # Count Element appear
    # def get_count(self, by_locator: tuple) -> int:
    #     return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))

    def get_count(self, by_locator: tuple) -> int:
        try:
            return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))
        except Exception:
            return 0

    # Wait for element exist
    def wait_for_element_exist(
        self, by_locator: tuple, timeout=setting.timeout
    ) -> bool:
        wait = WebDriverWait(self.wad, timeout)
        max_delay = 5
        interval_delay = 1
        total_delay = 0
        is_exist = False
        while total_delay < max_delay or is_exist:
            try:
                element = wait.until(EC.presence_of_element_located(by_locator))
                if element:
                    is_exist = True
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        return is_exist

    # Wait for element disappear
    def wait_for_element_disappear(self, by_locator: tuple, timeout=5) -> bool:
        # try:
        #     element = self.wad.find_element(*by_locator)
        #     if element:
        #         return False
        # except Exception:
        #     return True

        # return WebDriverWait(self.wad, timeout=timeout).until_not(EC.presence_of_element_located(by_locator))

        # wait = WebDriverWait(self.wad, timeout=timeout)
        interval_delay = 1
        total_delay = 0
        is_disappeared = True
        while total_delay < timeout:
            try:
                WebDriverWait(self.wad, timeout).until_not(
                    EC.presence_of_element_located(by_locator)
                )
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        return is_disappeared

    def wait_for_element_disappear2(self, by_locator: tuple, short_time=1, long_time=5):
        # self.driver.implicitly_wait(timeout)
        # wait = WebDriverWait(self.driver, short_time)
        try:
            # Wait for element present
            WebDriverWait(self.wad, short_time).until(
                EC.presence_of_element_located(by_locator)
            )
            # Wait for element disappear
            WebDriverWait(self.wad, long_time).until_not(
                EC.presence_of_element_located(by_locator)
            )
            # return True
        except TimeoutException:
            pass

    def is_element_disappeared(self, by_locator: tuple, timeout=5) -> bool:
        try:
            # Wait for element disappears
            WebDriverWait(self.wad, timeout).until_not(
                EC.presence_of_element_located(by_locator)
            )
            is_disappeared = True
        except TimeoutException:
            is_disappeared = False
        return is_disappeared

    def is_element_appeared(self, by_locator: tuple, timeout=5) -> bool:
        try:
            # Wait for element appears
            WebDriverWait(self.wad, timeout=timeout).until(
                EC.presence_of_element_located(by_locator)
            )
            is_appeared = True
        except TimeoutException:
            is_appeared = False
        return is_appeared

    def get_inner_text(self, by_locator: tuple) -> str:
        return self.get_element(by_locator).get_attribute("innerText")

    def get_text(self, by_locator: tuple) -> str:
        return self.get_element(by_locator).text

    def minimize_window(self) -> ActionChains:
        """
        Minimize all current active window
        Returns:
        """
        action_chains = ActionChains(self.wad)
        action_chains.key_down(
            Keys.COMMAND + Keys.ARROW_DOWN + Keys.ARROW_DOWN
        ).perform()

    def minimize_partial_window(self) -> ActionChains:
        """
        Minimize partial current active window
        Returns:
        """
        action_chains = ActionChains(self.wad)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_DOWN).perform()

    def maximize_window(self) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_UP + Keys.ARROW_UP).perform()

    def snap_selected_window_to_the_right_half_screen(self) -> ActionChains:
        """
        Snap the active windows to the right half of the screen
        Returns:
        """
        action_chains = ActionChains(self.wad)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_RIGHT + Keys.COMMAND).perform()

    def snap_selected_window_to_the_left_half_screen(self) -> ActionChains:
        """
        Snap the active windows to the left half of the screen
        Returns:
        """
        action_chains = ActionChains(self.wad)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_LEFT + Keys.COMMAND).perform()

    def move_to_element(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.move_to_element(self.get_element(by_locator)).perform()

    def move_to_element_off_set(
        self, by_locator: tuple, xoffset: int, yoffset: int
    ) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.move_to_element_with_offset(
            self.get_element(by_locator), xoffset, yoffset
        ).perform()

    def click_and_hold(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.click_and_hold(self.get_element(by_locator)).perform()

    def release_element(self, by_locator: tuple) -> ActionChains:
        """Release mouse from element

        Args:
            by_locator (_type_): _description_
        """
        action_chains = ActionChains(self.wad)
        action_chains.release(self.get_element(by_locator)).perform()

    def press_keyboard(self, keys: str) -> ActionChains:
        action_chains = ActionChains(self.wad)
        action_chains.send_keys(keys).perform()

    def get_element_location(self, by_locator: tuple) -> tuple:
        return self.get_element(by_locator).location

    @staticmethod
    def switch_tab_by_tab_number(tab_number: str = 1):
        send_keys(f"^{tab_number}")


class BaseSelenium(object):
    """
    Using driver from:
    WinAppDriver + Selenium
    """

    def __init__(self, driver, timeout=setting.timeout_selenium):
        self.scc: WebDriver = driver
        self.wait = WebDriverWait(
            self.scc,
            timeout=timeout,
            poll_frequency=1,
            ignored_exceptions=[WebDriverException],
        )

    def until(self, method, message=""):
        screen = None
        stacktrace = None
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except InvalidSelectorException as e:
                raise e
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutException(message, screen, stacktrace)

    # @func_set_timeout(setting.timeout_selenium)
    def open_page(self, url: str):
        try:
            self.scc.get(url)
        except FunctionTimedOut as e:
            raise e
        return self

    def open_new_tab(self):
        self.scc.execute_script("window.open('');")
        return self

    def open_new_tab2(self):
        self.get_element(by_locator=(By.CSS_SELECTOR, "body")).send_keys(
            Keys.CONTROL + "t"
        )
        # return self
        # self.press_keyboard(keys=Keys.DOWN(Keys.CONTROL) + "t")
        # self.press_keyboard_element(
        #     by_locator=(By.CSS_SELECTOR, "body"), keys=Keys.CONTROL + "t"
        # )

    def open_new_tab_with_specific_url(self, url: str):
        self.scc.execute_script(f"window.open('{url}')")
        return self

    def reload_page(self) -> None:
        self.scc.refresh()

    def go_back(self) -> None:
        self.execute_js("window.history.go(-1)")

    def get_current_url(self) -> str:
        return self.scc.current_url

    def wait_for_title(self, title_text: str) -> None:
        self.wait.until(EC.title_contains(title=title_text))

    def get_title(self) -> str:
        return self.scc.title

    def get_element(self, by_locator: tuple) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def get_elements(
        self, by_locator: tuple, timeout=setting.timeout_selenium
    ) -> List[WebElement]:
        self.wait = WebDriverWait(
            self.scc,
            timeout=timeout,
            poll_frequency=1,
            ignored_exceptions=[WebDriverException],
        )
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def get_count(self, by_locator: tuple) -> int:
        try:
            return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))
        except Exception:
            return 0

    def click_element(self, by_locator: tuple, is_scroll_in_view=False):
        # self.get_element(by_locator).click()
        if is_scroll_in_view:
            self.scroll_into_view_element(self.get_element(by_locator))
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        # self.wait.until(EC.presence_of_element_located(by_locator)).click()

    def double_click_element(self, by_locator: tuple):
        action_chains = ActionChains(self.scc)
        action_chains.double_click(self.get_element(by_locator)).perform()

    def right_click_element(self, by_locator: tuple):
        action_chains = ActionChains(self.scc)
        action_chains.context_click(self.get_element(by_locator)).perform()

    def right_click_element_by_element(self, element: WebElement):
        action_chains = ActionChains(self.scc)
        action_chains.context_click(element).perform()

    def click_element_by_js2(self, by_locator: tuple):
        """To click element by JS, parameter is locator

        Args:
            by_locator (_type_): Locator of element
        """
        element = self.get_element(by_locator)
        self.scc.execute_script("arguments[0].click();", element)

    def click_element_by_js(self, element: WebElement):
        """To click element using JS, parameter is Element

        Args:
            element (WebElement): Webelement of element
        """
        self.scc.execute_script("arguments[0].click();", element)

    def get_element_text(self, by_locator: tuple) -> str:
        return self.get_element(by_locator).text

    def get_element_text_by_element(self, element: WebElement) -> str:
        return element.text

    def clear_text_of_element(self, by_locator: tuple):
        element: WebElement = self.get_element(by_locator)
        self.click_element(by_locator)
        element.clear()

    def fill_texts(self, by_locator: tuple, text: str, is_press_enter=False):
        """
        Enter text to the element
        Args:
            by_locator:
            text:
            is_press_enter: True: press enter after send the text, False: just send the text only
        Returns:
        """
        element: WebElement = self.get_element(by_locator)
        # self.click_element(by_locator)
        element.clear()
        if is_press_enter:
            element.send_keys(text + Keys.RETURN)
        else:
            element.send_keys(text)

    def get_attribute_by_its_name_and_element(
        self, element: WebElement, attribute_name: str
    ) -> str:
        attribute_value: str = element.get_attribute(attribute_name)
        return attribute_value

    def get_element_attribute_by_its_name_and_locator(
        self, by_locator: tuple, attribute_name: str
    ) -> str:
        element: WebElement = self.get_element(by_locator)
        attribute_value: str = element.get_attribute(attribute_name)
        return attribute_value

    def get_element_css_value_by_its_name_and_locator(
        self, by_locator: tuple, css_property_name: str
    ) -> str:
        element: WebElement = self.get_element(by_locator)
        css_property_value: str = element.value_of_css_property(css_property_name)
        return css_property_value

    def wait_for_attribute_update_value(
        self,
        by_locator: tuple,
        attribute_name: str,
        att_value: str = None,
        timeout: int = setting.timeout_selenium,
    ) -> bool:
        """To wait for the attribute of element is updated to the expected value

        Args:
            by_locator (_type_): Locator
            attribute_name (str): atttribue like: class, status ...
            att_value (str): expected value to be checked
            timeout (_type_, optional): _description_. Defaults to setting.time_out_selenium.

        Returns:
            bool: _description_
        """
        is_updated = False
        interval_delay = 0.5
        total_delay = 0
        while total_delay < timeout:
            try:
                if (
                    self.get_element_attribute_by_its_name_and_locator(
                        by_locator, attribute_name
                    )
                    == att_value
                ):
                    is_updated = True
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > timeout:
                    print(
                        f"Timeout after {total_delay} seconds for att element updated"
                    )
                    break
            except Exception:
                pass
        return is_updated

    def is_element_disappeared(self, by_locator: tuple, timeout: int = 5) -> bool:
        try:
            # Wait for element disappear
            WebDriverWait(self.scc, timeout).until_not(
                EC.presence_of_element_located(by_locator)
            )
            is_disappeared = True
        except TimeoutException:
            is_disappeared = False
        return is_disappeared

    def is_element_appeared(self, by_locator: tuple, timeout: int = 5) -> bool:
        try:
            # Wait for element disappear
            WebDriverWait(self.scc, timeout).until(
                EC.presence_of_element_located(by_locator)
            )
            is_appeared = True
        except TimeoutException:
            is_appeared = False
        return is_appeared

    def action_chains(self) -> ActionChains:
        action_chains = ActionChains(self.scc)
        return action_chains

    def release(self, on_element: WebElement = None) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.release(on_element=on_element)
        return action_chains

    def perform(self) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.perform()
        return action_chains

    def move_to_element(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.move_to_element(self.get_element(by_locator)).perform()
        return action_chains

    def move_to_element_by_element(self, element: WebElement) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.move_to_element(element).perform()
        return action_chains

    def move_to_element_with_offset(
        self, by_locator: tuple, xoffset: int, yoffset: int
    ) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.move_to_element_with_offset(
            self.get_element(by_locator), xoffset, yoffset
        ).perform()
        return action_chains

    def drag_and_drop_by_offset(
        self, by_locator: tuple, xoffset: int, yoffset: int
    ) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.drag_and_drop_by_offset(
            self.get_element(by_locator), xoffset, yoffset
        ).perform()
        return action_chains

    def move_by_offset(self, xoffset: int, yoffset: int) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.move_by_offset(xoffset, yoffset).perform()
        return action_chains

    def click_and_hold(self, by_locator: tuple) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.click_and_hold(self.get_element(by_locator)).perform()
        return action_chains

    def scroll_into_view_element(self, element: WebElement):
        self.scc.execute_script("arguments[0].scrollIntoView(true);", element)
        # action_chains = ActionChains(self.scc)
        # action_chains.move_to_element(element).perform()

    def scroll_into_view_element_by_locator(self, by_locator: tuple):
        element = self.get_element(by_locator)
        self.scc.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_into_bottom_of_page(self) -> None:
        self.scc.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)

    def scroll_down_by_n_pixel(
        self, n_of_pixel: int, sleep_n_seconds: float = 0.5
    ) -> None:
        self.scc.execute_script(f"window.scrollBy(0,{n_of_pixel})", "")
        time.sleep(sleep_n_seconds)

    def scroll_up_by_n_pixel(
        self, n_of_pixel: int, sleep_n_seconds: float = 0.5
    ) -> None:
        self.scc.execute_script(f"window.scrollBy(0,-{n_of_pixel})", "")
        time.sleep(sleep_n_seconds)

    def scroll_to_top_page_by_js(self, sleep_n_seconds: float = 0.5) -> None:
        self.scc.execute_script("window.scrollTo(0, document.body.scrollTop);")
        time.sleep(sleep_n_seconds)

    def press_keyboard(self, keys: str) -> ActionChains:
        """Just press keyboard, no targeting to any element

        Args:
            keys (str): _description_

        Returns:
            ActionChains: _description_
        """
        action_chains = ActionChains(self.scc)
        action_chains.send_keys(keys).perform()
        return action_chains

    def press_keyboard_element(self, by_locator: tuple, keys: str) -> None:
        action_chains = ActionChains(self.scc)
        action_chains.send_keys_to_element(self.get_element(by_locator), keys).perform()
        return action_chains

    def snap_selected_window_to_the_right_half_screen(self) -> ActionChains:
        """
        Snap the active windows to the right half of the screen
        Returns:
        """
        action_chains = ActionChains(self.scc)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_RIGHT + Keys.COMMAND).perform()
        return action_chains

    def snap_selected_window_to_the_left_half_screen(self) -> ActionChains:
        """
        Snap the active windows to the left half of the screen
        Returns:
        """
        action_chains = ActionChains(self.scc)
        action_chains.key_down(Keys.COMMAND + Keys.ARROW_LEFT + Keys.COMMAND).perform()
        return action_chains

    def get_inner_text(self, by_locator: tuple) -> str:
        return self.get_element(by_locator).get_attribute("innerText")
        # return self.wait.until(
        #     EC.visibility_of_element_located(by_locator)
        # ).get_attribute("innerText")

    def wait_for_text_is_present(self, by_locator: tuple, text: str) -> bool:
        self.wait.until(EC.text_to_be_present_in_element(by_locator, text))

    def get_current_window(self):
        """To get the current window (the one handling by driver)

        Returns:
            _type_: _description_
        """
        return self.scc.current_window_handle

    def get_all_windows_handle(self) -> list:
        return self.scc.window_handles

    def switch_to_window(self, window_name) -> None:
        """Switch to window by its name

        Args:
            window (_type_): _description_
        """
        self.scc.switch_to.window(window_name=window_name)
        time.sleep(1)

    def count_total_elements(self, by_locator, timeout=setting.timeout_selenium) -> int:
        """To return the total elements appear

        Args:
            by_locator (_type_): Locator
            timeout (_type_, optional): custom timeout. Defaults to setting.time_out_selenium.

        Returns:
            int: 0 if no element, total if appears
        """
        self.wait = WebDriverWait(
            self.scc,
            timeout=timeout,
            poll_frequency=1,
            ignored_exceptions=[WebDriverException],
        )
        total: int = 0
        try:
            total = len(
                self.wait.until(EC.presence_of_all_elements_located(by_locator))
            )
        except Exception:
            total = 0
        finally:
            return total

    def select_by_visible_text(self, by_locator, text: str):
        select = Select(self.get_element(by_locator))
        # select by visible text
        select.select_by_visible_text(text)

    def switch_to_iframe(self, frame_reference) -> None:
        self.scc.switch_to.frame(frame_reference)

    def fullscreen_window(self) -> None:
        self.scc.fullscreen_window()

    def blacken_text(self, by_locator: tuple) -> None:
        """Blacken the text

        Args:
            by_locator (tuple): _description_
        """
        text_element: WebElement = self.get_element(by_locator)
        self.click_element(by_locator)
        self.move_to_element(by_locator)
        time.sleep(2)
        width_element: int = text_element.size["width"]
        self.move_to_element_with_offset(by_locator, 0, 0)
        time.sleep(1)
        self.click_and_hold(by_locator).move_by_offset(width_element, 0).perform()
        time.sleep(1)
        self.release(on_element=text_element)

    def blacken_text2(self, by_locator: tuple, is_need_full_screen=True) -> None:
        """Blacken the text by using pywinauto drag mouse and drop

        Args:
            by_locator (tuple): _description_
        """
        if is_need_full_screen:
            self.fullscreen_window()  # this tip help to get correct element coordinates
            time.sleep(4)
            # self.move_to_element(by_locator)
        time.sleep(2)
        text_element: WebElement = self.get_element(by_locator)
        # self.move_to_element_with_offset(by_locator, 0, 0)
        # get element coordinates
        frame_x = text_element.location["x"]
        frame_y = text_element.location["y"]
        # get the width of the element
        width_element: int = text_element.size["width"]

        pywinauto.mouse.move(
            coords=(frame_x - 3, frame_y + 3)
        )  # Minus 3 for sure blacken all text
        time.sleep(0.2)
        pywinauto.mouse.press(button="left", coords=(frame_x - 3, frame_y + 3))
        pywinauto.mouse.release(button="left", coords=(frame_x - 3, frame_y + 3))
        pywinauto.mouse.press(button="left", coords=(frame_x - 3, frame_y + 3))
        time.sleep(0.5)
        pywinauto.mouse.move(
            coords=(frame_x + width_element + 2, frame_y + 3)
        )  # Plus 2 for sure blacken all text
        # time.sleep(0.1)
        pywinauto.mouse.release(
            button="left", coords=(frame_x + width_element + 2, frame_y + 3)
        )
        # time.sleep(0.2)

    def blacken_text3(self, by_locator: tuple) -> None:
        """Blacken the text by using pywinauto drag mouse and drop

        Args:
            by_locator (tuple): _description_
        """
        # self.fullscreen_window()  # this tip help to get correct element coordinates
        time.sleep(3)
        text_element: WebElement = self.get_element(by_locator)
        # get element coordinates
        frame_x = 513
        frame_y = 178
        # get the width of the element
        width_element: int = 166
        pywinauto.mouse.move(coords=(frame_x, frame_y))
        time.sleep(0.1)
        pywinauto.mouse.press(button="left", coords=(frame_x, frame_y))
        time.sleep(0.1)
        pywinauto.mouse.move(coords=(frame_x + width_element, frame_y))
        time.sleep(0.1)
        pywinauto.mouse.release(
            button="left", coords=(frame_x + width_element, frame_y)
        )
        time.sleep(0.1)

    @staticmethod
    def press_mouse_by_offset(
        x_offset: int, y_offset: int, button: str = "left"
    ) -> None:
        """Press mouse using pywinauto

        Args:
            x_offset (int): _description_
            y_offset (int): _description_
            button (str, optional): _description_. Defaults to "left". 'right'
        """
        pywinauto.mouse.press(button=button, coords=(x_offset, y_offset))

    @staticmethod
    def click_mouse_by_offset(
        x_offset: int = 0, y_offset: int = 0, button: str = "left"
    ) -> None:
        """Click mouse using pywinauto

        Args:
            x_offset (int, optional): _description_. Defaults to 0.
            y_offset (int, optional): _description_. Defaults to 0.
            button (str, optional): _description_. Defaults to "left". 'right'
        """
        pywinauto.mouse.click(button=button, coords=(x_offset, y_offset))

    @staticmethod
    def double_click_mouse_by_offset(
        x_offset: int = 0, y_offset: int = 0, button: str = "left"
    ) -> None:
        """Double click mouse using pywinauto

        Args:
            x_offset (int, optional): _description_. Defaults to 0.
            y_offset (int, optional): _description_. Defaults to 0.
            button (str, optional): _description_. Defaults to "left". 'right'
        """
        pywinauto.mouse.double_click(button=button, coords=(x_offset, y_offset))

    def wait_for_page_to_load(
        self, load_status: str = "complete", timeout=setting.timeout_selenium
    ) -> None:
        """Wait for the page to load py using javascript

        Args:
            load_status (str): _description_
            timeout (_type_, optional): _description_. Defaults to setting.time_out_selenium.

        Returns:
            _type_: _description_
        """
        wait = WebDriverWait(
            self.scc,
            timeout=timeout,
            poll_frequency=1,
            ignored_exceptions=[WebDriverException],
        )
        wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == load_status
        )

    def dummy_click(self) -> ActionChains:
        """This method help to click dummy
            To close the tooltip is an using example
        Returns:
            ActionChains: _description_
        """
        action_chains = ActionChains(self.scc)
        action_chains.move_by_offset(0, 0).click().perform()
        return action_chains

    def execute_js(self, js_command: str):
        return self.scc.execute_script(script=js_command)

    def get_cookies_by_its_name(self, cookie_name: str) -> dict:
        """Return cookies as dict if have
        Args:
            cookie_name (str): _description_
        Returns:
            dict: _description_
        """
        try:
            return self.scc.get_cookie(cookie_name)
        except Exception:
            return None

    # ======================================================================================================================
    # Shadow Dom elements interactions ( By selenium + js_path)
    # ======================================================================================================================

    def get_shadow_element(
        self, js_path: str, timeout=setting.timeout_selenium
    ) -> WebElement:
        interval_delay = 0.5
        total_delay = 0
        element: WebElement = None
        while total_delay < timeout:
            try:
                element = self.scc.execute_script(f"return {js_path};")

            except Exception:
                pass
            else:
                if element is not None:
                    return element
                    # break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                raise ValueError(
                    f"Timeout after {total_delay} seconds for getting element by {js_path}"
                )
                # break
        return element

    def get_shadow_elements(
        self, js_path: str, timeout=setting.timeout_selenium
    ) -> List[WebElement]:
        """to get list of shadow elements by js_path
        To get them, we should use querySelectorAll
        sample: document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelectorAll("style")

        Args:
            js_path (str): _description_
            timeout (_type_, optional): _description_. Defaults to setting.time_out_selenium.

        Returns:
            List[WebElement]: _description_
        """
        interval_delay = 0.5
        total_delay = 0
        elements: List = None
        while total_delay < timeout:
            try:
                elements = self.scc.execute_script(f"return {js_path};")
                if len(elements) >= 1:
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
        if total_delay >= timeout:
            print(f"Timeout after {total_delay} seconds for getting elements")
        if elements:
            return elements
        else:
            return None

    def click_shadow_element(self, js_path: str) -> None:
        self.get_shadow_element(js_path).click()

    def get_attribute_value_of_shadow_element(
        self, js_path: str, attribute_name: str
    ) -> str:
        ele = self.get_shadow_element(js_path)

        return ele.get_attribute(attribute_name)

    def get_text_shadow_element(self, js_path) -> str:
        return self.get_shadow_element(js_path).text

    def get_count_shadow_elements(
        self, js_path: str, timeout=setting.timeout_selenium
    ) -> int:
        interval_delay = 0.5
        total_delay = 0
        elements: List = None
        no_of_ele: int = 0
        while total_delay < timeout:
            try:
                elements = self.scc.execute_script(f"return {js_path};")
                if len(elements) >= 1:
                    no_of_ele = len(elements)
                    break
            except Exception:
                pass
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                raise ValueError(
                    f"Timeout after {total_delay} seconds for getting elements"
                )
        return no_of_ele

    def fill_texts_shadow_element(
        self, js_path: str, text: str, is_press_enter=False
    ) -> None:
        """Enter text to the shadow element

        Args:
            js_path (str): JsPath of the element
            text (str): the text to be sent
            is_press_enter (bool, optional): Press enter after entering the text. Defaults to False.
        """
        element = self.get_shadow_element(js_path)
        element.click()
        element.clear()
        if is_press_enter:
            element.send_keys(text + Keys.RETURN)
        else:
            element.send_keys(text)

    def clear_text_of_shadow_element(self, js_path: str) -> None:
        element = self.get_shadow_element(js_path)
        element.click()
        element.clear()

    def double_click_shadow_element(self, js_path: str) -> ActionChains:
        action_chains = ActionChains(self.scc)
        action_chains.double_click(self.get_shadow_element(js_path)).perform()

    def is_shadow_element_disappeared(
        self, js_path: str, timeout=setting.timeout_selenium
    ) -> bool:
        """Check no element attached to the dom by:
            -Timeout for getting element -> return True (mean no element)
            -If any element found -> return False (Mean element found)
        Args:
            js_path (str): _description_
            timeout (_type_, optional): _description_. Defaults to setting.time_out_selenium.

        Returns:
            bool: True mean no element, False mean has element in the DOM
        """
        interval_delay = 0.5
        total_delay = 0
        element: WebElement = None
        while total_delay < timeout:
            try:
                element = self.scc.execute_script(f"return {js_path};")
            except Exception:
                pass
            else:
                if element is not None:
                    return False
                    # break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                return True
                # break

    def is_shadow_element_appeared(
        self, js_path: str, timeout=setting.timeout_selenium
    ) -> bool:
        interval_delay = 0.5
        total_delay = 0
        is_appeared: bool = False
        element: WebElement = None
        while total_delay < timeout:
            try:
                element = self.scc.execute_script(f"return {js_path};")
            except Exception:
                pass
            else:
                if element is not None:
                    is_appeared = True
                    break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay >= timeout:
                break
        return is_appeared

    def wait_for_attribute_update_value_shadow_element(
        self,
        js_path: str,
        attribute_name: str,
        att_value: str = None,
        timeout: int = setting.timeout_selenium,
    ) -> bool:
        """To wait for the attribute of element is updated to the expected value

        Args:
            js_path (_type_): jspath
            attribute_name (str): atttribue like: class, status ...
            att_value (str): expected value to be checked
            timeout (_type_, optional): _description_. Defaults to setting.time_out_selenium.
        Returns:
            bool: _description_
        """
        is_updated = False
        interval_delay = 0.5
        total_delay = 0
        while total_delay < timeout:
            try:
                if (
                    self.get_attribute_value_of_shadow_element(js_path, attribute_name)
                    == att_value
                ):
                    is_updated = True
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > timeout:
                    print(
                        f"Timeout after {total_delay} seconds for att element updated"
                    )
                    break
            except Exception:
                pass
        return is_updated

    def wait_for_text_is_present_shadow_element(
        self, js_path: str, text: str, timeout=setting.timeout_selenium
    ) -> bool:
        is_presented = False
        interval_delay = 1
        total_delay = 0
        while total_delay < timeout:
            if text in self.get_text_shadow_element(js_path):
                is_presented = True
                return is_presented
            time.sleep(interval_delay)
            total_delay += interval_delay

        return is_presented

    @staticmethod
    def switch_tab_by_tab_number(tab_number: str = 1):
        send_keys(f"^{tab_number}")


class OneExpectedConditionFromList:
    """At least 1 condition met --> return"""

    def __init__(self, expected_conditions) -> None:
        self.expected_conditions = expected_conditions

    def __call__(self, driver) -> Any:
        for expected_condition in self.expected_conditions:
            if expected_condition(driver):
                return True
        return False

    # sample using
    # conditions = [expected_conditions.presence_of_element_located((By.XPATH, 'hii'))]
    # driver.get('hii.com')
    # self.wait.until(OneExpectedConditionFromList(conditions))
