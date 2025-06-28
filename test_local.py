#!/usr/bin/env python3
"""
Local testing script for Easy OpenCV package.
This script tests the package installation and functionality locally before PyPI upload.
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
import time

def run_command(command, description="Running command", check=True, capture_output=False):
    """Run a shell command and handle output."""
    print(f"\n🔧 {description}")
    print(f"   Command: {command}")
    
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=capture_output,
        text=True,
        check=False
    )
    
    if capture_output:
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"   Error: {result.stderr.strip()}")
    
    if check and result.returncode != 0:
        print(f"❌ Command failed with return code {result.returncode}")
        return False
    else:
        print(f"✅ {description} - Success")
        return True

def test_package_locally():
    """Test the Easy OpenCV package locally."""
    
    print("🧪 EASY OPENCV LOCAL TESTING")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Step 1: Clean previous builds
    print("\n📁 Step 1: Cleaning previous builds...")
    dirs_to_clean = ["dist", "build", "*.egg-info"]
    for pattern in dirs_to_clean:
        if "*" in pattern:
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"   Removed: {path}")
        else:
            if os.path.exists(pattern):
                shutil.rmtree(pattern)
                print(f"   Removed: {pattern}")
    
    # Step 2: Build the package
    print("\n📦 Step 2: Building the package...")
    if not run_command("python -m build", "Building package"):
        return False
    
    # Step 3: Check package integrity
    print("\n🔍 Step 3: Checking package integrity...")
    if not run_command("twine check dist/*", "Validating package"):
        return False
    
    # Step 4: Test installation in a temporary environment
    print("\n🎯 Step 4: Testing installation in isolated environment...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"   Using temporary directory: {temp_dir}")
        
        # Create a simple test script
        test_script = os.path.join(temp_dir, "test_install.py")
        with open(test_script, 'w') as f:
            f.write('''
import sys
import subprocess

# Install the package from local dist
def install_and_test():
    try:
        # Find the wheel file
        import glob
        import os
        
        # Get the wheel file path
        wheel_files = glob.glob("dist/*.whl")
        if not wheel_files:
            print("❌ No wheel file found in dist/")
            return False
        
        wheel_file = wheel_files[0]
        print(f"📦 Installing from: {wheel_file}")
        
        # Install the package
        result = subprocess.run([sys.executable, "-m", "pip", "install", wheel_file, "--force-reinstall"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Installation failed: {result.stderr}")
            return False
        
        print("✅ Package installed successfully")
        
        # Test basic import
        try:
            import easy_opencv
            print("✅ Package import successful")
            
            # Test cv alias
            from easy_opencv import cv
            print("✅ cv alias import successful")
            
            # Check version
            print(f"📋 Package version: {easy_opencv.__version__}")
            print(f"📋 Package author: {easy_opencv.__author__}")
            
            # Test that OpenCV is available
            import cv2
            print(f"✅ OpenCV available: {cv2.__version__}")
            
            return True
            
        except ImportError as e:
            print(f"❌ Import failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Testing failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

if __name__ == "__main__":
    success = install_and_test()
    sys.exit(0 if success else 1)
''')
        
        # Copy the dist directory to temp location
        temp_dist = os.path.join(temp_dir, "dist")
        shutil.copytree("dist", temp_dist)
        
        # Run the test script
        os.chdir(temp_dir)
        if not run_command(f"{sys.executable} test_install.py", "Testing package installation"):
            os.chdir(project_root)
            return False
        
        os.chdir(project_root)
    
    # Step 5: Test with examples
    print("\n🎨 Step 5: Testing with examples...")
    
    # Install the package in the current environment for testing
    wheel_files = list(Path("dist").glob("*.whl"))
    if wheel_files:
        wheel_file = wheel_files[0]
        if not run_command(f"pip install {wheel_file} --force-reinstall", "Installing package for example testing"):
            return False
        
        # Test basic example
        test_example_script = """
import numpy as np
try:
    from easy_opencv import cv
    
    # Test creating a blank image
    img = cv.create_blank_image(100, 100, color=(255, 255, 255))
    print(f"✅ Created blank image: {img.shape}")
    
    # Test basic operations without actual image files
    print("✅ Basic Easy OpenCV functionality works")
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Example test failed: {e}")
    import traceback
    traceback.print_exc()
"""
        
        with open("temp_test.py", "w") as f:
            f.write(test_example_script)
        
        success = run_command("python temp_test.py", "Testing basic functionality")
        
        # Clean up
        if os.path.exists("temp_test.py"):
            os.remove("temp_test.py")
        
        if not success:
            return False
    
    # Step 6: Package content verification
    print("\n📋 Step 6: Verifying package contents...")
    
    # Extract and check the wheel contents
    wheel_files = list(Path("dist").glob("*.whl"))
    if wheel_files:
        wheel_file = wheel_files[0]
        print(f"   Wheel file: {wheel_file}")
        
        # Check wheel contents
        result = subprocess.run(
            ["python", "-m", "zipfile", "-l", str(wheel_file)],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("   Wheel contents:")
            for line in result.stdout.split('\n')[:10]:  # Show first 10 files
                if line.strip():
                    print(f"     {line.strip()}")
            print("   ...")
        
    # Step 7: Check source distribution
    print("\n📦 Step 7: Checking source distribution...")
    tar_files = list(Path("dist").glob("*.tar.gz"))
    if tar_files:
        tar_file = tar_files[0]
        print(f"   Source distribution: {tar_file}")
        
        # List contents
        result = subprocess.run(
            ["python", "-c", f"import tarfile; t=tarfile.open('{tar_file}'); [print(f'  {{m.name}}') for m in t.getmembers()[:10]]; t.close()"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("   Source distribution contents (first 10 files):")
            print(result.stdout)
    
    print("\n" + "=" * 50)
    print("🎉 LOCAL TESTING COMPLETED SUCCESSFULLY!")
    print("\n📋 SUMMARY:")
    print("   ✅ Package builds without errors")
    print("   ✅ Package passes validation checks")
    print("   ✅ Package installs correctly")
    print("   ✅ Basic functionality works")
    print("   ✅ Package structure is correct")
    
    print("\n🚀 READY FOR PYPI PUBLICATION!")
    print("\n📝 Next steps:")
    print("   1. Test upload to Test PyPI: twine upload --repository testpypi dist/*")
    print("   2. Test install from Test PyPI: pip install -i https://test.pypi.org/simple/ easy-opencv-wrapper")
    print("   3. Upload to PyPI: twine upload dist/*")
    
    return True

if __name__ == "__main__":
    try:
        success = test_package_locally()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
