# EXIF Datetime Updater

## Overview

The **EXIF Datetime Updater** is a Python script that updates the EXIF datetime metadata of images based on their filenames. It can be used as a command-line tool or integrated into macOS as a context menu service for easy right-click access.

## Update EXIF Datetime

## Setup

1. **Install dependencies** (if not already installed):
   ```bash
   pip3 install Pillow piexif tqdm
   ```

2. **Create the Shortcuts Quick Action**:
   - Open **Shortcuts.app** (search in Spotlight or find it in Applications).
   - Click the **+** button in the top-right to create a new shortcut.
   - In the search bar at the top, type "Run Shell Script" and add it to the shortcut.
   - Click the **(i) settings icon** in the top-right of the shortcut editor.
   - Turn ON **"Use as Quick Action"**.
   - Under **"Receive"**, select **"Files or Folders"** and choose **"Finder"**.
   - Select the **"Run Shell Script"** action in the shortcut.
   - Configure the action:
     - **Shell**: `/bin/zsh`
     - **Pass input**: `as arguments`
   - Paste this into the script box (replace the path if your repo is in a different location):
     ```
     osascript -e 'tell app "Terminal" to do script "python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py \"$f\" "'
     ```
     - Note: The `$f` represents the selected file/folder path passed from Finder. This uses AppleScript to open Terminal and run the script interactively.
   - Click **Done** and save the Shortcut as **"Update EXIF Datetime"**.

3. **Enable the Quick Action in Finder**:
   - Open **System Settings** → **Extensions** → **Finder Extensions**.
   - Check the box next to **"Update EXIF Datetime"**.
   - If not listed, restart Finder by running `killall Finder` in Terminal.

## Usage

- Right-click a folder containing images in Finder → **Quick Actions** → **Update EXIF Datetime**.
- A Terminal window will open, prompting for a custom date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or leave blank to auto-infer from filenames.
- Progress and results are shown in the Terminal.

## CLI Alternative

python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py /path/to/folder ["YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"]

## Permissions

For protected folders (e.g., Desktop, Documents), grant Full Disk Access to Terminal: System Settings → Privacy & Security → Full Disk Access → + → /System/Applications/Utilities/Terminal.app