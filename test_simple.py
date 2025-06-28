#!/usr/bin/env python3
"""
Simple local testing script for Easy OpenCV package.
This script tests the package installation and functionality locally.
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path

def run_command(command, description="Running command"):
    """Run a shell command and handle output."""
    print(f"\n{description}")
    print(f"Command: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("SUCCESS")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()[:200]}...")  # Truncate long output
        return True
    else:
        print("FAILED")
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
        return False

def test_package():
    """Test the Easy OpenCV package."""
    
    print("EASY OPENCV LOCAL TESTING")
    print("=" * 40)
    
    # Step 1: Clean and build
    print("\nStep 1: Building package...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("easy_opencv_wrapper.egg-info"):
        shutil.rmtree("easy_opencv_wrapper.egg-info")
    
    if not run_command("python -m build", "Building package"):
        return False
    
    # Step 2: Check package
    print("\nStep 2: Validating package...")
    if not run_command("twine check dist/*", "Checking package integrity"):
        return False
    
    # Step 3: Install and test
    print("\nStep 3: Testing installation...")
    
    # Find wheel file
    wheel_files = list(Path("dist").glob("*.whl"))
    if not wheel_files:
        print("ERROR: No wheel file found")
        return False
    
    wheel_file = wheel_files[0]
    print(f"Installing: {wheel_file}")
    
    # Install package
    if not run_command(f"pip install {wheel_file} --force-reinstall", "Installing package"):
        return False
    
    # Step 4: Test basic functionality
    print("\nStep 4: Testing functionality...")
    
    test_script = '''
import sys
try:
    # Test imports
    import easy_opencv
    print("easy_opencv import: OK")
    
    from easy_opencv import cv
    print("cv alias import: OK")
    
    # Test version info
    print(f"Version: {easy_opencv.__version__}")
    print(f"Author: {easy_opencv.__author__}")
    
    # Test basic functionality
    import numpy as np
    img = cv.create_blank_image(100, 100, color=(255, 255, 255))
    print(f"Created image shape: {img.shape}")
    
    # Test OpenCV availability
    import cv2
    print(f"OpenCV version: {cv2.__version__}")
    
    print("ALL TESTS PASSED")
    
except Exception as e:
    print(f"TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    # Write test script
    with open("temp_test.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    # Run test
    success = run_command("python temp_test.py", "Testing basic functionality")
    
    # Clean up
    if os.path.exists("temp_test.py"):
        os.remove("temp_test.py")
    
    if success:
        print("\n" + "=" * 40)
        print("LOCAL TESTING COMPLETED SUCCESSFULLY!")
        print("\nPackage is ready for PyPI publication!")
        print("\nNext steps:")
        print("1. Upload to Test PyPI: twine upload --repository testpypi dist/*")
        print("2. Test from Test PyPI: pip install -i https://test.pypi.org/simple/ easy-opencv-wrapper")
        print("3. Upload to PyPI: twine upload dist/*")
    
    return success

if __name__ == "__main__":
    try:
        success = test_package()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Testing failed: {e}")
        sys.exit(1)
