#!/usr/bin/env python3
"""
Quick verification script to test Easy OpenCV import and basic functionality.
Run this after installing the package to verify everything works correctly.
"""

def test_import():
    """Test importing Easy OpenCV."""
    print("🔍 Testing Easy OpenCV import...")
    
    try:
        # Test the correct import
        from easy_opencv import cv
        print("✅ Successfully imported: from easy_opencv import cv")
        return cv
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Solution: Run 'pip install easy-opencv-wrapper'")
        return None

def test_wrong_import():
    """Demonstrate the wrong import that causes errors."""
    print("\n🚫 Testing wrong import (this should fail)...")
    
    try:
        import easy_opencv_wrapper
        print("❌ This shouldn't work!")
    except ImportError:
        print("✅ Correctly failed: import easy_opencv_wrapper")
        print("💡 This confirms you need to use 'from easy_opencv import cv'")

def test_basic_functionality(cv):
    """Test basic functionality."""
    if cv is None:
        return False
        
    print("\n🧪 Testing basic functionality...")
    
    try:
        import numpy as np
        
        # Create a test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = [255, 0, 0]  # Red square
        
        # Test basic operations
        resized = cv.resize_image(test_image, width=50, height=50)
        blurred = cv.apply_gaussian_blur(test_image, kernel_size=5)
        
        print("✅ Basic image operations working!")
        print(f"   Original shape: {test_image.shape}")
        print(f"   Resized shape: {resized.shape}")
        print(f"   Blurred shape: {blurred.shape}")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main verification function."""
    print("🚀 Easy OpenCV Import Verification")
    print("=" * 40)
    
    # Test correct import
    cv = test_import()
    
    # Test wrong import
    test_wrong_import()
    
    # Test functionality
    success = test_basic_functionality(cv)
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Easy OpenCV is working correctly!")
        print("📚 Next steps:")
        print("   - Check examples/basic_examples.py")
        print("   - Read USAGE_GUIDE.md")
        print("   - Explore DOCUMENTATION.md")
    else:
        print("❌ Easy OpenCV verification failed!")
        print("📚 Troubleshooting:")
        print("   - Check INSTALLATION_GUIDE.md")
        print("   - Ensure you ran: pip install easy-opencv-wrapper")
        print("   - Try creating a virtual environment")

if __name__ == "__main__":
    main()
