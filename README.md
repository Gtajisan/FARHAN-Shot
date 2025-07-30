
# FARHAN-Shot - Termux Wi-Fi Security Tool

[![Python 3.5+](https://img.shields.io/badge/Python-3.5+-yellow.svg)](https://python.org)
[![Termux](https://img.shields.io/badge/Tested-Termux/Android-brightgreen.svg)](https://termux.com)
[![Root Required](https://img.shields.io/badge/Root-Required-red.svg)]()

<p align="center">
  <img src="https://user-images.githubusercontent.com/75953873/115979290-66309900-a55b-11eb-8259-4b125efc42bb.png" width="70%">
</p>

## Overview
FARHAN-Shot performs offline **Pixie Dust attacks** on WPS-enabled routers without switching to monitor mode. Ideal for Termux on Android devices.

# Quick Start
```
curl -sSf https://raw.githubusercontent.com/gtajisan/FARHAN-Shot_Termux_installer/master/installer.sh | bash
sudo python FARHAN-Shot/FARHAN-Shot.py -i wlan0 -K
```

## Features
- ✅ Pixie Dust attack (offline)
- ✅ 3WiFi WPS PIN generator
- ✅ Online WPS bruteforce
- ✅ Wi-Fi scanner with `iw`
- ✅ Push Button Connect (PBC)
- ✅ Custom vulnerable AP lists

## Requirements
- Rooted Android device
- Termux (latest version)
- Python 3.5+
- `wpa_supplicant`, `pixiewps`, `iw`, `openssl`

## Installation
### One-Line Install
```bash
curl -sSf https://raw.githubusercontent.com/gtajisan/FARHAN-Shot_Termux_installer/master/installer.sh | bash
```

### Manual Installation
```bash
pkg update && pkg upgrade -y
pkg install root-repo git tsu python wpa-supplicant pixiewps iw openssl -y
termux-setup-storage
git clone --depth 1 https://github.com/Gtajisan/FARHAN-Shot.git
```

## Usage
### Basic Commands
# Pixie Dust attack
```
sudo python FARHAN-Shot/FARHAN-Shot.py -i wlan0 -K
```
# Alternative version
```
sudo python FARHAN-Shot/File/3FRN.py -i wlan0 -K
```
```
sudo python FARHAN-Shot/File/FRN.PY -i wlan0 -K
```
# Online bruteforce
```
sudo python FARHAN-Shot/FARHAN-Shot.py -i wlan0 -b 00:90:4C:C1:AC:21 -B -p 1234
```

### Advanced Options
```bash
# Full command syntax
FARHAN-Shot.py -i <interface> [options]

Options:
  -b, --bssid       Target BSSID
  -p, --pin         Custom WPS PIN
  -K, --pixie-dust  Pixie Dust attack
  -B, --bruteforce  Online WPS bruteforce
  --push-button-connect  PBC WPS
  -d, --delay       Delay between pins
  -w, --write       Save credentials to file
  -F, --pixie-force Bruteforce full range
```

## Troubleshooting
### Common Issues
# Operation not possible due to RF-kill
```
sudo rfkill unblock wifi
```
# Device busy error
```
sudo python FARHAN-Shot.py -i wlan0 -K --iface-down
```
# MediaTek devices
```
sudo python FARHAN-Shot.py -i wlan0 -K --mtk-wifi
```

## Support & Contact
[![Facebook](https://img.shields.io/badge/Facebook-FARHAN-blue?logo=facebook)](https://www.facebook.com/profile.php?id=100094924471568)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat-green?logo=whatsapp)](https://wa.me/+8801305057238)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue?logo=telegram)](https://t.me/farhan_muh_tasim)

## Donations
[![Buy Me Coffee](https://img.shields.io/badge/Buy_Me_Coffee-FFDD00?logo=buy-me-a-coffee)](https://buymeacoffee.com/FARHAN-MUHTASIM)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?logo=paypal)](https://paypal.me/binodxd)

## Acknowledgements
Special thanks to:
- `DRYGDRYG` - Original developer
- `Wiire` - Pixiewps developer
- `rofl0r` - Initial implementation
- `FARHAN-MUH-TASIM` - Tool maintainer


<p align="center">
  <img src="https://i.postimg.cc/fbzJnQL6/Screenshot-20231026-084714-Termux.png" width="45%">
  <img src="https://i.postimg.cc/MKhWpDTR/Screenshot-20231029-202035-Termux.png" width="45%">
</p>


