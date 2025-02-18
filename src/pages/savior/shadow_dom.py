import time

from selenium import webdriver
from pyshadow.main import Shadow
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService


def open_youtube():
    coccoc_options = ChromeOptions()
    coccoc_options.binary_location = f'C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe'
    coccoc_options.add_argument("user-data-dir=C:\\Users\\taynq\\AppData\\Local\\CocCoc\\Browser\\User Data")
    coccoc_options.add_argument('profile-directory=Default')
    # coccoc_options.binary_location = f'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    coccoc_service = ChromeService(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=coccoc_service, options=coccoc_options)
    driver = webdriver.Chrome(chrome_options=coccoc_options)
    driver.get('https://www.youtube.com/watch?v=w9r4nSBXKcw')
    time.sleep(20)
    action = ActionChains(driver)
    action.move_to_element(driver.find_element(By.CSS_SELECTOR, '#movie_player > div.html5-video-container > video'))
    driver.find_element(By.CSS_SELECTOR, '#movie_player > div.html5-video-container > video').click()
    time.sleep(10)
    # shadow_host = driver.find_element(By.CSS_SELECTOR, 'div[style="position: absolute; top: 0px;"]')
    # shadow_root = shadow_host.shadow_root
    # shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '#hide-widget')
    # shadow_content.click()
    # driver.execute_script(
    # wait = WebDriverWait(driver, 10)
    # js_path = "document.querySelector('div[style="position: absolute; top: 0px;"]').shadowRoot.querySelector('#download-main')"
    # wait.until(EC.presence_of_element_located(driver.execute_script(
    #     'return ' + js_path
    # ))).click()
    first = "div[style='position: absolute; top: 0px;']"
    second = "#hide-widget"
    print('return document.querySelector("{}").shadowRoot.querySelector("{}")'.format(first, second))
    script = 'return document.querySelector("{}").shadowRoot.querySelector("{}")'.format(first, second)
    # element = WebElement(driver.execute_script(
    #             'return document.querySelector(arguments[0]).shadowRoot.querySelector(arguments[1])',
    #             first, second))
    element = driver.execute_script(script)

    print('====================')
    print(element)
    print('====================')
    element.click()

    # shadow = Shadow(driver)
    # time.sleep(20)
    # shadow.find_element('#hide-widget').click()
    # element.click()
    # elements = shadow.find_elements("paper-tab[title='Settings']")
    # text = element.text
