# macOS Context Menu Setup Instructions

This guide will help you set up the EXIF Datetime Updater as a macOS context menu (right-click) service.

## Prerequisites

1. **Python 3** with required packages:
   ```bash
   pip3 install Pillow piexif
   ```

2. **tkinter** (usually comes with Python, but on some systems you might need to install it):
   ```bash
   # If using Homebrew Python:
   brew install python-tk
   ```

## Setup Instructions

### Method 1: Using Automator (Recommended)

1. **Open Automator**:
   - Press `Cmd + Space` and type "Automator"
   - Click on Automator to open it

2. **Create a New Service**:
   - Choose "Quick Action" (or "Service" in older macOS versions)
   - Click "Choose"

3. **Configure the Service**:
   - At the top of the workflow:
     - Set "Service receives selected" to "files or folders"
     - Set "in" to "Finder"
   - Check "Output replaces selected text" if you want (optional)

4. **Add a Run Shell Script Action**:
   - In the search box, type "Run Shell Script"
   - Drag "Run Shell Script" to the workflow area
   - Set "Pass input" to "as arguments"
   - Replace the default script content with:
   ```bash
   #!/bin/bash
   
   # Path to your project directory (UPDATE THIS PATH!)
   PROJECT_DIR="/path/to/your/Image-Time-Correction"
   
   # Path to the shell script
   SHELL_SCRIPT="$PROJECT_DIR/exif_datetime_service.sh"
   
   # Run the shell script with all arguments
   bash "$SHELL_SCRIPT" "$@"
   ```
   
   **Important**: Update the `PROJECT_DIR` path to the actual location where you saved the project files.

5. **Save the Service**:
   - Press `Cmd + S` or go to File > Save
   - Name it "Update EXIF Datetime" (or any name you prefer)
   - The service will be saved automatically

6. **Test the Service**:
   - Go to Finder and select some image files or a folder containing images
   - Right-click and look for "Update EXIF Datetime" in the context menu
   - If you don't see it immediately, look under "Services" or "Quick Actions"

### Method 2: Manual Installation

If you prefer to install manually or the Automator method doesn't work:

1. **Copy the files** to a permanent location (e.g., `/usr/local/bin/` or a folder in your home directory)

2. **Create the Automator service** following steps 1-5 above

3. **Update file paths** in the shell script if necessary

## Usage

Once set up, you can:

1. **Right-click** on image files or folders in Finder
2. **Select "Update EXIF Datetime"** from the context menu
3. **Choose your approach**:
   - **"Yes, set custom date"**: Input a single date/time to apply to all selected images
   - **"No, extract from filenames"**: Automatically extract dates from individual filenames
4. **For custom date mode**: 
   - Enter your desired date and time in the dialog
   - Or click "Use Auto" to switch to filename extraction
   - Or click "Cancel" to abort
5. **Monitor progress** through the GUI progress bar
6. **View results** in the completion dialog

### Workflow Details

- **Initial Choice**: First, you'll be asked if you want to set a custom date for all images
- **Fallback Option**: If you initially choose custom date but change your mind, you can switch to auto mode
- **Smart Processing**: The system will use your custom date if provided, otherwise it automatically extracts dates from filenames
- **Flexible**: You can cancel at any point during the process

## Supported Filename Patterns

The automatic mode can extract dates from these filename patterns:

- `20220416-111049` or `20220416_111049` (YYYYMMDD-HHMMSS)
- `20240511_195513703` (YYYYMMDD_HHMMSSMMM)
- `2025-01-05 at 10.53.13` (YYYY-MM-DD at HH.MM.SS)

## Troubleshooting

### Service doesn't appear in context menu:
- Try logging out and back in
- Check System Preferences > Security & Privacy > Privacy > Accessibility
- Make sure the paths in the shell script are correct

### Python/Package errors:
- Verify Python 3 is installed: `python3 --version`
- Install required packages: `pip3 install Pillow piexif`
- For tkinter issues on macOS: `brew install python-tk`

### Permission errors:
- Make sure the shell script is executable: `chmod +x exif_datetime_service.sh`
- Check file permissions for the project directory

### Files not found:
- Verify all file paths in the scripts are correct
- Make sure all files are in the same directory

## File Structure

Your project should have these files:
```
Image-Time-Correction/
├── exif_datetime_gui.py          # Main GUI application
├── exif_datetime_service.sh      # Shell script for Automator
├── update_exif_datetimeoriginal.py  # Original script
├── README.md                     # This file
└── MACOS_SETUP.md               # Setup instructions
```

## Advanced Configuration

You can modify `exif_datetime_gui.py` to:
- Add new filename patterns in the `extract_datetime_from_filename` method
- Change the GUI appearance
- Add more image formats
- Customize error handling

## Security Note

When first running the service, macOS may ask for permissions to:
- Access files in Finder
- Run scripts
- Access the selected files/folders

Grant these permissions for the service to work properly.
