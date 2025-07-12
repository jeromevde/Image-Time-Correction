#!/usr/bin/env python3
"""
EXIF Datetime Updater - GUI Wrapper for macOS Context Menu
This script provides a graphical interface for updating EXIF datetime metadata
with options for automatic inference or manual date input.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
import re
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
from PIL import UnidentifiedImageError
from tqdm import tqdm
import argparse


class ExifDateTimeUpdater:
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.skipped_count = 0
        
    def extract_datetime_from_filename(self, filename):
        """Extract datetime from filename using various patterns."""
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

        return None

    def update_exif_datetime(self, image_path, custom_datetime=None):
        """Update EXIF datetime metadata of an image."""
        try:
            image = Image.open(image_path)

            metadata = image.info.get("exif", None)
            if metadata:
                metadata_dict = piexif.load(metadata)
            else:
                metadata_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

            date_time = None
            if "Exif" in metadata_dict:
                exif_data = metadata_dict["Exif"]
                if piexif.ExifIFD.DateTimeOriginal in exif_data:
                    date_time = exif_data[piexif.ExifIFD.DateTimeOriginal]

            filename = os.path.basename(image_path)

            if date_time is None:
                if custom_datetime:
                    # Use custom datetime
                    target_datetime = custom_datetime
                else:
                    # Try to extract from filename
                    target_datetime = self.extract_datetime_from_filename(filename)

                if target_datetime:
                    metadata_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = target_datetime.strftime("%Y:%m:%d %H:%M:%S").encode("utf-8")
                    exif_bytes = piexif.dump(metadata_dict)
                    image.save(image_path, exif=exif_bytes)
                    self.processed_count += 1
                    return f"Updated: {filename}"
                else:
                    self.skipped_count += 1
                    return f"Skipped (no valid date): {filename}"
            else:
                self.skipped_count += 1
                return f"Skipped (already has DateTimeOriginal): {filename}"

        except UnidentifiedImageError:
            self.error_count += 1
            return f"Error (unidentified image): {filename}"
        except Exception as e:
            self.error_count += 1
            return f"Error processing {filename}: {str(e)}"

    def get_image_files_recursive(self, folder_path):
        """Get all image files recursively from a folder."""
        image_files = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")) and not filename.startswith("._"):
                    image_files.append(os.path.join(root, filename))
        return image_files

    def get_image_files_from_paths(self, paths):
        """Get all image files from a list of file/folder paths."""
        image_files = []
        for path in paths:
            if os.path.isfile(path):
                if path.lower().endswith((".png", ".jpg", ".jpeg")) and not os.path.basename(path).startswith("._"):
                    image_files.append(path)
            elif os.path.isdir(path):
                image_files.extend(self.get_image_files_recursive(path))
        return image_files


class DateTimeDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Custom Date/Time")
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Instructions
        tk.Label(self.dialog, text="Enter the date and time to apply to all selected images:", 
                wraplength=400, justify="left", font=("Arial", 12)).pack(pady=15)
        
        # Note about fallback
        note_label = tk.Label(self.dialog, 
                             text="(If you change your mind, click 'Use Auto' to extract dates from filenames instead)",
                             wraplength=400, justify="center", font=("Arial", 9), fg="gray")
        note_label.pack(pady=5)
        
        # Date frame
        date_frame = tk.Frame(self.dialog)
        date_frame.pack(pady=15)
        
        tk.Label(date_frame, text="Date (YYYY-MM-DD):", font=("Arial", 11)).pack()
        self.date_entry = tk.Entry(date_frame, width=20, font=("Arial", 11))
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time frame
        time_frame = tk.Frame(self.dialog)
        time_frame.pack(pady=15)
        
        tk.Label(time_frame, text="Time (HH:MM:SS):", font=("Arial", 11)).pack()
        self.time_entry = tk.Entry(time_frame, width=20, font=("Arial", 11))
        self.time_entry.pack(pady=5)
        self.time_entry.insert(0, "12:00:00")
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=25)
        
        tk.Button(button_frame, text="Apply Custom Date", command=self.ok_clicked, 
                 width=15, height=2, bg="#2196F3", fg="white", font=("Arial", 10)).pack(side=tk.TOP, pady=5)
        
        button_row = tk.Frame(button_frame)
        button_row.pack(pady=10)
        
        tk.Button(button_row, text="Use Auto", command=self.auto_clicked, 
                 width=12, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row, text="Cancel", command=self.cancel_clicked, 
                 width=12, bg="#f44336", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Focus on date entry
        self.date_entry.focus()
        
    def ok_clicked(self):
        try:
            date_str = self.date_entry.get().strip()
            time_str = self.time_entry.get().strip()
            datetime_str = f"{date_str} {time_str}"
            self.result = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Invalid Date/Time", "Please enter a valid date (YYYY-MM-DD) and time (HH:MM:SS)")
    
    def auto_clicked(self):
        self.result = "auto"  # Special value to indicate auto mode
        self.dialog.destroy()
            
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()


def show_initial_dialog():
    """Show initial dialog asking if user wants to set a custom date."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create a custom dialog
    dialog = tk.Toplevel(root)
    dialog.title("EXIF DateTime Updater")
    dialog.geometry("520x280")
    dialog.resizable(False, False)
    
    # Center the dialog on screen
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (520 // 2)
    y = (dialog.winfo_screenheight() // 2) - (280 // 2)
    dialog.geometry(f"520x280+{x}+{y}")
    
    dialog.grab_set()
    dialog.focus_set()
    
    result = {"action": None}
    
    # Title
    title_label = tk.Label(dialog, text="EXIF DateTime Updater", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)
    
    # Instructions
    instruction_label = tk.Label(dialog, 
                                text="Do you want to set a custom date/time for all selected images?",
                                font=("Arial", 12))
    instruction_label.pack(pady=5)
    
    sub_instruction_label = tk.Label(dialog, 
                                   text="If you choose 'No', dates will be automatically extracted from filenames.",
                                   font=("Arial", 10), fg="gray")
    sub_instruction_label.pack(pady=5)
    
    # Buttons frame
    buttons_frame = tk.Frame(dialog)
    buttons_frame.pack(pady=30)
    
    def yes_custom():
        result["action"] = "custom"
        dialog.destroy()
        
    def no_auto():
        result["action"] = "auto"
        dialog.destroy()
        
    def cancel():
        result["action"] = None
        dialog.destroy()
    
    # Mode buttons
    yes_btn = tk.Button(buttons_frame, text="Yes, set custom date", 
                       command=yes_custom, width=20, height=2,
                       bg="#2196F3", fg="white", font=("Arial", 11))
    yes_btn.pack(pady=5)
    
    no_btn = tk.Button(buttons_frame, text="No, extract from filenames", 
                      command=no_auto, width=20, height=2,
                      bg="#4CAF50", fg="white", font=("Arial", 11))
    no_btn.pack(pady=5)
    
    cancel_btn = tk.Button(buttons_frame, text="Cancel", 
                          command=cancel, width=20,
                          bg="#f44336", fg="white", font=("Arial", 11))
    cancel_btn.pack(pady=5)
    
    dialog.wait_window()
    root.destroy()
    
    return result["action"]


def main():
    parser = argparse.ArgumentParser(description="Update EXIF datetime metadata for images")
    parser.add_argument("paths", nargs="+", help="Paths to image files or folders")
    args = parser.parse_args()
    
    # Show initial dialog asking if user wants custom date
    action = show_initial_dialog()
    if action is None:
        return  # User cancelled
    
    updater = ExifDateTimeUpdater()
    
    # Get all image files from the provided paths
    image_files = updater.get_image_files_from_paths(args.paths)
    
    if not image_files:
        messagebox.showinfo("No Images Found", "No image files found in the selected paths.")
        return
    
    custom_datetime = None
    if action == "custom":
        # Show custom datetime dialog
        root = tk.Tk()
        root.withdraw()
        
        datetime_dialog = DateTimeDialog(root)
        root.wait_window(datetime_dialog.dialog)
        dialog_result = datetime_dialog.result
        root.destroy()
        
        # Handle different dialog results
        if dialog_result is None:
            return  # User cancelled completely
        elif dialog_result == "auto":
            # User chose to use auto mode instead
            action = "auto"
            messagebox.showinfo("Switched to Auto Mode", 
                              "Will extract dates from filenames instead.")
        else:
            # User provided a custom datetime
            custom_datetime = dialog_result
    
    # Process the images
    results = []
    total_files = len(image_files)
    
    # Create progress window
    progress_root = tk.Tk()
    progress_root.title("Processing Images...")
    progress_root.geometry("500x150")
    progress_root.resizable(False, False)
    
    # Center the progress window
    progress_root.update_idletasks()
    x = (progress_root.winfo_screenwidth() // 2) - (500 // 2)
    y = (progress_root.winfo_screenheight() // 2) - (150 // 2)
    progress_root.geometry(f"500x150+{x}+{y}")
    
    mode_text = "custom date" if custom_datetime else "filename extraction"
    tk.Label(progress_root, text=f"Processing images using {mode_text}...", 
             font=("Arial", 12)).pack(pady=10)
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_root, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10, padx=20, fill=tk.X)
    
    status_label = tk.Label(progress_root, text="Starting...", font=("Arial", 10))
    status_label.pack(pady=5)
    
    progress_root.update()
    
    for i, image_path in enumerate(image_files):
        filename = os.path.basename(image_path)
        status_label.config(text=f"Processing: {filename}")
        progress_var.set((i / total_files) * 100)
        progress_root.update()
        
        result = updater.update_exif_datetime(image_path, custom_datetime)
        results.append(result)
    
    progress_var.set(100)
    progress_root.update()
    progress_root.destroy()
    
    # Show results
    mode_description = f"custom date ({custom_datetime.strftime('%Y-%m-%d %H:%M:%S')})" if custom_datetime else "filename extraction"
    result_message = f"Processing complete using {mode_description}!\n\n"
    result_message += f"Total files: {total_files}\n"
    result_message += f"Updated: {updater.processed_count}\n"
    result_message += f"Skipped: {updater.skipped_count}\n"
    result_message += f"Errors: {updater.error_count}\n"
    
    messagebox.showinfo("Results", result_message)


if __name__ == "__main__":
    main()
