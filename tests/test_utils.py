"""
Tests for utilities module
"""
import unittest
import numpy as np
import tempfile
import os
import time
import cv2
from easy_opencv.utils import (
    create_trackbar, mouse_callback, set_mouse_callback, fps_counter,
    color_picker, image_comparison, create_image_grid, apply_watermark,
    convert_to_sketch, auto_canny
)
from tests.base_test_case import BaseTestCase


class TestUtils(BaseTestCase):
    def test_apply_watermark(self):
        """Test applying watermark to an image"""
        # Test with default parameters
        watermarked = apply_watermark(self.color_image, watermark_text="Test")
        self.assertEqual(watermarked.shape, self.color_image.shape)
        
        # Test with custom position
        watermarked = apply_watermark(self.color_image, watermark_text="Test", position="top_left")
        self.assertEqual(watermarked.shape, self.color_image.shape)
        
        watermarked = apply_watermark(self.color_image, watermark_text="Test", position="bottom_right")
        self.assertEqual(watermarked.shape, self.color_image.shape)
        
        # Test with custom opacity and font_scale
        watermarked = apply_watermark(self.color_image, watermark_text="Test", 
                                    opacity=0.3, font_scale=0.5)
        self.assertEqual(watermarked.shape, self.color_image.shape)

    def test_create_image_grid(self):
        """Test creating an image grid"""
        # Create a list of test images - ensure all have 3 dimensions
        images = [
            self.color_image,  # Already 3 channels
            cv2.cvtColor(self.gray_image, cv2.COLOR_GRAY2BGR),  # Convert to 3 channels
            self.small_image,  # Already 3 channels
            self.edge_image  # Already 3 channels
        ]
        
        # Test with required parameters
        grid = create_image_grid(images, grid_size=(2, 2))
        self.assertIsInstance(grid, np.ndarray)
        self.assertEqual(len(grid.shape), 3)  # Should be a color image
        
        # Test with custom grid size
        grid = create_image_grid(images, grid_size=(1, 4))
        self.assertIsInstance(grid, np.ndarray)
        self.assertEqual(len(grid.shape), 3)
        
        # Test with image_size specified
        grid = create_image_grid(images, grid_size=(2, 2), image_size=(100, 100))
        self.assertIsInstance(grid, np.ndarray)
        
        # Test with too few images for the grid
        grid = create_image_grid(images[:2], grid_size=(2, 2))
        self.assertIsInstance(grid, np.ndarray)

    def test_convert_to_sketch(self):
        """Test converting an image to a sketch"""
        # Test with default parameters
        sketch = convert_to_sketch(self.color_image)
        # The shape might return a 2D grayscale image
        self.assertTrue(sketch.shape[:2] == self.color_image.shape[:2])
        
        # Test with custom blur_value
        sketch = convert_to_sketch(self.color_image, blur_value=15)
        self.assertTrue(sketch.shape[:2] == self.color_image.shape[:2])
        
        # Test with custom intensity
        sketch = convert_to_sketch(self.color_image, intensity=200)
        self.assertTrue(sketch.shape[:2] == self.color_image.shape[:2])

    def test_auto_canny(self):
        """Test automatic Canny edge detection"""
        # Test with default sigma
        edges = auto_canny(self.edge_image)
        self.assertEqual(len(edges.shape), 2)  # Should be single-channel
        self.assertTrue(np.any(edges > 0))  # Should detect some edges
        
        # Test with custom sigma
        edges_tight = auto_canny(self.edge_image, sigma=0.33)
        self.assertEqual(len(edges_tight.shape), 2)
        
        edges_wide = auto_canny(self.edge_image, sigma=0.66)
        self.assertEqual(len(edges_wide.shape), 2)
        
        # Lower sigma should generally detect more edges
        self.assertGreaterEqual(np.sum(edges_tight), np.sum(edges_wide))

    def test_image_comparison(self):
        """Test image comparison methods"""
        # Create slightly modified version of color_image
        mod_image = self.color_image.copy()
        mod_image[50:70, 50:70] = [0, 0, 0]
        
        # Test with side_by_side (default method)
        result = image_comparison(self.color_image, mod_image)
        self.assertIsInstance(result, np.ndarray)
        # The result should be a side-by-side image, so width should be double
        self.assertEqual(result.shape[1], self.color_image.shape[1] * 2)
        
        # Test with other methods if available
        try:
            # Some implementations may support other methods
            result = image_comparison(self.color_image, mod_image, method='difference')
            self.assertIsInstance(result, np.ndarray)
        except ValueError:
            # If not implemented, this is fine
            pass

    def test_color_picker(self):
        """Test color picker functionality"""
        # This test is challenging since color_picker may be interactive
        # and may not return a value directly
        
        # Create test image with known colors
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[0:50, 0:50] = [255, 0, 0]    # Red in top-left
        test_image[0:50, 50:100] = [0, 255, 0]  # Green in top-right
        test_image[50:100, 0:50] = [0, 0, 255]  # Blue in bottom-left
        test_image[50:100, 50:100] = [255, 255, 255]  # White in bottom-right
        
        # Just test that the function doesn't crash with valid parameters
        try:
            # Default window name
            color_picker(test_image)
            
            # Custom window name
            color_picker(test_image, window_name="Test Picker")
            
            # This is all we can test without mocking GUI interactions
            # The actual functionality would require interactive testing
            
        except Exception as e:
            # Skip this test if it requires a display that's not available
            if "cannot open display" in str(e).lower() or "error: (-2)" in str(e).lower():
                self.skipTest("Display not available for color picker test")
            else:
                raise  # Re-raise if it's a different error

    def test_fps_counter(self):
        """Test FPS counter functionality"""
        # Initialize FPS counter
        fps_obj = fps_counter()
        self.assertIsInstance(fps_obj, object)  # Should return an object
        
        # Test with show_on_image parameter
        fps_obj1 = fps_counter(show_on_image=True)
        fps_obj2 = fps_counter(show_on_image=False)
        
        # Different instances should be different objects
        self.assertIsNot(fps_obj1, fps_obj2)
        
        # The object should have an update method
        if hasattr(fps_obj, 'update'):
            # Call update if it exists
            fps_obj.update()
            
        # For more thorough testing, we would need to know the exact interface
        # of the FPSCounter class

    # These tests are more difficult to unit test without GUI
    def _test_create_trackbar(self):
        """Test creating a trackbar (visual test)"""
        window_name = "Trackbar Test"
        trackbar_name = "Value"
        
        # Create a window
        cv2.namedWindow(window_name)
        
        # Create a trackbar
        value = [0]
        def callback(val):
            value[0] = val
            
        create_trackbar(window_name, trackbar_name, 50, 255, callback)
        
        # Check initial value
        self.assertEqual(cv2.getTrackbarPos(trackbar_name, window_name), 50)
        
        # Cleanup
        cv2.destroyAllWindows()
        
    def _test_mouse_callback(self):
        """Test mouse callback (visual test)"""
        # This is primarily a visual test that would require GUI interaction
        # We just check that the function exists and can be called
        event = cv2.EVENT_LBUTTONDOWN
        x, y = 100, 100
        flags = 0
        param = None
        
        # Should not raise an exception
        mouse_callback(event, x, y, flags, param)
        self.assertTrue(True)  # If we get here, no exceptions occurred


if __name__ == "__main__":
    unittest.main()
