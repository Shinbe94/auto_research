import glob
import os
import time

from playwright.sync_api import sync_playwright
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.pages.coccoc_common import open_browser, interactions

global download_folder
from src.utilities import os_utils, file_utils
from tests import setting

BUILD_32BIT = (By.XPATH, '//a[text()="32-bit"]')
BUILD_64BIT = (By.XPATH, '//a[text()="64-bit"]')
BTN_TAI_COCCOC = (By.XPATH, '//span[text()="Tải Cốc Cốc"]')
BTN_DOWNLOAD_COCCOC_HERO = (By.CSS_SELECTOR, 'button[data-testid="btn-download-hero"]')


# BTN_DOWNLOAD_COCCOC=


def delete_installer_downloaded(installer_name="CocCocSetup"):
    downloaded_folder = f"C:\\Users\\{os_utils.get_username()}\\Downloads"
    os.chmod(downloaded_folder, 0o777)  # Change permission
    for filename in glob.glob(downloaded_folder + "\\" + installer_name + "*"):
        os.remove(filename)


def get_default_download_folder():
    # LOGGER.info("Get Default download folder...")

    global download_folder
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, executable_path=setting.chrome_binary_64bit
        )
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto("chrome://settings/")
        time.sleep(15)
        # download_folder = page.inner_text('//*[@id="defaultDownloadPath"]')
        # print('download folder = ' + download_folder)
        # browser.close()
    # from utils_automation.const import Urls
    # browser.maximize_window()
    # browser.get(url)
    # from models.pageobject.settings import SettingsPageObject
    # setting_page_object = SettingsPageObject()
    # download_folder = setting_page_object.get_download_folder(browser)
    # # LOGGER.info('Download folder at: ' + download_folder)
    # print(download_folder)
    # return download_folder


# To download CocCocSetUp.exe from coccoc.com
def download_coccoc_setup(
    language=setting.coccoc_language, platform="64bit", headless=True
):
    # print('download_coccoc_setup')
    delete_installer_downloaded()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless, executable_path=open_browser.get_chrome_executable_path()
        )
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        if language == "en":
            page.goto("https://coccoc.com/en/download")
        else:
            page.goto(setting.coccoc_homepage_url + "/vi/download")

        if platform == "32bit":
            with page.expect_download() as download_info:
                #     page.click('//a[text()="32-bit"]')
                page.goto(
                    "https://coccoc.com/en/download/thank-you?plat=win&arch=x32",
                    wait_until="domcontentloaded",
                )
                page.click(
                    'a[href="https://files.coccoc.com/browser/download/en?plat=win&arch=x32"]'
                )
            # download_coccoc_direct_link(
            #     url="https://coccoc.com/download/thank-you?plat=win&arch=x32"
            # )

        else:
            with page.expect_download() as download_info:
                # page.click('//a[text()="64-bit"]')
                page.click('//button[@aria-label="Download Cốc Cốc for Windows"]')
        download = download_info.value
        download.save_as(
            f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
        )
        context.close()
        browser.close()


def download_coccoc_setup2(language=setting.coccoc_language, headless=True):
    delete_installer_downloaded()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless, executable_path=open_browser.get_chrome_executable_path()
        )
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        if language == "en":
            page.goto(setting.coccoc_homepage_url + "/en/download")
        else:
            page.goto(setting.coccoc_homepage_url + "/vi/download")

        with page.expect_download() as download_info:
            page.click('button[data-testid="btn-download-hero"]')
        download = download_info.value
        download.save_as(
            f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
        )
        context.close()
        browser.close()


def download_coccoc_direct_link(url, headless=True):
    delete_installer_downloaded()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless, executable_path=open_browser.get_chrome_executable_path()
        )
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        with page.expect_download() as download_info:
            # Fix no need to wait for load all. as this link is triggered download automatically after accessing
            page.goto(url, wait_until="domcontentloaded")
        download = download_info.value
        download.save_as(
            f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
        )
        context.close()
        browser.close()


def upload_file():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, executable_path=open_browser.get_chrome_executable_path()
        )
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto("https://virustotal.com/gui/home/upload")
        time.sleep(4)
        # page.click('//*[@id="infoIcon"]')
        page.on(
            "filechooser",
            lambda file_chooser: file_chooser.set_files(
                rf"C:\Users\{os_utils.get_username()}\Downloads\CocCocSetup.exe"
            ),
        )
        # with page.expect_file_chooser() as fc_info:
        #     file_chooser = fc_info.value
        #     file_chooser.set_files(rf'C:\Users\{os_utils.get_username()}\Downloads\CocCocSetup.exe')
        time.sleep(10)
        context.close()
        browser.close()


# TODO
def download_coccoc_from_ftp(platform="64bit"):
    pass


def download_coccoc_setup_by_selenium(
    is_headless=True, language=setting.coccoc_language, platform=setting.platform
):
    delete_installer_downloaded()
    driver = open_browser.open_chrome_by_selenium(is_headless=is_headless)
    file_name = None
    try:
        if language == "en":
            # page.click('div[data-default="false"]')
            # page.click('div[data-value="en"]')
            driver.get("https://coccoc.com/en/download")
            # page.goto(setting.coccoc_homepage_url + '/en/download')
            # page.click('button[href="/en/download"]')
        else:
            driver.get(setting.coccoc_homepage_url + "/vi/download")
            # page.click('button[href="/download"]')

        if platform == "32bit":
            interactions.click_element(driver, BUILD_32BIT)
        else:
            interactions.click_element(driver, BUILD_64BIT)
        file_name = file_utils.wait_for_file_downloaded()
    finally:
        driver.quit()
        if file_name is not None:
            # file_utils.remove_a_file(file_name)
            return file_name


def test_download_coccoc_setup_by_selenium():
    download_coccoc_setup_by_selenium(is_headless=False)


def test_download_setup_file_automatically():
    download_setup_file_automatically(is_headless=False)


def download_setup_file_automatically(
    language=setting.coccoc_language, is_headless=True
):
    print('debug download_setup_file_automatically')
    delete_installer_downloaded()
    # arch = os_utils.get_window_arch().strip("_")
    # if is_use_playwright is False:
    if os_utils.get_real_system_arch(is_format=False) == "32bit":
        print('debug if')
        driver: WebDriver = open_browser.open_chrome_by_selenium(
            is_headless=is_headless
        )
        file_name = None
        current_window = None
        try:
            driver.get(setting.coccoc_homepage_url + rf"/{language}/download/thanks")
            current_window = driver.current_window_handle
            interactions.click_element(driver, BTN_DOWNLOAD_COCCOC_HERO)
            file_name = file_utils.wait_for_file_downloaded2()
        finally:
            driver.switch_to.window(current_window)
            driver.quit()
            if file_name is not None:
                return file_name
    else:
        print('debug else1')
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=is_headless,
                executable_path=open_browser.get_chrome_executable_path(),
            )
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()
            if language == "en":
                page.goto(setting.coccoc_homepage_url + "/en/")
                print(setting.coccoc_homepage_url + "/en/")
                with page.expect_download() as download_info:
                    print('prefinal')
                    # page.wait_for_selector('[data-testid="btn-download-hero"]')
                    # page.get_by_test_id('[data-testid="btn-download-hero"]').click()
                    page.get_by_test_id("btn-download-hero").click()
                    # page.evaluate('document.querySelector("button[data-testid=\'btn-download-hero\']").click()')
                    # page.click('//button[@data-testid="btn-download-hero"]')
                    # page.goto('https://files1.coccoc.com/browser/x64/coccoc_en_machine.exe')

                    print('final')
            else:
                page.goto(setting.coccoc_homepage_url + "/vi/")
                with page.expect_download() as download_info:
                    print('downloadpage')
                    page.get_by_test_id("btn-download-hero").click()
            print('debug else2')
            download = download_info.value
            print(download)
            print('debug download')
            download.save_as(
                f"C:\\Users\\{os_utils.get_username()}\\Downloads\\CocCocSetup.exe"
            )
            context.close()
            browser.close()
