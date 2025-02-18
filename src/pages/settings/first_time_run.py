import faulthandler
import json
import os
import subprocess
import time

from pywinauto import keyboard, Application, WindowSpecification
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from src.utilities.process_id_utils import get_running_process_ids

from tests import setting
from src.pages.coccoc_common import open_browser, interactions, interactions_windows
from src.pages.extensions import extensions_page, savior_extension_detail_page
from src.utilities import file_utils, browser_utils, os_utils, string_number_utils
from src.utilities.file_utils import get_project_root

BTN_CONFIRM_UPLOAD = 'document.querySelector("#view-container > home-view").shadowRoot.querySelector("#uploadForm").shadowRoot.querySelector("div > form > button:nth-child(6)")'
CHOOSE_FILE_VIRUS_TOTAL = 'document.querySelector("#view-container > home-view").shadowRoot.querySelector("#uploadForm").shadowRoot.querySelector("#infoIcon")'
VIRUS_TOTAL_RESULT = 'document.querySelector("#view-container > file-view").shadowRoot.querySelector("#report > vt-ui-file-card").shadowRoot.querySelector("vt-ui-generic-card div.detections > span > div > p")'
TOTAL_COMPONENTS = (
    By.XPATH,
    '//*[@id="component-placeholder"]/div/div/div/div/span[2]/span',
)
COCCOC_VERSION_ABOUT_PAGE = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page").shadowRoot.querySelector("settings-section div.flex.cr-padded-text > div.secondary")'
MESSAGE_UP_TO_DATE = 'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-about-page").shadowRoot.querySelector("#updateStatusMessage > div")'
COCCOC_VERSION_PAGE = (By.XPATH, '//*[@id="useragent"]')


def check_components_after_installed(
    timeout=setting.timeout_for_update_components,
) -> bool:
    driver: WebDriver = open_browser.open_coccoc_by_selenium()
    driver.get(setting.coccoc_components)

    total_components = int(
        interactions.get_text_from_element_by_inner_text(driver, TOTAL_COMPONENTS)
    )
    is_updated = False
    list_updated_component = []
    interval_delay = 15
    total_delay = 0
    try:
        while not is_updated:
            for i in range(total_components):
                txt_element = '//*[@id="component-placeholder"]/div/div[2]/div[2]/div[{0}]/div[1]/div/div/span[2]/span[2]'.format(
                    i + 1
                )
                # print(txt_element)
                element_id_component = (By.XPATH, txt_element)
                id_components = interactions.get_text_from_element_by_inner_text(
                    driver, element_id_component
                )
                id_components_int = int(id_components.replace(".", ""))
                if id_components_int > 0:
                    if element_id_component not in list_updated_component:
                        list_updated_component.append(element_id_component)
            # print(list_updated_component)
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > timeout:
                print("Timeout for updating all components")
                break
            if len(list_updated_component) is total_components:
                is_updated = True
    finally:
        if driver is not None:
            driver.quit()
        return is_updated


def check_task_manager(language):
    # wmic process where "name like '%browser.exe%'" get Description
    # wmic process where "name like '%coccoc%'" get Description
    try:
        open_browser.open_coccoc_by_pywinauto(language)
        time.sleep(5)
        # to check CocCocCrashHandler process_id
        command_filter_coccoc_pid = (
            "wmic process where " + "'name like '%coccoc%''" + " get Description"
        )
        output_text_crash_handler = subprocess.check_output(
            command_filter_coccoc_pid, encoding="utf-8"
        )
        assert "CocCocCrashHandler.exe" in output_text_crash_handler
        if os_utils.get_real_system_arch(is_format=False) == "64bit":
            assert "CocCocCrashHandler64.exe" in output_text_crash_handler

        # to check browser.exe process_id
        command_filter_browser_pid = (
            "wmic process where " + "'name like '%browser.exe%''" + " get Description"
        )
        output_text_browser_process = subprocess.check_output(
            command_filter_browser_pid, encoding="utf-8"
        )
        assert "browser.exe" in output_text_browser_process

    finally:
        open_browser.close_coccoc_by_new_tab(language)


def test_open_coccoc_extensions():
    open_coccoc_extensions()


def open_coccoc_extensions(language=setting.coccoc_language):
    driver = None
    try:
        driver = open_browser.open_and_connect_coccoc_by_selenium(language=language)[0]
        driver.get(setting.coccoc_extensions)
    except WebDriverException:
        browser_utils.kill_all_coccoc_process()
        if driver is not None:
            driver.quit()
        driver = open_browser.open_and_connect_coccoc_by_selenium(language=language)[0]
        driver.get(setting.coccoc_extensions)
    finally:
        return driver
    # driver = open_browser.open_coccoc_by_pywinauto_then_connect_coccoc_by_selenium(language)[0]
    # driver = open_browser.open_coccoc_by_selenium(language=language)
    # driver.get(setting.coccoc_extensions)
    # return driver


def test_check_extension_version_after_installed():
    check_extension_version_after_installed()


def check_extension_version_after_installed(language=setting.coccoc_language):
    title = None
    # driver = open_browser.open_coccoc_by_selenium(language=language)
    driver = open_browser.open_and_connect_coccoc_by_selenium(language=language)[0]
    driver.get(setting.coccoc_extensions)
    major_build = browser_utils.get_coccoc_major_build()
    try:
        # Check Extension page title
        title = driver.title
        if "en" in language:
            assert extensions_page.get_title(driver) == "Cốc Cốc Extensions"
        else:
            assert extensions_page.get_title(driver) == "Tiện ích mở rộng của Cốc Cốc"

        # Check 4 default extensions appear
        if "en" in language:
            if major_build <= 107:
                assert extensions_page.get_adblock_name(driver) == "Adblock"
            assert extensions_page.get_cashback_name(driver) == "Rủng Rỉnh"
            assert extensions_page.get_dictionary_name(driver) == "Dictionary"
            assert extensions_page.get_savior_name(driver) == "Download video & audio"
        else:
            if major_build <= 107:
                assert extensions_page.get_adblock_name(driver) == "Chặn quảng cáo"
            assert extensions_page.get_cashback_name(driver) == "Rủng Rỉnh"
            assert extensions_page.get_dictionary_name(driver) == "Tra Từ Điển"
            assert extensions_page.get_savior_name(driver) == "Tải video & audio"

        # check 4 default extensions version
        # Turn on developer mode
        extensions_page.turn_on_developer_mode(driver, toggle_status="ON")
        extensions_page.check_extension_updated(driver)
        if major_build <= 107:
            assert extensions_page.get_extension_version_by_name_via_api(
                extension_name="adblock"
            ) == extensions_page.get_adblock_version(driver)
        assert extensions_page.get_extension_version_by_name_via_api(
            extension_name="en2vi"
        ) == extensions_page.get_dictionary_version(driver)
        assert extensions_page.get_extension_version_by_name_via_api(
            extension_name="rungrinh"
        ) == extensions_page.get_cashback_version(driver)
        assert extensions_page.get_extension_version_by_name_via_api(
            extension_name="savior"
        ) == extensions_page.get_savior_version(driver)

        # Check Cashback, Dictionary, adblock is turned on by default:
        if major_build <= 107:
            assert extensions_page.get_adblock_toggle_status(driver) == "ON"
        assert extensions_page.get_dictionary_toggle_status(driver) == "ON"
        assert extensions_page.get_cashback_toggle_status(driver) == "ON"

        # Check Cashback, Dictionary, adblock can be turned off:
        if major_build <= 107:
            extensions_page.toggle_adblock(driver, "OFF")
            assert extensions_page.get_adblock_toggle_status(driver) == "OFF"
            extensions_page.toggle_adblock(driver, "ON")

        extensions_page.toggle_dictionary(driver, "OFF")
        assert extensions_page.get_dictionary_toggle_status(driver) == "OFF"
        extensions_page.toggle_dictionary(driver, "ON")

        extensions_page.toggle_cashback(driver, "OFF")
        assert extensions_page.get_cashback_toggle_status(driver) == "OFF"
        extensions_page.toggle_cashback(driver, "ON")

        # Check savior extension can be turned on by default and can be turned off:
        extensions_page.click_savior_detail(driver, language=language)
        assert savior_extension_detail_page.get_savior_toggle_status(driver) == "ON"
        savior_extension_detail_page.toggle_savior(driver, toggle_status="OFF")
        assert savior_extension_detail_page.get_savior_toggle_status(driver) == "OFF"
        savior_extension_detail_page.toggle_savior(driver, toggle_status="ON")
    finally:
        open_browser.close_coccoc_by_window_title(title=title)
        if driver is not None:
            driver.quit()


def check_folders_after_installed():
    coccoc_version = browser_utils.get_coccoc_version()

    # Check for build 64 bit
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        list_files_folders_in_application_64 = file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc\Browser\Application"
        )
        # Check folders and files in C:\Program Files \CocCoc :
        assert "Browser" in file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc"
        )
        assert "Application" in file_utils.list_all_files_and_folders(
            r"C:\Program Files\CocCoc\Browser"
        )
        assert coccoc_version in list_files_folders_in_application_64
        # assert 'Dictionaries' in list_files_folders_in_application_64
        assert "SetupMetrics" in list_files_folders_in_application_64
        assert "browser.exe" in list_files_folders_in_application_64
        assert "browser_proxy.exe" in list_files_folders_in_application_64
        assert "VisualElementsManifest.xml" in list_files_folders_in_application_64

        # Check files and folders in  C:\Users\<Account_login_Windows>\AppData\Local\CocCoc\ :
        assert "Browser" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc"
        )
        assert "User Data" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser"
        )

        # Check files and folders in C:\Users\<Account_login_Windows>\AppData\Roaming\CocCoc :
        assert "hid3" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc"
        )
        assert "uid" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc"
        )

    # Check for build 32 bit
    else:
        list_files_folders_in_application_32 = file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc\Browser\Application"
        )
        # Check files and folders in C:\Program\Files(x86)\CocCoc
        files_and_folder_in_coccoc = file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc"
        )
        assert "Browser" in files_and_folder_in_coccoc
        assert "CrashReports" in files_and_folder_in_coccoc
        assert "Update" in files_and_folder_in_coccoc
        assert "Temp" in files_and_folder_in_coccoc
        assert "Application" in file_utils.list_all_files_and_folders(
            r"C:\Program Files (x86)\CocCoc\Browser"
        )

        assert coccoc_version in list_files_folders_in_application_32
        # assert 'Dictionaries' in list_files_folders_in_application_32
        assert "SetupMetrics" in list_files_folders_in_application_32
        assert "browser.exe" in list_files_folders_in_application_32
        assert "browser_proxy.exe" in list_files_folders_in_application_32
        assert "VisualElementsManifest.xml" in list_files_folders_in_application_32

        # Check files and folders in  C:\Users\<Account_login_Windows>\AppData\Local\CocCoc\ :
        assert "Browser" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc"
        )
        assert "User Data" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser"
        )

        # Check files and folders in C:\Users\<Account_login_Windows>\AppData\Roaming\CocCoc :
        assert "hid3" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc"
        )
        assert "uid" in file_utils.list_all_files_and_folders(
            rf"C:\Users\{os_utils.get_username()}\AppData\Roaming\CocCoc"
        )


def check_dictionaries():
    coccoc_version = browser_utils.get_coccoc_version()

    # Check for build 64 bit
    if file_utils.check_file_is_exists(setting.coccoc_binary_64bit):
        assert "coccoc_en-vi.dat" in file_utils.list_all_files_and_folders(
            rf"C:\Program Files\CocCoc\Browser\Application\{coccoc_version}\Dictionaries"
        )
        assert "coccoc_zh-vi.dat" in file_utils.list_all_files_and_folders(
            rf"C:\Program Files\CocCoc\Browser\Application\{coccoc_version}\Dictionaries"
        )
    # Check for build 32 bit
    else:
        assert "coccoc_en-vi.dat" in file_utils.list_all_files_and_folders(
            rf"C:\Program Files (x86)\CocCoc\Browser\Application\{coccoc_version}\Dictionaries"
        )
        assert "coccoc_zh-vi.dat" in file_utils.list_all_files_and_folders(
            rf"C:\Program Files (x86)\CocCoc\Browser\Application\{coccoc_version}\Dictionaries"
        )


def test_check_browser_and_omaha_version():
    check_browser_and_omaha_version()


def open_about_coccoc(language=setting.coccoc_language):
    driver: WebDriver = open_browser.open_coccoc_by_selenium(language=language)
    try:
        driver.get(setting.coccoc_about)
    except WebDriverException:
        if driver is not None:
            driver.quit()
        driver = open_browser.open_coccoc_by_selenium(language=language)
        driver.get(setting.coccoc_about)
    finally:
        return driver


def check_browser_and_omaha_version(language=setting.coccoc_language):
    # check version via "About CocCoc", browser version at coccoc://version
    # and browser version at <Application path>\CocCoc\Browser\Application
    driver: WebDriver = open_about_coccoc()
    try:
        coccoc_chromium_version = browser_utils.get_coccoc_version()
        if language == "en":
            interactions.wait_for_text_present_shadow_element(
                driver, MESSAGE_UP_TO_DATE, "Cốc Cốc is up to date."
            )
            # version_from_about_page = interactions.get_text_from_element_by_inner_text_js_path(driver,
            #                                                                                    COCCOC_VERSION_ABOUT_PAGE)
            version_from_about_page = interactions.get_text_from_js_path(
                driver, COCCOC_VERSION_ABOUT_PAGE
            )
            version = string_number_utils.find_text_between_2_string(
                version_from_about_page, "Version ", " (Official Build)"
            )
            # print(version)
            # As chromium change to format MAJOR.0.0.0 so we need to format
            version = version.split(".", 1)[0] + ".0.0"  # change to "111.0.0"
            coccoc_chromium_version = (
                coccoc_chromium_version.split(".", 1)[0] + ".0.0"
            )  # change to "105.0.0"
            driver.get(setting.coccoc_version_page)
            time.sleep(1)
            version_from_version_page = interactions.get_text_from_element(
                driver, COCCOC_VERSION_PAGE
            )
            # print(version_from_version_page)
            assert "coc_coc_browser/" + version in version_from_version_page
            assert "Chrome/" + coccoc_chromium_version in version_from_version_page
        else:
            interactions.wait_for_text_present_shadow_element(
                driver, MESSAGE_UP_TO_DATE, "Cốc Cốc đã được cập nhật."
            )
            version_from_about_page = (
                interactions.get_text_from_element_by_inner_text_js_path(
                    driver, COCCOC_VERSION_ABOUT_PAGE
                )
            )
            version = string_number_utils.find_text_between_2_string(
                version_from_about_page, "Phiên bản ", " (Phiên bản Chính thức)"
            )
            # As chromium change to format MAJOR.0.0.0 so we need to format
            version = version.split(".", 1)[0] + ".0.0"  # change to "111.0.0"
            coccoc_chromium_version = (
                coccoc_chromium_version.split(".", 1)[0] + ".0.0"
            )  # change to "105.0.0"
            driver.get(setting.coccoc_version_page)
            time.sleep(1)
            version_from_version_page = interactions.get_text_from_element(
                driver, COCCOC_VERSION_PAGE
            )
            assert "coc_coc_browser/" + version in version_from_version_page
            assert "Chrome/" + coccoc_chromium_version in version_from_version_page
    finally:
        if driver is not None:
            driver.quit()

    if file_utils.check_folder_is_exists("C:\\Program Files (x86)\\CocCoc\\Update"):
        # if os_utils.get_real_system_arch(is_format=False) ==
        omaha_folder_name = file_utils.list_all_files_and_folders(
            directory="C:\\Program Files (x86)\\CocCoc\\Update"
        )[0]
        product_version = file_utils.get_file_properties(
            f"C:\\Program Files (x86)\\CocCoc\\Update\\{omaha_folder_name}\\CocCocUpdate.exe",
            property_name="ProductVersion",
        )
    else:
        omaha_folder_name = file_utils.list_all_files_and_folders(
            directory="C:\\Program Files\\CocCoc\\Update"
        )[0]
        product_version = file_utils.get_file_properties(
            f"C:\\Program Files\\CocCoc\\Update\\{omaha_folder_name}\\CocCocUpdate.exe",
            property_name="ProductVersion",
        )
    # print(product_version)
    assert omaha_folder_name == product_version
    try:
        """Adding host"""
        file_utils.rename_and_copy_file_host()
        """Execute upgrade browser via About us, then click Relaunch button"""
        # setting_about_coccoc.click_relaunch_button()

        # After change host, trying to restart 'Background intelligent tranfer service" for sure
        os_utils.restart_background_intellignet_transfer()

        os_utils.open_cmd_pywinauto()
        if file_utils.check_folder_is_exists("C:\\Program Files (x86)\\CocCoc\\Update"):
            keyboard.send_keys(
                "cd C:\\Program Files {(}x86{)}\\CocCoc\\Update", with_spaces=True
            )
        else:
            keyboard.send_keys("cd C:\\Program Files\\CocCoc\\Update", with_spaces=True)
        keyboard.send_keys("{ENTER}")
        keyboard.send_keys("CocCocUpdate.exe /ua /machine", with_spaces=True)
        keyboard.send_keys("{ENTER}")
        # TODO FIX handle omaha update vs non-update
        # Waiting for the update is done and the dialog is started automatically then close it
        print("active omaha", browser_utils.get_active_omaha_version())
        print("latest ftp", browser_utils.get_latest_omaha_from_ftp())
        if (
            browser_utils.get_active_omaha_version()
            != browser_utils.get_latest_omaha_from_ftp()
        ):
            wait_for_the_omaha_update_is_done()
        else:
            wait_for_the_update_is_done()
    finally:
        file_utils.remove_and_revert_file_host()
        # Close the CMD
        os_utils.kill_process_by_name("cmd.exe")
        time.sleep(1)
        # cmd_window['Administrator'].close()


# @always_wait_until_passes(300, 4)
def wait_for_the_update_is_done():
    app = None
    title = "Connecting to the Internet..., Cốc Cốc Application Installer"
    try:
        app = Application(backend="uia").connect(
            class_name="#32770",
            control_type=50033,
            title_re=title,
            timeout=setting.timeout_pywinauto,
        )
        assert (
            app[title]
            .child_window(
                title="No update is available.", auto_id="2011", control_type="Text"
            )
            .is_visible()
            is True
        )
    finally:
        app[title].child_window(
            title="Close", auto_id="2003", control_type="Button"
        ).click()
    # app[title].print_control_identifiers()
    # app[title].set_focus()
    # app[title].close()


def test_wait_for_the_update_is_done():
    wait_for_the_update_is_done()


def wait_for_the_omaha_update_is_done():
    pid = get_running_process_ids("CocCocUpdate.exe")[0]
    app: WindowSpecification = os_utils.connect_pid(pid)

    assert app
    app.child_window(
        title="Installation complete.",
        auto_id="2011",
        control_type="Text",
    ).wait("visible", timeout=10, retry_interval=1)
    os_utils.kill_process_by_name("CocCocUpdate.exe")

    # while total_delay < max_delay:
    #     try:
    #         app = Application(backend="uia").connect(
    #             class_name="#32770",
    #             control_type=50033,
    #             title_re=title,
    #             timeout=5,
    #             retry_interval=1,
    #         )
    #     except Exception:
    #         pass
    #     else:
    #         if app:
    #             assert (
    #                 app.window()
    #                 .child_window(
    #                     title="Installation complete.",
    #                     auto_id="2011",
    #                     control_type="Text",
    #                 )
    #                 .is_visible()
    #                 is True
    #             )
    #             break
    #         else:
    #             time.sleep(interval_delay)
    #             total_delay += interval_delay

    #             continue
    #     if total_delay >= max_delay:
    #         break
    # return

    # Application(backend="uia").connect(
    #     class_name="#32770",
    #     control_type=50033,
    #     title_re=title,
    #     timeout=5,
    #     retry_interval=1,
    # ).window().child_window(
    #     title="Close", auto_id="2003", control_type="Button"
    # ).click()


def test_wait_for_the_omaha_update_is_done():
    wait_for_the_omaha_update_is_done()


def check_task_scheduler():
    faulthandler.disable()
    # Start CMD as Administrator
    # cmd_window = os_utils.open_cmd_as_administrator()
    cmd_window = os_utils.open_cmd_pywinauto()
    try:
        keyboard.send_keys(
            rf"schtasks /query | findstr CocCoc > C:\Users\{os_utils.get_username()}\Downloads\output.txt",
            with_spaces=True,
        )
        keyboard.send_keys("{ENTER}")
        time.sleep(2)
        # cmd_window['Administrator'].close()

        with open(
            rf"C:\Users\{os_utils.get_username()}\Downloads\output.txt",
            "r",
            encoding="utf-8",
        ) as f:
            lines = f.readlines()
            output_content = ""
            for line in lines:
                output_content = output_content + " " + str(line)
            assert "CocCocUpdateTaskMachineCore" in output_content
            assert "CocCocUpdateTaskMachineUA" in output_content
    finally:
        os_utils.kill_process_by_name("cmd.exe")
        os.remove(rf"C:\Users\{os_utils.get_username()}\Downloads\output.txt")


def check_file_by_virus_total(version, file_name):
    # download_setup_file.download_coccoc_setup()
    chrome_instance = open_browser.open_chrome_by_pywinauto_then_connect_by_selenium()
    driver = chrome_instance[0]
    is_verified_done = False
    max_delay = 120
    interval_delay = 2
    total_delay = 0
    element_text = None
    try:
        driver.get("https://virustotal.com/gui/home/upload")
        choose_file = interactions.get_shadow_element3(driver, CHOOSE_FILE_VIRUS_TOTAL)
        choose_file.click()
        time.sleep(2)

        keyboard.send_keys(
            rf"C:\Users\{os_utils.get_username()}\Downloads\corom\{version}{os_utils.get_window_arch()}\installers\{file_name}"
        )
        keyboard.send_keys("{ENTER}")
        time.sleep(3)
        if file_name == "CocCocSetup.exe":
            pass
        else:
            confirm_upload = interactions.get_shadow_element3(
                driver, BTN_CONFIRM_UPLOAD
            )
            if confirm_upload:
                confirm_upload.click()

        while True:
            element_text = interactions.get_shadow_element3(
                driver, VIRUS_TOTAL_RESULT, timeout=5
            )
            if element_text is not None:
                break
            time.sleep(interval_delay)
            total_delay += interval_delay
            if total_delay > max_delay:
                print(f"Timeout for waiting to check from total virus")
                break
        assert (
            "No security vendors and no sandboxes flagged this file as malicious"
            == element_text.text
        )
    finally:
        open_browser.close_chrome_by_kill_process(sleep_n_seconds=1)
        if driver is not None:
            driver.quit()


def test_check_file_by_virus_total():
    # check_file_by_virus_total(file_name='CocCocSetup.exe')
    check_file_by_virus_total(file_name="standalone_106.0.5249.56_machine.exe")


# def check_file_by_virus_total2()


def check_registry_win11():
    faulthandler.disable()
    windows_version = os_utils.get_windows_version()
    time.sleep(0.5)
    if windows_version == "11":
        if setting.platform == "32bit" and os_utils.get_real_arch == "32bit":
            coccoc_x32 = subprocess.check_output(
                r'Reg Query "HKEY_CURRENT_USER\SOFTWARE\Clients\StartMenuInternet"',
                encoding="utf-8",
            )
            time.sleep(0.5)
            assert "Cốc Cốc" not in coccoc_x32
            assert "CocCoc" in coccoc_x32
        else:
            coccoc_x64 = subprocess.check_output(
                r'Reg Query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node"', encoding="utf-8"
            )
            time.sleep(0.5)
            assert "Cốc Cốc" not in coccoc_x64
            assert "CocCoc" in coccoc_x64


def check_signatures_for_dll_exe_file():
    faulthandler.disable()
    process = subprocess.Popen(
        [
            "powershell.exe",
            str(get_project_root())
            + r"\src\data\scripts\checking_Digital_Signatures.ps1",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
    )
    stdout_value = process.communicate()[0]
    # print(stdout_value)
    assert "Test passed, no file has invalid sig" in str(stdout_value)


def test_check_signatures_for_dll_exe_file():
    check_signatures_for_dll_exe_file()


def check_browser_after_installed(platform: str, language: str):
    # check version
    assert browser_utils.get_coccoc_version() == setting.coccoc_test_version

    # check platform 32bit or 64bit
    if platform == "64bit":
        assert (
            file_utils.check_file_is_exists(browser_utils.get_coccoc_executable_path())
            is True
        )
    else:
        assert (
            file_utils.check_file_is_exists(browser_utils.get_coccoc_executable_path())
            is True
        )

    # Check language
    assert language in browser_utils.get_current_coccoc_language()


def check_terms(language):
    driver = None
    try:
        driver = open_browser.open_coccoc_by_selenium(language=language)
        driver.get("coccoc://terms/")
        time.sleep(1)
        if language == "vi":
            interactions.wait_for_text_is_present(
                driver, (By.CSS_SELECTOR, "body > h3"), "ĐIỀU KHOẢN SỬ DỤNG"
            )
            assert "ĐIỀU KHOẢN SỬ DỤNG" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h3")
            )

            assert "1. QUY ĐỊNH CHUNG" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h4:nth-child(3)")
            )
            assert "2. TỪ CHỐI BẢO ĐẢM" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h4:nth-child(7)")
            )
            assert (
                "3. THAY ĐỔI ĐIỀU KHOẢN SỬ DỤNG"
                == interactions.get_text_from_element(
                    driver, (By.CSS_SELECTOR, "body > h4:nth-child(10)")
                )
            )
        else:
            interactions.wait_for_text_is_present(
                driver, (By.CSS_SELECTOR, "body > h3"), "TERMS OF USE"
            )
            assert "TERMS OF USE" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h3")
            )
            assert "1. GENERAL REGULATION" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h4:nth-child(4)")
            )
            assert "2. REFUSALS OF WARRANTIES" == interactions.get_text_from_element(
                driver, (By.CSS_SELECTOR, "body > h4:nth-child(7)")
            )
            assert (
                "3. MODIFICATION OF TERM OF USE"
                == interactions.get_text_from_element(
                    driver, (By.CSS_SELECTOR, "body > h4:nth-child(10)")
                )
            )
    finally:
        interactions_windows.close_coccoc_by_window_title(
            title=driver.title, language=language
        )
        if driver is not None:
            driver.quit()


def test_check_terms():
    check_terms(language="en")


# Open a coccoc then reload repeatedly and wait for the metrics sent
def wait_for_metrics_is_sent(url="https://www.google.com", timeout=300) -> bool:
    max_delay = timeout
    interval_delay = 10
    total_delay = 0
    metrics_json = rf"C:\Users\{os_utils.get_username()}\Documents\metrics_log.json"
    # metrics_json = str(file_utils.get_project_root()) + r'\data\dummy_data\metrics.json'
    # driver = open_browser.open_coccoc_by_selenium()
    # driver.get(url)
    # while total_delay < max_delay:
    #     try:
    #         driver.refresh()
    #         if file_utils.check_file_is_exists(metrics_json):
    #             break
    #     except Exception:
    #         pass
    #     time.sleep(interval_delay)
    #     total_delay += interval_delay

    # driver.quit()
    address_bar_and_search = open_browser.open_url_from_coccoc_by_pywinauto()
    while total_delay < max_delay:
        try:
            address_bar_and_search.type_keys("{F5}")
            if file_utils.check_file_is_exists(metrics_json):
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay

    if file_utils.check_file_is_exists(metrics_json):
        return True
    else:
        print(rf"Time out after {timeout} seconds of waiting for the metrics sent")
        return False


def test_wait_for_metrics_is_sent():
    wait_for_metrics_is_sent()


def read_metrics_sent_when_open_browser():
    metrics_json = rf"C:\Users\{os_utils.get_username()}\Documents\metrics_log.json"
    if file_utils.check_file_is_exists(metrics_json):
        with open(metrics_json, encoding="utf-8") as file:
            parsed_json = json.load(file)
            return parsed_json
    else:
        print(rf"No {metrics_json} file found")
