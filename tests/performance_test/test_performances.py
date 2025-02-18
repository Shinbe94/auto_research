from datetime import datetime
from pytest_pytestrail import pytestrail

from tests import setting
from src.pages.performance import performance

import logging
import os

from src.utilities import file_utils, read_write_data_by

start_browser = 0
LOGGER = logging.getLogger(__name__)


@pytestrail.case("C82299")
def xtest_browser_plt(
    is_enable_adblock=setting.enable_browser_adblock,
    browser_list=setting.performance_browsers_test,
    no_of_loop_time: int = 3,
):
    for browser_name in browser_list:
        dir_name, run_name = os.path.split(os.path.abspath(__file__))
        filename = dir_name + r"\test_data" + r"\testbenchmark.csv"
        filename_result = (
            dir_name + r"\test_result" + rf"\{browser_name} results_plt.csv"
        )
        performance.get_page_load_time(
            filename,
            filename_result,
            browser_name,
            is_enable_adblock=is_enable_adblock,
            no_of_loop_time=no_of_loop_time,
        )


@pytestrail.case("C82490")
def test_ram_cpu_by_open_all_sites_by_sequence(
    browser_list=setting.performance_browsers_test,
    opening_type="sequence",
    no_of_loop_time: int = 5,
):
    # Remove old results data
    file_utils.remove_files_re(
        directory=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
        filename_re="cpu_ram_all_sites_by_sequence",
    )
    results_average_browser = []
    dir_name, run_name = os.path.split(os.path.abspath(__file__))
    filename = dir_name + r"\test_data" + r"\testbenchmark.csv"
    file_name_result = (
        dir_name
        + r"\test_result"
        + rf'\results_cpu_ram_all_sites_by_sequence_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.csv'
    )

    for browser_name in browser_list:
        average = performance.get_ram_cpu_by_open_all_sites(
            filename,
            file_name_result,
            browser_name,
            opening_type,
            None,
            no_of_loop_time=no_of_loop_time,
        )
        results_average_browser.append(
            {"browser_name": browser_name, "cpu": average[0], "mem": average[1]}
        )

    # get the browser usage: highest cpu/ram, lowest cpu/ram
    max_cpu = max(results_average_browser, key=lambda x: x["cpu"]).get("browser_name")
    max_mem = max(results_average_browser, key=lambda x: x["mem"]).get("browser_name")
    min_cpu = min(results_average_browser, key=lambda x: x["cpu"]).get("browser_name")
    min_mem = min(results_average_browser, key=lambda x: x["mem"]).get("browser_name")
    # Write the final conclusion into file
    read_write_data_by.write_result_data_for_cpu_ram_for_all_sites_comparing(
        file_name_result, results_average_browser, max_cpu, max_mem, min_cpu, min_mem
    )


@pytestrail.case("1177926")
def test_ram_cpu_by_open_all_sites_by_parallel(
    browser_list=setting.performance_browsers_test,
    opening_type="parallel",
    no_of_loop_time: int = 1,
):
    # Remove old results data
    file_utils.remove_files_re(
        directory=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
        filename_re="cpu_ram_all_sites_by_parallel",
    )
    results_average_browser = []
    dir_name, run_name = os.path.split(os.path.abspath(__file__))
    filename = dir_name + r"\test_data" + r"\testbenchmark.csv"
    file_name_result = (
        dir_name
        + r"\test_result"
        + rf'\results_cpu_ram_all_sites_by_parallel_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.csv'
    )
    for browser_name in browser_list:
        average = performance.get_ram_cpu_by_open_all_sites(
            filename,
            file_name_result,
            browser_name,
            opening_type,
            None,
            no_of_loop_time=no_of_loop_time,
        )
        results_average_browser.append(
            {"browser_name": browser_name, "cpu": average[0], "mem": average[1]}
        )

    # get the browser usage: highest cpu/ram, lowest cpu/ram
    max_cpu = max(results_average_browser, key=lambda x: x["cpu"]).get("browser_name")
    max_mem = max(results_average_browser, key=lambda x: x["mem"]).get("browser_name")
    min_cpu = min(results_average_browser, key=lambda x: x["cpu"]).get("browser_name")
    min_mem = min(results_average_browser, key=lambda x: x["mem"]).get("browser_name")
    # Write the final conclusion into file
    read_write_data_by.write_result_data_for_cpu_ram_for_all_sites_comparing(
        file_name_result, results_average_browser, max_cpu, max_mem, min_cpu, min_mem
    )


@pytestrail.case("C1164168")
def test_ram_cpu_by_open_each_site_from_list(no_of_loop_time: int = 5):
    # remove old file before test
    file_utils.remove_files_re(
        directory=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
        filename_re="cpu_ram_each_site",
    )

    dir_name, run_name = os.path.split(os.path.abspath(__file__))
    filename = dir_name + r"\test_data" + r"\testbenchmark2.csv"
    file_name_result = (
        dir_name
        + r"\test_result"
        + rf'\browsers_results_cpu_ram_each_site_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.csv'
    )
    performance.get_ram_cpu_of_each_site_from_list(
        filename, file_name_result, None, no_of_loop_time=no_of_loop_time
    )


@pytestrail.case("C1164177")
def test_ram_cpu_when_launching_browser(no_of_loop_time: int = 20):
    # remove old file before test
    file_utils.remove_files_re(
        directory=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
        filename_re="results_cpu_ram_when_launching",
    )
    dir_name, run_name = os.path.split(os.path.abspath(__file__))
    file_name_result = (
        dir_name
        + r"\test_result"
        + rf'\browsers_results_cpu_ram_when_launching_{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.csv'
    )
    performance.get_ram_cpu_when_launching_browser(
        file_name_result, no_of_loop_time=no_of_loop_time
    )
