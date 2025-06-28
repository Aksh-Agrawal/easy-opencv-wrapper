#!/usr/bin/env python3
"""
Test the installed Easy OpenCV package functionality.
"""

import sys

def test_functionality():
    """Test the Easy OpenCV package functionality."""
    
    print("TESTING EASY OPENCV FUNCTIONALITY")
    print("=" * 40)
    
    try:
        # Test basic import
        print("\n1. Testing imports...")
        import easy_opencv
        print("✅ easy_opencv import successful")
        
        from easy_opencv import cv
        print("✅ cv alias import successful")
        
        # Test package metadata
        print(f"✅ Package version: {easy_opencv.__version__}")
        print(f"✅ Package author: {easy_opencv.__author__}")
        
        # Test OpenCV availability
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        # Test basic functionality
        print("\n2. Testing basic functionality...")
        import numpy as np
        
        # Test creating blank image using numpy
        import numpy as np
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255  # White image
        print(f"✅ Created blank image shape: {img.shape}")
        print(f"✅ Image dtype: {img.dtype}")
        
        # Test image operations without files
        print("\n3. Testing image operations...")
        
        # Test resize
        resized = cv.resize_image(img, width=50, height=50)
        print(f"✅ Resized image shape: {resized.shape}")
        
        # Test blur
        blurred = cv.apply_gaussian_blur(img, kernel_size=5)
        print(f"✅ Blurred image shape: {blurred.shape}")
        
        # Test drawing operations
        print("\n4. Testing drawing operations...")
        
        # Draw rectangle
        img_with_rect = cv.draw_rectangle(img, (10, 10), (90, 90), color=(255, 0, 0), thickness=2)
        print(f"✅ Drew rectangle on image")
        
        # Draw circle
        img_with_circle = cv.draw_circle(img, (50, 50), 20, color=(0, 255, 0), filled=True)
        print(f"✅ Drew circle on image")
        
        # Draw text
        img_with_text = cv.draw_text(img, "Test", (10, 30), color=(0, 0, 255))
        print(f"✅ Drew text on image")
        
        # Test color space conversion
        print("\n5. Testing color space conversion...")
        gray = cv.convert_color_space(img, 'bgr', 'gray')
        print(f"✅ Converted to grayscale shape: {gray.shape}")
        
        # Test thresholding
        binary = cv.apply_threshold(gray, threshold_value=127)
        print(f"✅ Applied threshold shape: {binary.shape}")
        
        print("\n" + "=" * 40)
        print("🎉 ALL FUNCTIONALITY TESTS PASSED!")
        print("✅ Package is working correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_functionality()
    sys.exit(0 if success else 1)
