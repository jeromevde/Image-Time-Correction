#!/usr/bin/env python3
import re
from datetime import datetime
from PIL import Image
import piexif
import os
from tqdm import tqdm
import sys

def extract_datetime_from_filename(filename):
    patterns = [
        (r"(\d{8})[-_](\d{6})", "%Y%m%d%H%M%S"),
        (r"(\d{8})_(\d{8})", "%Y%m%d%H%M%S"),
        (r"(\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})", "%Y-%m-%d%H%M%S"),
    ]
    for pattern, fmt in patterns:
        match = re.search(pattern, filename)
        if match:
            if fmt == "%Y%m%d%H%M%S":
                if pattern == r"(\d{8})_(\d{8})":
                    dt_str = match.group(1) + match.group(2)[:6]
                else:
                    dt_str = match.group(1) + match.group(2)
                return datetime.strptime(dt_str, fmt)
            else:
                dt_str = match.group(1) + match.group(2) + match.group(3) + match.group(4)
                return datetime.strptime(dt_str, fmt)
    return None

def update_exif_datetime(image_path, custom_datetime_str=None):
    try:
        image = Image.open(image_path)
        exif_dict = piexif.load(image.info.get("exif", b""))
        if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
            print(f"EXIF already set for {os.path.basename(image_path)}")
            return
        parsed_datetime = None
        if custom_datetime_str:
            try:
                parsed_datetime = datetime.strptime(custom_datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                parsed_datetime = datetime.strptime(custom_datetime_str, "%Y-%m-%d")
        else:
            parsed_datetime = extract_datetime_from_filename(os.path.basename(image_path))
        if parsed_datetime:
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = parsed_datetime.strftime("%Y:%m:%d %H:%M:%S").encode()
            exif_bytes = piexif.dump(exif_dict)
            image.save(image_path, exif=exif_bytes)
            print(f"Updated {os.path.basename(image_path)}")
        else:
            print(f"No datetime found for {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Error: {e}")

def get_image_files_recursive(folder_path):
    image_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")) and not filename.startswith("._"):
                image_files.append(os.path.join(root, filename))
    return image_files

def prompt_for_date():
    try:
        return input("Enter date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or blank: ").strip()
    except EOFError:
        return ""

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    custom_date = sys.argv[2] if len(sys.argv) > 2 else prompt_for_date()
    image_files = get_image_files_recursive(folder_path)
    for image_path in tqdm(image_files, desc="Processing"):
        update_exif_datetime(image_path, custom_date)
