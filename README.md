# EXIF Datetime Updater

## Overview

The **EXIF Datetime Updater** is a Python script that updates the EXIF datetime metadata of images based on their filenames. It can be used as a command-line tool or integrated into macOS as a context menu service for easy right-click access.

## Update EXIF Datetime

The script prompts for a custom date in terminal if not provided; otherwise infers from filenames.

**CLI**: 

```bash
python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py /path/to/folder ["YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"]
```

**Shortcuts**: create Quick Action (Files/Folders) with Run Shell Script: 

```bash
open -a Terminal.app "python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py '$f'"
```

This opens a Terminal window for input and logging. Progress bar and messages (red for errors) are shown.

**Permissions**: For protected folders, grant Full Disk Access to Terminal: System Settings → Privacy & Security → Full Disk Access → + → /System/Applications/Utilities/Terminal.app

If permission errors occur, ensure the folder is writable or grant Full Disk Access to Shortcuts/Terminal in System Settings → Privacy & Security.

make sure to have the python shebang #!/usr/bin/env python3 at the top of the script and make it executable