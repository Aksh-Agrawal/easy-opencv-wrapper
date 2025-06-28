#!/usr/bin/env python3
"""
Final verification script before PyPI publication.
"""

import os
import subprocess
import sys
from pathlib import Path

def verify_package_ready():
    """Verify the package is ready for PyPI publication."""
    
    print("🔍 FINAL PYPI READINESS CHECK")
    print("=" * 50)
    
    # Check 1: Package files exist
    print("\n1. Checking package files...")
    dist_dir = Path("dist")
    wheel_files = list(dist_dir.glob("*.whl"))
    tar_files = list(dist_dir.glob("*.tar.gz"))
    
    if wheel_files and tar_files:
        print(f"✅ Wheel file: {wheel_files[0]} ({wheel_files[0].stat().st_size} bytes)")
        print(f"✅ Source dist: {tar_files[0]} ({tar_files[0].stat().st_size} bytes)")
    else:
        print("❌ Missing package files!")
        return False
    
    # Check 2: Package validation
    print("\n2. Validating packages...")
    result = subprocess.run(["twine", "check", "dist/*"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Package validation passed")
    else:
        print("❌ Package validation failed")
        print(result.stderr)
        return False
    
    # Check 3: Import test
    print("\n3. Testing package import...")
    try:
        import easy_opencv
        from easy_opencv import cv
        print(f"✅ Package imported successfully (v{easy_opencv.__version__})")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Check 4: Quick functionality test
    print("\n4. Testing basic functionality...")
    try:
        import numpy as np
        test_img = np.ones((50, 50, 3), dtype=np.uint8) * 255
        resized = cv.resize_image(test_img, width=25, height=25)
        blurred = cv.apply_gaussian_blur(test_img, kernel_size=5)
        print("✅ Basic functions work correctly")
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False
    
    # Check 5: Essential files
    print("\n5. Checking essential files...")
    essential_files = [
        "README.md", "LICENSE", "CHANGELOG.md", 
        "pyproject.toml", "setup.py", "requirements.txt"
    ]
    
    for file in essential_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ Missing {file}")
            return False
    
    # Check 6: Documentation
    print("\n6. Checking documentation...")
    doc_files = [
        "DOCUMENTATION.md", "USAGE_GUIDE.md", "DIFFERENCES.md", 
        "EASY_OPENCV_BENEFITS.md", "WHY_EASY_OPENCV.md"
    ]
    
    for file in doc_files:
        if Path(file).exists():
            print(f"✅ {file}")
    
    print("\n" + "=" * 50)
    print("🎉 PACKAGE IS READY FOR PYPI PUBLICATION!")
    print("\n📦 Package Summary:")
    print(f"   Name: easy-opencv-wrapper")
    print(f"   Version: {easy_opencv.__version__}")
    print(f"   Author: {easy_opencv.__author__}")
    print(f"   Wheel size: {wheel_files[0].stat().st_size:,} bytes")
    print(f"   Source size: {tar_files[0].stat().st_size:,} bytes")
    
    print("\n🚀 Next Steps for Publication:")
    print("   1. Test PyPI upload:")
    print("      twine upload --repository testpypi dist/*")
    print("   2. Test installation from Test PyPI:")
    print("      pip install -i https://test.pypi.org/simple/ easy-opencv-wrapper")
    print("   3. Production PyPI upload:")
    print("      twine upload dist/*")
    print("   4. Test final installation:")
    print("      pip install easy-opencv-wrapper")
    
    return True

if __name__ == "__main__":
    try:
        success = verify_package_ready()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        sys.exit(1)
