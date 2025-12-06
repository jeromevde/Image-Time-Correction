# EXIF Datetime Updater

Simple Python script to set EXIF DateTimeOriginal on photos. It prompts for a date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS). If left blank, it tries to infer the date from the filename.
Processes png, jpg, jpeg
## Install
```bash
pip3 install Pillow piexif tqdm
```
## Terminal usage
```bash
python3 update_exif_datetimeoriginal.py /path/to/folder
```
- You’ll be prompted for a date. Leave blank to infer from filenames.

## Shortcut setup
Run this command in the repository folder to add a simple shortcut command named `dt` to your shell:

```bash
echo "alias dt='python3 \"$(pwd)/update_exif_datetimeoriginal.py\"'" >> ~/.zshrc && source ~/.zshrc
```

Then run:
```bash
dt /path/to/folder
# or run in the current directory:
dt
```