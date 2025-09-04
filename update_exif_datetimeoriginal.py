#!/usr/bin/env python3
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import os 
from PIL import UnidentifiedImageError  # minimal import
from tqdm import tqdm  # progress bar
import sys
import subprocess


def print_metadata(image_path):
    """
    Prints the EXIF metadata of an image.
    Args:
        image_path (str): The file path to the image from which to read the EXIF metadata.
    This function opens the image located at `image_path`, retrieves its EXIF data, 
    and prints each IFD (Image File Directory) along with the corresponding metadata 
    tags and their values.
    """
    image = Image.open(image_path)
    exif_dict = piexif.load(image.info.get("exif", b""))
    for ifd_name, ifd_data in exif_dict.items():
        print(f"{ifd_name}:")
        if ifd_data:
            for tag, value in ifd_data.items():
                tag_name = piexif.TAGS[ifd_name].get(tag, {}).get("name", tag)
                print(f"  {tag_name}: {value}")



def extract_datetime_from_filename(filename):
    patterns = [
        r"(\d{8})[-_](\d{6})",  # Matches '20220416-111049' or '20220416_111049'
        r"(\d{8})_(\d{8})",  # Matches '20240511_195513703'
        r"(\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})",  # Matches '2025-01-05 at 10.53.13'
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            if pattern == r"(\d{8})[-_](\d{6})":
                date_part = match.group(1)  # e.g., '20220416'
                time_part = match.group(2)  # e.g., '111049'
                datetime_str = f"{date_part} {time_part}"
                return datetime.strptime(datetime_str, "%Y%m%d %H%M%S")
            
            elif pattern == r"(\d{8})_(\d{8})":
                date_part = match.group(1)  # e.g., '20240511'
                time_part = match.group(2)  # e.g., '195513703'
                time_part_trimmed = time_part[:6]  # '195513'
                datetime_str = f"{date_part} {time_part_trimmed}"
                return datetime.strptime(datetime_str, "%Y%m%d %H%M%S")
            
            elif pattern == r"(\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})":
                date_part = match.group(1)  # e.g., '2025-01-05'
                hour = match.group(2)  # e.g., '10'
                minute = match.group(3)  # e.g., '53'
                second = match.group(4)  # e.g., '13'
                datetime_str = f"{date_part} {hour}:{minute}:{second}"
                return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            

    return None  # Return None if no pattern matches


def update_exif_datetime(image_path, custom_datetime_str=None):
    """
    Updates the EXIF datetime metadata of an image based on the filename or custom datetime.
    Args:
        image_path (str): The file path to the image whose EXIF datetime needs to be updated.
        custom_datetime (datetime, optional): Custom datetime to set. If None, extracts from filename.
    This function checks the EXIF metadata of the specified image for a "DateTimeOriginal" 
    entry. If not found, it extracts the date and time from the filename using a 
    predefined pattern. It then updates the EXIF metadata with the parsed datetime, 
    specifically setting the `DateTimeOriginal` tag in the Exif IFD.
    If the filename does not contain valid datetime information or if the EXIF 
    already contains a "DateTimeOriginal" entry, it prints a message indicating the status.
    """
    image = Image.open(image_path)

    metadata = image.info.get("exif", None)
    if metadata:
        metadata_dict = piexif.load(metadata)
    else:
        metadata_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

    date_time = None
    if "Exif" in metadata_dict:
        exif_data = metadata_dict["Exif"]
        # piexif.ExifIFD.DateTimeOriginal is 36867 which is the tag for DateTimeOriginal
        if piexif.ExifIFD.DateTimeOriginal in exif_data:
            date_time = exif_data[36867]

    filename = image_path.split('/')[-1]

    if date_time is None:
        # If a custom date string is provided, parse it here; otherwise try to infer from filename
        parsed_datetime = None
        if custom_datetime_str:
            try:
                parsed_datetime = datetime.strptime(custom_datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"Invalid custom datetime format for {filename}. Use YYYY-MM-DD HH:MM:SS")
                return
        else:
            parsed_datetime = extract_datetime_from_filename(filename)
        if parsed_datetime:
            metadata_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = parsed_datetime.strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")
            exif_bytes = piexif.dump(metadata_dict)
            try:
                image.save(image_path, exif=exif_bytes)
                print(f"EXIF of {filename} datetime updated and image saved.")
            except (PermissionError, OSError) as e:
                print(f"Error saving {filename}: {e}. Check permissions or run from Terminal with Full Disk Access.")
        else:
            print(f"No valid time found {filename} to update EXIF datetime")
    else:
        print(f"EXIF already contains DateTimeOriginal for {filename}. No update needed.")



def get_image_files_recursive(folder_path):
    image_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")) and not filename.startswith("._"):
                image_files.append(os.path.join(root, filename))
    return image_files

def prompt_for_date():
    try:
        result = subprocess.run([
            'osascript', '-e',
            'text returned of (display dialog "Enter custom date (YYYY-MM-DD HH:MM:SS) or leave blank for auto:" default answer "")'
        ], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else ""
    except:
        return ""

if __name__ == "__main__":
    folder_path = "/Volumes/Extreme SSD/Images/Pellicule"  # Default path
    if not os.path.exists(folder_path):
        folder_path = "."  # Fallback to current directory
    custom_date_arg = None
    if len(sys.argv) > 1 and sys.argv[1].strip() != "":
        folder_path = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2].strip() != "":
        custom_date_arg = sys.argv[2]
    else:
        # If no custom date provided, prompt for it
        custom_date_arg = prompt_for_date()
    image_files = get_image_files_recursive(folder_path)
    for image_path in tqdm(image_files, desc="Processing images"):
        filename = os.path.basename(image_path)
        try:
            update_exif_datetime(image_path, custom_date_arg)
        except UnidentifiedImageError:
            print(f"Cannot identify image file: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
      
# %%
