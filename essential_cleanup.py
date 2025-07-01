#!/usr/bin/env python
"""
Essential Library Files Cleanup
This script keeps only the core essential files for the library and removes everything else
"""

import os
import shutil
import glob
from pathlib import Path
import sys
import time

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent

class EssentialFilesCleaner:
    def __init__(self, force=False):
        """Initialize the cleaner"""
        self.force = force
        self.removed_count = 0
        self.removal_list = []
        
        # Define ONLY essential files/directories to keep
        self.essential_files = [
            "README.md",
            "requirements.txt",
            "setup.py",
            "pyproject.toml", 
            "LICENSE",
            "MANIFEST.in",
            "easy_opencv"  # Core library directory
        ]
        
        # Define files that should never be deleted (safety measure)
        self.never_delete = [
            ".git",  # Don't delete git repository
            "essential_cleanup.py"  # Don't delete this script
        ]

    def is_essential(self, path):
        """Check if a path is considered essential"""
        rel_path = os.path.relpath(path, ROOT_DIR)
        
        # Check if the file is in the essential list
        for essential in self.essential_files:
            essential_path = os.path.join(ROOT_DIR, essential)
            if os.path.samefile(path, essential_path):
                return True
            elif os.path.isdir(essential_path) and path.startswith(essential_path):
                return True
                
        # Check if the file is in the never delete list
        for safe in self.never_delete:
            safe_path = os.path.join(ROOT_DIR, safe)
            if os.path.exists(safe_path) and (os.path.samefile(path, safe_path) or 
                                             (os.path.isdir(safe_path) and path.startswith(safe_path))):
                return True
                
        # If this is the script itself, don't delete it
        if os.path.samefile(path, __file__):
            return True
            
        return False

    def remove_path(self, path):
        """Remove a file or directory if it's not essential"""
        if self.is_essential(path):
            return False
            
        rel_path = os.path.relpath(path, ROOT_DIR)
        
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                print(f"Removed file: {rel_path}")
                self.removal_list.append(rel_path)
                self.removed_count += 1
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Removed directory: {rel_path}")
                self.removal_list.append(rel_path)
                self.removed_count += 1
                return True
        except Exception as e:
            print(f"Error removing {rel_path}: {str(e)}")
            
        return False

    def run(self):
        """Run the cleanup process"""
        print("\n===== Essential Files Cleanup =====\n")
        print("This will keep ONLY essential files and remove everything else.\n")
        
        if not self.force:
            confirmation = input("This is a DESTRUCTIVE operation. Are you sure? (type 'YES' to confirm): ")
            if confirmation != "YES":
                print("Cleanup cancelled.")
                sys.exit(0)
        
        # Get all files and directories in the root directory
        for item in os.listdir(ROOT_DIR):
            item_path = os.path.join(ROOT_DIR, item)
            
            # Skip items that are in the essential or never delete lists
            if self.is_essential(item_path):
                print(f"Keeping essential: {item}")
                continue
                
            # Remove everything else
            self.remove_path(item_path)
        
        # Generate report
        report_file = os.path.join(ROOT_DIR, "CLEANUP_REPORT.md")
        with open(report_file, "w") as f:
            f.write(f"# Essential Files Cleanup Report\n\n")
            f.write(f"Cleanup performed on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## {self.removed_count} items removed\n\n")
            for item in sorted(self.removal_list):
                f.write(f"- `{item}`\n")
            
            f.write("\n\n## Kept Essential Files\n\n")
            for item in sorted(self.essential_files):
                f.write(f"- `{item}`\n")
                
        print(f"\nRemoved {self.removed_count} non-essential items.")
        print("\nThe library now contains only core essential files needed for distribution.")
        print(f"\nCleanup report written to {report_file}")

def main():
    """Main function to parse arguments and run the cleaner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Keep only essential files for the library.")
    parser.add_argument("--force", action="store_true", help="Skip the confirmation prompt")
    args = parser.parse_args()
    
    cleaner = EssentialFilesCleaner(force=args.force)
    cleaner.run()

if __name__ == "__main__":
    main()
