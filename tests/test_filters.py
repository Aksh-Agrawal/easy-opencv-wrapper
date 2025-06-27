"""
Tests for filters module.
"""

import unittest
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestFilters(BaseTestCase):
    """Test cases for filter functions"""
    
    def test_apply_gaussian_blur(self):
        """Test applying Gaussian blur"""
        # Test with default parameters
        blurred = cv.apply_gaussian_blur(self.color_image)
        self.assert_image_not_empty(blurred)
        self.assert_image_dimensions(blurred, self.color_image.shape[1], self.color_image.shape[0], 3)
        
        # Test with custom kernel size
        blurred_custom = cv.apply_gaussian_blur(self.color_image, kernel_size=31)
        self.assert_image_not_empty(blurred_custom)
        
        # Test with custom sigmas
        blurred_sigmas = cv.apply_gaussian_blur(self.color_image, sigma_x=5, sigma_y=2)
        self.assert_image_not_empty(blurred_sigmas)
        
        # Test with odd kernel size (should adjust automatically)
        blurred_odd = cv.apply_gaussian_blur(self.color_image, kernel_size=10)  # Should become 11
        self.assert_image_not_empty(blurred_odd)
    
    def test_apply_median_blur(self):
        """Test applying median blur"""
        # Create image with salt and pepper noise
        noisy = self.color_image.copy()
        # Add random white and black pixels
        noise_mask = np.random.random(self.color_image.shape[:2]) > 0.95
        noisy[noise_mask] = 255
        noise_mask = np.random.random(self.color_image.shape[:2]) > 0.95
        noisy[noise_mask] = 0
        
        # Test with default parameters
        denoised = cv.apply_median_blur(noisy)
        self.assert_image_not_empty(denoised)
        self.assert_image_dimensions(denoised, noisy.shape[1], noisy.shape[0], 3)
        
        # Test with custom kernel size
        denoised_custom = cv.apply_median_blur(noisy, kernel_size=7)
        self.assert_image_not_empty(denoised_custom)
        
        # Test with odd kernel size (should adjust automatically)
        denoised_odd = cv.apply_median_blur(noisy, kernel_size=8)  # Should become 9
        self.assert_image_not_empty(denoised_odd)
    
    def test_apply_bilateral_filter(self):
        """Test applying bilateral filter"""
        # Test with default parameters
        filtered = cv.apply_bilateral_filter(self.color_image)
        self.assert_image_not_empty(filtered)
        self.assert_image_dimensions(filtered, self.color_image.shape[1], self.color_image.shape[0], 3)
        
        # Test with custom diameter
        filtered_diameter = cv.apply_bilateral_filter(self.color_image, diameter=15)
        self.assert_image_not_empty(filtered_diameter)
        
        # Test with custom sigmas
        filtered_sigmas = cv.apply_bilateral_filter(self.color_image, 
                                                 sigma_color=100, sigma_space=50)
        self.assert_image_not_empty(filtered_sigmas)
    
    def test_apply_custom_kernel(self):
        """Test applying custom convolution kernel"""
        # Define some test kernels
        identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)
        blur = np.ones((3, 3), dtype=np.float32) / 9
        edge = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
        
        # Test identity kernel (should be similar to original)
        identity_result = cv.apply_custom_kernel(self.color_image, identity)
        self.assert_image_not_empty(identity_result)
        self.assert_image_dimensions(identity_result, 
                                   self.color_image.shape[1], 
                                   self.color_image.shape[0], 3)
        
        # Test blur kernel
        blur_result = cv.apply_custom_kernel(self.color_image, blur)
        self.assert_image_not_empty(blur_result)
        
        # Test edge kernel
        edge_result = cv.apply_custom_kernel(self.color_image, edge)
        self.assert_image_not_empty(edge_result)
    
    def test_apply_noise_reduction(self):
        """Test applying noise reduction"""
        # Create noisy image
        noisy = self.noise_image.copy()
        
        # Test non-local means
        nlm = cv.apply_noise_reduction(noisy, method='nlm')
        self.assert_image_not_empty(nlm)
        self.assert_image_dimensions(nlm, noisy.shape[1], noisy.shape[0], 3)
        
        # Test gaussian method
        gauss = cv.apply_noise_reduction(noisy, method='gaussian', strength=5)
        self.assert_image_not_empty(gauss)
        
        # Test median method
        median = cv.apply_noise_reduction(noisy, method='median', strength=3)
        self.assert_image_not_empty(median)
        
        # Test bilateral method
        bilateral = cv.apply_noise_reduction(noisy, method='bilateral', strength=5)
        self.assert_image_not_empty(bilateral)
    
    def test_apply_emboss_filter(self):
        """Test applying emboss filter"""
        # Test with default direction
        embossed = cv.apply_emboss_filter(self.color_image)
        self.assert_image_not_empty(embossed)
        self.assert_image_dimensions(embossed, 
                                   self.color_image.shape[1], 
                                   self.color_image.shape[0], 3)
        
        # Test with different directions
        directions = ['north', 'northeast', 'east', 'southeast', 
                     'south', 'southwest', 'west', 'northwest']
        for direction in directions:
            dir_emboss = cv.apply_emboss_filter(self.color_image, direction=direction)
            self.assert_image_not_empty(dir_emboss)
    
    def test_apply_edge_enhance_filter(self):
        """Test applying edge enhancement filter"""
        # Test with default strength
        enhanced = cv.apply_edge_enhance_filter(self.color_image)
        self.assert_image_not_empty(enhanced)
        self.assert_image_dimensions(enhanced, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with different strengths
        weak = cv.apply_edge_enhance_filter(self.color_image, strength=0.5)
        self.assert_image_not_empty(weak)
        
        strong = cv.apply_edge_enhance_filter(self.color_image, strength=2.0)
        self.assert_image_not_empty(strong)
    
    def test_apply_unsharp_mask(self):
        """Test applying unsharp mask"""
        # Test with default parameters
        sharpened = cv.apply_unsharp_mask(self.color_image)
        self.assert_image_not_empty(sharpened)
        self.assert_image_dimensions(sharpened, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with custom kernel size
        sharpened_k = cv.apply_unsharp_mask(self.color_image, kernel_size=9)
        self.assert_image_not_empty(sharpened_k)
        
        # Test with custom strength
        sharpened_s = cv.apply_unsharp_mask(self.color_image, strength=2.0)
        self.assert_image_not_empty(sharpened_s)
    
    def test_apply_high_pass_filter(self):
        """Test applying high pass filter"""
        # Test with default cutoff
        high_pass = cv.apply_high_pass_filter(self.color_image)
        self.assert_image_not_empty(high_pass)
        self.assert_image_dimensions(high_pass, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with custom cutoff
        high_pass_custom = cv.apply_high_pass_filter(self.color_image, cutoff=70)
        self.assert_image_not_empty(high_pass_custom)
    
    def test_apply_motion_blur(self):
        """Test applying motion blur"""
        # Test with default parameters
        motion = cv.apply_motion_blur(self.color_image)
        self.assert_image_not_empty(motion)
        self.assert_image_dimensions(motion, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with custom size
        motion_size = cv.apply_motion_blur(self.color_image, size=25)
        self.assert_image_not_empty(motion_size)
        
        # Test with custom angle
        motion_angle = cv.apply_motion_blur(self.color_image, angle=90)
        self.assert_image_not_empty(motion_angle)
    
    def test_apply_vintage_filter(self):
        """Test applying vintage filter"""
        # Test with default intensity
        vintage = cv.apply_vintage_filter(self.color_image)
        self.assert_image_not_empty(vintage)
        self.assert_image_dimensions(vintage, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with low intensity
        vintage_low = cv.apply_vintage_filter(self.color_image, intensity=0.3)
        self.assert_image_not_empty(vintage_low)
        
        # Test with high intensity
        vintage_high = cv.apply_vintage_filter(self.color_image, intensity=1.5)
        self.assert_image_not_empty(vintage_high)
    
    def test_apply_cartoon_filter(self):
        """Test applying cartoon filter"""
        # Test with default parameters
        cartoon = cv.apply_cartoon_filter(self.color_image)
        self.assert_image_not_empty(cartoon)
        self.assert_image_dimensions(cartoon, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with custom edges parameter
        cartoon_edges = cv.apply_cartoon_filter(self.color_image, edges=2)
        self.assert_image_not_empty(cartoon_edges)
        
        # Test with custom bilateral parameter
        cartoon_bilateral = cv.apply_cartoon_filter(self.color_image, bilateral=5)
        self.assert_image_not_empty(cartoon_bilateral)

if __name__ == "__main__":
    unittest.main()
