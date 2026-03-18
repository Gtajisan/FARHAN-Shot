<div align="center">

<img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Android-3DDC84?style=for-the-badge&logo=android&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/License-Educational%20Use%20Only-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Version-0.0.2-blue?style=for-the-badge"/>

# 🔐 FARHAN-Shot

**Fast, automated WiFi WPS security auditing tool with advanced reconnaissance and attack simulation capabilities.**

*Designed for authorized penetration testing and WiFi security research.*

</div>

---

> [!WARNING]
> **FARHAN-Shot is optimized for [Termux (F-Droid)](https://f-droid.org/en/packages/com.termux/) on Android.**
> Kali Linux / Debian support is available but considered legacy. For best compatibility and performance, use Termux.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Attack Modes](#-attack-modes)
- [Command Reference](#-command-reference)
- [Session Management](#-session-management)
- [Reporting](#-reporting)
- [File Structure](#-file-structure)
- [Network Status Indicators](#-network-status-indicators)
- [Output Reference](#-output-reference)
- [Troubleshooting](#-troubleshooting)
- [Legal Notice](#️-legal-notice)

---

## 🧭 Overview

FARHAN-Shot is a feature-rich WPS (Wi-Fi Protected Setup) security auditing tool built for mobile penetration testers and security researchers. It wraps industry-standard tools — `aircrack-ng`, `wpa_supplicant`, and `pixiewps` — into a unified, scriptable CLI interface with session persistence, MAC spoofing, rate-limit bypass, reporting, and more.

**Key capabilities:**

- Pixie Dust, Brute Force, and Dictionary attack modes
- Multi-threaded online bruteforce engine
- Session save/resume across interrupted tests
- Automated vulnerability list population
- HTML, JSON, and CSV report generation
- Advanced network reconnaissance & signal analysis
- MAC address spoofing and rate-limit detection/bypass

---

## 🧰 Prerequisites

Ensure the following are installed and accessible before running FARHAN-Shot:

| Dependency       | Purpose                              |
|------------------|--------------------------------------|
| `Python 3.8+`    | Core runtime                         |
| `aircrack-ng`    | Wireless interface management        |
| `wpa_supplicant` | WPS protocol communication           |
| `pixiewps`       | Pixie Dust offline attack engine     |
| `Termux`         | Android terminal environment (recommended) |

---

## 📦 Installation

### Termux (Recommended)

Run the following one-liner to install FARHAN-Shot with all dependencies and patches:

```bash
curl -sSf https://raw.githubusercontent.com/Gtajisan/FARHAN-Shot_Termux_installer/master/installer.sh | bash && \
curl -sL https://raw.githubusercontent.com/Gtajisan/Termux-fix/main/fix_sudo.sh | bash && \
sudo rm -rf FARHAN-Shot && \
git clone --depth 1 https://github.com/Gtajisan/FARHAN-Shot.git && \
chmod +x FARHAN-Shot/main.py
```

> [!NOTE]
> The installer handles dependency resolution, `sudo` patching, and a fresh clone automatically.

---

### Uninstall

```bash
# Remove tool directory
rm -rf /path/to/FARHAN-Shot

# Remove user data and session files (optional)
rm -rf ~/.FARHAN-Shot/
```

---

## 🚀 Usage

### Basic Syntax
**<interface> [options]**

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 
```

### Quick Start Examples

```bash
# Scan for nearby WPS-enabled networks
sudo python3 FARHAN-Shot/main.py -i wlan0

# Pixie Dust attack on a specific target
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -K

# Brute force attack
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -B

# Dictionary attack with custom wordlist
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF --dictionary-attack --wordlist /path/to/wordlist.txt

# Full penetration test with reporting
sudo python3 FARHAN-Shot/main.py -i wlan0 -K --advanced-recon --detect-weak-algo --spoof-mac --html-report --auto-vuln-list
```

---

## ⚔️ Attack Modes

### 1. Pixie Dust Attack

Performs an offline cryptographic attack against vulnerable WPS implementations using `pixiewps`.

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -K
```

### 2. Online Brute Force

Multi-threaded sequential PIN guessing against the target AP.

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF --online-bruteforce --bruteforce-threads 8 --pin-limit 5000
```

### 3. Dictionary Attack

Tests a list of known/common PINs from a wordlist file.

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF --dictionary-attack --wordlist /path/to/wordlist.txt
```

### 4. Custom PIN Test

Tests a single, known PIN directly.

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -p 12345678
```

### 5. Push Button Connect (PBC)

Simulates a physical WPS button press for PBC-based enrollment testing.

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 --pbc
```

---

## 📋 Command Reference

### Attack Flags

| Flag | Long Form | Description |
|------|-----------|-------------|
| `-K` | `--pixie-dust` | Pixie Dust offline attack |
| `-B` | `--bruteforce` | Online PIN brute force |
| `-F` | `--pixie-force` | Pixiewps force mode |
| `-p PIN` | `--pin PIN` | Test a specific PIN |
| | `--pbc` | Push Button Connect |
| | `--dictionary-attack` | Dictionary-based attack |
| | `--wordlist FILE` | Path to wordlist file |

### Network & Interface

| Flag | Description |
|------|-------------|
| `-i IFACE` | Wireless interface (required) |
| `-b BSSID` | Target AP MAC address |
| `--channel-hop` | Enable dynamic channel hopping |
| `--spoof-mac` | Randomize/spoof MAC address |

### Detection & Evasion

| Flag | Description |
|------|-------------|
| `--detect-rate-limit` | Detect AP-side rate limiting |
| `--bypass-rate-limit` | Attempt to bypass rate limiting |
| `--detect-weak-algo` | Identify weak WPS implementations |
| `--advanced-recon` | Deep network fingerprinting |
| `--signal-analysis` | Include signal strength analysis |

### Output & Reporting

| Flag | Description |
|------|-------------|
| `-w` | Save discovered credentials |
| `--auto-vuln-list` | Append target to `vulnwsc.txt` |
| `--html-report` | Generate an HTML report |
| `--detailed-report` | Include verbose report data |
| `--report-dir DIR` | Custom directory for reports |
| `--json-output FILE` | Save results as JSON |
| `--csv-output FILE` | Save results as CSV |

### Performance Tuning

| Flag | Description |
|------|-------------|
| `-t SEC` | Receive timeout in seconds |
| `-d SEC` | Delay between attempts |
| `-l SEC` | Wait time after AP lock |
| `--bruteforce-threads N` | Thread count for brute force |

---

## 💾 Session Management

FARHAN-Shot supports full session persistence — pause and resume long-running tests without losing progress.

```bash
# Start and save a named session
sudo python3 FARHAN-Shot/main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -K -s session1

# Resume an existing session
sudo python3 FARHAN-Shot/main.py -i wlan0 --resume-session session1

# List all saved sessions
sudo python3 FARHAN-Shot/main.py --list-sessions
```

---

## 📊 Reporting

Generate structured reports after any test run:

```bash
sudo python3 FARHAN-Shot/main.py -i wlan0 --html-report --detailed-report --report-dir ./reports
```

Supported output formats:

| Format | Flag | Use Case |
|--------|------|----------|
| HTML | `--html-report` | Human-readable browser report |
| JSON | `--json-output FILE` | Programmatic/API consumption |
| CSV | `--csv-output FILE` | Spreadsheet / SIEM ingestion |

---

## 📁 File Structure

```
~/.FARHAN-Shot/
├── sessions/          # Saved session states & cracked credentials
├── wordlists/         # Custom dictionary files
└── reports/           # Generated HTML/JSON/CSV reports

vulnwsc.txt            # Running list of audited vulnerable networks
```

---

## 🌐 Network Status Indicators

During scanning, each discovered network is color-coded based on its WPS state:

| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 Green | **Possibly Vulnerable** | WPS enabled, no active protection detected |
| 🔴 Red | **WPS Locked** | AP is actively blocking WPS attempts |
| 🟡 Yellow | **Already Stored** | Credentials previously cracked and saved in `vulnwsc.txt` |
| ⚪ White | **Unclear / Needs Analysis** | WPS state ambiguous; further probing recommended |

---

## 📟 Output Reference

All output lines are prefixed with a status indicator:

| Prefix | Meaning |
|--------|---------|
| `[+]` | Success — operation completed |
| `[i]` | Informational — status update |
| `[!]` | Warning — non-fatal issue |
| `[-]` | Error — operation failed |
| `[?]` | Prompt — user input required |

---

## 🔧 Troubleshooting

### Interface not found

```bash
# List all wireless interfaces
iwconfig

# Check for monitor-mode capable adapters
sudo airmon-ng
```

### Permission denied

```bash
# Always run with elevated privileges
sudo python3 main.py -i wlan0
```

### Target not responding / timeout

```bash
# Increase receive timeout
sudo python3 main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -K -t 20
```

### Rate limited by AP

```bash
# Enable rate-limit bypass mode
sudo python3 main.py -i wlan0 -b AA:BB:CC:DD:EE:FF -K --bypass-rate-limit
```

---

## ⚖️ Legal Notice

> [!CAUTION]
> **FARHAN-Shot is strictly intended for authorized security assessments.**

- ✅ Only test networks you **own** or have **explicit written permission** to test
- ❌ Unauthorized access to computer networks is a **criminal offense** in most jurisdictions
- 📋 The developer assumes **no liability** for misuse or illegal activity
- 🔒 Use responsibly, ethically, and in compliance with all applicable laws

---

<div align="center">

**FARHAN-Shot v0.0.2** &nbsp;|&nbsp; Modified by [@Mohammad Alamin](https://github.com/Gtajisan)

*Built for security professionals. Use with permission. Use with purpose.*

</div>
