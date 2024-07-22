import os
import subprocess
import sys
from datetime import datetime
import msvcrt
import shutil

# Check and install required modules
def install_required_modules():
    required_modules = ['pystyle', 'rich', 'chipsec']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])

install_required_modules()

from pystyle import Colors, Colorate, Center, Write, Col
from rich.console import Console

# Clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print with colors
def print_colored(text, color=Colors.white):
    print(Colorate.Color(color, text))

def print_gradient(text):
    gradient = Colorate.Horizontal(Colors.blue_to_green, text)
    print(gradient)

# Check if the script is running on Windows 10 oder 11
def check_windows_version():
    if os.name != 'nt':
        print_colored("This script can only run on Windows 10 or 11.", Colors.red)
        sys.exit(1)
    
    version = sys.getwindowsversion()
    if version.major < 10:
        print_colored("This script requires Windows 10 or higher.", Colors.red)
        sys.exit(1)
    
    print_colored("Windows version check: OK", Colors.green)

# Check if AFUWIN is installed
def check_tools_installed():
    afuwin_path = r"C:\AFUWIN\AFUWINx64.EXE"  # Path to AFUWIN

    if not os.path.isfile(afuwin_path):
        print_colored("AFUWIN not found. Please download it from the official website and install it.", Colors.red)
        sys.exit(1)
    else:
        print_colored("AFUWIN is already installed.", Colors.green)
    
    return afuwin_path

# Run a command and handle its output
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

# Dump the BIOS to a file
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

# Restore the BIOS from a backup file and restart the PC after 60 seconds
def restore_bios(afuwin_path, backup_file):
    restore_command = f'"{afuwin_path}" {backup_file} /P /B /K /N'
    print_colored(f"Executing command: {restore_command}", Colors.yellow)
    result, output = run_command(restore_command)

    if result == 0:
        print_colored(f"BIOS settings successfully restored from {backup_file}. The PC will restart in 60 seconds.", Colors.green)
        os.system("shutdown /r /t 60")
        return True
    else:
        print_colored("Failed to restore BIOS settings.", Colors.red)
        print("\n".join(output))
        return False

# Update the console title with the number of backups created
def update_console_title(backup_dir):
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
    backup_count = len(backups)
    title = "BIOS Backup and Restore Utility"
    if backup_count > 0:
        title += f" - Backups created {backup_count}"
    os.system(f"title {title}")

# Wait for a keypress and return the pressed key
def wait_for_keypress():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            if key in ['1', '2', '3', '4']:
                return key

# Analyze the BIOS ROM file using chipsec and save the output to a text file
def analyze_bios_with_chipsec(rom_file, output_file):
    try:
        chipsec_cmd = [sys.executable, "-m", "chipsec_util", "decode", rom_file, "-o", output_file]
        result = subprocess.run(chipsec_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_colored(f"BIOS analysis completed successfully. Output saved to {output_file}", Colors.green)
        else:
            print_colored(f"Failed to analyze BIOS. Error: {result.stderr}", Colors.red)
    except Exception as e:
        print_colored(f"An error occurred while analyzing the BIOS: {e}", Colors.red)

# Read and print the BIOS version from an OCB file and rename it
def read_ocb_bios_version(ocb_file):
    try:
        with open(ocb_file, 'rb') as f:
            data = f.read()

            # Extract the BIOS version assuming it starts with "$MOS$" and ends at the first null byte
            start_index = data.find(b"$MOS$")
            if start_index != -1:
                end_index = data.find(b'\x00', start_index)
                if end_index != -1:
                    bios_version = data[start_index + 5:end_index].decode('utf-8', errors='ignore')
                    print_colored(f"BIOS Version: {bios_version}", Colors.green)
                    
                    timestamp = datetime.now().strftime("%d.%m.%Y_%H%M")
                    new_ocb_file = f"MSI_BIOS_{bios_version}_{timestamp}.ocb"
                    new_ocb_file_path = os.path.join(os.path.dirname(ocb_file), new_ocb_file)
                    
                    # Ensure the file is not open before renaming
                    f.close()
                    os.rename(ocb_file, new_ocb_file_path)
                    print_colored(f"OCB file renamed to {new_ocb_file}", Colors.green)
                else:
                    print_colored("BIOS Version not found.", Colors.red)
            else:
                print_colored("BIOS Version not found.", Colors.red)
    except Exception as e:
        print_colored(f"An error occurred while reading the OCB file: {e}", Colors.red)

def main():
    try:
        clear_console()
        check_windows_version()
        afuwin_path = check_tools_installed()

        # Path to the backup directory in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = os.path.join(script_dir, "backups")
        analysis_dir = os.path.join(script_dir, "analysis")
        ocb_dir = os.path.join(script_dir, "ocb_files")

        # Ensure the directories exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        if not os.path.exists(analysis_dir):
            os.makedirs(analysis_dir)
        if not os.path.exists(ocb_dir):
            os.makedirs(ocb_dir)

        # Update the console title
        update_console_title(backup_dir)

        print_gradient("1. Create a backup of the BIOS settings")
        print_gradient("2. Restore the BIOS settings from a backup")
        print_gradient("3. Analyze BIOS ROM file (WIP)")
        print_gradient("4. Check BIOS Version of OCB File (MSI)")
        
        print("Enter your choice (1, 2, 3, or 4): ", end='', flush=True)
        choice = wait_for_keypress()

        clear_console()

        if choice == '1':
            timestamp = datetime.now().strftime("%d.%m.%Y_%H%M")
            backup_file = os.path.join(backup_dir, f"bios_backup_{timestamp}.rom")
            
            if dump_bios(afuwin_path, backup_file):
                print_colored("The backup of the BIOS settings was successful.", Colors.green)
            else:
                print_colored("The backup of the BIOS settings failed.", Colors.red)
        elif choice == '2':
            print_colored("Available backups:", Colors.cyan)
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
            for idx, backup in enumerate(backups):
                # Format the backup filename for better readability
                file_date = backup.split('_')[2]
                file_time = backup.split('_')[3].split('.')[0]
                formatted_name = f"Backup - {file_date} created at {file_time[:2]}:{file_time[2:]}"
                print_colored(f"{idx + 1}. {formatted_name}", Colors.yellow)
            
            backup_choice = int(input("Enter the number of the backup to restore: ")) - 1
            backup_file = os.path.join(backup_dir, backups[backup_choice])
            
            if restore_bios(afuwin_path, backup_file):
                print_colored("BIOS settings successfully restored.", Colors.green)
            else:
                print_colored("Failed to restore BIOS settings.", Colors.red)
        elif choice == '3':
            print_colored("Available ROM files:", Colors.cyan)
            rom_files = [f for f in os.listdir(backup_dir) if f.endswith('.rom')]
            for idx, rom in enumerate(rom_files):
                print_colored(f"{idx + 1}. {rom}", Colors.yellow)
            
            rom_choice = int(input("Enter the number of the ROM file to analyze: ")) - 1
            rom_file = os.path.join(backup_dir, rom_files[rom_choice])
            
            timestamp = datetime.now().strftime("%d.%m.%Y_%H%M")
            output_file = os.path.join(analysis_dir, f"bios_analysis_{timestamp}.txt")
            
            analyze_bios_with_chipsec(rom_file, output_file)
        elif choice == '4':
            print_colored("Available OCB files:", Colors.cyan)
            ocb_files = [f for f in os.listdir(ocb_dir) if f.endswith('.ocb')]
            for idx, ocb in enumerate(ocb_files):
                print_colored(f"{idx + 1}. {ocb}", Colors.yellow)
            
            ocb_choice = int(input("Enter the number of the OCB file to check: ")) - 1
            ocb_file = os.path.join(ocb_dir, ocb_files[ocb_choice])
            
            read_ocb_bios_version(ocb_file)
        else:
            print_colored("Invalid choice, please restart the script and select 1, 2, 3, or 4.", Colors.red)

        print("\nPress Enter to return to the main menu or ESC to exit.")
        while True:
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                main()
            elif key == b'\x1b':  # ESC key
                sys.exit(0)

    except Exception as e:
        print_colored(f"An error occurred: {e}", Colors.red)

    input("Press Enter to exit the script...")

if __name__ == "__main__":
    main()
