# BIOS Backup and Restore Utility ![Stable](https://img.shields.io/badge/status-stable-brightgreen) ![Discord](https://dcbadge.limes.pink/api/shield/741265873779818566?compact=true)

A utility to backup and restore BIOS settings using AFUWINx64. This script allows you to create a backup of your BIOS settings and restore them when needed.

## Prerequisites

- Windows 10 or 11
- Python 3.8 or higher
- AFUWINx64 installed in `C:\AFUWIN\AFUWINx64.EXE`

## Installation

1. Clone the repository or download the script.
2. Download `AFUWINx64` from [AMI BIOS UEFI Utilities](https://www.ami.com/bios-uefi-utilities/) and place the `AFUWINx64.EXE` into the folder `C:\AFUWIN`.

## Usage

1. Navigate to the directory where the script is located.
2. Run the script with the `start.bat` file to automatically get admin rights.
3. The script includes a module installer, so you don't need to install dependencies manually.
4. Choose one of the options displayed in the GUI.

## Options

The script provides the following options:

1. **Create a backup of the BIOS settings**: This option creates a backup of your current BIOS settings and saves it in a `.rom` file in the `backups` directory.
2. **Restore the BIOS settings from a backup**: This option allows you to restore BIOS settings from a previously created backup.
3. **MSI - Check BIOS version of .ocb file (WIP)**: This option reads the BIOS version from an MSI OCB file and renames the OCB file accordingly.

## Notes

- Ensure AFUWINx64 is installed at `C:\AFUWIN\AFUWINx64.EXE`.
- Backup files are named in the format `bios_backup_{date}_{time}.rom`.
- OCB files are renamed in the format `MSI_BIOS_{BIOS_Version}_{date}_{time}.ocb` after successfully checking the BIOS version related to the OCB file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
