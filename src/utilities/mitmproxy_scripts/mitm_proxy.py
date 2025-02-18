from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# from src.pages.coccoc_common.open_browser import get_chrome_executable_path


def main():
    # the mitm proxy ip and port
    proxy = "127.0.0.1:8080"
    chrome_options = ChromeOptions()
    chrome_options.binary_location = (
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    )
    chrome_service = ChromeService(ChromeDriverManager().install())

    # tel the driver to use the proxy
    webdriver.DesiredCapabilities.CHROME["proxy"] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("https://www.stackoverflow.com")
    # Just to make sure all AJAX calls are done. What if it takes more than 5s?
    # No other better way, hence using this.
    time.sleep(5)
    driver.close()


if __name__ == "__main__":
    main()
