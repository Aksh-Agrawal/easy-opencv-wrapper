"""
Basic test to verify the core functionality works as expected.
This test focuses only on the actual implemented parameters and features,
rather than expected or ideal interfaces.
"""

import unittest
import numpy as np
import os
import tempfile
import cv2
from easy_opencv import cv
from tests.base_test_case import BaseTestCase


class TestCoreFunction(BaseTestCase):
    """Test only the core functionality that should work without errors"""
    
    def setUp(self):
        super().setUp()
        # Create a temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        # Clean up temp files that are not directories
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)
        super().tearDown()
    
    def test_image_operations_basic(self):
        """Test basic image operations with actually supported parameters"""
        # Test resize
        resized = cv.resize_image(self.color_image, width=150)
        self.assertEqual(resized.shape[1], 150)
        
        # Test crop - using the actual interface
        cropped = cv.crop_image(self.color_image, 50, 50, 100, 100)
        self.assertEqual(cropped.shape[:2], (100, 100))
        
        # Test color conversion with the actual interface
        gray = cv.convert_color_space(self.color_image, 'bgr', 'gray')
        self.assertEqual(len(gray.shape), 2)
    
    def test_drawing_operations_basic(self):
        """Test basic drawing operations with actually supported parameters"""
        # Create a canvas
        canvas = np.zeros((200, 200, 3), dtype=np.uint8)
        
        # Test rectangle
        with_rect = cv.draw_rectangle(canvas.copy(), (10, 10), (50, 50), (255, 255, 255))
        self.assertTrue(np.any(with_rect > 0))
        
        # Test circle
        with_circle = cv.draw_circle(canvas.copy(), (100, 100), 30, (0, 255, 0))
        self.assertTrue(np.any(with_circle > 0))
        
        # Test text
        with_text = cv.draw_text(canvas.copy(), "Test", (10, 100), color=(255, 0, 0))
        self.assertTrue(np.any(with_text > 0))
    
    def test_filters_basic(self):
        """Test basic filters with actually supported parameters"""
        # Test Gaussian blur
        blurred = cv.apply_gaussian_blur(self.color_image, kernel_size=5)
        self.assertEqual(blurred.shape, self.color_image.shape)
        
        # Test median blur
        median = cv.apply_median_blur(self.color_image, kernel_size=5)
        self.assertEqual(median.shape, self.color_image.shape)
        
        # Test bilateral filter with actually supported params
        bilateral = cv.apply_bilateral_filter(self.color_image, diameter=9)
        self.assertEqual(bilateral.shape, self.color_image.shape)
    
    def test_transformations_basic(self):
        """Test basic transformations with actually supported parameters"""
        # Test rotation with params that actually work
        rotated = cv.rotate_image(self.color_image, angle=45)
        self.assertEqual(rotated.shape, self.color_image.shape)
        
        # Test with custom center
        rotated_center = cv.rotate_image(self.color_image, angle=45, center=(100, 100))
        self.assertEqual(rotated_center.shape, self.color_image.shape)
        
        # Test with border mode
        rotated_reflect = cv.rotate_image(self.color_image, angle=45, border_mode='reflect')
        self.assertEqual(rotated_reflect.shape, self.color_image.shape)
        
        # Test flip with the actual interface
        flipped = cv.flip_image(self.color_image, direction='horizontal')
        self.assertEqual(flipped.shape, self.color_image.shape)
        
        vertical_flip = cv.flip_image(self.color_image, direction='vertical')
        self.assertEqual(vertical_flip.shape, self.color_image.shape)
        
        both_flip = cv.flip_image(self.color_image, direction='both')
        self.assertEqual(both_flip.shape, self.color_image.shape)
        
        # Test translate with the actual interface
        translated = cv.translate_image(self.color_image, tx=50, ty=30)
        self.assertEqual(translated.shape, self.color_image.shape)
        
        # Test resize with aspect ratio
        resized = cv.resize_with_aspect_ratio(self.color_image, target_size=(150, 150))
        self.assertLessEqual(resized.shape[0], 150)
        self.assertLessEqual(resized.shape[1], 150)
    
    def test_load_save_basic(self):
        """Test basic file operations"""
        test_path = os.path.join(self.temp_dir, "test_img.jpg")
        
        # Save an image
        cv.save_image(self.color_image, test_path)
        self.assertTrue(os.path.exists(test_path))
        
        # Load the image
        loaded = cv.load_image(test_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.shape[:2], self.color_image.shape[:2])


if __name__ == "__main__":
    unittest.main()
