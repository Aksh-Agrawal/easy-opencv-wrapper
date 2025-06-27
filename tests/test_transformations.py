"""
Tests for transformations module.
"""

import unittest
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestTransformations(BaseTestCase):
    """Test cases for transformation functions"""
    
    def test_rotate_image(self):
        """Test rotating images"""
        # Test with default parameters (rotate around center)
        rotated = cv.rotate_image(self.color_image, angle=45)
        self.assert_image_not_empty(rotated)
        # Shape could change unless keep_size is True
        
        # Test with keep_size=True
        rotated_same_size = cv.rotate_image(self.color_image, angle=45, keep_size=True)
        self.assert_image_dimensions(rotated_same_size, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test rotation with custom center
        h, w = self.color_image.shape[:2]
        custom_center = (w//4, h//4)  # Top-left quarter
        rotated_custom = cv.rotate_image(self.color_image, angle=30, center=custom_center)
        self.assert_image_not_empty(rotated_custom)
        
        # Test with scale
        rotated_scaled = cv.rotate_image(self.color_image, angle=45, scale=0.5)
        self.assert_image_not_empty(rotated_scaled)
    
    def test_flip_image(self):
        """Test flipping images"""
        # Test horizontal flip
        flipped_h = cv.flip_image(self.color_image, direction='horizontal')
        self.assert_image_not_empty(flipped_h)
        self.assert_image_dimensions(flipped_h, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        # Check that left and right sides are swapped
        left_original = self.color_image[:, :10, :]
        right_flipped = flipped_h[:, -10:, :]
        self.assertTrue(np.any(left_original != right_flipped), 
                       "Left and right sides should be swapped")
        
        # Test vertical flip
        flipped_v = cv.flip_image(self.color_image, direction='vertical')
        self.assert_image_not_empty(flipped_v)
        self.assert_image_dimensions(flipped_v, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test both directions
        flipped_both = cv.flip_image(self.color_image, direction='both')
        self.assert_image_not_empty(flipped_both)
        self.assert_image_dimensions(flipped_both, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
    
    def test_translate_image(self):
        """Test translating images"""
        # Test horizontal translation
        translated_h = cv.translate_image(self.color_image, x=50, y=0)
        self.assert_image_not_empty(translated_h)
        self.assert_image_dimensions(translated_h, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test vertical translation
        translated_v = cv.translate_image(self.color_image, x=0, y=50)
        self.assert_image_not_empty(translated_v)
        
        # Test diagonal translation
        translated_diag = cv.translate_image(self.color_image, x=30, y=30)
        self.assert_image_not_empty(translated_diag)
        
        # Test negative translation
        translated_neg = cv.translate_image(self.color_image, x=-20, y=-20)
        self.assert_image_not_empty(translated_neg)
    
    def test_apply_perspective_transform(self):
        """Test applying perspective transform"""
        h, w = self.color_image.shape[:2]
        
        # Define source points (original corners)
        src_points = [(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)]
        
        # Define destination points (new corners)
        # Creating a trapezoid effect
        dst_points = [(w//4, 0), (3*w//4, 0), (w-1, h-1), (0, h-1)]
        
        # Apply transformation
        transformed = cv.apply_perspective_transform(self.color_image, src_points, dst_points)
        self.assert_image_not_empty(transformed)
        self.assert_image_dimensions(transformed, w, h, 3)
    
    def test_apply_affine_transform(self):
        """Test applying affine transform"""
        h, w = self.color_image.shape[:2]
        
        # Define source points (original triangle)
        src_points = [(0, 0), (w-1, 0), (0, h-1)]
        
        # Define destination points (new triangle)
        # Creating a shear effect
        dst_points = [(w//4, 0), (w-1, 0), (0, h-1)]
        
        # Apply transformation
        transformed = cv.apply_affine_transform(self.color_image, src_points, dst_points)
        self.assert_image_not_empty(transformed)
        self.assert_image_dimensions(transformed, w, h, 3)
    
    def test_warp_image(self):
        """Test warping image with custom transformation matrix"""
        h, w = self.color_image.shape[:2]
        
        # Create a translation matrix
        M = np.float32([[1, 0, 50], [0, 1, 30]])
        
        # Apply warp
        warped = cv.warp_image(self.color_image, M)
        self.assert_image_not_empty(warped)
        self.assert_image_dimensions(warped, w, h, 3)
        
        # Create a scaling matrix
        M = np.float32([[0.5, 0, 0], [0, 0.5, 0]])
        
        # Apply warp
        warped_scale = cv.warp_image(self.color_image, M)
        self.assert_image_not_empty(warped_scale)
    
    def test_apply_barrel_distortion(self):
        """Test applying barrel distortion"""
        # Test with default parameters
        distorted = cv.apply_barrel_distortion(self.color_image)
        self.assert_image_not_empty(distorted)
        self.assert_image_dimensions(distorted, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with custom k1, k2
        distorted_k = cv.apply_barrel_distortion(self.color_image, k1=0.2, k2=0.0)
        self.assert_image_not_empty(distorted_k)
        
        # Test with custom center
        h, w = self.color_image.shape[:2]
        distorted_center = cv.apply_barrel_distortion(self.color_image, 
                                                    center=(w//3, h//3))
        self.assert_image_not_empty(distorted_center)
        
        # Test pincushion effect (negative k values)
        pincushion = cv.apply_barrel_distortion(self.color_image, k1=-0.3, k2=-0.3)
        self.assert_image_not_empty(pincushion)
    
    def test_apply_fisheye_effect(self):
        """Test applying fisheye effect"""
        # Test with default strength
        fisheye = cv.apply_fisheye_effect(self.color_image)
        self.assert_image_not_empty(fisheye)
        self.assert_image_dimensions(fisheye, 
                                  self.color_image.shape[1], 
                                  self.color_image.shape[0], 3)
        
        # Test with lower strength
        fisheye_low = cv.apply_fisheye_effect(self.color_image, strength=0.8)
        self.assert_image_not_empty(fisheye_low)
        
        # Test with higher strength
        fisheye_high = cv.apply_fisheye_effect(self.color_image, strength=2.0)
        self.assert_image_not_empty(fisheye_high)
        
        # Test with custom center
        h, w = self.color_image.shape[:2]
        fisheye_center = cv.apply_fisheye_effect(self.color_image, center=(w//4, h//4))
        self.assert_image_not_empty(fisheye_center)
    
    def test_resize_with_aspect_ratio(self):
        """Test resizing with maintained aspect ratio"""
        # Test with width constraint
        width_resized = cv.resize_with_aspect_ratio(self.color_image, width=150)
        self.assert_image_not_empty(width_resized)
        self.assertEqual(width_resized.shape[1], 150)
        # Height should change proportionally
        expected_height = int(self.color_image.shape[0] * (150 / self.color_image.shape[1]))
        self.assertEqual(width_resized.shape[0], expected_height)
        
        # Test with height constraint
        height_resized = cv.resize_with_aspect_ratio(self.color_image, height=100)
        self.assert_image_not_empty(height_resized)
        self.assertEqual(height_resized.shape[0], 100)
        # Width should change proportionally
        expected_width = int(self.color_image.shape[1] * (100 / self.color_image.shape[0]))
        self.assertEqual(height_resized.shape[1], expected_width)
        
        # Test with different interpolation methods
        interps = ['nearest', 'linear', 'cubic', 'area']
        for interp in interps:
            resized = cv.resize_with_aspect_ratio(self.color_image, width=150, inter=interp)
            self.assert_image_not_empty(resized)
            self.assertEqual(resized.shape[1], 150)

if __name__ == "__main__":
    unittest.main()
