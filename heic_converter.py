#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def convert_heic_to_jpeg(folder_path):
    """
    Converts all HEIC files in the specified folder to JPEG format.
    
    Args:
        folder_path (str): Path to the folder containing HEIC files
    """
    # Check if sips command is available (macOS built-in)
    try:
        subprocess.run(['sips', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: 'sips' command not found. This script requires macOS.")
        return False
    
    folder = Path(folder_path)
    
    # Check if folder exists
    if not folder.exists() or not folder.is_dir():
        print(f"Error: Folder '{folder_path}' does not exist or is not a directory.")
        return False
    
    # Find all HEIC files in the folder
    heic_files = list(folder.glob('*.HEIC'))
    heic_files.extend(folder.glob('*.heic'))
    
    if not heic_files:
        print(f"No HEIC files found in '{folder_path}'.")
        return False
    
    print(f"Found {len(heic_files)} HEIC files. Converting to JPEG...")
    
    # Convert each HEIC file to JPEG
    conversion_count = 0
    for heic_file in heic_files:
        jpeg_file = heic_file.with_suffix('.jpg')
        
        # Skip if JPEG already exists
        if jpeg_file.exists():
            print(f"Skipping {heic_file.name} - JPEG version already exists.")
            continue
        
        print(f"Converting {heic_file.name} to JPEG...", end='')
        
        # Use sips to convert HEIC to JPEG
        cmd = ['sips', '-s', 'format', 'jpeg', str(heic_file), '--out', str(jpeg_file)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(" Done!")
            conversion_count += 1
        else:
            print(" Failed!")
            print(f"Error: {result.stderr.decode('utf-8')}")
    
    print(f"\nConversion complete! Successfully converted {conversion_count} out of {len(heic_files)} files.")
    return True

if __name__ == "__main__":
    # Get folder path from command line or use current folder
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # Default to Desktop folder if no path is provided
        folder_path = str(Path.home() / 'Desktop')
    
    print(f"Processing HEIC files in: {folder_path}")
    convert_heic_to_jpeg(folder_path)