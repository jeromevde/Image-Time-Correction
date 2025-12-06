#!/usr/bin/env python3
import re
from datetime import datetime
from PIL import Image
import piexif
import os
from tqdm import tqdm
import sys

def extract_datetime_from_filename(filename):
    # Define patterns as (regex, date_format, extractor_function)
    # extractor_function receives the regex match object and returns the string to parse
    patterns = [
        (
            r"(\d{8})[-_](\d{6})", 
            "%Y%m%d%H%M%S", 
            lambda m: m.group(1) + m.group(2)
        ), # Example: 20210904_090442 or 20210904-090442
        (
            r"(\d{8})_(\d{8})", 
            "%Y%m%d%H%M%S", 
            lambda m: m.group(1) + m.group(2)[:6]
        ), # Example: 20210904_09044200 (takes first 6 digits of time)
        (
            r"(\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})", 
            "%Y-%m-%d%H%M%S", 
            lambda m: m.group(1) + m.group(2) + m.group(3) + m.group(4)
        ), # Example: 2021-09-04 at 09.04.42
        (
            r"IMG-(\d{8})-WA\d+",
            "%Y%m%d",
            lambda m: m.group(1)
        ), # Example: IMG-20190712-WA0045.jpg
        (
            r"Snapchat-(\d{14})",
            "%Y%m%d%H%M%S",
            lambda m: m.group(1)
        ), # Example: Snapchat-20140402073118.jpg
        (
            r"CamScanner (\d{2}-\d{2}-\d{4}) (\d{2}\.\d{2})",
            "%m-%d-%Y %H.%M",
            lambda m: m.group(1) + " " + m.group(2)
        ), # Example: CamScanner 09-29-2022 20.24 (2).jpg
        (
            r"^(\d{13})",
            "timestamp_ms", 
            lambda m: m.group(1)
        ), # Example: 1645285721828... (Unix timestamp in ms)
        (
            r"Snapchat-(\d{10})",
            "%s",
            lambda m: m.group(1)
        ), # Example: Snapchat-1698719360.jpg (Unix timestamp in seconds)
        (
            r"bereal-(\d{4}-\d{2}-\d{2}-\d{4})",
            "%Y-%m-%d-%H%M",
            lambda m: m.group(1)
        ), # Example: bereal-2024-07-11-0139.jpg
        (
            r"FB_IMG_(\d{13})",
            "timestamp_ms",
            lambda m: m.group(1)
        ), # Example: FB_IMG_1660148763169.jpg
        (
            r"received_(\d{15})",
            "timestamp_ms",
            lambda m: m.group(1)
        ), # Example: received_463644631440651.jpeg
        (
            r"AirBrush_(\d{14})",
            "%Y%m%d%H%M%S",
            lambda m: m.group(1)
        ), # Example: AirBrush_20220220171939.jpg
        (
            r"Screenshot_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})",
            "%Y-%m-%d-%H-%M-%S",
            lambda m: m.group(1)
        ), # Example: Screenshot_2015-02-28-01-44-11.png
    ]

    for pattern, fmt, extractor in patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                dt_str = extractor(match)
                if fmt == "timestamp_ms":
                    return datetime.fromtimestamp(int(dt_str) / 1000.0)
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
    return None

DO_NOT_MODIFY_EXIF = False # for test runs, set to True to avoid modifying EXIF data

def update_exif_datetime(image_path, custom_datetime_str=None):
    try:
        image = Image.open(image_path)
        exif_data = image.info.get("exif")
        if exif_data:
            exif_dict = piexif.load(exif_data)
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        if "Exif" in exif_dict and piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
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
            if not DO_NOT_MODIFY_EXIF:
                if "Exif" not in exif_dict:
                    exif_dict["Exif"] = {}
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
        return input("Enter date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) or blank if you want the program to infer from filename: ").strip()
    except EOFError:
        return ""

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    custom_date = prompt_for_date()
    image_files = get_image_files_recursive(folder_path)
    for image_path in tqdm(image_files, desc="Processing"):
        update_exif_datetime(image_path, custom_date)
