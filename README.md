# BIOS Backup and Restore Utility

A utility to backup and restore BIOS settings using AFUWINx64. This script allows you to create a backup of your BIOS settings and restore them when needed.

## Prerequisites

- Windows 10 or 11
- Python 3.8 or higher
- AFUWINx64 version 5.16.02.0111 installed in `C:\AFUWIN\AFUWINx64.EXE`

## Installation

1. Clone the repository or download the script.
2. Install the required Python modules:
    ```sh
    pip install pystyle
    ```

## Usage

1. Open a command prompt as Administrator.
2. Navigate to the directory where the script is located.
3. Run the script:
    ```sh
    python bios_backup_restore.py
    ```

## Options

The script provides the following options:

1. **Create a backup of the BIOS settings**: This option creates a backup of your current BIOS settings and saves it in a `.rom` file in the `backups` directory.
2. **Restore the BIOS settings from a backup**: This option allows you to restore BIOS settings from a previously created backup.

## Notes

- Ensure AFUWINx64 is installed at `C:\AFUWIN\AFUWINx64.EXE`.
- The script will prompt you to select an option and guide you through the process.
- Backup files are named in the format `bios_backup_{date}_{time}.rom`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
