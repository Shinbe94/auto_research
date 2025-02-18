import time

from pywinauto import Application
from pywinauto.keyboard import send_keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from tests import setting


def close_coccoc_by_alt_f4():
    send_keys("%{F4}")


def close_coccoc_by_menu_exit():
    app = Application(backend="uia").start(
        r"C:\Program Files\CocCoc\Browser\Application\browser.exe", timeout=20
    )
    current_window = app.window(class_name="Chrome_WidgetWin_1")
    current_window.child_window(control_type=50011, title="Cốc Cốc").select()
    current_window.child_window(control_type=50011, title="Exit").select()
    current_window.child_window(control_type=50000, title="Yes").click()


# To get the WebElement from Shadow Element by jsPath
def get_shadow_element(
    driver: WebDriver, js_path: str, timeout=setting.timeout
) -> WebElement:
    element: WebElement = None
    interval_delay = 1
    total_delay = 0
    while element is None:
        try:
            element = driver.execute_script(f"return {js_path};")
        except Exception:
            pass
        else:
            if element:
                return element
            else:
                continue
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            raise ValueError(f"No element found after {timeout} seconds!")


def get_shadow_element2(
    driver: WebDriver, js_path: str, timeout=setting.timeout_selenium
) -> WebElement:
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    element: WebElement = None
    while element is None:
        try:
            element = driver.execute_script(f"return {js_path};")
        except Exception:
            pass
        else:
            if element:
                return element
            else:
                continue
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= max_delay:
            print(f"Timeout for wait for getting the element by js_path: {js_path}")
            break
    return element


def get_shadow_element3(
    driver: WebDriver, js_path: str, timeout=setting.timeout_selenium
) -> WebElement:
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    element: WebElement = None
    while total_delay < max_delay:
        try:
            element = driver.execute_script(f"return {js_path};")
            if element is not None:
                break
        except Exception:
            pass
        else:
            if element:
                return element
            else:
                continue
        time.sleep(interval_delay)
        total_delay += interval_delay
    return element


# To click the shadow element
def click_shadow_element(driver: WebDriver, js_path: str):
    ele = get_shadow_element3(driver, js_path)
    ele.click()


# To get the attribute's value by shadow element
def get_attribute_value_by_element(ele: WebElement, attribute_name: str):
    attribute_value = ele.get_attribute(attribute_name)
    return attribute_value


# To get the attribute's value by jsPath
def get_attribute_value_by_js_path(
    driver: WebDriver, js_path: str, attribute_name: str
):
    ele = get_shadow_element3(driver, js_path)
    attribute_value = ele.get_attribute(attribute_name)
    return attribute_value


def click_element(driver: WebDriver, by_locator: tuple):
    wait = WebDriverWait(driver, setting.timeout, poll_frequency=1)
    wait.until((EC.element_to_be_clickable(by_locator))).click()


def get_element(driver: WebDriver, by_locator: tuple) -> WebElement:
    wait = WebDriverWait(driver, setting.timeout, poll_frequency=1)
    return wait.until(EC.presence_of_element_located(by_locator))


def send_text(driver: WebDriver, by_locator: tuple, value: str):
    wait = WebDriverWait(driver, setting.timeout, poll_frequency=1)
    wait.until(EC.element_to_be_clickable(by_locator)).clear()
    wait.until(EC.element_to_be_clickable(by_locator)).send_keys(value)


def get_text_from_element_by_inner_text(driver: WebDriver, by_locator: tuple):
    return get_element(driver, by_locator).get_attribute("innerText")


def get_text_from_element_by_inner_text_js_path(driver: WebDriver, js_path: str) -> str:
    ele = get_shadow_element3(driver, js_path)
    return ele.get_attribute("innerText")


def get_text_from_element(driver: WebDriver, by_locator: tuple) -> str:
    return get_element(driver, by_locator).text


def scroll_to_element(driver: WebDriver, by_locator: tuple):
    ele = get_element(driver, by_locator)
    driver.execute_script(
        'arguments[0].scrollIntoView({behavior: "instant", block: "start", inline: "start"});',
        ele,
    )
    time.sleep(1)


def scroll_up_down(driver: WebDriver, y: int):
    """
    Scroll upr or down
    Args:
        driver:
        y: y < 0 --> scroll down, y > 0 scroll up
    Returns:
    """
    js_scroll = rf"window.scrollBy(0, {y});"
    driver.execute_script(js_scroll)


def select_by_visible_text(driver: WebDriver, by_locator: tuple, text: str):
    select = Select(get_element(driver, by_locator))
    select.select_by_visible_text(text)


def scroll_to_element_by_js_path(driver: WebDriver, js_path: str):
    ele = get_shadow_element3(driver, js_path)
    driver.execute_script("arguments[0].scrollIntoView(block: 'start');", ele)


def wait_for_element_presented(driver: WebDriver, by_locator: tuple):
    wait = WebDriverWait(driver, setting.timeout, poll_frequency=1)
    wait.until(EC.visibility_of_element_located(by_locator))


def wait_for_element_presented_by_js_path(
    driver: WebDriver, js_path: str, timeout=setting.timeout
):
    wait = WebDriverWait(driver, timeout, poll_frequency=1)
    wait.until(EC.visibility_of(get_shadow_element3(driver, js_path)))


def get_text_from_js_path(driver: WebDriver, js_path: str) -> str:
    element_text = get_shadow_element3(driver, js_path).text
    return element_text


def is_element_existed(driver: WebDriver, by_locator: str, timeout=5) -> bool:
    max_delay = timeout
    interval_delay = 0.5
    total_delay = 0
    # element = None
    is_existed = False
    while total_delay < max_delay:
        try:
            element = driver.find_element(*by_locator)
            if element is not None:
                is_existed = True
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    return is_existed


def wait_for_text_is_present(
    driver: WebDriver, by_locator: tuple, text: str, timeout=setting.timeout
) -> bool:
    wait = WebDriverWait(driver, timeout, poll_frequency=1)
    wait.until(EC.text_to_be_present_in_element(by_locator, text))


def wait_for_text_present_shadow_element(
    driver: WebDriver, js_path: str, text: str, timeout=setting.timeout_selenium
):
    interval_delay = 2
    total_delay = 0
    element: WebElement = None
    while total_delay < timeout:
        try:
            element = get_shadow_element3(driver, js_path)
        except Exception:
            pass
        else:
            if element:
                if text in element.text:
                    break
            else:
                continue
        time.sleep(interval_delay)
        total_delay += interval_delay
        if total_delay >= timeout:
            raise ValueError("No text present")


def wait_for_title(driver: WebDriver, title: str, timeout=setting.timeout):
    wait = WebDriverWait(driver, timeout, poll_frequency=1)
    # wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))
    wait.until(EC.title_contains(title))
