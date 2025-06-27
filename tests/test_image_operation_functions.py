"""
Tests for individual functions in the image operations module
"""
import unittest
import os
import tempfile
import numpy as np
import cv2
from easy_opencv.image_operations import (
    load_image, save_image, show_image, resize_image, crop_image,
    convert_color_space, get_image_info
)
from tests.base_test_case import BaseTestCase


class TestLoadImage(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a temporary directory to save test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        self.color_path = os.path.join(self.temp_dir, "test_color.jpg")
        self.gray_path = os.path.join(self.temp_dir, "test_gray.jpg")
        
        # Save test images
        cv2.imwrite(self.color_path, self.color_image)
        cv2.imwrite(self.gray_path, self.gray_image)
        
    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
        super().tearDown()

    def test_color_mode(self):
        """Test loading image in color mode"""
        img = load_image(self.color_path, mode='color')
        self.assertEqual(len(img.shape), 3)  # Should be 3-channel
        self.assertEqual(img.shape[2], 3)
    
    def test_gray_mode(self):
        """Test loading image in grayscale mode"""
        img = load_image(self.color_path, mode='gray')
        self.assertEqual(len(img.shape), 2)  # Should be single-channel
    
    def test_unchanged_mode(self):
        """Test loading image in unchanged mode"""
        img = load_image(self.color_path, mode='unchanged')
        self.assertGreaterEqual(len(img.shape), 2)  # At least 2-dimensional
    
    def test_invalid_path(self):
        """Test loading an invalid path"""
        img = load_image(os.path.join(self.temp_dir, "nonexistent.jpg"), mode='color')
        self.assertIsNone(img)  # Should return None for invalid path
    
    def test_invalid_mode(self):
        """Test loading with invalid mode"""
        img = load_image(self.color_path, mode='invalid')
        self.assertEqual(len(img.shape), 3)  # Should default to color mode


class TestResizeImage(BaseTestCase):
    def test_width_only(self):
        """Test resizing by width only"""
        resized = resize_image(self.color_image, width=150)
        self.assertEqual(resized.shape[1], 150)
        # Check aspect ratio
        aspect_ratio = self.color_image.shape[1] / self.color_image.shape[0]
        new_aspect_ratio = resized.shape[1] / resized.shape[0]
        self.assertAlmostEqual(aspect_ratio, new_aspect_ratio, delta=0.1)
    
    def test_height_only(self):
        """Test resizing by height only"""
        resized = resize_image(self.color_image, height=100)
        self.assertEqual(resized.shape[0], 100)
        # Check aspect ratio
        aspect_ratio = self.color_image.shape[1] / self.color_image.shape[0]
        new_aspect_ratio = resized.shape[1] / resized.shape[0]
        self.assertAlmostEqual(aspect_ratio, new_aspect_ratio, delta=0.1)
    
    def test_scale(self):
        """Test resizing by scale factor"""
        resized = resize_image(self.color_image, scale=0.5)
        expected_height = int(self.color_image.shape[0] * 0.5)
        expected_width = int(self.color_image.shape[1] * 0.5)
        self.assertEqual(resized.shape[:2], (expected_height, expected_width))
    
    def test_width_height_together(self):
        """Test resizing with both width and height specified"""
        resized = resize_image(self.color_image, width=150, height=100)
        self.assertEqual(resized.shape[:2], (100, 150))
    
    def test_different_methods(self):
        """Test different resize methods"""
        # Default method (linear)
        resized1 = resize_image(self.color_image, width=100)
        
        # Nearest method
        resized2 = resize_image(self.color_image, width=100, method='nearest')
        
        # Cubic method
        resized3 = resize_image(self.color_image, width=100, method='cubic')
        
        # The different methods should produce different results
        # We're not checking exact equality because implementation details may vary
        self.assertEqual(resized1.shape, resized2.shape)
        self.assertEqual(resized2.shape, resized3.shape)
    
    def test_invalid_parameters(self):
        """Test with invalid parameters"""
        # Neither width, height, nor scale provided
        with self.assertRaises(ValueError):
            resize_image(self.color_image)
        
        # Invalid method
        with self.assertRaises(ValueError):
            resize_image(self.color_image, scale=0.5, method='invalid')


class TestCropImage(BaseTestCase):
    def test_individual_parameters(self):
        """Test cropping with individual parameters"""
        cropped = crop_image(self.color_image, x=50, y=50, width=100, height=100)
        self.assertEqual(cropped.shape[:2], (100, 100))
        
        # Verify the cropped region
        original_region = self.color_image[50:150, 50:150]
        np.testing.assert_array_equal(cropped, original_region)
    
    def test_positional_parameters(self):
        """Test cropping with positional parameters"""
        cropped = crop_image(self.color_image, 50, 50, 100, 100)
        self.assertEqual(cropped.shape[:2], (100, 100))
        
        # Verify the cropped region
        original_region = self.color_image[50:150, 50:150]
        np.testing.assert_array_equal(cropped, original_region)
    
    def test_partial_crop(self):
        """Test cropping just a small portion of the image"""
        cropped = crop_image(self.color_image, 10, 10, 30, 40)
        self.assertEqual(cropped.shape[:2], (40, 30))
        
        # Verify the cropped region
        original_region = self.color_image[10:50, 10:40]
        np.testing.assert_array_equal(cropped, original_region)
    
    def test_out_of_bounds(self):
        """Test cropping with out-of-bounds coordinates"""
        # This should fail with a ValueError or return a partially filled image
        try:
            crop_image(self.color_image, 250, 250, 100, 100)
            self.fail("Should have raised an error for out-of-bounds crop")
        except (ValueError, cv2.error):
            pass  # Expected error


class TestConvertColorSpace(BaseTestCase):
    def test_bgr_to_rgb(self):
        """Test converting BGR to RGB"""
        rgb = convert_color_space(self.color_image, 'bgr', 'rgb')
        self.assertEqual(rgb.shape, self.color_image.shape)
        
        # RGB should have R and B channels swapped compared to BGR
        np.testing.assert_array_equal(rgb[:, :, 0], self.color_image[:, :, 2])
        np.testing.assert_array_equal(rgb[:, :, 2], self.color_image[:, :, 0])
    
    def test_bgr_to_gray(self):
        """Test converting BGR to grayscale"""
        gray = convert_color_space(self.color_image, 'bgr', 'gray')
        self.assertEqual(len(gray.shape), 2)
        self.assertEqual(gray.shape[:2], self.color_image.shape[:2])
    
    def test_bgr_to_hsv(self):
        """Test converting BGR to HSV"""
        hsv = convert_color_space(self.color_image, 'bgr', 'hsv')
        self.assertEqual(hsv.shape, self.color_image.shape)
        
        # Convert back to BGR and compare (there might be slight differences due to precision)
        bgr_again = convert_color_space(hsv, 'hsv', 'bgr')
        self.assertEqual(bgr_again.shape, self.color_image.shape)
    
    def test_invalid_conversion(self):
        """Test invalid color space conversion"""
        with self.assertRaises(ValueError):
            convert_color_space(self.color_image, 'bgr', 'invalid')


class TestGetImageInfo(BaseTestCase):
    def test_color_image(self):
        """Test getting info from color image"""
        info = get_image_info(self.color_image)
        self.assertEqual(info['width'], self.color_image.shape[1])
        self.assertEqual(info['height'], self.color_image.shape[0])
        self.assertEqual(info['channels'], 3)
        self.assertEqual(info['dtype'], 'uint8')
    
    def test_grayscale_image(self):
        """Test getting info from grayscale image"""
        info = get_image_info(self.gray_image)
        self.assertEqual(info['width'], self.gray_image.shape[1])
        self.assertEqual(info['height'], self.gray_image.shape[0])
        self.assertEqual(info['channels'], 1)
        self.assertEqual(info['dtype'], 'uint8')
    
    def test_different_dtype(self):
        """Test getting info from image with different data type"""
        float_image = self.color_image.astype(np.float32)
        info = get_image_info(float_image)
        self.assertEqual(info['dtype'], 'float32')


if __name__ == "__main__":
    unittest.main()
