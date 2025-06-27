"""
Debug script to examine the actual function signatures and behavior 
of the Easy OpenCV package to understand what's causing test failures.
"""

import inspect
import numpy as np
from easy_opencv import cv

def print_function_signature(func):
    """Print the signature of a function"""
    try:
        sig = inspect.signature(func)
        print(f"Function: {func.__name__}")
        print(f"Signature: {sig}")
        print(f"Parameters: {sig.parameters}")
        print("-" * 70)
    except Exception as e:
        print(f"Error examining {func.__name__}: {e}")
        print("-" * 70)

def test_function_behavior(func_name, func, test_case):
    """Test a function with various arguments to see what works"""
    print(f"\nTesting {func_name}:")
    
    for test_name, args, kwargs in test_case:
        try:
            print(f"  Test: {test_name}")
            result = func(*args, **kwargs)
            if isinstance(result, np.ndarray):
                print(f"  Result shape: {result.shape}, dtype: {result.dtype}")
            else:
                print(f"  Result: {result}")
        except Exception as e:
            print(f"  Error: {e}")
    print("-" * 70)

# Create a test image
test_img = np.ones((200, 300, 3), dtype=np.uint8) * 128

print("=" * 70)
print("DEBUGGING EASY OPENCV FUNCTION INTERFACES")
print("=" * 70)

# Image operations
print("\n=== IMAGE OPERATIONS ===")
print_function_signature(cv.load_image)
print_function_signature(cv.save_image)
print_function_signature(cv.resize_image)
print_function_signature(cv.crop_image)
print_function_signature(cv.convert_color_space)

# Test resize_image behavior
resize_tests = [
    ("Width only", [test_img], {"width": 150}),
    ("Height only", [test_img], {"height": 100}),
    ("Scale only", [test_img], {"scale": 0.5}),
    ("Width and height tuple", [test_img, (150, 100)], {}),
    ("Width and height separate", [test_img], {"width": 150, "height": 100}),
]
test_function_behavior("resize_image", cv.resize_image, resize_tests)

# Test crop_image behavior
crop_tests = [
    ("4 separate args", [test_img, 50, 50, 100, 100], {}),
    ("Rect tuple", [test_img, (50, 50, 100, 100)], {}),
    ("Named args", [test_img], {"x": 50, "y": 50, "width": 100, "height": 100}),
    ("Center crop", [test_img], {"width": 100, "height": 100, "center": True}),
]
test_function_behavior("crop_image", cv.crop_image, crop_tests)

# Transformations
print("\n=== TRANSFORMATIONS ===")
print_function_signature(cv.rotate_image)
print_function_signature(cv.flip_image)
print_function_signature(cv.translate_image)
print_function_signature(cv.resize_with_aspect_ratio)

# Test rotate_image behavior
rotate_tests = [
    ("Basic rotation", [test_img, 45], {}),
    ("Custom center", [test_img, 45], {"center": (100, 100)}),
    ("With scale", [test_img, 45], {"scale": 0.5}),
    ("With keep_size", [test_img, 45], {"keep_size": True}),
    ("With border mode", [test_img, 45], {"border_mode": "reflect"}),
]
test_function_behavior("rotate_image", cv.rotate_image, rotate_tests)

# Test translate_image behavior
translate_tests = [
    ("Basic x,y", [test_img, 50, 30], {}),
    ("Named tx,ty", [test_img], {"tx": 50, "ty": 30}),
    ("Named x_shift,y_shift", [test_img], {"x_shift": 50, "y_shift": 30}),
]
test_function_behavior("translate_image", cv.translate_image, translate_tests)

# Drawing Operations
print("\n=== DRAWING OPERATIONS ===")
print_function_signature(cv.draw_rectangle)
print_function_signature(cv.draw_circle)
print_function_signature(cv.draw_line)
print_function_signature(cv.draw_text)
print_function_signature(cv.draw_contour)
print_function_signature(cv.draw_arrow)
print_function_signature(cv.draw_grid)

# Filters
print("\n=== FILTERS ===")
print_function_signature(cv.apply_gaussian_blur)
print_function_signature(cv.apply_median_blur)
print_function_signature(cv.apply_bilateral_filter)
print_function_signature(cv.apply_emboss_filter)
print_function_signature(cv.apply_unsharp_mask)

# Utilities
print("\n=== UTILITIES ===")
print_function_signature(cv.color_picker)
print_function_signature(cv.create_image_grid)
print_function_signature(cv.apply_watermark)
print_function_signature(cv.convert_to_sketch)
print_function_signature(cv.image_comparison)
print_function_signature(cv.fps_counter)

# Feature Detection
print("\n=== FEATURE DETECTION ===")
print_function_signature(cv.detect_contours)
print_function_signature(cv.detect_corners)
print_function_signature(cv.detect_keypoints)

print("\nDebug completed.")
