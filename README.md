# EXIF Datetime Updater

## Overview

The **EXIF Datetime Updater** is a Python script that updates the EXIF datetime metadata of images based on their filenames. It searches for images in a specified folder, extracts datetime information from the filenames, and updates the EXIF tags accordingly.

## Features

- Reads EXIF metadata from image files.
- Updates the `DateTimeOriginal` EXIF tags if not already present by extracting it from the imagename
- Works with common image formats like JPEG and PNG.
- Prints existing metadata for verification.

## Requirements

- Python 3.x
- PIL (Pillow) library
- piexif library

## Installation

You can install the required libraries using pip:

```bash
pip install Pillow piexif
```

## Run

```bash
python update_exif_datetimeoriginal.py
```