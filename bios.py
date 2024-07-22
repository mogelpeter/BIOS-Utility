import os
import subprocess
import sys
from datetime import datetime

# Überprüfen und Installieren benötigter Module
def install_required_modules():
    required_modules = ['pystyle']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

install_required_modules()

from pystyle import Colors, Colorate

# Konsole aufräumen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Farben zum Drucken verwenden
def print_colored(text, color=Colors.white):
    print(Colorate.Color(color, text))

def check_windows_version():
    if os.name != 'nt':
        print_colored("Dieses Skript kann nur unter Windows 10 oder 11 ausgeführt werden.", Colors.red)
        sys.exit(1)
    
    version = sys.getwindowsversion()
    if version.major < 10:
        print_colored("Dieses Skript erfordert Windows 10 oder höher.", Colors.red)
        sys.exit(1)
    
    print_colored("Windows-Version überprüft: OK", Colors.green)

def check_afuwin_installed():
    afuwin_path = r"C:\AFUWIN\AFUWINx64.EXE"  # Zielpfad für AFUWIN
    if not os.path.isfile(afuwin_path):
        print_colored("AFUWIN nicht gefunden. Bitte laden Sie es von der offiziellen Website herunter und installieren Sie es.", Colors.red)
        sys.exit(1)
    else:
        print_colored("AFUWIN ist bereits installiert.", Colors.green)
    return afuwin_path

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)
    output_lines = []

    try:
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())
                output_lines.append(output.strip())
                if "already exists" in output:
                    process.stdin.write("y\n")
                    process.stdin.flush()
    except Exception as e:
        print_colored(f"Ein Fehler ist aufgetreten: {e}", Colors.red)

    rc = process.poll()
    return rc, output_lines

def dump_bios(afuwin_path, backup_file):
    # Überprüfen, ob die Datei bereits existiert und löschen
    if os.path.isfile(backup_file):
        os.remove(backup_file)

    dump_command = f'"{afuwin_path}" {backup_file} /O'
    print_colored(f"Führe Befehl aus: {dump_command}", Colors.yellow)
    result, output = run_command(dump_command)

    if result != 0:
        print_colored("Fehler beim Sichern der BIOS-Einstellungen.", Colors.red)
        print("\n".join(output))
        return False

    if os.path.isfile(backup_file) and os.path.getsize(backup_file) > 0:
        print_colored(f"BIOS-Einstellungen erfolgreich gesichert nach {backup_file}", Colors.green)
        return True
    else:
        print_colored("Fehler: Die Backup-Datei ist ungültig oder leer.", Colors.red)
        return False

def restore_bios(afuwin_path, backup_file):
    restore_command = f'"{afuwin_path}" {backup_file} /I'
    print_colored(f"Führe Befehl aus: {restore_command}", Colors.yellow)
    result, output = run_command(restore_command)

    if result == 0:
        print_colored(f"BIOS-Einstellungen erfolgreich wiederhergestellt von {backup_file}", Colors.green)
    else:
        print_colored("Fehler beim Wiederherstellen der BIOS-Einstellungen.", Colors.red)
        print("\n".join(output))

def main():
    try:
        clear_console()
        check_windows_version()
        afuwin_path = check_afuwin_installed()

        # Pfad zum Backup-Verzeichnis im selben Verzeichnis wie das Skript
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = os.path.join(script_dir, "backups")

        print_colored("Wählen Sie eine Option:", Colors.cyan)
        print_colored("1. Backup der BIOS-Einstellungen erstellen", Colors.cyan)
        print_colored("2. Backup der BIOS-Einstellungen wiederherstellen", Colors.cyan)
        
        choice = input("Geben Sie Ihre Wahl ein (1 oder 2): ")

        if choice == '1':
            timestamp = datetime.now().strftime("%d.%m.%Y_%H%M")
            backup_file = os.path.join(backup_dir, f"bios_backup_{timestamp}.rom")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            if dump_bios(afuwin_path, backup_file):
                print_colored("Das Backup der BIOS-Einstellungen war erfolgreich.", Colors.green)
            else:
                print_colored("Das Backup der BIOS-Einstellungen ist fehlgeschlagen.", Colors.red)
        elif choice == '2':
            print_colored("Verfügbare Backups:", Colors.cyan)
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
            for idx, backup in enumerate(backups):
                print_colored(f"{idx + 1}. {backup}", Colors.yellow)
            
            backup_choice = int(input("Geben Sie die Nummer des wiederherzustellenden Backups ein: ")) - 1
            backup_file = os.path.join(backup_dir, backups[backup_choice])
            
            restore_bios(afuwin_path, backup_file)
        else:
            print_colored("Ungültige Wahl, bitte starten Sie das Skript erneut und wählen Sie 1 oder 2.", Colors.red)

    except Exception as e:
        print_colored(f"Ein Fehler ist aufgetreten: {e}", Colors.red)

    input("Drücken Sie Enter, um das Skript zu beenden...")

    finally:
        print_colored("Beende alle gestarteten Prozesse, um sicherzustellen, dass keine Ressourcen hängen bleiben.", Colors.cyan)
        os.system(f"taskkill /f /im {os.path.basename(afuwin_path)}")

if __name__ == "__main__":
    main()
