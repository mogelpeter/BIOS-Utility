# BIOS Backup and Restore Utility

A utility to backup and restore BIOS settings using AFUWINx64. This script allows you to create a backup of your BIOS settings and restore them when needed.

## Prerequisites

- Windows 10 or 11
- Python 3.8 or higher
- AFUWINx64 version 5.16.02.0111 installed in `C:\AFUWIN\AFUWINx64.EXE`
- UEFITool installed in `C:\AFUWIN\UEFITool.exe`

## Installation

1. Clone the repository or download the script.
2. Download `AFUWINx64` from https://www.ami.com/bios-uefi-utilities/ and put the `AFUWINx64.EXE` into the folder `C:\AFUWIN`.
3. Download `UEFITool` from https://github.com/LongSoft/UEFITool and put the `UEFITool.exe` into the folder `C:\AFUWIN`.

## Usage

1. Navigate to the directory where the script is located.
2. Run the script with the `start.bat` file to get automatically admin rights.

## Options

The script provides the following options:

1. **Create a backup of the BIOS settings**: This option creates a backup of your current BIOS settings and saves it in a `.rom` file in the `backups` directory.
2. **Restore the BIOS settings from a backup**: This option allows you to restore BIOS settings from a previously created backup.
3. **Analyze BIOS ROM file**: This option analyzes a selected BIOS ROM file using UEFITool and saves the output to a readable text file.
4. **Check BIOS Version of OCB File (MSI)**: This option reads the BIOS version from an MSI OCB file.

## Notes

- Ensure AFUWINx64 is installed at `C:\AFUWIN\AFUWINx64.EXE`.
- Ensure UEFITool is installed at `C:\AFUWIN\UEFITool.exe`.
- The script will prompt you to select an option and guide you through the process.
- Backup files are named in the format `bios_backup_{date}_{time}.rom`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
