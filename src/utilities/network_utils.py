import os
import platform
import subprocess
import time

import pyshark

from src.utilities import os_utils, file_utils
from tests import setting


def test_block_network_by_interface():
    block_network_by_interface()


def block_network_by_interface(interface_name="Ethernet"):
    """Blocking the network for specific interface

    Args:
        interface_name (str, optional): _description_. Defaults to "Ethernet".
    """
    # To print out all network interfaces (Ethernet, Wi-Fi)
    # print((os.system('netsh interface show interface')))
    os.system(f'netsh interface set interface "{interface_name}" disable')
    wait_for_the_network_is_down()


def test_enable_network_by_interface():
    enable_network_by_interface()


def enable_network_by_interface(interface_name="Ethernet"):
    """Enable the network for specific interface

    Args:
        interface_name (str, optional): _description_. Defaults to "Ethernet".
    """
    os.system(f'netsh interface set interface "{interface_name}" enable')
    # Wait for the network is up again
    # wait_for_the_network_is_up()


def test_disable_enable_network():
    block_network_by_interface(interface_name="Ethernet")
    # time.sleep(5)
    enable_network_by_interface(interface_name="Ethernet")


def block_network_by_ip(ip_address):
    # Ip format remoteip=192.xxx.xxx.x/xx
    os.system(
        f'netsh advfirewall firewall add rule name="BLOCKED IP" interface=any dir=in action=block remoteip={ip_address}'
    )
    os.system(
        f'netsh advfirewall firewall add rule name="BLOCKED IP" interface=any dir=out action=block remoteip={ip_address}'
    )


def get_packet_info(interface=None, filter_string=None):
    """
    Returns the size of the transmitted data using Wireshark.

    Args:
        interface: A string. Name of the interface to sniff on.

    Returns: Size of the packet sent over WebSockets in a given event.
    """
    packet_info = None
    if interface is None:
        raise Exception("Please provide the interface used.")
    else:
        capture = pyshark.LiveCapture(interface=interface, bpf_filter=filter_string)
        capture.sniff(timeout=60)
        # for packet in capture:
        #     try:
        #         packet_info = packet.pretty_print()
        #     except:
        #         raise Exception("Cannot determine packet info.")
        # return packet_info
    for packet in capture:
        print(packet.pretty_print())


def test_get_packet_info():
    # print(get_packet_info(interface='Ethernet'))
    get_packet_info()


def capture_live_ring():
    capture = pyshark.LiveCapture()
    capture.sniff(timeout=50)
    for packet in capture.sniff_continuously(packet_count=5):
        print("Just arrived:", packet.ip.addr)
        print("Just out:", packet.ip.host)


def test_capture_live_ring():
    capture_live_ring()


def dump_network_log(file_name: str):
    cmd_windows = os_utils.open_cmd_pywinauto()
    deactivate = (
        rf"{str(file_utils.get_project_root().parent)}\venv\Scripts\deactivate.bat"
    )
    command = rf"mitmdump -s {str(file_utils.get_project_root())}\src\utilities\mitmproxy_scripts\{file_name} --listen-port=9090 --listen-host=127.0.0.1"

    # cmd_windows.type_keys(deactivate, with_spaces=True)
    # cmd_windows.type_keys('{ENTER}', with_spaces=True)

    cmd_windows.type_keys(command, with_spaces=True)
    cmd_windows.type_keys("{ENTER}", with_spaces=True)
    time.sleep(15)


def test_dump_network_log():
    # os_utils.turn_proxy_on()

    # Start mitmdump
    dump_network_log()
    #
    # time.sleep(10)

    # os_utils.turn_proxy_off()


def test_check_the_network_is_up():
    wait_for_the_network_is_up()


def check_the_network_is_up(
    hostname: str = "google.com", timeout=setting.timeout_waiting_for_network_up
):
    is_connected = False
    interval_delay = 1
    total_delay = 0

    while total_delay < timeout:
        try:
            if os.system("ping -c 1 " + hostname) == 0:
                is_connected = True  # Mean connecting is OK
                break

        except Exception:
            pass
        time.sleep(interval_delay)
        total_delay += interval_delay
    if total_delay >= timeout:
        print(rf"timeout for waiting the network is up after {timeout} seconds")
    return is_connected


def wait_for_the_network_is_up(
    hostname: str = "google.com", timeout=setting.timeout_waiting_for_network_up
) -> bool:
    is_connected = False
    interval_delay = 1
    total_delay = 0
    param = "-n" if platform.system().lower() == "windows" else "-c"
    while total_delay < timeout:
        try:
            command = ["ping", param, "1", hostname]
            if (
                subprocess.call(
                    command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
                == 0  # Mean connecting is OK
            ):
                is_connected = True
                break
        except Exception:
            time.sleep(interval_delay)
            total_delay += interval_delay
            pass

    if total_delay >= timeout:
        print(f"timeout for waiting the network is up after {timeout} seconds")
    return is_connected


def test_check_the_network_is_down():
    wait_for_the_network_is_down()


def wait_for_the_network_is_down(
    hostname: str = "google.com", timeout=setting.timeout_waiting_for_network_down
) -> bool:
    is_down = False
    interval_delay = 1
    total_delay = 0
    param = "-n" if platform.system().lower() == "windows" else "-c"
    while total_delay < timeout:
        try:
            command = ["ping", param, "1", hostname]
            if (
                subprocess.call(
                    command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
                != 0  # Mean disconnecting is OK
            ):
                is_down = True
                break
        except Exception:
            time.sleep(interval_delay)
            total_delay += interval_delay
            pass

    if total_delay >= timeout:
        print(f"timeout for waiting the network is down after {timeout} seconds")
    return is_down


def check_the_current_up_network_interface(interface_name: str = "Ethernet") -> bool:
    """To check the current UP network interface
    Args:
        interface_name (str, optional): _description_. Defaults to "Ethernet".
    Raises:
        e: _description_
    Returns:
        bool: True if UP, False if DOWN
    """
    cmd = (
        'Get-NetAdapter | % { Process { If (( $_.Status -eq "up" ) -and ($_.Name -eq "'
        + interface_name
        + '") ){ $_.ifIndex } }}'
    )
    try:
        process = subprocess.Popen(
            ["powershell", "& {" + cmd + "}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
            encoding="utf-8",
        )
    except Exception as e:
        raise e
    else:
        stdout_value = process.communicate()[0]
        return True if len(stdout_value) >= 1 else False


def test_get_the_current_up_network_interface():
    print(check_the_current_up_network_interface())


def block_network():
    if check_the_current_up_network_interface(interface_name="Ethernet"):
        block_network_by_interface(interface_name="Ethernet")
        wait_for_the_network_is_down()
    else:
        block_network_by_interface(interface_name="Wi-Fi")
        wait_for_the_network_is_down()


def enable_network():
    enable_network_by_interface(interface_name="Ethernet")
    enable_network_by_interface(interface_name="Wi-Fi")
    wait_for_the_network_is_up()
