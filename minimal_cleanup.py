"""
Essential Library Files Cleanup
This script keeps only the core essential files for the library and removes everything else
"""

import os
import shutil
import sys
import time
from datetime import datetime

# Define the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define ONLY essential files/directories to keep
ESSENTIAL_FILES = [
    "README.md",
    "requirements.txt",
    "setup.py",
    "pyproject.toml", 
    "LICENSE",
    "MANIFEST.in",
    "easy_opencv"  # Core library directory
]

# Define files that should never be deleted (safety measure)
NEVER_DELETE = [
    ".git",  # Don't delete git repository
    "minimal_cleanup.py"  # Don't delete this script
]

def is_essential(path):
    """Check if a path is considered essential"""
    rel_path = os.path.relpath(path, ROOT_DIR)
    
    # Check if the file is in the essential list
    for essential in ESSENTIAL_FILES:
        essential_path = os.path.join(ROOT_DIR, essential)
        if os.path.exists(essential_path):
            if os.path.samefile(path, essential_path):
                return True
            elif os.path.isdir(essential_path) and path.startswith(essential_path):
                return True
            
    # Check if the file is in the never delete list
    for safe in NEVER_DELETE:
        safe_path = os.path.join(ROOT_DIR, safe)
        if os.path.exists(safe_path):
            if os.path.samefile(path, safe_path):
                return True
            elif os.path.isdir(safe_path) and path.startswith(safe_path):
                return True
            
    # If this is the script itself, don't delete it
    if os.path.samefile(path, __file__):
        return True
        
    return False

def remove_path(path, removal_list):
    """Remove a file or directory if it's not essential"""
    if is_essential(path):
        return False
        
    rel_path = os.path.relpath(path, ROOT_DIR)
    
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            print(f"Removed file: {rel_path}")
            removal_list.append(rel_path)
            return True
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Removed directory: {rel_path}")
            removal_list.append(rel_path)
            return True
    except Exception as e:
        print(f"Error removing {rel_path}: {str(e)}")
        
    return False

def main():
    """Run the cleanup process"""
    print("\n===== Essential Files Cleanup =====\n")
    print("This will keep ONLY essential files and remove everything else.\n")
    
    # Ask for confirmation
    confirmation = input("This is a DESTRUCTIVE operation. Are you sure? (type 'YES' to confirm): ")
    if confirmation != "YES":
        print("Cleanup cancelled.")
        sys.exit(0)
    
    removed_count = 0
    removal_list = []
    
    # Get all files and directories in the root directory
    for item in os.listdir(ROOT_DIR):
        item_path = os.path.join(ROOT_DIR, item)
        
        # Skip items that are in the essential or never delete lists
        if is_essential(item_path):
            print(f"Keeping essential: {item}")
            continue
            
        # Remove everything else
        if remove_path(item_path, removal_list):
            removed_count += 1
    
    # Generate report
    report_file = os.path.join(ROOT_DIR, "CLEANUP_REPORT.md")
    with open(report_file, "w") as f:
        f.write(f"# Essential Files Cleanup Report\n\n")
        f.write(f"Cleanup performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## {removed_count} items removed\n\n")
        for item in sorted(removal_list):
            f.write(f"- `{item}`\n")
        
        f.write("\n\n## Kept Essential Files\n\n")
        for item in sorted(ESSENTIAL_FILES):
            f.write(f"- `{item}`\n")
            
    print(f"\nRemoved {removed_count} non-essential items.")
    print("\nThe library now contains only core essential files needed for distribution.")
    print(f"\nCleanup report written to {report_file}")

if __name__ == "__main__":
    main()
