import os
import subprocess
import sys
from datetime import datetime
import time

# Check and install required modules
def install_required_modules():
    required_modules = ['pystyle']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

install_required_modules()

from pystyle import Colors, Colorate

# Clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print with colors
def print_colored(text, color=Colors.white):
    print(Colorate.Color(color, text))

def check_windows_version():
    if os.name != 'nt':
        print_colored("This script can only run on Windows 10 or 11.", Colors.red)
        sys.exit(1)
    
    version = sys.getwindowsversion()
    if version.major < 10:
        print_colored("This script requires Windows 10 or higher.", Colors.red)
        sys.exit(1)
    
    print_colored("Windows version check: OK", Colors.green)

def check_afuwin_installed():
    afuwin_path = r"C:\AFUWIN\AFUWINx64.EXE"  # Path to AFUWIN
    if not os.path.isfile(afuwin_path):
        print_colored("AFUWIN not found. Please download it from the official website and install it.", Colors.red)
        sys.exit(1)
    else:
        print_colored("AFUWIN is already installed.", Colors.green)
    return afuwin_path

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
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
        print_colored(f"An error occurred: {e}", Colors.red)

    rc = process.poll()
    return rc, output_lines

def dump_bios(afuwin_path, backup_file):
    # Check if the file already exists and delete it
    if os.path.isfile(backup_file):
        os.remove(backup_file)

    dump_command = f'"{afuwin_path}" {backup_file} /O'
    print_colored(f"Executing command: {dump_command}", Colors.yellow)
    result, output = run_command(dump_command)

    if result != 0:
        print_colored("Failed to backup BIOS settings.", Colors.red)
        print("\n".join(output))
        return False

    if os.path.isfile(backup_file) and os.path.getsize(backup_file) > 0:
        print_colored(f"BIOS settings successfully backed up to {backup_file}", Colors.green)
        return True
    else:
        print_colored("Error: The backup file is invalid or empty.", Colors.red)
        return False

def restore_bios(afuwin_path, backup_file):
    restore_command = f'"{afuwin_path}" {backup_file} /I'
    print_colored(f"Executing command: {restore_command}", Colors.yellow)
    result, output = run_command(restore_command)

    if result == 0:
        print_colored(f"BIOS settings successfully restored from {backup_file}", Colors.green)
        return True
    else:
        print_colored("Failed to restore BIOS settings.", Colors.red)
        print("\n".join(output))
        return False

def update_console_title(backup_dir):
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
    backup_count = len(backups)
    title = "BIOS Backup and Restore Utility"
    if backup_count > 0:
        title += f" - Backups created {backup_count}"
    os.system(f"title {title}")

def main():
    try:
        clear_console()
        check_windows_version()
        afuwin_path = check_afuwin_installed()

        # Path to the backup directory in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = os.path.join(script_dir, "backups")

        # Update the console title
        update_console_title(backup_dir)

        print_colored("Select an option:", Colors.cyan)
        print_colored("1. Create a backup of the BIOS settings", Colors.cyan)
        print_colored("2. Restore the BIOS settings from a backup", Colors.cyan)
        
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            timestamp = datetime.now().strftime("%d.%m.%Y_%H%M")
            backup_file = os.path.join(backup_dir, f"bios_backup_{timestamp}.rom")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            if dump_bios(afuwin_path, backup_file):
                print_colored("The backup of the BIOS settings was successful.", Colors.green)
            else:
                print_colored("The backup of the BIOS settings failed.", Colors.red)
        elif choice == '2':
            print_colored("Available backups:", Colors.cyan)
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
            for idx, backup in enumerate(backups):
                print_colored(f"{idx + 1}. {backup}", Colors.yellow)
            
            backup_choice = int(input("Enter the number of the backup to restore: ")) - 1
            backup_file = os.path.join(backup_dir, backups[backup_choice])
            
            if restore_bios(afuwin_path, backup_file):
                print_colored("Would you like to restart the PC in one minute?", Colors.cyan)
                print_colored("1. Yes", Colors.cyan)
                print_colored("2. No", Colors.cyan)
                restart_choice = input("Enter your choice (1 or 2): ")
                if restart_choice == '1':
                    print_colored("The PC will restart in one minute.", Colors.green)
                    os.system("shutdown /r /t 60")
                elif restart_choice == '2':
                    print_colored("The PC will not restart.", Colors.green)
                else:
                    print_colored("Invalid choice, the PC will not restart.", Colors.red)
            else:
                print_colored("Failed to restore BIOS settings.", Colors.red)
        else:
            print_colored("Invalid choice, please restart the script and select 1 or 2.", Colors.red)

    except Exception as e:
        print_colored(f"An error occurred: {e}", Colors.red)

    input("Press Enter to exit the script...")

if __name__ == "__main__":
    main()
