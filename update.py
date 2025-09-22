#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Git Updater Tool
Author: Gtajisan (Farhan)
GitHub: https://github.com/Gtajisan
License: MIT License

Disclaimer:
    This tool is intended for educational purposes and authorized penetration testing only.
    Do NOT use on networks without permission.
    The author is not responsible for any misuse.
"""

import os
import sys
import subprocess

# ==========================
# Color helpers
# ==========================
class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    CYAN = "\033[1;36m"
    RESET = "\033[0m"

def info(msg):
    print(f"{Colors.CYAN}[+]{Colors.RESET} {msg}")

def warn(msg):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")

def error(msg):
    print(f"{Colors.RED}[-]{Colors.RESET} {msg}")

# ==========================
# Utility functions
# ==========================
def is_termux():
    """Detect if running inside Termux"""
    return os.getenv("PREFIX", "").startswith("/data/data/com.termux/files/usr")

def check_git_repo():
    if not os.path.isdir('.git'):
        error("This folder does not appear to be a Git repository (missing .git directory).")
        sys.exit(1)

def git_pull():
    info("Pulling latest changes from Git repository...")
    try:
        result = subprocess.run(
            ["git", "pull"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        info("Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        error(f"Git pull failed:\n{e.stderr}")
        sys.exit(1)

# ==========================
# Main
# ==========================
def main():
    info("Starting Termux Git Updater Tool...")

    if not is_termux():
        warn("It seems you are not running inside Termux. Proceeding anyway.")

    check_git_repo()
    git_pull()

    info("All done! Your repository is up to date.")

if __name__ == "__main__":
    main()
