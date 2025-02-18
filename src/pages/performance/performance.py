import psutil
from selenium.common.exceptions import UnexpectedAlertPresentException

from tests import setting
from src.pages.coccoc_common import open_browser
from src.utilities import read_write_data_by, browser_utils, process_id_utils

import logging
import multiprocessing as mp
import concurrent.futures
import time

from selenium.webdriver import DesiredCapabilities

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

start_browser = 0
LOGGER = logging.getLogger(__name__)


def open_webpage(self, source, binary_file, default_dir, options_list=None, enabled_ads_block=True):
    # browser = Browsers()
    # browser.kill_all_browsers()
    browser_utils.kill_all_coccoc_process()
    global start_browser

    opts = Options()
    opts.binary_location = binary_file
    opts.add_argument("start-maximized")
    opts.add_argument('user-data-dir=' + default_dir)
    # opts.add_argument("--headless --disable-gpu")
    if enabled_ads_block == "True":
        opts.add_argument("--start-maximized")
        opts.add_argument("--proxy-server='direct://'")
        opts.add_argument("--proxy-bypass-list=*")
        opts.add_argument("--start-maximized")
        opts.add_argument('--disable-gpu')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--ignore-certificate-errors')
        opts.add_argument("--allow-insecure-localhost")
        # opts.add_argument("--enable-features=CocCocBlockAdByExtension")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"  # complete
    # caps["pageLoadStrategy"] = "eager"
    if options_list is not None:
        for i in options_list:
            opts.add_argument(i)
    start_browser = int(round(time.time() * 1000))
    driver = webdriver.Chrome(options=opts, desired_capabilities=caps)

    driver.get(source)
    return driver


def get_navigation_start(driver, timeout: int = 5) -> int:
    interval_delay = 0.5
    total_delay = 0
    navigation_start = None
    while total_delay < timeout:
        try:
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            if navigation_start is not None:
                if int(navigation_start) > 0:
                    break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    # if navigation_start is None:
    #     pass
    # else:
    return int(navigation_start)


def get_response_start(driver, timeout: int = 5) -> int:
    interval_delay = 0.5
    total_delay = 0
    response_start = None
    while total_delay < timeout:
        try:
            response_start = driver.execute_script("return window.performance.timing.responseStart")
            if response_start is not None:
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if response_start is None:
        pass
    else:
        return int(response_start)


def get_dom_complete(driver, timeout: int = 5) -> int:
    interval_delay = 0.5
    total_delay = 0
    dom_complete = None
    while total_delay < timeout:
        try:
            dom_complete = driver.execute_script("return window.performance.timing.domComplete")
            if dom_complete is not None:
                break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if dom_complete is None:
        pass
    else:
        return int(dom_complete)


def get_page_complete(driver, timeout: int = 5) -> int:
    interval_delay = 0.5
    total_delay = 0
    page_complete = None
    while total_delay < timeout:
        try:
            page_complete = driver.execute_script("return window.performance.timing.loadEventEnd")
            if page_complete is not None:
                if int(page_complete) > 0:
                    break
        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    # if page_complete is None:
    #     pass
    # else:
    return page_complete


def measure_time(driver):
    global browser_startup
    page_load_time: int = 0
    navigation_start = get_navigation_start(driver)
    # print(rf'navigation start: {navigation_start}')
    response_start = get_response_start(driver)
    # print(rf' responsd start: {response_start}')
    dom_complete = get_dom_complete(driver)
    # print(rf'Dom completed: {dom_complete}')
    page_complete = get_page_complete(driver)
    # print(rf'page complete: {page_complete}')
    # #
    # if navigation_start > 0:
    #     browser_startup = navigation_start - start_browser
    # if response_start > 0 and navigation_start > 0:
    #     backend_performance = response_start - navigation_start
    # if dom_complete > 0 and response_start > 0:
    #     frontend_performance = dom_complete - response_start
    if page_complete > 0 and navigation_start > 0:
        page_load_time = page_complete - navigation_start
        # print(page_load_time)

    # LOGGER.info("Browser startup time: %s" % browser_startup)
    # LOGGER.info("First frame displayed: %s" % backend_performance)
    # LOGGER.info("DOM Load Event completed: %s" % frontend_performance)
    # LOGGER.info("Total PageLoad Time: %s" % page_load_time)

    # print(rf'page load time: {page_load_time}')
    # time.sleep(2)
    driver.quit()
    time.sleep(1)
    return page_load_time


def get_page_load_time(filename, file_name_result, browser_name,
                       is_enable_adblock=True, no_of_loop_time: int = 3):
    global page_load_time_avg
    list_websites = read_write_data_by.get_data_from_csv(filename)
    load_times = []
    index = 1
    LOGGER.info('%-25s' '%-60s' '%s' % ('No.', 'Url', 'Page load time Average'))

    for url in list_websites:
        load_time = 0
        looptime = no_of_loop_time
        for j in range(looptime):
            if browser_name == 'CocCoc':
                if not is_enable_adblock:
                    driver = open_browser.open_coccoc_by_selenium(is_enable_adblock=is_enable_adblock)
                else:
                    driver = open_browser.open_coccoc_by_selenium()
            elif browser_name == 'Chrome':
                driver = open_browser.open_chrome_by_selenium()
            else:
                driver = open_browser.open_brave_by_selenium()
            try:
                driver.get(url)
                load_time = load_time + measure_time(driver)
                page_load_time_avg = round(load_time / looptime, 1)
            except Exception as e:
                driver.quit()
            # load_time = load_time + measure_time(driver)
            # page_load_time_avg = round(load_time / looptime, 1)
        if page_load_time_avg:
            load_times.append(page_load_time_avg)
            LOGGER.info('%-25s' '%-60s' '%s' % (index, url, page_load_time_avg))
        index += 1
    read_write_data_by.write_result_data_for_page_load_time(file_name=file_name_result, keyname_list=list_websites,
                                                            value_list=load_times, browser_name=browser_name,
                                                            result_type='Page load time')


def get_cpu_per_single_process(pid):
    try:
        current_cpu_utilization = psutil.Process(pid).cpu_percent(interval=2)
        if current_cpu_utilization is None:
            current_cpu_utilization = 0.0
        return current_cpu_utilization / psutil.cpu_count()
    except Exception as e:
        print('EXCEPTION:', e)
        return 0.0


def get_memory_per_single_process(pid):
    try:
        memory_infor_pid = psutil.Process(pid).memory_info()[1]
        if memory_infor_pid is None:
            memory_infor_pid = 0.0
        return memory_infor_pid / float(2 ** 20)
    except Exception as e:
        print('EXCEPTION:', e)
        return 0.0


def test_get_pid_list():
    print(get_pid_list('browser.exe'))


def get_pid_list(process_name):
    pid_list = [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if process_name in p.info['name']]
    return pid_list


def test_benchmark():
    list_pids = [17024]
    benchmark(list_pids)


def benchmark(pid_list):
    cpus = mp.cpu_count()  # check available memory of cpu
    start = time.perf_counter()  # point of time for starting running

    try:
        with concurrent.futures.ThreadPoolExecutor(cpus) as executor:
            total_cpu = 0
            total_mem = 0
            try:
                for pid, cpu in zip(pid_list, executor.map(get_cpu_per_single_process, pid_list)):
                    print('%d has cpu usage: %s' % (pid, cpu))
                    total_cpu = total_cpu + cpu
                for pid, memory in zip(pid_list, executor.map(get_memory_per_single_process, pid_list)):
                    print('%d has memory usage: %s' % (pid, memory))
                    total_mem = total_mem + memory
            except Exception as e:
                print(e)
        end = time.perf_counter()
        print("All jobs finished in {}s".format(round(end - start, 2)))
        print("Total CPU used = %s" % total_cpu)
        print("Total Mem used = %s" % total_mem)
        return total_cpu, total_mem
    except Exception:
        print("Some pid is unavailable")


def open_webpage_with_tabs(filename, browser_name, opening_type, options_list=None, enabled_ads_block=False):
    """
        opening_type='sequence': open site1 then site2 then ... til end. if 'parallel': open all sites at the same time
    """
    # browser_utils.kill_all_coccoc_process()
    list_websites = read_write_data_by.get_data_from_csv(filename)
    # opts = Options()
    # opts.binary_location = binary_file
    # opts.add_argument("start-maximized")
    # opts.add_argument('user-data-dir=' + default_dir)
    # if enabled_ads_block == "True":
    #     opts.add_argument("--start-maximized")
    #     opts.add_argument("--proxy-server='direct://'")
    #     opts.add_argument("--proxy-bypass-list=*")
    #     opts.add_argument("--start-maximized")
    #     opts.add_argument('--disable-gpu')
    #     opts.add_argument('--disable-dev-shm-usage')
    #     opts.add_argument('--no-sandbox')
    #     opts.add_argument('--ignore-certificate-errors')
    #     opts.add_argument("--allow-insecure-localhost")
    #     opts.add_argument("--enable-features=CocCocBlockAdByExtension")
    # caps = DesiredCapabilities().CHROME
    # # caps["pageLoadStrategy"] = "normal"  # complete
    # caps["pageLoadStrategy"] = "eager"

    # if options_list is not None:
    #     for i in options_list:
    #         opts.add_argument(i)
    # driver = webdriver.Chrome(options=opts, desired_capabilities=caps)
    if browser_name == 'CocCoc':
        browser_utils.kill_all_coccoc_process()
        driver = open_browser.open_coccoc_by_selenium()
    elif browser_name == 'Chrome':
        browser_utils.kill_chrome_process()
        driver = open_browser.open_chrome_by_selenium()
    else:
        browser_utils.kill_brave_process()
        driver = open_browser.open_brave_by_selenium()
    # first tab
    try:
        driver.get(list_websites[0])
    except Exception:
        pass

    # next tabs
    # Opening site1 then site2 ... then end
    if opening_type == 'sequence':
        for i in range(len(list_websites)):
            if i + 1 < len(list_websites):
                tab_name = str(i + 1)
                try:
                    js_command = "window.open('about:blank', \'" + tab_name + "\');"
                    driver.execute_script(js_command)
                    driver.switch_to.window(tab_name)
                    print(f"\n %d. {browser_name} Open tab page: %s" % (i + 1, list_websites[i + 1]))
                    driver.get(list_websites[i + 1])
                except UnexpectedAlertPresentException:
                    alert = driver.switch_to.alert
                    alert.accept()
                except Exception as e:
                    pass
        return driver
    # Open all sites from the list at the same time
    elif opening_type == 'parallel':
        try:
            for url in list_websites[1:]:
                driver.execute_script('window.open("{}", "_blank");'.format(url))
        except Exception:
            pass
        finally:
            return driver
    else:
        print(f'Wrong opening type: {opening_type}')


def get_ram_cpu_by_open_all_sites(filename, file_name_result, browser_name, options_list=None,
                                  enabled_ads_block=False, no_of_loop_time: int = 3):
    res = []
    results_average = []
    i = 1
    LOGGER.info('%-25s' '%-60s' '%s' % ('No.', 'CPU', 'Memory'))
    for _ in range(no_of_loop_time):
        # Open all list url from file
        web_driver = open_webpage_with_tabs(filename, browser_name, options_list,
                                            enabled_ads_block=enabled_ads_block)
        # Calculate usage of Mem, Cpu
        if browser_name == 'CocCoc':
            # pid_list = get_pid_list('browser.exe')
            pid_list = process_id_utils.get_running_process_ids('browser.exe')
        elif browser_name == 'Chrome':
            # pid_list = get_pid_list('chrome.exe')
            pid_list = process_id_utils.get_running_process_ids('chrome.exe')
        else:
            # pid_list = get_pid_list('brave.exe')
            pid_list = process_id_utils.get_running_process_ids('brave.exe')
        cpu, mem = benchmark(pid_list)
        res.append({"cpu": cpu, "mem": mem})
        LOGGER.info('%-25s' '%-60s' '%s' % (i, round(cpu, 2), round(mem, 2)))
        i += 1
        web_driver.quit()
    # Write data into file
    read_write_data_by.write_result_data_for_cpu_ram_for_all_sites(file_name_result, res, browser_name,
                                                                   result_type='CPU RAM')
    # Calculate average data for each browser then return
    cpu_total = 0
    mem_total = 0
    for i in range(len(res)):
        cpu_total += int(res[i].get("cpu"))
        mem_total += int(res[i].get("mem"))
    cpu_average = cpu_total / len(res)
    mem_average = mem_total / len(res)
    results_average.append(round(cpu_average, 2))
    results_average.append(round(mem_average, 2))
    return results_average


def open_webpage_by_browser(browser_name, url, enabled_ads_block):
    if browser_name == 'CocCoc':
        browser_utils.kill_all_coccoc_process()
        driver = open_browser.open_coccoc_by_selenium()
    elif browser_name == 'Chrome':
        browser_utils.kill_chrome_process()
        driver = open_browser.open_chrome_by_selenium()
    else:
        browser_utils.kill_brave_process()
        driver = open_browser.open_brave_by_selenium()

    # Open url
    try:
        driver.get(url)
    except Exception as e:
        pass
        # print(e)
    # return the driver
    finally:
        if driver is not None:
            return driver


def get_ram_cpu_of_each_site_from_list(filename, file_name_result, options_list=None,
                                       enabled_ads_block=False, no_of_loop_time: int = 3):
    LOGGER.info('%-25s' '%-60s' '%s' % ('No.', 'CPU', 'Memory'))
    # Read list urls
    list_websites = read_write_data_by.get_data_from_csv(filename)

    # Write file and column title
    read_write_data_by.write_result_data_for_cpu_ram_of_each_site_preset_title(file_name_result)

    # Open all list url from file
    for url in list_websites:
        res = []
        # Loop in list browsers
        for browser_name in setting.performance_browsers_test:
            # Calculate usage of Mem, Cpu
            if browser_name == 'CocCoc':
                web_driver = open_webpage_by_browser(browser_name, url, enabled_ads_block=enabled_ads_block)
                # pid_list = process_id_utils.get_process_ids_by_name('browser.exe')
                pid_list = process_id_utils.get_running_process_ids('browser.exe')
            elif browser_name == 'Chrome':
                web_driver = open_webpage_by_browser(browser_name, url, enabled_ads_block=enabled_ads_block)
                pid_list = process_id_utils.get_running_process_ids('chrome.exe')
            else:
                web_driver = open_webpage_by_browser(browser_name, url, enabled_ads_block=enabled_ads_block)
                pid_list = process_id_utils.get_running_process_ids('brave.exe')
            # Get cpu, mem
            cpu, mem = benchmark(pid_list)
            # Add cpu, mem ... to result
            res.append({"browser_name": browser_name, "url": url, "cpu": cpu, "mem": mem})
            # Quit driver
            web_driver.quit()

        # get the browser usage: highest cpu/ram, lowest cpu/ram
        max_cpu = max(res, key=lambda x: x['cpu']).get('browser_name')
        max_mem = max(res, key=lambda x: x['mem']).get('browser_name')
        min_cpu = min(res, key=lambda x: x['cpu']).get('browser_name')
        min_mem = min(res, key=lambda x: x['mem']).get('browser_name')

        # Write data to file
        read_write_data_by.write_result_data_for_cpu_ram_of_each_site(file_name_result,
                                                                      res, max_cpu, max_mem, min_cpu, min_mem)


# Draft test
def test_max():
    res = [{"browser_name": "CocCoc", "url": "https://google.com", "cpu": 1.02, "mem": 1.95},
           {"browser_name": "Chrome", "url": "https://google.com", "cpu": 0.75, "mem": 1.25},
           {"browser_name": "Brave", "url": "https://google.com", "cpu": 1.32, "mem": 1.85}]

    max_cpu = max(res, key=lambda x: x['cpu'])
    max_mem = max(res, key=lambda x: x['mem'])
    print(max_cpu.get('browser_name'))
    print(max_mem.get('browser_name'))


def get_ram_cpu_when_launching_browser(file_name_result, no_of_loop_time):
    LOGGER.info('%-25s' '%-60s' '%s' % ('No.', 'CPU', 'Memory'))

    # Write file and column title
    read_write_data_by.write_result_data_for_cpu_ram_when_launching_browser_preset_title(file_name_result)

    # Loop n times
    for i in range(no_of_loop_time):
        res = []
        # Loop in list browsers
        for browser_name in setting.performance_browsers_test:
            # Calculate usage of Mem, Cpu
            if browser_name == 'CocCoc':
                browser_utils.kill_all_coccoc_process()
                web_driver = open_browser.open_coccoc_by_selenium()
                pid_list = process_id_utils.get_process_ids_by_name('browser.exe')
            elif browser_name == 'Chrome':
                browser_utils.kill_chrome_process()
                web_driver = open_browser.open_chrome_by_selenium()
                pid_list = process_id_utils.get_running_process_ids('chrome.exe')
            else:
                browser_utils.kill_brave_process()
                web_driver = open_browser.open_brave_by_selenium()
                pid_list = process_id_utils.get_running_process_ids('brave.exe')
            # Get cpu, mem
            cpu, mem = benchmark(pid_list)
            # add data to result
            res.append({"browser_name": browser_name, "cpu": cpu, "mem": mem})
            # close driver
            web_driver.quit()

        # get the browser usage: highest cpu/ram, lowest cpu/ram
        max_cpu = max(res, key=lambda x: x['cpu']).get('browser_name')
        max_mem = max(res, key=lambda x: x['mem']).get('browser_name')
        min_cpu = min(res, key=lambda x: x['cpu']).get('browser_name')
        min_mem = min(res, key=lambda x: x['mem']).get('browser_name')

        # Write data to file
        read_write_data_by.write_result_data_for_cpu_ram_when_launching_browser(file_name_result,
                                                                                res, max_cpu, max_mem, min_cpu, min_mem,
                                                                                i + 1)
