# BIOS Backup and Restore Utility

A utility to backup and restore BIOS settings using AFUWINx64. This script allows you to create a backup of your BIOS settings and restore them when needed.

## Prerequisites

- Windows 10 or 11
- Python 3.8 or higher
- AFUWINx64 version 5.16.02.0111 installed in `C:\AFUWIN\AFUWINx64.EXE`

## Installation

1. Clone the repository or download the script.
2. Download AFUWINx64 from > https://www.ami.com/bios-uefi-utilities/ and put the named file into the folder `C:\AFUWIN`

## Usage

1. Navigate to the directory where the script is located.
2. Run the script with the start.bat file.

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
