"""
Base test case for Easy OpenCV tests.
"""

import unittest
import numpy as np
import os
from easy_opencv import cv

class BaseTestCase(unittest.TestCase):
    """Base class for all Easy OpenCV test cases"""
    
    def setUp(self):
        """Set up test environment before each test method"""
        # Create test image folders if they don't exist
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create test images of different sizes and types
        # Grayscale image (100x100)
        self.gray_image = np.ones((100, 100), dtype=np.uint8) * 128
        
        # Color image (200x300)
        self.color_image = np.ones((200, 300, 3), dtype=np.uint8) * 128
        # Add some features to the color image
        self.color_image = cv.draw_rectangle(self.color_image, (50, 50), (150, 100), 
                                           (255, 0, 0), filled=True)
        self.color_image = cv.draw_circle(self.color_image, (200, 100), 30, 
                                        (0, 255, 0), filled=True)
        self.color_image = cv.draw_text(self.color_image, "Test", (50, 150), 
                                      font_scale=1.0, color=(255, 255, 255))
        
        # Small image with features (50x50)
        self.small_image = np.zeros((50, 50, 3), dtype=np.uint8)
        self.small_image = cv.draw_rectangle(self.small_image, (10, 10), (40, 40), 
                                           (128, 128, 128), filled=True)
        
        # Image with sharp features for edge detection
        self.edge_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.edge_image[20:80, 20:80] = 255
        
        # Image with random noise
        self.noise_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    def tearDown(self):
        """Clean up after each test method"""
        pass
    
    def save_test_image(self, image, name):
        """Save an image to the test output directory"""
        path = os.path.join(self.test_output_dir, f"{name}.jpg")
        cv.save_image(image, path)
        return path
    
    def assert_image_not_empty(self, image):
        """Assert that an image has some non-zero content"""
        self.assertTrue(np.any(image > 0), "Image should not be empty (all zeros)")
    
    def assert_image_dimensions(self, image, width, height, channels=None):
        """Assert that an image has the expected dimensions"""
        if channels:
            self.assertEqual(image.shape, (height, width, channels), 
                           f"Image dimensions don't match expected {height}x{width}x{channels}")
        else:
            self.assertEqual(image.shape[:2], (height, width), 
                           f"Image dimensions don't match expected {height}x{width}")
    
    def assert_image_value_range(self, image, min_val=0, max_val=255):
        """Assert that image values are in the expected range"""
        self.assertTrue(np.all(image >= min_val) and np.all(image <= max_val),
                       f"Image values should be in range [{min_val}, {max_val}]")
