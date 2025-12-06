import os
from PIL import Image
import piexif
import argparse

def count_missing_datetime_original(folder_path):
    missing_count = 0
    total_count = 0
    
    print(f"Scanning {folder_path}...")
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")) and not filename.startswith("._"):
                total_count += 1
                image_path = os.path.join(root, filename)
                try:
                    with Image.open(image_path) as image:
                        exif_bytes = image.info.get("exif")
                        if not exif_bytes:
                            print(f"Missing Exif bytes: {filename}")
                            missing_count += 1
                            continue
                            
                        exif_dict = piexif.load(exif_bytes)
                        if "Exif" not in exif_dict or piexif.ExifIFD.DateTimeOriginal not in exif_dict["Exif"]:
                            missing_count += 1
                            if missing_count <= 20:
                                print(f"Missing DateTimeOriginal: {filename}")
                except Exception as e:
                    missing_count += 1
                    if missing_count <= 20:
                        print(f"Error reading {filename}: {e}")
    
    print(f"Total Images (JPEG/PNG): {total_count}")
    print(f"Images without DateTimeOriginal: {missing_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count images without DateTimeOriginal EXIF data.")
    parser.add_argument("path", help="Path to the folder to scan")
    args = parser.parse_args()
    count_missing_datetime_original(args.path)
