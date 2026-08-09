#!/usr/bin/env python3
# SnapchatBoost - main.py (Clean Selenium Version)
import os
import sys
import time
import json
import platform
import webbrowser
import urllib.request
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

# Selenium Imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import keyboard
except Exception:
    keyboard = None

# ----------------------------------------------------------------------
# Default Settings
# ----------------------------------------------------------------------
DEFAULT_SETTINGS = {
    "loop_delay": 0.2,
    "click_delay": 0.29,
    "position_delay": 0.5,
    "shortcut_count": 100,
    "positions": {},
    "auto_open_readme": True,
    "readme_url": "https://github.com/OhnoMain/SnapchatBoost/",
    "snapchat_login": "https://web.snapchat.com/",
    "discord": "https://discord.com/invite/FKXR3TkQnt"
}

BASE_DIR = Path(__file__).parent.resolve()
SETTINGS_PATH = BASE_DIR / "settings.json"
SNAP_IMAGE = BASE_DIR / "snapscore_100k.png"

SNAP_Y = Fore.YELLOW
SNAP_ACC = Fore.LIGHTYELLOW_EX
SNAP_W = Fore.WHITE

VERSION = "1.2.1"
VERSION_URL = "https://raw.githubusercontent.com/OhnoMain/SnapchatBoost/main/version.txt"
RELEASES_URL = "https://github.com/OhnoMain/SnapchatBoost/"

def check_version():
    """Check version but don't force exit if mismatched."""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as resp:
            remote = resp.read().decode('utf-8').strip()
            if remote != VERSION:
                pretty_print("NEW VERSION AVAILABLE ON GITHUB!", SNAP_W)
                pretty_print(f"Local : {VERSION}", SNAP_W)
                pretty_print(f"Latest: {remote}", SNAP_W)
                pretty_print("You can download the new version here:", SNAP_W)
                pretty_print(RELEASES_URL, SNAP_ACC)
                time.sleep(2)
                return True
            else:
                pretty_print(f"Version up-to-date: {VERSION}", SNAP_ACC)
                return True
    except Exception as e:
        pretty_print(f"Could not check version (network error): {e}", SNAP_W)
        pretty_print("Continuing offline.", SNAP_W)
        return True

def ensure_snap_image():
    if not SNAP_IMAGE.exists():
        pretty_print(f"snapscore image missing: {SNAP_IMAGE}", SNAP_W)

# ----------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def title(msg):
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(msg)
        except:
            pass
    else:
        sys.stdout.write(f"\33]0;{msg}\a")
        sys.stdout.flush()

def pretty_print(text, color=SNAP_Y, delay=0.005):
    for ch in str(text):
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def load_settings():
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r") as fh:
                loaded = json.load(fh)
            settings = DEFAULT_SETTINGS.copy()
            settings.update(loaded)
            return settings
        except:
            pretty_print("Corrupted settings.json – using defaults.", SNAP_W)
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(data):
    try:
        with open(SETTINGS_PATH, "w") as fh:
            json.dump(data, fh, indent=2)
        return True
    except:
        return False

# ----------------------------------------------------------------------
# ASCII Banner
# ----------------------------------------------------------------------
BANNER_LINES = [
    "███████╗███╗   ██╗ █████╗ ██████╗  ██████╗ ██████╗  ██████╗ ███████╗████████╗",
    "██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝",
    "███████╗██╔██╗ ██║███████║██████╔╝██████╔╝██║   ██║██║   ██║███████╗   ██║   ",
    "╚════██║██║╚██╗██║██╔══██║██╔═══╝ ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   ",
    "███████║██║ ╚████║██║  ██║██║     ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ",
    "╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   "
]

def print_banner():
    print(SNAP_Y + "       Ghost")
    for i, line in enumerate(BANNER_LINES):
        cols = [SNAP_Y, SNAP_ACC, SNAP_W]
        print(cols[i % len(cols)] + line + Style.RESET_ALL)
    print(SNAP_ACC + "                                                       by Ohno" + Style.RESET_ALL)
    print("")

def boot_sequence():
    clear()
    print(SNAP_Y + "\n       Ghost\n")
    steps = ["Checking version...", "Calibrating camera...", "Verifying UI...", "Loading engine...", "Finalizing..."]
    for s in steps:
        pretty_print(s, SNAP_ACC, delay=0.004)
        for _ in range(5):
            sys.stdout.write(SNAP_Y + "." + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.06)
        print("")
    pretty_print("Boot complete Checkmark", SNAP_Y, delay=0.002)
    time.sleep(0.4)
    clear()

# ----------------------------------------------------------------------
# Selenium Automation Controls
# ----------------------------------------------------------------------
driver = None

def check_browser_active(d):
    if d is None:
        return False
    try:
        d.title
        return True
    except Exception:
        return False

def get_driver():
    global driver
    if not SELENIUM_AVAILABLE:
        pretty_print("Selenium ist nicht installiert! Führe install.bat aus.", SNAP_W)
        input("Drücke ENTER zum Beenden...")
        sys.exit(1)
        
    if driver is None or not check_browser_active(driver):
        pretty_print("Starte gesteuertes Chrome-Fenster...", SNAP_ACC)
        try:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            driver.get("https://web.snapchat.com/")
            pretty_print("Browser geöffnet. Bitte logge dich ein.", SNAP_Y)
            pretty_print("Sobald du eingeloggt bist und das Kamera-Symbol siehst,", SNAP_Y)
            input(SNAP_ACC + "drücke ENTER in dieser Konsole, um das Menü aufzurufen...")
        except Exception as e:
            pretty_print(f"Fehler beim Starten von Chrome: {e}", SNAP_W)
            input("Drücke ENTER zum Beenden...")
            sys.exit(1)
    return driver

def virtual_click(d, x, y):
    """Clicks at (x, y) relative to page viewport without moving physical mouse."""
    try:
        body = WebDriverWait(d, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        width = body.size['width']
        height = body.size['height']
        x_offset = int(x - width / 2)
        y_offset = int(y - height / 2)
        ActionChains(d).move_to_element_with_offset(body, x_offset, y_offset).click().perform()
    except Exception as e:
        pretty_print(f"Virtueller Klick fehlgeschlagen: {e}", SNAP_W)

def get_click(d, step_name):
    pretty_print(f"-> Bitte klicke im Browser-Fenster auf: {step_name}", SNAP_Y)
    
    # Inject click tracker script
    d.execute_script("""
    if (!window.hasClickTracker) {
        window.hasClickTracker = true;
        document.addEventListener('click', function(e) {
            window.lastClick = {x: e.clientX, y: e.clientY};
        }, true);
    }
    window.lastClick = null;
    """)
    
    while True:
        try:
            click = d.execute_script("return window.lastClick;")
            if click:
                d.execute_script("window.lastClick = null;")
                return click['x'], click['y']
        except Exception as e:
            pretty_print(f"Fehler beim Lesen der Klick-Koordinaten: {e}", SNAP_W)
            break
        time.sleep(0.1)
    return 0, 0

# ----------------------------------------------------------------------
# Bot Actions
# ----------------------------------------------------------------------
def send_snap(d, settings, started_time, shortcut_user_count, first_try):
    pos = settings.get('positions', {})
    required = ['switch_to_camera', 'send_to', 'shortcut', 'select_all']
    if not all(k in pos for k in required):
        pretty_print("Positionen fehlen. Bitte zuerst kalibrieren (Option 2)!", SNAP_W)
        return False, first_try

    try:
        # Camera Capture Click
        virtual_click(d, pos['switch_to_camera'][0], pos['switch_to_camera'][1])
        if first_try:
            time.sleep(settings.get('click_delay', 0.29))
            virtual_click(d, pos['switch_to_camera'][0], pos['switch_to_camera'][1])
            first_try = False
        time.sleep(settings.get('click_delay', 0.29))

        # Send To Click
        virtual_click(d, pos['send_to'][0], pos['send_to'][1])
        time.sleep(settings.get('click_delay', 0.29))

        # Shortcut Click
        virtual_click(d, pos['shortcut'][0], pos['shortcut'][1])
        time.sleep(settings.get('click_delay', 0.29))

        # Select All Click
        virtual_click(d, pos['select_all'][0], pos['select_all'][1])
        time.sleep(settings.get('click_delay', 0.29))

        # Final Send Click (utilizes the send_to coordinate at bottom right)
        virtual_click(d, pos['send_to'][0], pos['send_to'][1])
        return True, first_try
    except Exception as e:
        pretty_print(f"Fehler bei Klick-Reihenfolge: {e}", SNAP_W)
        return False, first_try

# ----------------------------------------------------------------------
# Calibration Menu
# ----------------------------------------------------------------------
def configure_positions(d, settings):
    pretty_print("====== KALIBRIERUNG: SNAP BOOST ======", SNAP_ACC)
    pretty_print("Klicke nacheinander auf die gefragten Schaltflächen im Browser.", SNAP_W)
    try:
        x, y = get_click(d, "Kamera (Kamera-Button)")
        settings['positions']['switch_to_camera'] = [x, y]
        pretty_print(f"CAMERA positioniert bei: {[x, y]}", SNAP_ACC)
        time.sleep(0.5)

        x, y = get_click(d, "Senden (Send-To Button)")
        settings['positions']['send_to'] = [x, y]
        pretty_print(f"SEND TO positioniert bei: {[x, y]}", SNAP_ACC)
        time.sleep(0.5)

        x, y = get_click(d, "Shortcut auswählen (dein Verknüpfungsemoji)")
        settings['positions']['shortcut'] = [x, y]
        pretty_print(f"SHORTCUT positioniert bei: {[x, y]}", SNAP_ACC)
        time.sleep(0.5)

        x, y = get_click(d, "Alle auswählen (Select-All Checkbox)")
        settings['positions']['select_all'] = [x, y]
        pretty_print(f"SELECT ALL positioniert bei: {[x, y]}", SNAP_ACC)
        
        save_settings(settings)
        pretty_print("Kalibrierung erfolgreich gespeichert!", SNAP_ACC)
    except Exception as e:
        pretty_print(f"Fehler bei Kalibrierung: {e}", SNAP_W)
    input('ENTER')

# ----------------------------------------------------------------------
# Other Menu Helpers
# ----------------------------------------------------------------------
def settings_menu(settings):
    clear()
    print_banner()
    pretty_print("Settings (leerlassen behält aktuellen Wert)", SNAP_W)
    try:
        ld = input(f"Loop delay [{settings.get('loop_delay')}]: ").strip()
        if ld:
            settings['loop_delay'] = float(ld)

        cd = input(f"Click delay [{settings.get('click_delay')}]: ").strip()
        if cd:
            settings['click_delay'] = float(cd)

        sc = input(f"Shortcut size [{settings.get('shortcut_count')}]: ").strip()
        if sc:
            settings['shortcut_count'] = int(sc)
    except:
        pretty_print("Ungültige Eingabe – Werte beibehalten.", SNAP_W)

    save_settings(settings)
    pretty_print("Gespeichert.", SNAP_ACC)
    input("ENTER")

def open_help_pages(settings):
    try:
        webbrowser.open(settings.get('readme_url'))
        webbrowser.open(settings.get('snapchat_login'))
        webbrowser.open(settings.get('discord'))
    except:
        pass

def help_menu(settings):
    clear()
    print_banner()
    pretty_print('Hilfe & Anleitungen', SNAP_Y)
    pretty_print('Öffne README und Snapchat Web im Browser...', SNAP_W)
    open_help_pages(settings)
    input('ENTER')

def exit_screen():
    clear()
    box = (
        "╔════════════════════════════════════════════════╗\n"
        "║           Vielen Dank für die Nutzung!         ║\n"
        "║    https://github.com/OhnoMain/SnapchatBoost   ║\n"
        "║      https://discord.com/invite/FKXR3TkQnt     ║\n"
        "╚════════════════════════════════════════════════╝\n"
    )
    print(SNAP_Y + box + Style.RESET_ALL)
    global driver
    if driver is not None:
        try:
            driver.quit()
        except:
            pass
    time.sleep(3)

# ----------------------------------------------------------------------
# Main Program Loop
# ----------------------------------------------------------------------
def main():
    title('SnapchatBoost [Mauszeigerfrei]')
    settings = load_settings()
    check_version()
    boot_sequence()
    ensure_snap_image()

    global driver
    while True:
        # Auto-detect driver closure
        if driver is not None and not check_browser_active(driver):
            pretty_print("Browser-Fenster wurde geschlossen – setze Verbindung zurück.", SNAP_W)
            try:
                driver.quit()
            except:
                pass
            driver = None

        clear()
        print_banner()
        pretty_print('1) Start Snap Boost', SNAP_Y)
        pretty_print('2) Configure Snap Positions (Calibration)', SNAP_Y)
        pretty_print('3) Settings', SNAP_W)
        pretty_print('4) Help', SNAP_W)
        pretty_print('5) Discord', SNAP_Y)
        pretty_print('6) Exit', SNAP_ACC)

        c = input('> ').strip()
        if c == '1':
            d = get_driver()
            pretty_print('Starte Snap Boost. Drücke ESC zum Stoppen.', SNAP_Y)
            started = time.time()
            first_try = True
            sent_count = 0
            while True:
                if keyboard and keyboard.is_pressed('esc'):
                    pretty_print('Stoppen...', SNAP_ACC)
                    break
                success, first_try = send_snap(d, settings, started, settings.get('shortcut_count', 1), first_try)
                if success:
                    sent_count += 1
                    pretty_print(f"Sent batch #{sent_count} ({sent_count * settings.get('shortcut_count', 1)} snaps). Elapsed {int(time.time() - started)}s", SNAP_ACC)
                time.sleep(settings.get('loop_delay', 0.2))
            save_settings(settings)
            input('ENTER')

        elif c == '2':
            d = get_driver()
            configure_positions(d, settings)

        elif c == '3':
            settings_menu(settings)

        elif c == '4':
            help_menu(settings)

        elif c == '5':
            try:
                webbrowser.open(settings.get('discord'))
            except:
                pass

        elif c == '6':
            exit_screen()
            break

if __name__ == '__main__':
    main()
