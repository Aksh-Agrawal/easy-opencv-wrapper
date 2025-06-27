"""
Tests for drawing operations module.
"""

import unittest
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestDrawingOperations(BaseTestCase):
    """Test cases for drawing operations functions"""
    
    def test_draw_rectangle(self):
        """Test drawing rectangles"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test unfilled rectangle
        rect = cv.draw_rectangle(canvas.copy(), (10, 20), (50, 70), color=(255, 0, 0))
        self.assert_image_not_empty(rect)
        
        # Check that only the boundaries have color
        inner = rect[21:69, 11:49]
        self.assertTrue(np.all(inner == 0), "Inside of unfilled rectangle should be black")
        
        # Test filled rectangle
        filled_rect = cv.draw_rectangle(canvas.copy(), (10, 20), (50, 70), 
                                      color=(0, 255, 0), filled=True)
        self.assert_image_not_empty(filled_rect)
        
        # Check that inner area is colored
        inner = filled_rect[30:60, 20:40]
        self.assertTrue(np.any(inner[:, :, 1] > 0), "Inside of filled rectangle should be colored")
        
        # Test different thickness
        thick_rect = cv.draw_rectangle(canvas.copy(), (10, 20), (50, 70), 
                                     color=(0, 0, 255), thickness=5)
        self.assert_image_not_empty(thick_rect)
    
    def test_draw_circle(self):
        """Test drawing circles"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test unfilled circle
        circle = cv.draw_circle(canvas.copy(), (50, 50), 30, color=(255, 0, 0))
        self.assert_image_not_empty(circle)
        
        # Check that center is not colored
        self.assertEqual(circle[50, 50, 0], 0, "Center of unfilled circle should be black")
        
        # Test filled circle
        filled_circle = cv.draw_circle(canvas.copy(), (50, 50), 30, 
                                     color=(0, 255, 0), filled=True)
        self.assert_image_not_empty(filled_circle)
        
        # Check that center is colored
        self.assertTrue(filled_circle[50, 50, 1] > 0, "Center of filled circle should be colored")
        
        # Test different thickness
        thick_circle = cv.draw_circle(canvas.copy(), (50, 50), 30, 
                                     color=(0, 0, 255), thickness=5)
        self.assert_image_not_empty(thick_circle)
    
    def test_draw_line(self):
        """Test drawing lines"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test simple line
        line = cv.draw_line(canvas.copy(), (10, 10), (90, 90), color=(255, 0, 0))
        self.assert_image_not_empty(line)
        
        # Test line with different thickness
        thick_line = cv.draw_line(canvas.copy(), (10, 90), (90, 10), 
                               color=(0, 255, 0), thickness=5)
        self.assert_image_not_empty(thick_line)
        
        # Test different line types
        line_types = ['aa', '4', '8']
        for line_type in line_types:
            typed_line = cv.draw_line(canvas.copy(), (10, 50), (90, 50), 
                                  color=(0, 0, 255), line_type=line_type)
            self.assert_image_not_empty(typed_line)
    
    def test_draw_text(self):
        """Test drawing text"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test simple text
        text_img = cv.draw_text(canvas.copy(), "Test", (10, 50), color=(255, 255, 255))
        self.assert_image_not_empty(text_img)
        
        # Test with background
        bg_text = cv.draw_text(canvas.copy(), "BG", (10, 50), color=(255, 255, 255),
                             background=True, bg_color=(0, 0, 255))
        self.assert_image_not_empty(bg_text)
        # Check that background color is present
        self.assertTrue(np.any(bg_text[:, :, 2] > 0), "Blue background should be present")
        
        # Test with different font faces
        font_faces = ['simplex', 'plain', 'duplex', 'complex']
        for font in font_faces:
            font_text = cv.draw_text(canvas.copy(), "Font", (10, 50), 
                                   color=(255, 255, 255), font_face=font)
            self.assert_image_not_empty(font_text)
    
    def test_draw_polygon(self):
        """Test drawing polygons"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        points = [(10, 10), (90, 10), (90, 90), (10, 90)]
        
        # Test unfilled polygon
        poly = cv.draw_polygon(canvas.copy(), points, color=(255, 0, 0))
        self.assert_image_not_empty(poly)
        
        # Test filled polygon
        filled_poly = cv.draw_polygon(canvas.copy(), points, color=(0, 255, 0), filled=True)
        self.assert_image_not_empty(filled_poly)
        
        # Check center is filled
        self.assertTrue(np.any(filled_poly[50, 50, 1] > 0), 
                       "Center of filled polygon should be colored")
    
    def test_draw_contour(self):
        """Test drawing contours"""
        # Create an image with a simple shape
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        canvas = cv.draw_rectangle(canvas, (20, 20), (80, 80), color=(255, 255, 255), filled=True)
        
        # Detect contours
        contours = cv.detect_contours(canvas)
        self.assertTrue(len(contours) > 0, "Should detect at least one contour")
        
        # Draw all contours
        all_contours = cv.draw_contour(canvas.copy(), contours, color=(0, 255, 0))
        self.assert_image_not_empty(all_contours)
        
        # Draw specific contour
        single_contour = cv.draw_contour(canvas.copy(), contours, 
                                       color=(0, 0, 255), contour_index=0)
        self.assert_image_not_empty(single_contour)
    
    def test_draw_arrow(self):
        """Test drawing arrows"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test simple arrow
        arrow = cv.draw_arrow(canvas.copy(), (10, 50), (90, 50), color=(255, 0, 0))
        self.assert_image_not_empty(arrow)
        
        # Test arrow with different thickness
        thick_arrow = cv.draw_arrow(canvas.copy(), (50, 10), (50, 90), 
                                  color=(0, 255, 0), thickness=3)
        self.assert_image_not_empty(thick_arrow)
        
        # Test with different arrow size
        big_arrow = cv.draw_arrow(canvas.copy(), (10, 10), (90, 90), 
                                color=(0, 0, 255), arrow_size=20)
        self.assert_image_not_empty(big_arrow)
    
    def test_draw_grid(self):
        """Test drawing grid"""
        canvas = np.ones((100, 100, 3), dtype=np.uint8) * 255
        
        # Test default grid
        grid = cv.draw_grid(canvas.copy())
        self.assert_image_not_empty(grid)
        
        # Test custom grid size
        custom_grid = cv.draw_grid(canvas.copy(), grid_size=(5, 5), 
                                 color=(255, 0, 0), thickness=2)
        self.assert_image_not_empty(custom_grid)
    
    def test_draw_crosshair(self):
        """Test drawing crosshair"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Test default crosshair
        crosshair = cv.draw_crosshair(canvas.copy(), (50, 50))
        self.assert_image_not_empty(crosshair)
        
        # Test custom crosshair
        custom_crosshair = cv.draw_crosshair(canvas.copy(), (50, 50), 
                                          size=20, color=(0, 0, 255), thickness=2)
        self.assert_image_not_empty(custom_crosshair)
    
    def test_draw_bounding_boxes(self):
        """Test drawing bounding boxes"""
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        boxes = [(10, 10, 40, 40), (50, 50, 90, 90)]
        
        # Test simple boxes
        boxed = cv.draw_bounding_boxes(canvas.copy(), boxes)
        self.assert_image_not_empty(boxed)
        
        # Test with labels
        labels = ["Box 1", "Box 2"]
        labeled_boxes = cv.draw_bounding_boxes(canvas.copy(), boxes, 
                                            labels=labels, thickness=2)
        self.assert_image_not_empty(labeled_boxes)
        
        # Test with custom colors
        colors = [(255, 0, 0), (0, 255, 0)]
        colored_boxes = cv.draw_bounding_boxes(canvas.copy(), boxes, colors=colors)
        self.assert_image_not_empty(colored_boxes)

if __name__ == "__main__":
    unittest.main()
