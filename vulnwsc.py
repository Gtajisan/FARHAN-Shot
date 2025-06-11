import json
from colorama import init, Fore, Style

init(autoreset=True)

def load_and_clean(filename):
    seen = set()
    cleaned = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            device = line.strip()
            if not device or device in seen:
                continue
            # Skip entries with weird placeholders or obvious invalid entries
            if '<#' in device or 'N/A' in device:
                continue
            seen.add(device)
            cleaned.append(device)
    return cleaned

def build_vuln_db(devices):
    # Here you can add real attackability info or keep all attackable by default
    vulndb = []
    for dev in devices:
        # Simple heuristic: if device string contains a version number or model known vulnerable
        attackable = True
        # Example: skip generic or ambiguous entries
        if any(x in dev.lower() for x in ['wireless router', 'wireless access point']):
            attackable = False
        vulndb.append({
            'model': dev,
            'attackable': attackable
        })
    return vulndb

def is_attackable(model, vulndb):
    for dev in vulndb:
        # Using simple substring match for demo, you can make it more precise
        if dev['model'].lower() in model.lower():
            return dev['attackable']
    return False

def attack_device(device):
    # Your attack code here. For demo, just print attacking message.
    print(Fore.GREEN + f"Attacking device: {device}")

def main():
    print(Fore.CYAN + "Loading and cleaning vulnwsc.txt...")
    devices = load_and_clean('vulnwsc.txt')
    print(f"Total unique devices loaded: {len(devices)}")

    print(Fore.CYAN + "Building vulnerability database...")
    vulndb = build_vuln_db(devices)

    # Example list of devices you want to test / attack (simulate scan)
    targets = [
        "Archer C6 3.20",
        "Wireless Router 123456",
        "TL-WR841N 14.0",
        "Unknown Device Model"
    ]

    print("\n" + Fore.YELLOW + "Starting attack simulation...\n")
    for t in targets:
        if is_attackable(t, vulndb):
            attack_device(t)
        else:
            print(Fore.RED + f"Skipping device: {t} (not attackable)")

if __name__ == "__main__":
    main()
