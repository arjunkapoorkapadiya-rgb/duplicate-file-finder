# duplicate-file-finder

Find duplicate files using SHA-256 without deleting anything.

Maintained by @arjunkapoorkapadiya-rgb.

## Requirements

Python 3.9 or newer. No third-party packages required.

## Usage

    python main.py "C:\Users\chinm\Downloads"

## Behavior and limitations

Recursively scans regular files, skips symbolic links, and reports matching SHA-256 hashes as JSON. No files are modified. Large folders can take time. Files changing during the scan may produce inconsistent results. Exit code 2 indicates an input or scan error.