#!/usr/bin/env python3
"""
Comprehensive cleanup script for Easy OpenCV library
This script removes unnecessary files and prepares the library for distribution
"""

import os
import shutil
import glob
import argparse
from pathlib import Path
import sys
import time

# Define the root directory
ROOT_DIR = Path(__file__).resolve().parent

class LibraryCleaner:
    def __init__(self, mode="standard", dry_run=False):
        """Initialize the cleaner with the specified mode"""
        self.mode = mode
        self.dry_run = dry_run
        self.removed_count = 0
        self.removal_list = []
        
        # Files and directories to remove in standard mode
        self.standard_files = [
            # Build artifacts
            "build/",
            "dist/",
            "*.egg-info/",
            "**/__pycache__/",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            
            # Development files
            "build_publish.py",
            "cleanup_for_pypi.py",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            ".venv/",
            "venv/",
            ".env/",
            "env/",
            
            # System files
            "**/.DS_Store",
            "**/Thumbs.db",
            "**/.directory",
        ]
        
        # Additional files to remove in deep mode
        self.deep_files = [
            # More build artifacts
            ".tox/",
            "**/.hypothesis/",
            "**/.mypy_cache/",
            
            # Internal documentation not needed for distribution
            "CLEANUP_SUMMARY.md",
            "PYPI_PUBLISHING_GUIDE.md",
            "LOCAL_TEST_RESULTS.md", 
            "DIFFERENCES.md",
            "error_module.md",
            "No_Module_Error.md",
            
            # Test files that aren't part of the main test suite
            "test_local.py",
            "test_simple.py",
            
            # Temporary files
            "m.py",  # Temporary test file
            "temp/",
            "**/~*",
        ]
        
        # Define files to preserve (never delete)
        self.preserve = [
            "README.md",
            "LICENSE",
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            "MANIFEST.in",
            "easy_opencv/",
            "tests/",  # Keep main tests
            "examples/",  # Keep examples
            ".git/",  # Preserve git history
            ".gitignore",
            "ssd_mobilenet_v2_coco_2018_03_29/",  # Model files
        ]

    def should_remove(self, path):
        """Check if a path should be removed"""
        rel_path = os.path.relpath(path, ROOT_DIR)
        
        # Never remove preserved files/directories
        for preserved in self.preserve:
            preserved_path = os.path.join(ROOT_DIR, preserved)
            if preserved.endswith('/'):
                if path.startswith(preserved_path):
                    return False
            elif path == preserved_path:
                return False
                
        # Skip the script itself
        if os.path.samefile(path, __file__):
            return False
            
        return True

    def remove_path(self, path):
        """Remove a file or directory"""
        if not self.should_remove(path):
            return False
            
        rel_path = os.path.relpath(path, ROOT_DIR)
        
        if self.dry_run:
            print(f"Would remove: {rel_path}")
            self.removal_list.append(rel_path)
            self.removed_count += 1
            return True
            
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

    def process_patterns(self, patterns):
        """Process a list of file patterns to remove"""
        for pattern in patterns:
            # Handle absolute paths
            if os.path.isabs(pattern):
                if os.path.exists(pattern):
                    self.remove_path(pattern)
                continue
                
            # Handle patterns
            full_pattern = os.path.join(ROOT_DIR, pattern)
            for path in glob.glob(full_pattern, recursive=True):
                self.remove_path(path)

    def run(self):
        """Run the cleanup process"""
        print(f"\n===== Easy OpenCV Library Cleanup ({self.mode}) =====\n")
        
        # Display mode information
        if self.mode == "standard":
            print("Standard cleanup: Removing build artifacts and cache files.")
        elif self.mode == "deep":
            print("Deep cleanup: Removing build artifacts, cache files, and non-essential documentation.")
        
        if self.dry_run:
            print("DRY RUN: No files will actually be deleted.\n")
        
        # Process standard files
        self.process_patterns(self.standard_files)
        
        # Process deep files if in deep mode
        if self.mode == "deep":
            self.process_patterns(self.deep_files)
        
        # Generate report
        if not self.dry_run:
            report_file = os.path.join(ROOT_DIR, "CLEANUP_REPORT.md")
            with open(report_file, "w") as f:
                f.write(f"# Library Cleanup Report ({self.mode.title()} Mode)\n\n")
                f.write(f"Cleanup performed on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## {self.removed_count} items removed:\n\n")
                for item in self.removal_list:
                    f.write(f"- `{item}`\n")
            print(f"\nCleanup report written to {report_file}")
        
        # Summary
        action = "Would remove" if self.dry_run else "Removed"
        print(f"\n{action} {self.removed_count} items.")
        print("\nThe library is now clean and ready for distribution.")

def main():
    """Main function to parse arguments and run the cleaner"""
    parser = argparse.ArgumentParser(description="Clean up unnecessary files from the Easy OpenCV library.")
    parser.add_argument("--mode", choices=["standard", "deep"], default="standard",
                      help="Cleanup mode: 'standard' removes build artifacts, 'deep' also removes non-essential docs")
    parser.add_argument("--dry-run", action="store_true", 
                      help="Show what would be deleted without actually deleting anything")
    parser.add_argument("--force", action="store_true",
                      help="Skip the confirmation prompt")
    args = parser.parse_args()
    
    cleaner = LibraryCleaner(mode=args.mode, dry_run=args.dry_run)
    
    if not args.force and not args.dry_run:
        # Ask for confirmation
        mode_msg = "standard" if args.mode == "standard" else "deep (more aggressive)"
        confirmation = input(f"This will perform a {mode_msg} cleanup of the library. Continue? (y/n): ")
        if confirmation.lower() not in ['y', 'yes']:
            print("Cleanup cancelled.")
            sys.exit(0)
    
    # Run the cleaner
    cleaner.run()

if __name__ == "__main__":
    main()
