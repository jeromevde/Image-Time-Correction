# EXIF Datetime Updater

## Overview

The **EXIF Datetime Updater** is a Python script that updates the EXIF datetime metadata of images based on their filenames. It can be used as a command-line tool or integrated into macOS as a context menu service for easy right-click access.

## Update EXIF Datetime

The script prompts for a custom date if not provided; otherwise infers from filenames.

**CLI**: 

```bash
python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py /path/to/folder ["YYYY-MM-DD HH:MM:SS"]
```

**Shortcuts**: create Quick Action (Files/Folders) with Run Shell Script: 


```bash
/usr/bin/env python3 /Users/jerome/Documents/Image-Time-Correction/update_exif_datetimeoriginal.py "$f"
```

**Note**: For protected folders, use CLI from Terminal with Full Disk Access granted. Shortcuts may be sandboxed and fail with "operation not permitted".

**Permissions**: For protected folders, grant Full Disk Access to Shortcuts: System Settings → Privacy & Security → Full Disk Access → + → /System/Applications/Shortcuts.app

If permission errors occur, ensure the folder is writable or grant Full Disk Access to Shortcuts/Terminal in System Settings → Privacy & Security.

make sure to have the python shebang #!/usr/bin/env python3 at the top of the script and make it executable