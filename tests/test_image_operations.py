"""
Tests for image operations module.
"""

import unittest
import os
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestImageOperations(BaseTestCase):
    """Test cases for image operations functions"""
    
    def test_load_image(self):
        """Test loading images with different modes"""
        # Save a test image first
        test_image_path = self.save_test_image(self.color_image, "test_load")
        
        # Test color mode (default)
        image = cv.load_image(test_image_path)
        self.assertEqual(len(image.shape), 3, "Color image should have 3 dimensions")
        
        # Test grayscale mode
        gray = cv.load_image(test_image_path, mode='gray')
        self.assertEqual(len(gray.shape), 2, "Grayscale image should have 2 dimensions")
        
        # Test unchanged mode
        unchanged = cv.load_image(test_image_path, mode='unchanged')
        self.assertIsNotNone(unchanged, "Image should load in unchanged mode")
    
    def test_save_image(self):
        """Test saving images with different qualities"""
        # Test saving JPEG with default quality
        jpg_path = os.path.join(self.test_output_dir, "test_save.jpg")
        result = cv.save_image(self.color_image, jpg_path)
        self.assertTrue(result, "Image save should return True")
        self.assertTrue(os.path.exists(jpg_path), "Saved image file should exist")
        
        # Test saving JPEG with high quality
        jpg_high_path = os.path.join(self.test_output_dir, "test_save_high.jpg")
        cv.save_image(self.color_image, jpg_high_path, quality=100)
        self.assertTrue(os.path.exists(jpg_high_path), "High quality image file should exist")
        
        # Test saving PNG (quality parameter should be ignored)
        png_path = os.path.join(self.test_output_dir, "test_save.png")
        cv.save_image(self.color_image, png_path)
        self.assertTrue(os.path.exists(png_path), "PNG image file should exist")
    
    def test_resize_image(self):
        """Test resizing images with different parameters"""
        # Test resize with specified width
        width_resized = cv.resize_image(self.color_image, width=150)
        self.assertEqual(width_resized.shape[1], 150, "Width should be 150")
        
        # Test resize with specified height
        height_resized = cv.resize_image(self.color_image, height=100)
        self.assertEqual(height_resized.shape[0], 100, "Height should be 100")
        
        # Test resize with both width and height
        both_resized = cv.resize_image(self.color_image, width=150, height=100)
        self.assertEqual(both_resized.shape[:2], (100, 150), "Dimensions should be 100x150")
        
        # Test resize with scale
        scale_resized = cv.resize_image(self.color_image, scale=0.5)
        expected_shape = (self.color_image.shape[0] // 2, self.color_image.shape[1] // 2)
        self.assertEqual(scale_resized.shape[:2], expected_shape, 
                        f"Scale resized dimensions should be {expected_shape}")
        
        # Test resize with different interpolation methods
        interpolations = ['nearest', 'linear', 'cubic', 'area', 'lanczos']
        for interp in interpolations:
            resized = cv.resize_image(self.color_image, width=100, interpolation=interp)
            self.assertEqual(resized.shape[1], 100, f"Width should be 100 with {interp} interpolation")
    
    def test_crop_image(self):
        """Test cropping images"""
        # Test normal crop
        cropped = cv.crop_image(self.color_image, 50, 50, 100, 80)
        self.assertEqual(cropped.shape[:2], (80, 100), "Crop dimensions should be 80x100")
        
        # Test crop near boundaries
        edge_crop = cv.crop_image(self.color_image, 250, 150, 40, 30)
        self.assertEqual(edge_crop.shape[:2], (30, 40), "Edge crop dimensions should be 30x40")
    
    def test_convert_color_space(self):
        """Test color space conversions"""
        # Test BGR to Gray
        gray = cv.convert_color_space(self.color_image, 'BGR', 'GRAY')
        self.assertEqual(len(gray.shape), 2, "Grayscale image should have 2 dimensions")
        
        # Test BGR to HSV
        hsv = cv.convert_color_space(self.color_image, 'BGR', 'HSV')
        self.assertEqual(hsv.shape, self.color_image.shape, "HSV image should have same dimensions")
        
        # Test BGR to RGB
        rgb = cv.convert_color_space(self.color_image, 'BGR', 'RGB')
        self.assertEqual(rgb.shape, self.color_image.shape, "RGB image should have same dimensions")
        # Check that R and B channels are swapped
        self.assertTrue(np.any(rgb[:,:,0] != self.color_image[:,:,2]), 
                       "RGB conversion should swap R and B channels")
        
        # Test RGB to LAB
        lab = cv.convert_color_space(rgb, 'RGB', 'LAB')
        self.assertEqual(lab.shape, rgb.shape, "LAB image should have same dimensions")
    
    def test_get_image_info(self):
        """Test getting image information"""
        # Test color image info
        color_info = cv.get_image_info(self.color_image)
        self.assertEqual(color_info['width'], self.color_image.shape[1])
        self.assertEqual(color_info['height'], self.color_image.shape[0])
        self.assertEqual(color_info['channels'], 3)
        self.assertEqual(color_info['dtype'], 'uint8')
        
        # Test grayscale image info
        gray_info = cv.get_image_info(self.gray_image)
        self.assertEqual(gray_info['width'], self.gray_image.shape[1])
        self.assertEqual(gray_info['height'], self.gray_image.shape[0])
        self.assertEqual(gray_info['channels'], 1)
        self.assertEqual(gray_info['dtype'], 'uint8')

if __name__ == "__main__":
    unittest.main()
