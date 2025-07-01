#!/usr/bin/env python3
"""
Cleanup script for Easy OpenCV library
This script removes unnecessary files from the library to make it cleaner
"""

import os
import shutil
import glob
from pathlib import Path
import sys

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent

# Files to be removed
FILES_TO_REMOVE = [
    # Build artifacts
    "build_publish.py",
    "cleanup_for_pypi.py",
    "easy_opencv_wrapper.egg-info",
    "dist",
    "__pycache__",
    
    # Internal documents not needed for users
    "CLEANUP_SUMMARY.md",
    "PYPI_PUBLISHING_GUIDE.md",
    "LOCAL_TEST_RESULTS.md",
    "DIFFERENCES.md",
    "error_module.md",
    "No_Module_Error.md",
    "m.py",  # Looks like a temporary test file
    
    # Keep only necessary test files
    "test_local.py",
    "test_simple.py",
    
    # Temporary files that might exist
    "**/*.pyc",
    "**/__pycache__",
    "**/.DS_Store",
]

def remove_file_or_dir(path):
    """Remove a file or directory safely"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"Removed file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
    except Exception as e:
        print(f"Error removing {path}: {str(e)}")

def main():
    """Main cleanup function"""
    print("\n===== Easy OpenCV Library Cleanup =====\n")
    
    # Ask for confirmation
    confirmation = input("This will remove unnecessary files from the library. Continue? (y/n): ")
    if confirmation.lower() not in ['y', 'yes']:
        print("Cleanup cancelled.")
        sys.exit(0)
    
    removed_count = 0
    
    # Process each file/pattern to remove
    for item in FILES_TO_REMOVE:
        # Handle glob patterns
        if "*" in item:
            for path in glob.glob(os.path.join(ROOT_DIR, item), recursive=True):
                if os.path.exists(path):
                    remove_file_or_dir(path)
                    removed_count += 1
        else:
            path = os.path.join(ROOT_DIR, item)
            if os.path.exists(path):
                remove_file_or_dir(path)
                removed_count += 1
    
    # Clean up any remaining __pycache__ directories
    for pycache_dir in glob.glob(os.path.join(ROOT_DIR, "**/__pycache__"), recursive=True):
        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir)
            print(f"Removed directory: {pycache_dir}")
            removed_count += 1
    
    print(f"\nCleanup complete! Removed {removed_count} items.")
    print("\nThe library now contains only necessary files for distribution and usage.")
    
    # Create a summary file
    with open(os.path.join(ROOT_DIR, "CLEANUP_REPORT.md"), "w") as f:
        f.write("# Library Cleanup Report\n\n")
        f.write("The following unnecessary files were removed from the project:\n\n")
        for item in FILES_TO_REMOVE:
            f.write(f"- `{item}`\n")
        f.write("\n\nCleanup completed successfully.\n")
    
    print("\nA cleanup report has been created at CLEANUP_REPORT.md")

if __name__ == "__main__":
    main()
