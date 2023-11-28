import os
import subprocess
import time
from colorama import Fore, Style
from clint.textui import colored

DELAY_TO_CONNECT = 5
DELAY_TO_SCAN_ON_ATTACKS = 1

Fore.RESET
Style.RESET_ALL

def print_banner():
    print(colored.red(" _   _ ____   ____ _  __"))
    print(colored.red("| | | / ___| / ___| |/ /"))
    print(colored.red("| |_| \___ \| |   | ' / "))
    print(colored.red("|  _  |___) | |___| . \ "))
    print(colored.red("|_| |_|____/ \____|_|\_\ "))
    print(colored.red("                        "))

def write_log(message):
    with open('arp_spoof_detector.log', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def notify_user(message, color=Fore.RED):
    print(color + message + Style.RESET_ALL)
    write_log(message)

def disconnect_from_network():
    os.system("ipconfig /release")
    notify_user("[X] Disconnected from the network", color=Fore.RED)
    notify_user(f"[V] Waiting for {DELAY_TO_CONNECT} seconds, we will automatically reconnect", color=Fore.GREEN)
    time.sleep(DELAY_TO_CONNECT)
    os.system("ipconfig /renew")
    notify_user("[x] Successfully connected to the network", color=Fore.GREEN)

def arp_spoof_detector():
    arp_mac_address_table = list()
    router_mac = ""
    new_arp_table = list()

    try:
        notify_user("[x] Scanning for attacks", color=Fore.BLUE)
        check = subprocess.check_output(["arp", "-a"], encoding="latin-1")
    except Exception as e:
        notify_user(f"Error during ARP scan: {e}", color=Fore.YELLOW)
        return

    check = check.split(" ")

    for mac_address in check:
        if ("-" in mac_address or ":" in mac_address) and "Interface" not in mac_address and "---" not in mac_address:
            arp_mac_address_table.append(mac_address)

    router_mac = str(arp_mac_address_table[1])

    for i in arp_mac_address_table:
        if router_mac in i:
            pass
        else:
            new_arp_table.append(i)

    try:
        calc = 2
        for j in arp_mac_address_table:
            if router_mac == arp_mac_address_table[calc]:
                potential_attacker_mac = arp_mac_address_table[calc - 1]
                notify_user(f"[!] Spoof attack detected from MAC address: {potential_attacker_mac}", color=Fore.RED)
                disconnect_from_network()

            calc += 1

    except IndexError:
        pass

def main():
    print_banner()

    while True:
        try:
            arp_spoof_detector()
        except Exception as e:
            notify_user(f"An error occurred: {e}", color=Fore.YELLOW)

        time.sleep(DELAY_TO_SCAN_ON_ATTACKS)

if __name__ == "__main__":
    main()
