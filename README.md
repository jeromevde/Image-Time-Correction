# EXIF Datetime Updater

## Overview

The **EXIF Datetime Updater** is a Python script that updates the EXIF datetime metadata of images based on their filenames. It can be used as a command-line tool or integrated into macOS as a context menu service for easy right-click access.

## Features

- **Command Line Tool**: Batch process images in folders
- **macOS Context Menu Integration**: Right-click on files/folders in Finder
- **Dual Mode Operation**:
  - **Custom Date**: Apply a single date/time to all selected images
  - **Automatic**: Extracts datetime from filenames using pattern matching
  - **Flexible Workflow**: Can switch between modes during operation
- **GUI Interface**: User-friendly dialogs for mode selection and custom date input
- **Progress Tracking**: Visual progress bar during processing
- **Comprehensive Error Handling**: Detailed reporting of successes, skips, and errors
- **Multiple Filename Patterns**: Supports various datetime formats in filenames
- Works with common image formats like JPEG and PNG
- Preserves existing EXIF data when DateTimeOriginal is already present

## Requirements

- Python 3.x
- PIL (Pillow) library
- piexif library
- tkinter (for GUI - usually included with Python)

## Installation

You can install the required libraries using pip:

```bash
pip3 install Pillow piexif
```

For macOS users wanting to use the context menu feature, tkinter might need to be installed separately:

```bash
# If using Homebrew Python:
brew install python-tk
```

## Usage

### Method 1: macOS Context Menu (Recommended for Mac users)

1. Follow the setup instructions in [MACOS_SETUP.md](MACOS_SETUP.md)
2. Right-click on image files or folders in Finder
3. Select "Update EXIF Datetime" from the context menu
4. Choose whether to set a custom date or extract from filenames
5. For custom date: enter your date/time or switch to auto mode if you change your mind
6. Monitor progress and view results

### Method 2: Command Line

Run the original script directly:

```bash
python3 update_exif_datetimeoriginal.py
```

Or use the GUI version:

```bash
python3 exif_datetime_gui.py /path/to/images/
```

## Supported Filename Patterns

The automatic mode recognizes these filename patterns:

- `20220416-111049` or `20220416_111049` (YYYYMMDD-HHMMSS)
- `20240511_195513703` (YYYYMMDD_HHMMSSMMM)  
- `2025-01-05 at 10.53.13` (YYYY-MM-DD at HH.MM.SS)

## File Structure

```
Image-Time-Correction/
├── update_exif_datetimeoriginal.py  # Original command-line script
├── exif_datetime_gui.py             # GUI wrapper for context menu
├── exif_datetime_service.sh         # Shell script for Automator
├── ExifDatetimeUpdater.applescript  # AppleScript for service
├── README.md                        # This file  
└── MACOS_SETUP.md                  # macOS setup instructions
```