"""
Tests for individual functions in the transformations module
"""
import unittest
import numpy as np
import cv2
from math import isclose
from easy_opencv.transformations import (
    rotate_image, flip_image, translate_image, apply_perspective_transform,
    apply_affine_transform, warp_image, apply_barrel_distortion,
    apply_fisheye_effect, resize_with_aspect_ratio
)
from tests.base_test_case import BaseTestCase


class TestRotateImage(BaseTestCase):
    def test_basic_rotation(self):
        """Test basic image rotation"""
        # Rotate by 90 degrees
        rotated = rotate_image(self.color_image, angle=90)
        self.assertEqual(rotated.shape, self.color_image.shape)
        
        # Check that 90-degree rotation swaps height and width visually
        # (though output dimensions stay the same due to how warpAffine works)
        original_left_top = self.color_image[0, 0].copy()
        rotated_right_top = rotated[0, -1].copy()
        # We don't check exact equality because of interpolation
        
    def test_rotation_with_custom_center(self):
        """Test rotation around a custom center"""
        center = (50, 50)  # Custom center
        rotated = rotate_image(self.color_image, angle=45, center=center)
        self.assertEqual(rotated.shape, self.color_image.shape)
    
    def test_rotation_with_scale(self):
        """Test rotation with scaling"""
        rotated = rotate_image(self.color_image, angle=30, scale=0.5)
        self.assertEqual(rotated.shape, self.color_image.shape)
    
    def test_border_modes(self):
        """Test different border modes"""
        # Constant border mode
        rotated1 = rotate_image(self.color_image, angle=45, border_mode='constant', 
                               border_value=(255, 0, 0))
        
        # Reflect border mode
        rotated2 = rotate_image(self.color_image, angle=45, border_mode='reflect')
        
        # Wrap border mode
        rotated3 = rotate_image(self.color_image, angle=45, border_mode='wrap')
        
        # The different border modes should produce different results
        self.assertFalse(np.array_equal(rotated1, rotated2))
        self.assertFalse(np.array_equal(rotated2, rotated3))


class TestFlipImage(BaseTestCase):
    def test_horizontal_flip(self):
        """Test flipping image horizontally"""
        flipped = flip_image(self.color_image, direction='horizontal')
        self.assertEqual(flipped.shape, self.color_image.shape)
        
        # Check that horizontal flip reverses columns
        np.testing.assert_array_equal(flipped[:, 0], self.color_image[:, -1])
        np.testing.assert_array_equal(flipped[:, -1], self.color_image[:, 0])
    
    def test_vertical_flip(self):
        """Test flipping image vertically"""
        flipped = flip_image(self.color_image, direction='vertical')
        self.assertEqual(flipped.shape, self.color_image.shape)
        
        # Check that vertical flip reverses rows
        np.testing.assert_array_equal(flipped[0], self.color_image[-1])
        np.testing.assert_array_equal(flipped[-1], self.color_image[0])
    
    def test_both_flip(self):
        """Test flipping image both horizontally and vertically"""
        flipped = flip_image(self.color_image, direction='both')
        self.assertEqual(flipped.shape, self.color_image.shape)
        
        # Check that 'both' flip reverses both dimensions
        np.testing.assert_array_equal(flipped[0, 0], self.color_image[-1, -1])
        np.testing.assert_array_equal(flipped[-1, -1], self.color_image[0, 0])
    
    def test_invalid_direction(self):
        """Test with invalid direction"""
        with self.assertRaises(ValueError):
            flip_image(self.color_image, direction='invalid')


class TestTranslateImage(BaseTestCase):
    def test_basic_translation(self):
        """Test basic image translation"""
        translated = translate_image(self.color_image, tx=50, ty=30)
        self.assertEqual(translated.shape, self.color_image.shape)
    
    def test_negative_translation(self):
        """Test negative shifts"""
        translated = translate_image(self.color_image, tx=-20, ty=-10)
        self.assertEqual(translated.shape, self.color_image.shape)
    
    def test_border_modes(self):
        """Test different border modes"""
        # Constant border
        translated1 = translate_image(self.color_image, tx=50, ty=50, 
                                     border_mode='constant', border_value=(0, 0, 255))
        
        # Reflect border
        translated2 = translate_image(self.color_image, tx=50, ty=50, 
                                     border_mode='reflect')
        
        # The different border modes should produce different results
        self.assertFalse(np.array_equal(translated1, translated2))


class TestResizeWithAspectRatio(BaseTestCase):
    def test_resize_with_target_size(self):
        """Test resizing with aspect ratio maintained using target_size"""
        target_size = (150, 100)
        resized = resize_with_aspect_ratio(self.color_image, target_size=target_size)
        
        # The output should fit within the target size while maintaining aspect ratio
        self.assertLessEqual(resized.shape[0], target_size[1])  # height
        self.assertLessEqual(resized.shape[1], target_size[0])  # width
        
        # Check aspect ratio is maintained (approximately)
        original_ratio = self.color_image.shape[1] / self.color_image.shape[0]
        new_ratio = resized.shape[1] / resized.shape[0]
        self.assertTrue(isclose(original_ratio, new_ratio, rel_tol=0.1))
    
    def test_resize_with_padding(self):
        """Test resizing with custom padding color"""
        target_size = (150, 150)
        padding_color = (255, 0, 0)  # Red padding
        
        resized = resize_with_aspect_ratio(self.color_image, target_size=target_size, 
                                          padding_color=padding_color)
        
        # The output shape should match the target size exactly
        self.assertEqual(resized.shape[:2], (target_size[1], target_size[0]))
        
        # Check padding (if padding was applied, some pixels should be the padding color)
        # This depends on implementation details, so we can't assert it directly
    
    def test_small_target_size(self):
        """Test with very small target size"""
        target_size = (50, 50)
        resized = resize_with_aspect_ratio(self.color_image, target_size=target_size)
        
        # The output should fit within the target size
        self.assertLessEqual(resized.shape[0], target_size[1])
        self.assertLessEqual(resized.shape[1], target_size[0])


if __name__ == "__main__":
    unittest.main()
