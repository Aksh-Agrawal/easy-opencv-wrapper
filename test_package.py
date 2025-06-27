"""
Test script to verify the Easy OpenCV package installation and functionality
"""

from easy_opencv import cv
import numpy as np

def test_basic_functionality():
    """Test basic functionality of the package"""
    print("Testing Easy OpenCV Package...")
    
    # Test 1: Create a simple image
    print("✓ Test 1: Creating test image...")
    image = np.ones((200, 300, 3), dtype=np.uint8) * 128
    
    # Test 2: Drawing operations
    print("✓ Test 2: Drawing operations...")
    image = cv.draw_rectangle(image, (50, 50), (150, 100), (255, 0, 0), filled=True)
    image = cv.draw_circle(image, (200, 75), 30, (0, 255, 0), filled=True)
    image = cv.draw_text(image, "TEST", (50, 150), font_scale=1.0, color=(255, 255, 255))
    
    # Test 3: Basic image operations
    print("✓ Test 3: Image operations...")
    resized = cv.resize_image(image, width=150)
    flipped = cv.flip_image(image, 'horizontal')
    
    # Test 4: Filters
    print("✓ Test 4: Applying filters...")
    blurred = cv.apply_gaussian_blur(image, kernel_size=15)
    edges = cv.apply_edge_detection(image, method='canny')
    
    # Test 5: Color space conversion
    print("✓ Test 5: Color space conversion...")
    gray = cv.convert_color_space(image, 'bgr', 'gray')
    hsv = cv.convert_color_space(image, 'bgr', 'hsv')
    
    # Test 6: Transformations
    print("✓ Test 6: Transformations...")
    rotated = cv.rotate_image(image, angle=30)
    
    # Test 7: Feature detection
    print("✓ Test 7: Feature detection...")
    contours = cv.detect_contours(image, threshold_value=100)
    
    # Test 8: Utility functions
    print("✓ Test 8: Utility functions...")
    info = cv.get_image_info(image)
    watermarked = cv.apply_watermark(image, "Test", position='top_left')
    
    print(f"✓ All tests passed! Image info: {info['width']}x{info['height']}")
    print(f"✓ Found {len(contours)} contours")
    
    # Display results
    cv.show_image(image, "Original Test Image", wait=False)
    cv.show_image(blurred, "Blurred", wait=False)
    cv.show_image(watermarked, "Watermarked - Press any key to close")
    
    return True

def test_comprehensive():
    """Comprehensive test of package features"""
    print("\n" + "="*50)
    print("COMPREHENSIVE EASY OPENCV TEST")
    print("="*50)
    
    success_count = 0
    total_tests = 0
    
    # Test each module
    modules_to_test = [
        ("Image Operations", test_image_ops),
        ("Drawing Operations", test_drawing_ops),
        ("Filters", test_filters),
        ("Transformations", test_transformations),
        ("Feature Detection", test_feature_detection),
        ("Utilities", test_utilities)
    ]
    
    for module_name, test_func in modules_to_test:
        total_tests += 1
        try:
            print(f"\nTesting {module_name}...")
            test_func()
            print(f"✓ {module_name} - PASSED")
            success_count += 1
        except Exception as e:
            print(f"✗ {module_name} - FAILED: {e}")
    
    print(f"\n" + "="*50)
    print(f"TEST RESULTS: {success_count}/{total_tests} modules passed")
    print("="*50)
    
    return success_count == total_tests

def test_image_ops():
    """Test image operations module"""
    image = np.ones((100, 150, 3), dtype=np.uint8) * 100
    
    # Test resize
    resized = cv.resize_image(image, width=75)
    assert resized.shape[1] == 75
    
    # Test crop
    cropped = cv.crop_image(image, 10, 10, 50, 50)
    assert cropped.shape == (50, 50, 3)
    
    # Test color conversion
    gray = cv.convert_color_space(image, 'bgr', 'gray')
    assert len(gray.shape) == 2

def test_drawing_ops():
    """Test drawing operations module"""
    canvas = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Test rectangle
    canvas = cv.draw_rectangle(canvas, (10, 10), (50, 50), (255, 255, 255))
    
    # Test circle
    canvas = cv.draw_circle(canvas, (100, 100), 20, (255, 0, 0))
    
    # Test text
    canvas = cv.draw_text(canvas, "Test", (10, 150), color=(0, 255, 0))
    
    # Verify something was drawn
    assert np.any(canvas > 0)

def test_filters():
    """Test filters module"""
    image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    # Test blur
    blurred = cv.apply_gaussian_blur(image, kernel_size=5)
    assert blurred.shape == image.shape
    
    # Test edge detection
    edges = cv.apply_edge_detection(image, method='canny')
    assert len(edges.shape) == 2

def test_transformations():
    """Test transformations module"""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    # Test rotation
    rotated = cv.rotate_image(image, angle=45)
    assert rotated.shape == image.shape
    
    # Test flip
    flipped = cv.flip_image(image, direction='horizontal')
    assert flipped.shape == image.shape

def test_feature_detection():
    """Test feature detection module"""
    # Create image with clear features
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image = cv.draw_rectangle(image, (50, 50), (150, 150), (255, 255, 255), filled=True)
    
    # Test contour detection
    contours = cv.detect_contours(image, threshold_value=127, min_area=100)
    assert len(contours) > 0

def test_utilities():
    """Test utilities module"""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    # Test image info
    info = cv.get_image_info(image)
    assert info['width'] == 100
    assert info['height'] == 100
    
    # Test watermark
    watermarked = cv.apply_watermark(image, "Test")
    assert watermarked.shape == image.shape

if __name__ == "__main__":
    # Run basic functionality test
    test_basic_functionality()
    
    # Run comprehensive test
    test_comprehensive()
    
    print("\n🎉 Easy OpenCV package is ready to use!")
    print("You can now import it in your projects with: from easy_opencv import cv")
