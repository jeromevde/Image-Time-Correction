#!/bin/bash

# EXIF Datetime Updater - Shell Script for macOS Automator Service
# This script is called by the Automator service when users right-click on files/folders

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the Python GUI script
PYTHON_SCRIPT="$SCRIPT_DIR/exif_datetime_gui.py"

# Make sure the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    osascript -e 'display dialog "Error: exif_datetime_gui.py not found!" buttons {"OK"} default button "OK"'
    exit 1
fi

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    osascript -e 'display dialog "Error: Python not found! Please install Python 3." buttons {"OK"} default button "OK"'
    exit 1
fi

# Check if required Python packages are installed
$PYTHON_CMD -c "import PIL, piexif, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    osascript -e 'display dialog "Error: Required Python packages not installed!\n\nPlease install:\npip3 install Pillow piexif" buttons {"OK"} default button "OK"'
    exit 1
fi

# Run the Python GUI script with all passed arguments
$PYTHON_CMD "$PYTHON_SCRIPT" "$@"
