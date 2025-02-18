import csv
import json
import sys

from src.utilities import os_utils, file_utils


def get_data_from_csv(filename_with_full_path):
    list_temp = []
    # dirname, runname = os.path.split(os.path.abspath(__file__))
    # filename = dirname + filename
    with open(filename_with_full_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # print("CSV Reader: READING CSV FILE >>", filename)
        try:
            for row in reader:
                for q in row:
                    if q is None or len(q) == 0:
                        pass
                    else:
                        list_temp.append(q)
            # LOGGER.info("CSV Reader: FINISHED READING CSV FILE =>", filename)
            return list_temp
        except csv.Error as i:
            sys.exit(
                "file {}, line {}: {}".format(
                    filename_with_full_path, reader.line_num, i
                )
            )
            # return None
        except EOFError as e:
            # LOGGER.info("Can not read file CSV:", filename)
            # LOGGER.info("System error:", e)
            return None


def write_result_data_for_page_load_time(
    file_name, keyname_list: list, value_list: list, browser_name, result_type=""
):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        total_value = 0
        # file.write(rf"{browser_name}: Results for {result_type} is as below :\n")
        for keyname, value in zip(keyname_list, value_list):
            file.write("%-60s" "%s" % (keyname, value))
            file.write("\n")
            total_value += value
        average_value = total_value / len(value_list)
        file.write(f"Average is : {average_value}")
    file.close()


def write_result_data_for_cpu_ram_for_all_sites(
    file_name, res, browser_name, result_type=""
):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        # file.write(f"Results for {result_type} is as below :\n")
        cpu_total = 0
        mem_total = 0
        file.write(f"\n\n{browser_name} results:\n")
        file.write("%-25s" "%-60s" "%s" % ("No.", "CPU", "Memory"))
        for i in range(len(res)):
            cpu_total += int(res[i].get("cpu"))
            mem_total += int(res[i].get("mem"))
            # file.write("i is %d\n" % i)
            # file.write("CPU is %s, Mem is %s\n" % (res[i].get("cpu"), res[i].get("mem")))
            file.write("\n")
            file.write(
                "%-25s"
                "%-60s"
                "%s" % (i + 1, round(res[i].get("cpu"), 2), round(res[i].get("mem"), 2))
            )
        cpu_average = cpu_total / len(res)
        mem_average = mem_total / len(res)
        # file.write("\nAverage value is :\n")
        # file.write(f"CPU % : {cpu_average}\n")
        # file.write(f"MEM (MB) : {mem_average}")
        file.write(
            "%-25s"
            "%-60s"
            "%s" % ("\nAverage:", round(cpu_average, 2), round(mem_average, 2))
        )
    file.close()


def write_result_data_for_cpu_ram_of_each_site_preset_title(file_name):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        file.write(
            "%-35s"
            "%-25s"
            "%-25s"
            "%-25s"
            "%-25s"
            "%s" % ("Sites", "CocCoc", "Chrome", "Brave", "HIGHEST", "LOWEST")
        )
        file.write("\n")
        file.write(
            "%-35s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                "Factors",
                "CPU %",
                "RAM(MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
            )
        )
        file.write("\n")
    file.close()


def write_result_data_for_cpu_ram_of_each_site(
    file_name, res, max_cpu, max_mem, min_cpu, min_mem
):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        file.write("\n")
        file.write(
            "%-35s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                res[0].get("url"),
                round(res[0].get("cpu"), 2),
                round(res[0].get("mem"), 2),
                round(res[1].get("cpu"), 2),
                round(res[1].get("mem"), 1),
                round(res[2].get("cpu"), 2),
                round(res[2].get("mem"), 2),
                max_cpu,
                max_mem,
                min_cpu,
                min_mem,
            )
        )

    file.close()


def write_result_data_for_cpu_ram_when_launching_browser_preset_title(file_name):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        file.write(
            "%-35s"
            "%-25s"
            "%-25s"
            "%-25s"
            "%-25s"
            "%s" % ("Loop No.", "CocCoc", "Chrome", "Brave", "HIGHEST", "LOWEST")
        )
        file.write("\n")
        file.write(
            "%-35s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                "Factors",
                "CPU %",
                "RAM(MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
            )
        )
        file.write("\n")
    file.close()


def write_result_data_for_cpu_ram_when_launching_browser(
    file_name, res, max_cpu, max_mem, min_cpu, min_mem, loop_no
):
    with open(file_name, "a+", encoding="utf-8") as file:
        # file.truncate(0)
        file.write("\n")
        file.write(
            "%-35s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                loop_no,
                round(res[0].get("cpu"), 2),
                round(res[0].get("mem"), 2),
                round(res[1].get("cpu"), 2),
                round(res[1].get("mem"), 1),
                round(res[2].get("cpu"), 2),
                round(res[2].get("mem"), 2),
                max_cpu,
                max_mem,
                min_cpu,
                min_mem,
            )
        )

    file.close()


def write_result_data_for_cpu_ram_for_all_sites_comparing(
    file_name, res, max_cpu, max_mem, min_cpu, min_mem
):
    with open(file_name, "a+", encoding="utf-8") as file:
        file.write("\n\nFINAL RESULTS:")
        file.write(
            "\n========================================================================================================================\n"
        )
        file.write(
            "%-25s"
            "%-25s"
            "%-25s"
            "%-25s"
            "%s" % ("CocCoc", "Chrome", "Brave", "HIGHEST", "LOWEST")
        )
        file.write("\n")
        file.write(
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                "CPU %",
                "RAM(MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
                "CPU %",
                "RAM (MB)",
            )
        )
        file.write("\n")
        file.write(
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%-15s"
            "%-10s"
            "%s"
            % (
                round(res[0].get("cpu"), 2),
                round(res[0].get("mem"), 2),
                round(res[1].get("cpu"), 2),
                round(res[1].get("mem"), 1),
                round(res[2].get("cpu"), 2),
                round(res[2].get("mem"), 2),
                max_cpu,
                max_mem,
                min_cpu,
                min_mem,
            )
        )
    file.close()


def read_json_file(file_name: str) -> dict:
    json_file = rf"C:\Users\{os_utils.get_username()}\Documents\{file_name}.json"
    if file_utils.check_file_is_exists(json_file):
        with open(json_file, encoding="utf-8") as file:
            parsed_json = json.load(file)
            return parsed_json
    else:
        print(rf"No {json_file} file found")


def write_text_to_file(file_name: str, content: str):
    with open(file_name, "a+", encoding="utf-8") as file:
        file.write(content)
    file.close()
