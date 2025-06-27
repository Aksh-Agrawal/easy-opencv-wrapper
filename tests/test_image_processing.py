"""
Tests for image processing module
"""
import unittest
import numpy as np
from easy_opencv.image_processing import (
    apply_blur, apply_sharpen, apply_edge_detection, apply_threshold,
    apply_morphology, apply_histogram_equalization, adjust_brightness_contrast,
    apply_gamma_correction
)
from tests.base_test_case import BaseTestCase


class TestImageProcessing(BaseTestCase):
    def test_apply_blur(self):
        """Test applying different blur types"""
        # Test Gaussian blur
        blurred = apply_blur(self.color_image, blur_type='gaussian', strength=5)
        self.assertEqual(blurred.shape, self.color_image.shape)
        # Blurred image should have less variance than original
        self.assertLess(np.var(blurred), np.var(self.color_image))
        
        # Test median blur
        blurred = apply_blur(self.color_image, blur_type='median', strength=5)
        self.assertEqual(blurred.shape, self.color_image.shape)
        
        # Test average blur
        blurred = apply_blur(self.color_image, blur_type='average', strength=5)
        self.assertEqual(blurred.shape, self.color_image.shape)
        
        # Test with even kernel size (should convert to odd)
        blurred = apply_blur(self.color_image, blur_type='gaussian', strength=6)
        self.assertEqual(blurred.shape, self.color_image.shape)
        
        # Test with invalid blur type
        blurred = apply_blur(self.color_image, blur_type='invalid')
        np.testing.assert_array_equal(blurred, self.color_image)  # Should return original

    def test_apply_sharpen(self):
        """Test sharpening an image"""
        # Test with default strength
        sharpened = apply_sharpen(self.color_image)
        self.assertEqual(sharpened.shape, self.color_image.shape)
        
        # Test with higher strength
        sharpened_strong = apply_sharpen(self.color_image, strength=2.0)
        self.assertEqual(sharpened_strong.shape, self.color_image.shape)
        
        # Higher strength should increase contrast/variance
        self.assertGreater(np.var(sharpened_strong), np.var(sharpened))

    def test_apply_edge_detection(self):
        """Test edge detection methods"""
        # Test Canny
        edges = apply_edge_detection(self.edge_image, method='canny')
        self.assertEqual(len(edges.shape), 2)  # Should be single-channel
        self.assertTrue(np.any(edges > 0))  # Should detect some edges
        
        # Test Sobel
        edges = apply_edge_detection(self.edge_image, method='sobel')
        self.assertEqual(len(edges.shape), 2)
        self.assertTrue(np.any(edges > 0))
        
        # Test Laplacian
        edges = apply_edge_detection(self.edge_image, method='laplacian')
        self.assertEqual(len(edges.shape), 2)
        self.assertTrue(np.any(edges > 0))
        
        # Test with custom thresholds for Canny
        edges = apply_edge_detection(self.edge_image, method='canny', 
                                    threshold1=100, threshold2=200)
        self.assertEqual(len(edges.shape), 2)

    def test_apply_threshold(self):
        """Test thresholding methods"""
        gray = np.array(self.gray_image, copy=True)
        
        # Test binary thresholding
        threshold = apply_threshold(gray, thresh_type='binary', value=127)
        self.assertEqual(threshold.shape, gray.shape)
        self.assertTrue(np.all((threshold == 0) | (threshold == 255)))
        
        # Test adaptive thresholding
        threshold = apply_threshold(gray, thresh_type='adaptive')
        self.assertEqual(threshold.shape, gray.shape)
        self.assertTrue(np.all((threshold == 0) | (threshold == 255)))
        
        # Test Otsu thresholding
        threshold = apply_threshold(gray, thresh_type='otsu')
        self.assertEqual(threshold.shape, gray.shape)
        self.assertTrue(np.all((threshold == 0) | (threshold == 255)))

    def test_apply_morphology(self):
        """Test morphological operations"""
        # Create a binary test image
        binary = np.zeros((100, 100), dtype=np.uint8)
        binary[40:60, 40:60] = 255  # Create a white square
        
        # Test erosion
        eroded = apply_morphology(binary, operation='erode', kernel_size=3)
        self.assertEqual(eroded.shape, binary.shape)
        self.assertLess(np.sum(eroded), np.sum(binary))  # Erosion reduces white area
        
        # Test dilation
        dilated = apply_morphology(binary, operation='dilate', kernel_size=3)
        self.assertEqual(dilated.shape, binary.shape)
        self.assertGreater(np.sum(dilated), np.sum(binary))  # Dilation increases white area
        
        # Test opening
        opened = apply_morphology(binary, operation='open', kernel_size=3)
        self.assertEqual(opened.shape, binary.shape)
        
        # Test closing
        closed = apply_morphology(binary, operation='close', kernel_size=3)
        self.assertEqual(closed.shape, binary.shape)

    def test_apply_histogram_equalization(self):
        """Test histogram equalization"""
        # Test on grayscale image
        gray = np.array(self.gray_image, copy=True)
        equalized = apply_histogram_equalization(gray)
        self.assertEqual(equalized.shape, gray.shape)
        
        # Test on color image
        equalized = apply_histogram_equalization(self.color_image)
        self.assertEqual(equalized.shape, self.color_image.shape)
        
        # Check adaptive histogram equalization
        equalized = apply_histogram_equalization(gray, method='adaptive')
        self.assertEqual(equalized.shape, gray.shape)

    def test_adjust_brightness_contrast(self):
        """Test brightness and contrast adjustment"""
        # Increase brightness
        brightened = adjust_brightness_contrast(self.color_image, brightness=50)
        self.assertEqual(brightened.shape, self.color_image.shape)
        self.assertGreater(np.mean(brightened), np.mean(self.color_image))
        
        # Decrease brightness
        darkened = adjust_brightness_contrast(self.color_image, brightness=-50)
        self.assertEqual(darkened.shape, self.color_image.shape)
        self.assertLess(np.mean(darkened), np.mean(self.color_image))
        
        # Increase contrast
        contrasted = adjust_brightness_contrast(self.color_image, contrast=50)
        self.assertEqual(contrasted.shape, self.color_image.shape)
        self.assertGreater(np.var(contrasted), np.var(self.color_image))
        
        # Decrease contrast
        less_contrast = adjust_brightness_contrast(self.color_image, contrast=-50)
        self.assertEqual(less_contrast.shape, self.color_image.shape)
        self.assertLess(np.var(less_contrast), np.var(self.color_image))
        
        # Both brightness and contrast
        adjusted = adjust_brightness_contrast(self.color_image, brightness=30, contrast=20)
        self.assertEqual(adjusted.shape, self.color_image.shape)

    def test_apply_gamma_correction(self):
        """Test gamma correction"""
        # Gamma > 1 (darker)
        darker = apply_gamma_correction(self.color_image, gamma=2.0)
        self.assertEqual(darker.shape, self.color_image.shape)
        self.assertLess(np.mean(darker), np.mean(self.color_image))
        
        # Gamma < 1 (brighter)
        brighter = apply_gamma_correction(self.color_image, gamma=0.5)
        self.assertEqual(brighter.shape, self.color_image.shape)
        self.assertGreater(np.mean(brighter), np.mean(self.color_image))
        
        # Test with lookup table
        corrected = apply_gamma_correction(self.color_image, gamma=1.5, use_lookup=True)
        self.assertEqual(corrected.shape, self.color_image.shape)


if __name__ == "__main__":
    unittest.main()
