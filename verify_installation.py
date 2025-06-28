#!/usr/bin/env python3
"""
Easy OpenCV Installation Verification Script

Run this script to verify that Easy OpenCV is installed and working correctly.
"""

def main():
    print("🔍 Easy OpenCV Installation Verification")
    print("=" * 50)
    
    # Test 1: Import test
    print("\n1️⃣ Testing package import...")
    try:
        from easy_opencv import cv
        print("   ✅ Successfully imported easy_opencv")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print("   💡 Solution: Run 'pip install easy-opencv-wrapper'")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False
    
    # Test 2: Version check
    print("\n2️⃣ Checking package version...")
    try:
        if hasattr(cv, '__version__'):
            print(f"   📦 Easy OpenCV version: {cv.__version__}")
        else:
            print("   📦 Easy OpenCV is available (version info not accessible)")
    except Exception as e:
        print(f"   ⚠️ Cannot access version info: {e}")
    
    # Test 3: Dependencies check
    print("\n3️⃣ Testing dependencies...")
    try:
        import cv2
        print(f"   ✅ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("   ❌ OpenCV not found")
        print("   💡 Solution: Run 'pip install opencv-python'")
        return False
    
    try:
        import numpy as np
        print(f"   ✅ NumPy version: {np.__version__}")
    except ImportError:
        print("   ❌ NumPy not found")
        return False
    
    try:
        import PIL
        print(f"   ✅ Pillow version: {PIL.__version__}")
    except ImportError:
        print("   ❌ Pillow not found")
        return False
    
    # Test 4: Basic functionality
    print("\n4️⃣ Testing basic functionality...")
    try:
        import numpy as np
        
        # Create a test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = [255, 0, 0]  # Red square
        
        # Test resize function
        resized = cv.resize_image(test_image, width=50, height=50)
        print("   ✅ Image resize operation successful")
        
        # Test blur function
        blurred = cv.apply_gaussian_blur(test_image, kernel_size=15)
        print("   ✅ Gaussian blur operation successful")
        
        # Test edge detection
        edges = cv.apply_edge_detection(test_image, low_threshold=50, high_threshold=150)
        print("   ✅ Edge detection operation successful")
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False
    
    # Test 5: Module availability
    print("\n5️⃣ Checking available modules...")
    modules_to_check = [
        'image_operations',
        'filters', 
        'transformations',
        'drawing_operations',
        'feature_detection',
        'object_detection',
        'video_operations',
        'utils'
    ]
    
    available_modules = []
    for module_name in modules_to_check:
        try:
            module = getattr(cv, module_name, None)
            if module is not None:
                available_modules.append(module_name)
                print(f"   ✅ {module_name}")
            else:
                # Try importing directly
                exec(f"from easy_opencv import {module_name}")
                available_modules.append(module_name)
                print(f"   ✅ {module_name}")
        except Exception:
            print(f"   ⚠️ {module_name} (not accessible)")
    
    print(f"\n   📊 Available modules: {len(available_modules)}/{len(modules_to_check)}")
    
    # Final result
    print("\n" + "=" * 50)
    print("🎉 INSTALLATION VERIFICATION COMPLETE!")
    print("✅ Easy OpenCV is installed and working correctly!")
    print("\n📚 Next steps:")
    print("   • Check out README.md for usage examples")
    print("   • Try the examples in examples/ directory")
    print("   • Read USAGE_GUIDE.md for detailed documentation")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n💡 For help, see INSTALLATION_GUIDE.md")
            exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during verification: {e}")
        print("💡 For help, see INSTALLATION_GUIDE.md")
        exit(1)
