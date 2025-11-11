# EXIF Datetime Updater

A simple Python script to update EXIF datetime metadata in images based on filenames. Use as a Finder context menu action via Shortcuts.

## Setup

1. Install dependencies:
   ```bash
   pip3 install Pillow piexif tqdm
   ```

2. Create a Shortcut:
   - Open Shortcuts.app.
   - Create a new shortcut with "Run Shell Script".
   - Set as Quick Action for Finder (files/folders).
   - Use shell: `/bin/zsh`, pass input as arguments.
   - Script:
     ```
     osascript -e 'tell app "Terminal" to do script "python3 /Users/jerome/Desktop/Image-Time-Correction/update_exif_datetimeoriginal.py \"$f\" "'
     ```
   - Save as "Run Datetime Modifier Here".

3. Enable in Finder: System Settings → Extensions → Finder Extensions → Enable "Run Datetime Modifier Here".

4. Grant permissions: For folders like Desktop, grant Full Disk Access to Terminal: System Settings → Privacy & Security → Full Disk Access → + → /System/Applications/Utilities/Terminal.app

## Usage

- Right-click a folder in Finder → Quick Actions → Run Datetime Modifier Here.
- Terminal opens: Enter date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or leave blank to infer from filenames.

## CLI

python3 update_exif_datetimeoriginal.py /path/to/folder ["YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"]

