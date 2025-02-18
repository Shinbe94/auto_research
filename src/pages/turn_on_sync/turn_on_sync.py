import faulthandler
import time

from pywinauto import Application
from playwright.sync_api import Page
from src.pages.constant import CocCocTitles
from tests import setting
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.pages.coccoc_common import open_browser, interactions, interactions_windows
from src.pages.installations.base_window import BrowserBasePage

BTN_TURN_ON_SYNC = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section settings-people-page").shadowRoot.querySelector("#pages > div > settings-sync-account-control").shadowRoot.querySelector("#signIn")'


class TurnOnSync(BrowserBasePage):
    LOGIN_BY_EMAIL = (By.CSS_SELECTOR, "#email_button")
    EMAIL_FIELD = (By.CSS_SELECTOR, 'input[name="email"]')
    PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="password"]')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')

    # def login_to_account(self, account_url, username, password):
    #     coccoc = open_browser.open_and_connect_coccoc_by_selenium()
    #     driver = coccoc[0]
    #     driver.get(account_url)

    """
    To Open the account and login via email
    """

    def login_coccoc_account_by_email(self, accounts_url, email, password):
        self.get_url(accounts_url)
        self.click(self.LOGIN_BY_EMAIL)
        self.send_keys(self.EMAIL_FIELD, email)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BTN)
        time.sleep(2)

    # Login CCA(no need to access CCA)
    def login_coccoc_account_by_email2(self, email, password):
        # print(self.driver.current_url)
        self.driver.get(self.driver.current_url)
        self.driver.refresh()
        self.click(self.LOGIN_BY_EMAIL)
        # time.sleep(2)
        self.send_keys(self.EMAIL_FIELD, email)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BTN)

    """ To click button "Yes, I'm in" from pop-up confirm syncing" """

    def click_confirm_sync_btn(self):
        title = self.get_current_window_title() + " - Cốc Cốc"
        current_coccoc_language = self.get_current_coccoc_language()
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            # self.app[title].print_control_identifiers()
            if "en" in current_coccoc_language:
                self.app[title].child_window(
                    title="Yes, I'm in", auto_id="confirmButton", control_type=50000
                ).wait("visible", timeout=5).click()
            else:
                self.app[title].child_window(
                    title="Có, tôi đồng ý", auto_id="confirmButton", control_type=50000
                ).wait("visible", timeout=5).click()
        except Exception as the_exception:
            print(the_exception)
        time.sleep(1)

    """
    to click button "Turn on sync" from coccoc://settings"
    """

    def click_btn_turn_on_sync(self):
        title = self.get_current_window_title() + " - Cốc Cốc"
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            # self.app[title].print_control_identifiers()

            self.app[title].child_window(
                auto_id="sync-button", control_type=50000
            ).wait("visible", timeout=5).click()

        except Exception as the_exception:
            print(the_exception)

    def login_and_sync(self, account_url, email, password):
        # self.login_coccoc_account_by_email2(account_url, email, password)
        self.click_bubble()
        self.click_confirm_sync_btn()

    # This function is used for click the bubble when no syncing made
    def click_bubble(self):
        title = self.get_current_window_title() + " - Cốc Cốc"
        current_coccoc_language = self.get_current_coccoc_language()
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            # self.app[title].print_control_identifiers()
            if "en" in current_coccoc_language:
                self.app[title].child_window(title="You", control_type="Button").click()

        except Exception as the_exception:
            print(the_exception)

    """This function is used for click the bubble when no syncing made"""

    def process_syncing(self, email, password):
        # Run this command to disable PIP Ads
        # self.execute_js(
        #     'ntp.apiHandle.newTabPage.setPIPProperties(400, 300, "https://google.com.vn/", 0, false, false)')
        windows_before = self.driver.current_window_handle
        print("original window is: " + windows_before)
        title = self.get_current_window_title() + " - Cốc Cốc"
        current_coccoc_language = self.get_current_coccoc_language()

        # Open syncing from bubble
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            # self.app[title].print_control_identifiers()
            if "en" in current_coccoc_language:
                self.app[title].child_window(title="You", control_type="Button").wait(
                    "visible", timeout=setting.timeout_pywinauto
                ).click()
                self.app[title].child_window(
                    title="Turn on sync…", control_type="Button"
                ).wait("visible", timeout=setting.timeout_pywinauto).click()
            else:
                self.app[title].child_window(title="Bạn", control_type="Button").wait(
                    "visible"
                ).click()
                self.app[title].child_window(
                    title="Bật tính năng đồng bộ hóa…", control_type="Button"
                ).wait("visible", timeout=setting.timeout_pywinauto).click()

            # Handle the PIP ADs shows
            if self.is_pip_ads_appeared():
                print("PIP ads displayed!")
                print(
                    "current window after PIP" + str(self.driver.current_window_handle)
                )
                windows_after = self.driver.window_handles
                for win in windows_after:
                    print(win)
                new_window = [x for x in windows_after if x != windows_before][0]
                self.driver.switch_to.window(new_window)
                print(
                    "current window after switch:"
                    + str(self.driver.current_window_handle)
                )
                # print(self.driver.title)
                # self.driver.close()
                self.driver.switch_to.window(windows_before)
                print(
                    "current window after switch back:"
                    + str(self.driver.current_window_handle)
                )
                # print(self.driver.title)
            else:
                pass
            print(self.driver.current_window_handle)
            # time.sleep(2)
            # Execute login by email and password
            self.login_coccoc_account_by_email2(email, password)
            # Click to confirm syncing
            self.click_confirm_sync_btn()
            time.sleep(5)

        except Exception as the_exception:
            print(the_exception)
        finally:
            title = self.get_current_window_title() + " - Cốc Cốc"
            current_coccoc_language = self.get_current_coccoc_language()
            self.close_coccoc_by_window_title(title, current_coccoc_language)

        # self.is_pip_ads_appeared()
        # if self.is_pip_ads_appeared():
        #     print('video ads appears, should handle it')
        #     # self.driver.switch_to.default_content()
        #     self.driver.switch_to.window(original_window)
        # else:
        #     pass
        #     # print('No video ads appear, continue the rest')
        # self.driver.switch_to.window(original_window)
        # # Execute login by email and password
        # self.login_coccoc_account_by_email2(email, password)
        # # Click to confirm syncing
        # self.click_confirm_sync_btn()
        # time.sleep(5)
        # title = self.get_current_window_title() + " - Cốc Cốc"
        # current_coccoc_language = self.get_current_coccoc_language()
        # self.close_coccoc_by_window_title(title, current_coccoc_language)

    """ To click the bubble icon after synced """

    def click_bubble_by_name(self, name):
        title = self.get_current_window_title() + " - Cốc Cốc"
        try:
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            self.app[title].child_window(title=name, control_type="Button").click()

        except Exception as the_exception:
            print(the_exception)

    # This function is used for click the bubble when no syncing made
    def process_syncing_pywinauto(self, email, password):
        # Run this command to disable PIP Ads
        # self.execute_js(
        #     'ntp.apiHandle.newTabPage.setPIPProperties(400, 300, "https://google.com.vn/", 0, false, false)')

        current_coccoc_language = self.get_current_coccoc_language()

        # Open syncing from bubble
        try:
            title = self.get_current_window_title() + " - Cốc Cốc"
            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()
            # self.app[title].print_control_identifiers()
            if "en" in current_coccoc_language:
                self.app[title].child_window(title="You", control_type="Button").wait(
                    "visible", timeout=setting.timeout_pywinauto
                ).click()
                self.app[title].child_window(
                    title="Turn on sync…", control_type="Button"
                ).wait("visible", timeout=setting.timeout_pywinauto).click()
            else:
                self.app[title].child_window(title="Bạn", control_type="Button").wait(
                    "visible"
                ).click()
                self.app[title].child_window(
                    title="Bật tính năng đồng bộ hóa…", control_type="Button"
                ).wait("visible", timeout=setting.timeout_pywinauto).click()

        except Exception as the_exception:
            print(the_exception)
        # finally:
        #     title = self.get_current_window_title() + " - Cốc Cốc"
        #     current_coccoc_language = self.get_current_coccoc_language()
        #     self.close_coccoc_by_window_title(title, current_coccoc_language)

        try:
            if "en" == setting.coccoc_language:
                new_title = "Sign in to Cốc Cốc - Cốc Cốc"
            else:
                new_title = "Đăng nhập Cốc Cốc - Cốc Cốc"

            self.app = Application(backend="uia").connect(
                class_name="Chrome_WidgetWin_1",
                control_type=50033,
                title_re=new_title,
                timeout=setting.timeout_pywinauto,
            )
            self.app[new_title].wait(
                "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
            ).set_focus()

            self.app[new_title].child_window(
                auto_id="email_button", control_type=50000
            ).wait("visible", timeout=2).click()

            self.app[new_title].child_window(
                auto_id="login_form", control_type=50026
            ).wait("visible", timeout=2).print_control_identifiers()

            if "en" == setting.coccoc_language:
                new_title = "Sign in to Cốc Cốc - Cốc Cốc"
                self.app[new_title].wait(
                    "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
                ).set_focus()
                # self.app[new_title].child_window(title="Email", control_type=50020).wait('visible',
                #                                                                   timeout=2).click()
                self.app[new_title].child_window(
                    title="Email", control_type=50020
                ).wait("visible", timeout=2).type_keys(email)

                self.app[new_title].child_window(
                    title="Password", control_type=50020
                ).wait("visible", timeout=2).click()
                self.app[new_title].child_window(
                    title="Password", control_type=50020
                ).type_keys(password)
                self.app[new_title].child_window(
                    title="Sign in", control_type=50000
                ).click()

            # Click to confirm syncing
            self.click_confirm_sync_btn()
            time.sleep(5)
        finally:
            new_title = self.get_current_window_title() + " - Cốc Cốc"
            current_coccoc_language = self.get_current_coccoc_language()
            self.close_coccoc_by_window_title(new_title, current_coccoc_language)

    def turn_on_sync_from_setting(self, email, password):
        self.execute_js(
            'ntp.apiHandle.newTabPage.setPIPProperties(400, 300, "https://google.com.vn/", 0, false, false)'
        )
        self.get_url("coccoc://settings/")
        windows_before = self.driver.current_window_handle
        self.click_shadow_element(BTN_TURN_ON_SYNC)
        windows_after = self.driver.window_handles
        new_window = [x for x in windows_after if x != windows_before][0]
        self.driver.switch_to.window(new_window)
        self.login_coccoc_account_by_email2(email, password)
        self.click_confirm_sync_btn()
        time.sleep(5)
        # self.driver.close()
        self.driver.switch_to.window(windows_before)
        self.driver.close()
        title = self.get_current_window_title() + " - Cốc Cốc"
        self.close_coccoc_by_window_title(title=title)

    def alert(self):
        self.execute_js('alert("Hello! I am an alert box!");')


def test_turn_on_sync_from_setting():
    turn_on_sync_from_setting(
        email=setting.cc_account_user, password=setting.cc_account_password
    )


def turn_on_sync_from_setting(email, password, is_close_after_synced=True):
    faulthandler.disable()
    driver: WebDriver = open_browser.open_and_connect_coccoc_by_selenium()[0]
    driver.execute_script(
        'ntp.apiHandle.newTabPage.setPIPProperties(400, 300, "https://google.com.vn/", 0, false, false)'
    )
    driver.get("coccoc://settings/people")
    windows_before = driver.current_window_handle
    # self.click_shadow_element(BTN_TURN_ON_SYNC)
    interactions.click_shadow_element(driver, BTN_TURN_ON_SYNC)
    windows_after = driver.window_handles
    new_window = [x for x in windows_after if x != windows_before][0]
    driver.switch_to.window(new_window)
    # self.login_coccoc_account_by_email2(email, password)
    driver.get(driver.current_url + "&by-pass-captcha=1")
    driver.refresh()
    interactions.click_element(driver, TurnOnSync.LOGIN_BY_EMAIL)
    # time.sleep(2)
    # self.send_keys(self.EMAIL_FIELD, email)
    interactions.send_text(driver, TurnOnSync.EMAIL_FIELD, email)
    # self.send_keys(self.PASSWORD_FIELD, password)
    interactions.send_text(driver, TurnOnSync.PASSWORD_FIELD, password)
    interactions.click_element(driver, TurnOnSync.LOGIN_BTN)
    time.sleep(3)
    click_confirm_sync_btn(driver)
    time.sleep(30)
    # self.driver.close()
    driver.switch_to.window(windows_before)
    if is_close_after_synced:
        interactions_windows.close_coccoc_by_window_title(
            title=driver.title + " - Cốc Cốc"
        )
        if driver is not None:
            driver.quit()
    # title = self.get_current_window_title() + " - Cốc Cốc"
    # self.close_coccoc_by_window_title(title=title)
    time.sleep(2)


def click_confirm_sync_btn(driver):
    title = driver.title + " - Cốc Cốc"
    current_coccoc_language = driver.execute_script(
        "return window.navigator.userLanguage || window.navigator.language"
    )
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
        app[title].wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).set_focus()
        # self.app[title].print_control_identifiers()
        if "en" in current_coccoc_language:
            app[title].child_window(
                title="Yes, I'm in", auto_id="confirmButton", control_type=50000
            ).wait("visible", timeout=15, retry_interval=1).click()
        else:
            app[title].child_window(
                title="Có, tôi đồng ý", auto_id="confirmButton", control_type=50000
            ).wait("visible", timeout=15, retry_interval=1).click()
    except Exception as the_exception:
        print(the_exception)
    time.sleep(1)


def turn_on_sync_from_setting_by_playwright(
    pcc: Page, email, password, is_close_after_synced=True
):
    faulthandler.disable()
    pcc.evaluate(
        'ntp.apiHandle.newTabPage.setPIPProperties(400, 300, "https://google.com.vn/", 0, false, false)'
    )
    pcc.goto("coccoc://settings/people")
    pcc.locator("#signIn").click()
    pages = pcc.context.wait_for_event("page")  # Wait for 'page' event fired.
    page = pages.context.pages[1]  # switch to new tab
    page.goto(
        "https://accounts.coccoc.com/?signin=sync&continue=https%3A%2F%2Fcoccoc.com&by-pass-captcha=1"
    )
    page.locator("#email_button").click()
    page.locator('input[name="email"]').fill(email)
    page.locator('input[name="password"]').fill(password)
    page.locator('button[type="submit"]').click()

    click_confirm_sync_btn2(page)
    time.sleep(15)
    if is_close_after_synced:
        interactions_windows.close_coccoc_by_window_title(
            title=CocCocTitles.NEW_TAB_TITLE
        )
        pcc.close()


def click_confirm_sync_btn2(page: Page):
    title = page.title() + " - Cốc Cốc"
    current_coccoc_language = page.evaluate(
        "window.navigator.userLanguage || window.navigator.language"
    )
    try:
        app = Application(backend="uia").connect(
            class_name="Chrome_WidgetWin_1",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
        app[title].wait(
            "visible", timeout=setting.timeout_pywinauto, retry_interval=0.5
        ).set_focus()
        if "en" in current_coccoc_language:
            app[title].child_window(
                title="Yes, I'm in", auto_id="confirmButton", control_type=50000
            ).wait("visible", timeout=15, retry_interval=1).click()
        else:
            app[title].child_window(
                title="Có, tôi đồng ý", auto_id="confirmButton", control_type=50000
            ).wait("visible", timeout=15, retry_interval=1).click()
    except Exception as the_exception:
        print(the_exception)
    time.sleep(1)


def test_turn_on_sync_from_setting2(pcc):
    turn_on_sync_from_setting_by_playwright(
        pcc, email=setting.cc_account_user, password=setting.cc_account_password
    )
