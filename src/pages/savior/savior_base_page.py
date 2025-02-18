import logging
import os
import random
import time

from pywinauto import Application
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tests import setting
from src.utilities import string_number_utils


def get_text_by_ele(element):
    return element.get_attribute("innerText")


class SaviorBasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def get_driver(self):
        return self.driver

    def get_page_title(self):
        return self.driver.title

    def get_url(self, url, is_wait_for_loaded=True):
        self.driver.get(url)
        if is_wait_for_loaded:
            self.wait_for_page_loaded_completely()

    def reload_page(self):
        self.driver.refresh()

    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    # Click element by its relative (from selenium v4 and onward)
    # def click_element_by_its_relative(self, by_locator, tag, relation_type):
    #     ele = self.get_element(by_locator)
    #     match relation_type:
    #         case 'above':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).above(ele))
    #             self.click(target_ele)
    #         case 'below':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).below(ele))
    #             self.click(target_ele)
    #         case 'to_left_of':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).to_left_of(ele))
    #             self.click(target_ele)
    #         case 'to_right_of':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).to_right_of(ele))
    #             self.click(target_ele)
    #         case 'near':
    #             target_ele = self.driver.find_element(locate_with(By.TAG_NAME, tag).near(ele))
    #             self.click(target_ele)
    #         case _:
    #             raise Exception(f'Value of relation_type {relation_type} must be in (above, below, to_left_of, '
    #                             f'to_right_of, near )')

    def click_by_js(self, by_locator):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].click();", ele)

    def click_element_by_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_dummy_ele(self):
        action = ActionChains(self.driver)
        action.move_by_offset(0, 0).click()
        action.perform()

    def send_keys(self, by_locator, value):
        # self.wait.until(EC.element_to_be_clickable(by_locator)).send_keys(value)
        # ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.wait.until(EC.presence_of_element_located(by_locator)).fill_texts(value)
        # ele.send_keys(value).submit()
        # ele.submit()

    def send_keys_by_js(self, by_locator, text):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].value='" + text + "';", ele)

    def get_text(self, by_locator):
        return self.wait.until(
            EC.visibility_of_element_located(by_locator)
        ).get_attribute("innerText")

    def get_element(self, by_locator):
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def get_ele(self, by_locator):
        self.wait.until(EC.presence_of_element_located(by_locator))
        return self.driver.find_element(*by_locator)

    def get_elements(self, by_locator):
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def get_value_of_element_attribute(self, by_locator, attribute_name):
        return self.wait.until(
            EC.presence_of_element_located(by_locator)
        ).get_attribute(attribute_name)

    def get_value_of_ele_attribute(self, ele, attribute_name):
        return ele.get_attribute(attribute_name)

    def get_element_by_variable(self, first_string, last_string, value):
        element = first_string + value + last_string
        return self.wait.until(EC.presence_of_element_located(element))

    def clear_text(self, by_locator):
        # ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.wait.until(EC.presence_of_element_located(by_locator)).fill_texts(
            Keys.CONTROL, "a", Keys.DELETE
        )
        # self.wait.until(EC.element_to_be_clickable(by_locator)).click()
        # self.wait.until(EC.presence_of_element_located(by_locator)).clear()

    def wait_for_element_presented(self, by_locator):
        self.wait.until(EC.visibility_of_element_located(by_locator))

    def get_count(self, by_locator):
        return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))

    def get_count2(self, by_locator):
        return len(self.wait.until(EC.presence_of_all_elements_located(by_locator)))

    def select_by_text(self, by_locator, option):
        select = Select(self.get_element(by_locator))
        select.select_by_visible_text(option)

    # def select_dropdown_element(self):
    #     Select(self.get_element())

    def drag_and_drop(self, source_element, target_element):
        action = ActionChains(self.driver)
        # action.drag_and_drop(self.get_element(source_element), self.get_element(target_element)).perform()
        action.click_and_hold(self.get_element(source_element)).pause(
            2
        ).move_to_element(self.get_element(target_element)).perform()

    def hover_on_element(self, by_locator, is_click_before_hover=False):
        self.wait.until(EC.presence_of_element_located(by_locator))
        # element = self.driver.find_element(*by_locator)
        element = self.get_element(by_locator)
        action = ActionChains(self.driver)
        # action.move_to_element(element).perform()
        if is_click_before_hover:
            action.click(element).perform()
        action.move_to_element(element)
        action.perform()
        time.sleep(1)
        # print('element hovered')

    def hover_and_hold_element(self, by_locator):
        self.wait.until(EC.presence_of_element_located(by_locator))
        # element = self.driver.find_element(*by_locator)
        element = self.get_element(by_locator)
        action = ActionChains(self.driver)
        # action.move_to_element(element).perform()
        action.click_and_hold(element)
        action.perform()
        time.sleep(2)
        action.release(element).perform()

    def hover_on_element_by_class_name_js(self, by):
        self.driver.execute_script(f"document.getElementsByClassName('{by}').focus()")

    def scroll_to_element(self, by_locator):
        ele = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)

    def execute_js(self, script):
        self.driver.execute_script(script)

    def switch_to(self, frame):
        self.driver.switch_to.frame(frame)

    def switch_to_frame(self, by_locator):
        # Store iframe web element
        iframe = self.get_element(by_locator)
        # switch to selected iframe
        self.switch_to(iframe)
        # return self.driver

    def leave_frame(self):
        self.driver.switch_to.default_content()

    # def take_screen_shot(self):
    #     allure.attach(self, name="error", attachment_type=allure.attachment_type.PNG)

    def assert_visible(self, by_locator):
        try:
            return self.get_element(by_locator)
        except NoSuchElementException:
            return False

    def is_element_exist(self, by_locator, timeout=0.1):
        self.driver.implicitly_wait(timeout)
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located(by_locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_exist(self, by_locator, timeout):
        wait = WebDriverWait(self.driver, timeout)
        is_exist = False
        while not is_exist:
            try:
                wait.until(
                    EC.visibility_of_element_located(self.get_element(by_locator))
                )
                is_exist = True
                break
            except:
                pass
        return is_exist

    def wait_for_element_disappear(self, by_locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        is_disappear = False
        while not is_disappear:
            try:
                wait.until(EC.invisibility_of_element_located(by_locator))
                is_disappear = True
                break
            except:
                pass
        return is_disappear

    def wait_for_element_disappear2(self, by_locator, short_time=1, long_time=5):
        # self.driver.implicitly_wait(timeout)
        # wait = WebDriverWait(self.driver, short_time)
        try:
            # Wait for element present
            WebDriverWait(self.driver, short_time).until(
                EC.presence_of_element_located(by_locator)
            )
            # Wait for element disappear
            WebDriverWait(self.driver, long_time).until_not(
                EC.presence_of_element_located(by_locator)
            )
            # return True
        except TimeoutException:
            pass
            # return False

    def wait_for_page_loaded_completely(self):
        WebDriverWait(self.driver, setting.timeout_selenium).until(
            lambda wd: self.driver.execute_script("return document.readyState")
            == "complete",
            "Page taking too long to load",
        )
        # print('The page is loaded completely')

    # To get the WebElement from Shadow Element by jsPath
    def get_shadow_element(self, js_path) -> WebElement:
        try:
            return self.driver.execute_script(f"return {js_path};")
        except Exception as e:
            raise e

    # To click the shadow element
    def click_shadow_element_by_js_path(self, js_path):
        try:
            ele = self.get_shadow_element(js_path)
            ele.click()
        except Exception as e:
            print(e)

    def hover_on_element_by_query_selector(self, query_selector):
        scripts = (
            """
         // Targeting video element 
        let clip = document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """)

        clip.addEventListener("mouseover", function () {
            setTimeout(function() {}, 1000);
        })
        /*
        clip.addEventListener("mouseover", function (e) {
            console.log('Event triggered');
        })
        */
        """
        )
        self.execute_js(scripts)

    def hover_on_element_by_query_selector2(self, query_selector):
        scripts = (
            """
        var event = new MouseEvent('mouseover', {
          'view': window,
          'bubbles': true,
          'cancelable': true
        });
        //var element = document.getElementById('name');
        var element = document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """)
        element.addEventListener('mouseover', function() {
          console.log('Event triggered');
        });
        element.dispatchEvent(event);
        """
        )
        self.execute_js(scripts)

    def hover_mouse_center(self, query_selector):
        scripts = (
            """
        document.querySelector("""
            + "'"
            + query_selector
            + "'"
            + """).dispatchEvent(new MouseEvent('mouseenter', { 'view': window, 'bubbles': true, 'cancelable': true }));
        """
        )
        self.execute_js(scripts)

    """
    THIS IS FOR SAVIOR PART
    """

    def wait_for_savior_element(self, script):
        global savior_element
        max_delay = 120
        interval_delay = 0.5
        total_delay = 0
        is_done = False
        while not is_done:
            savior_element = self.driver.execute_script(script=script)
            if savior_element is not None:
                is_done = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                is_done = True
                break
        if not is_done:
            logging.error("File(s) couldn't be loaded")
        return savior_element

    def wait_for_prefetch_savior_dock(self):
        max_delay = 20
        interval_delay = 0.5
        total_delay = 0
        has_not_shown_yet = True
        while has_not_shown_yet:
            try:
                preferred_select = self.driver.execute_script(
                    'return document.querySelector("html > div").shadowRoot.querySelector("#preferred-select")'
                )
                # print('Savior dock: ' + str(preferred_select))
                if preferred_select is not None:
                    has_not_shown_yet = False
                    # print('got savior dock at: ' + str(total_delay))
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    has_not_shown_yet = False
                    print("timeout when wait for the prefetch savior")
                    break
            except:
                logging.error("Savior Dock couldn't be loaded")

    # Wait for download done then return the file with path.
    @staticmethod
    def wait_for_downloads(download_path):
        max_delay = 3600
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

    def show_savior_dock(self):
        # self.driver.execute_script(
        #     "document.querySelector('html > div').shadowRoot.querySelector('.overlay').classList.remove('hidden')")
        max_delay = 5
        interval_delay = 0.5
        total_delay = 0
        is_loaded = False
        while not is_loaded:
            try:
                ele = self.execute_js(
                    'document.querySelector("html > div").shadowRoot.querySelector("div > div.savior-widget.main")'
                )
                if ele is not None:
                    self.execute_js(
                        'document.querySelector("html > div").shadowRoot.querySelector("div > div.savior-widget.main").removeAttribute("hidden")'
                    )
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    print("Timeout for showing savior dock")
                    break
            finally:
                break
        # self.execute_js('document.querySelector("html > div").shadowRoot.querySelector("div > div.savior-widget.main").removeAttribute("hidden")')
        # print('The savior dock is shown')

    def click_btn_download(self):
        # Click when media_quality has not loaded yet!
        if self.is_quality_loaded() is False:
            # print('Clicking no quality')
            self.driver.execute_script(
                'document.querySelector("html > div").shadowRoot.querySelector("#download-main").click()'
            )
        # Click when media_quality already loaded!
        else:
            self.click_btn_download_after_media_quality_loaded()

    def is_quality_loaded(self):
        max_delay = 10
        interval_delay = 1
        total_delay = 0
        is_loaded = False
        while not is_loaded:
            # try:
            #     quality_element = self.driver.execute_script('return document.querySelector("html > div").shadowRoot.querySelector("#downloads").classList.length')
            #     # display_status = quality_element.value_of_css_property('display')
            #     if str(quality_element) == '1':
            #         print('Media quality is loaded OK')
            #         is_loaded = True
            #         break
            #         # return True
            #     time.sleep(interval_delay)
            #     total_delay += interval_delay
            #     if total_delay > max_delay:
            #         # is_loaded = False
            #         print('Timeout for wait for loading video quality')
            #         break
            #         # return False
            # except:
            #     print('Media quality is not loaded yet')
            #     break
            # return is_loaded

            quality_element = self.driver.execute_script(
                'return document.querySelector("html > div").shadowRoot.querySelector("#downloads")'
            )
            print("quality element: " + str(quality_element))
            display_status = quality_element.value_of_css_property("display")
            print("display is " + display_status)
            if str(display_status) == "block":
                print("Media quality list is loaded OK")
                is_loaded = True
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print("Timeout for wait for loading video quality")
                break
        return is_loaded

    def click_btn_download_after_media_quality_loaded(self):
        # try:
        #     list_media_quality = self.driver.execute_script(
        #         'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li").getElementsByTagName("a")')
        #     # if list_media_quality is not None:
        #     for item in list_media_quality:
        #         if item.value_of_css_property("display") == 'flex':
        #             print(item)
        #             item.click()
        #         break
        # except:
        #     print('Error when loading media quality')

        list_media_qualities = self.driver.execute_script(
            'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > div > ul > li").getElementsByTagName("a")'
        )
        if len(list_media_qualities) >= 1:
            for list_media_quality in list_media_qualities:
                if list_media_quality.value_of_css_property("display") == "flex":
                    assert "DOWNLOAD" == get_text_by_ele(list_media_quality)
                    list_media_quality.click()
                    assert "DOWNLOAD" == get_text_by_ele(list_media_quality)
                    break

    def list_media_quality(self):
        data_qualities = dict()
        if self.is_quality_loaded():
            list_media_qualities = self.driver.execute_script(
                'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li").getElementsByTagName("a")'
            )
            if len(list_media_qualities) > 0:
                for list_media_quality in list_media_qualities:
                    data_qualities[  # type: ignore
                        list_media_quality.get_attribute("data-quality")
                    ] = list_media_quality
        if len(data_qualities) > 0:
            # print(data_qualities)
            return data_qualities
        else:
            return data_qualities
        # else:
        #     print("No media printed!")

    def list_media_quality2(self):
        max_delay = 5
        interval_delay = 0.5
        total_delay = 0
        list_elements = []
        list_quality = []
        if self.is_quality_loaded():
            print("Media quality is loaded")
            while len(list_elements) == 0:
                try:
                    list_elements = self.driver.execute_script(
                        'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > div > ul > li").getElementsByTagName("a")'
                    )
                    if len(list_elements) > 0:
                        break
                    time.sleep(interval_delay)
                    total_delay += interval_delay
                    if total_delay > max_delay:
                        print("Timeout for wait for getting list video quality")
                        break
                finally:
                    break
        else:
            print("No media loaded")
            # except StaleElementReferenceException:
            #     list_elements = self.driver.execute_script(
            #         'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li > div > div").getElementsByTagName("div")')
        if len(list_elements) > 0:
            for ele in list_elements:
                print(ele)
                if ele.get_attribute("data-quality") is not None:
                    list_quality.append(ele.get_attribute("data-quality"))

        if len(list_quality) > 0:
            # print(list_quality)
            return list_quality
        else:
            print("No media printed!")

    def select_media_quality(self, media_quality="Standard/480p"):
        data_qualities = self.list_media_quality()
        for key, value in data_qualities.items():
            if media_quality in key:
                value.click()
                # self.click_element_by_js(value)
                # self.driver.execute_script("arguments[0].click();", value)
                # print(f'Clicking {key}')
                time.sleep(1)
                assert (
                    string_number_utils.find_text_between_2_string(
                        media_quality, "/", "/"
                    )
                    == self.get_selected_media_quality()
                )
                break

    def select_media_quality_js_path(self, media_quality="mp4/Medium/360p"):
        data_qualities = self.list_media_quality()
        js_path = (
            f'document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li div[data-quality-value='
            + "'"
            + media_quality
            + "'"
            + ']")'
        )
        for key, value in data_qualities.items():
            if media_quality in key:
                self.click_shadow_element_by_js_path(js_path)
                time.sleep(1)
                assert (
                    string_number_utils.find_text_between_2_string(
                        media_quality, "/", "/"
                    )
                    == self.get_selected_media_quality()
                )
                break

    def select_random_media_quality_js_path(self):
        # data_qualities = self.list_media_quality()
        # media_quality = random.choice(list(data_qualities))
        data_qualities = self.list_media_quality2()
        media_quality = random.choice(data_qualities)  # type: ignore
        # print(media_quality)
        js_path = (
            f'document.querySelector("html > div").shadowRoot.querySelector("#downloads ul li div[data-quality-value='
            + "'"
            + media_quality
            + "'"
            + ']")'
        )
        self.click_shadow_element_by_js_path(js_path)
        time.sleep(2)
        # print(self.get_selected_media_quality())
        # print(string_number_utils.find_text_between_2_string(media_quality, '/', '/'))
        # print(self.get_selected_media_quality())
        assert (
            string_number_utils.find_text_between_2_string(media_quality, "/", "/")
            == self.get_selected_media_quality()
        )
        extension_of_media = string_number_utils.substring_before_char(
            media_quality, "/"
        )
        return extension_of_media

    def get_selected_media_quality(self):
        media_text = None
        list_elements_quality = self.driver.execute_script(
            'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > div > ul > li > div > span").getElementsByClassName("j-quality-option quality-option")'
        )
        if len(list_elements_quality) > 0:
            for element_quality in list_elements_quality:
                if element_quality.value_of_css_property("display") == "flex":
                    element = element_quality.find_element(
                        By.CLASS_NAME, "quality-option-ext-quality"
                    )
                    text_ele = element.text
                    media_text = text_ele.strip()
                    break
        if media_text is not None:
            return str(media_text)

    def get_selected_media_quality2(self):
        media_text = None
        list_elements_quality = self.driver.execute_script(
            'return document.querySelector("html > div").shadowRoot.querySelector("#downloads ul > li > div > span").getElementsByClassName("j-quality-option quality-option")'
        )
        if len(list_elements_quality) > 0:
            for element_quality in list_elements_quality:
                if element_quality.value_of_css_property("display") == "flex":
                    element = element_quality.find_element(
                        By.CLASS_NAME, "quality-option-ext-quality"
                    )
                    text_ele = element.text
                    media_text = text_ele.strip()
                    break
        if media_text is not None:
            return str(media_text)

    def get_list_media_quality_elements(self):
        if self.is_quality_loaded():
            list_quality_elements = self.driver.execute_script(
                'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li div[class="extension-box"]").getElementsByClassName("quality-label j-quality")'
            )
            for list_quality_element in list_quality_elements:
                print(list_quality_element.get)

    def get_list_possible_media_type(self):
        media_types = []
        if self.is_quality_loaded():
            media_types_elements = self.driver.execute_script(
                'return document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li").getElementsByClassName("extension-box")'
            )
            for media_types_element in media_types_elements:
                ele = media_types_element.find_element(By.TAG_NAME, "strong")
                media_types.append(self.get_text(ele))
        if len(media_types) > 0:
            # print(media_types)
            return media_types

    def click_preferred_quality_dropdown(self):
        # is_preferred_disabled = self.driver.execute_script('return document.querySelector("html > div").shadowRoot.querySelector("#preferred-select").getAttribute("disabled")')
        # print('is disabled: ' + str(is_preferred_disabled))
        if self.is_quality_loaded():
            self.driver.execute_script(
                'document.querySelector("html > div").shadowRoot.querySelector("#downloads > ul > li > div > span").click()'
            )
            print("Quality dropdown is clicked after loaded!")
        else:
            self.driver.execute_script(
                'document.querySelector("html > div").shadowRoot.querySelector("#preferred-select").click()'
            )
            print("Quality dropdown is clicked!")
        time.sleep(1)

    @staticmethod
    def play_media(file_name):
        os.startfile(file_name)
        time.sleep(10)
        play_media = Application(backend="uia").connect(
            title="Movies & TV", class_name="ApplicationFrameWindow", control_type=50032
        )
        play_media["Movies & TV"].close()
        os.remove(file_name)

    # def wait_for_the_video_is_playing(self, by_locator):
    #     is_not_playing = True
    #     while is_not_playing:
    #         self.hover_on_element(by_locator)
    #         # length_str = self.driver.find_element_by_class_name("ytp-time-duration").text
    #         while self.get_ele(by_locator).text is None:
    #             self.hover_on_element(by_locator)
    #             current_time_str = self.get_ele(by_locator).text
    #             second = int(current_time_str[-1:])
    #             if second >= 1:
    #                 is_not_playing = False
    #                 break
    #             print("current time sec is: " + str(second) + ' seconds')
    #         break
    def wait_for_the_video_is_playing(self, by_locator):
        max_delay = 10
        interval_delay = 0.5
        total_delay = 0
        is_not_playing = True
        while is_not_playing:
            self.hover_on_element(by_locator)
            try:
                self.hover_on_element(by_locator)
                current_time_str = self.get_ele(by_locator).text
                second = int(current_time_str[-1:])
                if second >= 1:
                    is_not_playing = False
                    # print("current playing time is: " + str(second) + ' seconds')
                    break
                time.sleep(interval_delay)
                total_delay += interval_delay
                if total_delay > max_delay:
                    is_not_playing = False
                    print("Timeout for wait for loading video")
                    break
            finally:
                pass

    def get_media_duration_from_site(self, by_locator, is_need_format=True):
        media_length = str(self.get_text(by_locator))
        if is_need_format:
            # Format to fit with HH:MM:SS
            if len(media_length) == 4:
                media_length = "00:0" + media_length
            elif len(media_length) == 5:
                media_length = "00:" + media_length
            elif len(media_length) == 7:
                media_length = "0" + media_length
        return media_length
