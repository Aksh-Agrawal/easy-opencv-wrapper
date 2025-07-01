"""
Test script for the new class-based object detection system
This script tests the basic functionality without requiring actual images or webcam
"""

import sys
import os

# Add the parent directory to the path so we can import easy_opencv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all new classes can be imported"""
    print("Testing imports...")
    
    try:
        from easy_opencv.object_detection import (
            ImageSource, FaceDetector, EyeDetector, CascadeDetector,
            MotionDetector, CircleDetector, LineDetector, ColorDetector,
            DNNObjectDetector
        )
        print("✓ All object detection classes imported successfully")
        
        # Test importing from main package
        from easy_opencv import (
            FaceDetector, EyeDetector, MotionDetector, 
            CircleDetector, LineDetector, ColorDetector
        )
        print("✓ Classes imported from main package successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_class_instantiation():
    """Test that classes can be instantiated with default parameters"""
    print("\nTesting class instantiation...")
    
    try:
        from easy_opencv.object_detection import (
            FaceDetector, EyeDetector, CascadeDetector,
            MotionDetector, CircleDetector, LineDetector, ColorDetector
        )
        
        # Test basic instantiation
        face_detector = FaceDetector()
        print("✓ FaceDetector created")
        
        eye_detector = EyeDetector()
        print("✓ EyeDetector created")
        
        motion_detector = MotionDetector()
        print("✓ MotionDetector created")
        
        circle_detector = CircleDetector()
        print("✓ CircleDetector created")
        
        line_detector = LineDetector()
        print("✓ LineDetector created")
        
        color_detector = ColorDetector()
        print("✓ ColorDetector created")
        
        # Test with custom parameters
        face_detector_custom = FaceDetector(scale_factor=1.2, min_neighbors=3)
        print("✓ FaceDetector with custom parameters created")
        
        color_detector_blue = ColorDetector(target_color='blue', tolerance=30)
        print("✓ ColorDetector for blue color created")
        
        return True
        
    except Exception as e:
        print(f"✗ Instantiation error: {e}")
        return False

def test_legacy_functions():
    """Test that legacy functions still work"""
    print("\nTesting legacy function compatibility...")
    
    try:
        from easy_opencv.object_detection import (
            detect_faces, detect_eyes, detect_circles, detect_lines, color_detection
        )
        print("✓ Legacy functions imported successfully")
        
        # Test that they're callable (we won't actually call them without an image)
        assert callable(detect_faces), "detect_faces is not callable"
        assert callable(detect_eyes), "detect_eyes is not callable"
        assert callable(detect_circles), "detect_circles is not callable"
        assert callable(detect_lines), "detect_lines is not callable"
        assert callable(color_detection), "color_detection is not callable"
        
        print("✓ All legacy functions are callable")
        
        return True
        
    except Exception as e:
        print(f"✗ Legacy function error: {e}")
        return False

def test_easy_cv_integration():
    """Test that new classes are available through EasyCV"""
    print("\nTesting EasyCV integration...")
    
    try:
        from easy_opencv import cv, EasyCV
        
        # Test that cv instance has the new classes
        assert hasattr(cv, 'FaceDetector'), "cv.FaceDetector not found"
        assert hasattr(cv, 'EyeDetector'), "cv.EyeDetector not found"
        assert hasattr(cv, 'MotionDetector'), "cv.MotionDetector not found"
        assert hasattr(cv, 'ColorDetector'), "cv.ColorDetector not found"
        
        print("✓ New classes available through cv instance")
        
        # Test creating a new EasyCV instance
        cv_new = EasyCV()
        face_detector = cv_new.FaceDetector()
        print("✓ Can create detectors through EasyCV instance")
        
        return True
        
    except Exception as e:
        print(f"✗ EasyCV integration error: {e}")
        return False

def test_image_source_basic():
    """Test ImageSource basic functionality (without actual sources)"""
    print("\nTesting ImageSource basic functionality...")
    
    try:
        from easy_opencv.object_detection import ImageSource
        
        # Test instantiation with different parameters
        source1 = ImageSource()  # Default (None)
        source2 = ImageSource(0)  # Webcam index
        source3 = ImageSource("test.jpg")  # Image file
        source4 = ImageSource("test.mp4")  # Video file
        
        print("✓ ImageSource can be instantiated with different parameters")
        
        # Test that source types are detected correctly
        assert source1.source is None
        assert source2.source == 0
        assert source3.source == "test.jpg"
        assert source4.source == "test.mp4"
        
        print("✓ ImageSource stores source parameters correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ ImageSource error: {e}")
        return False

def test_detector_parameters():
    """Test that detectors accept and store parameters correctly"""
    print("\nTesting detector parameters...")
    
    try:
        from easy_opencv.object_detection import (
            FaceDetector, EyeDetector, CircleDetector, 
            LineDetector, ColorDetector, MotionDetector
        )
        
        # Test FaceDetector parameters
        face_detector = FaceDetector(scale_factor=1.2, min_neighbors=3, min_size=(40, 40))
        assert face_detector.scale_factor == 1.2
        assert face_detector.min_neighbors == 3
        assert face_detector.min_size == (40, 40)
        print("✓ FaceDetector parameters stored correctly")
        
        # Test EyeDetector parameters
        eye_detector = EyeDetector(scale_factor=1.3, min_neighbors=4, min_size=(25, 25))
        assert eye_detector.scale_factor == 1.3
        assert eye_detector.min_neighbors == 4
        assert eye_detector.min_size == (25, 25)
        print("✓ EyeDetector parameters stored correctly")
        
        # Test CircleDetector parameters
        circle_detector = CircleDetector(min_radius=5, max_radius=200, sensitivity=60)
        assert circle_detector.min_radius == 5
        assert circle_detector.max_radius == 200
        assert circle_detector.sensitivity == 60
        print("✓ CircleDetector parameters stored correctly")
        
        # Test LineDetector parameters
        line_detector = LineDetector(threshold=150, min_line_length=40, max_line_gap=15)
        assert line_detector.threshold == 150
        assert line_detector.min_line_length == 40
        assert line_detector.max_line_gap == 15
        print("✓ LineDetector parameters stored correctly")
        
        # Test ColorDetector parameters
        color_detector = ColorDetector(target_color='green', tolerance=25)
        assert color_detector.target_color == 'green'
        assert color_detector.tolerance == 25
        print("✓ ColorDetector parameters stored correctly")
        
        # Test MotionDetector parameters
        motion_detector = MotionDetector(method='knn', learning_rate=0.02, sensitivity=1000)
        assert motion_detector.method == 'knn'
        assert motion_detector.learning_rate == 0.02
        assert motion_detector.sensitivity == 1000
        print("✓ MotionDetector parameters stored correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Detector parameters error: {e}")
        return False

def main():
    """Run all tests"""
    print("Easy OpenCV Object Detection Classes Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_class_instantiation,
        test_legacy_functions,
        test_easy_cv_integration,
        test_image_source_basic,
        test_detector_parameters
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The object detection classes are working correctly.")
        print("\nYou can now use the new classes like this:")
        print("```python")
        print("from easy_opencv import FaceDetector")
        print("detector = FaceDetector()")
        print("results = detector.detect_from_source()  # Uses webcam")
        print("```")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
