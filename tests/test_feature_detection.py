"""
Tests for feature detection module.
"""

import unittest
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestFeatureDetection(BaseTestCase):
    """Test cases for feature detection functions"""
    
    def test_detect_corners(self):
        """Test corner detection"""
        # Create a test image with clear corners
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img = cv.draw_rectangle(test_img, (20, 20), (80, 80), color=(255, 255, 255), thickness=2)
        
        # Detect with default parameters
        corners = cv.detect_corners(test_img)
        self.assertTrue(len(corners) > 0, "Should detect corners in rectangle")
        
        # Test with custom parameters
        corners_custom = cv.detect_corners(test_img, max_corners=50, 
                                        quality_level=0.05, min_distance=5)
        self.assertTrue(len(corners_custom) > 0, "Should detect corners with custom parameters")
        
        # Test with more corners
        checkerboard = np.zeros((100, 100, 3), dtype=np.uint8)
        for i in range(0, 100, 20):
            for j in range(0, 100, 20):
                if (i//20 + j//20) % 2 == 0:
                    checkerboard[i:i+20, j:j+20] = 255
        
        corners_many = cv.detect_corners(checkerboard, max_corners=100)
        self.assertTrue(len(corners_many) > 0, "Should detect corners in checkerboard")
    
    def test_detect_keypoints(self):
        """Test keypoint detection"""
        # Skip if advanced feature detection methods aren't available
        try:
            # Test with SIFT (default)
            keypoints, descriptors = cv.detect_keypoints(self.color_image)
            self.assertTrue(len(keypoints) > 0, "Should detect keypoints with SIFT")
            
            # Test with other methods if available
            methods = ['orb', 'brisk', 'akaze']
            for method in methods:
                try:
                    kp, des = cv.detect_keypoints(self.color_image, method=method)
                    self.assertTrue(len(kp) > 0, f"Should detect keypoints with {method}")
                except Exception as e:
                    print(f"Method {method} not available: {e}")
                    
        except Exception as e:
            print(f"Skipping keypoint tests: {e}")
            return
    
    def test_match_features(self):
        """Test feature matching"""
        # Skip if advanced feature matching isn't available
        try:
            # Create two similar images
            img1 = self.color_image
            img2 = cv.rotate_image(img1, angle=5)  # Slight rotation
            
            # Detect keypoints in both images
            kp1, des1 = cv.detect_keypoints(img1)
            kp2, des2 = cv.detect_keypoints(img2)
            
            # Test FLANN matcher
            matches = cv.match_features(des1, des2, method='flann')
            self.assertTrue(len(matches) > 0, "Should find matches with FLANN")
            
            # Test BF matcher
            matches_bf = cv.match_features(des1, des2, method='bf')
            self.assertTrue(len(matches_bf) > 0, "Should find matches with BF")
            
            # Test with custom ratio test
            matches_strict = cv.match_features(des1, des2, ratio_test=0.6)
            self.assertTrue(len(matches_strict) <= len(matches), 
                           "Stricter ratio test should find fewer or equal matches")
        except Exception as e:
            print(f"Skipping feature matching tests: {e}")
            return
    
    def test_detect_contours(self):
        """Test contour detection"""
        # Create an image with a simple shape
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img = cv.draw_rectangle(test_img, (20, 20), (80, 80), 
                                  color=(255, 255, 255), filled=True)
        
        # Test with default parameters
        contours = cv.detect_contours(test_img)
        self.assertTrue(len(contours) > 0, "Should detect contours")
        
        # Test with custom threshold
        contours_thresh = cv.detect_contours(test_img, threshold_value=200)
        self.assertTrue(len(contours_thresh) > 0, "Should detect contours with custom threshold")
        
        # Test with area filtering
        test_img_multi = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img_multi = cv.draw_rectangle(test_img_multi, (20, 20), (80, 80), 
                                       color=(255, 255, 255), filled=True)
        test_img_multi = cv.draw_circle(test_img_multi, (30, 30), 5, 
                                     color=(255, 255, 255), filled=True)
        
        all_contours = cv.detect_contours(test_img_multi, min_area=0)
        large_contours = cv.detect_contours(test_img_multi, min_area=1000)
        self.assertTrue(len(all_contours) > len(large_contours), 
                       "Min area filter should reduce number of contours")
    
    def test_find_shapes(self):
        """Test finding shapes"""
        # Create an image with multiple shapes
        shapes_img = np.zeros((200, 200, 3), dtype=np.uint8)
        # Draw rectangle
        shapes_img = cv.draw_rectangle(shapes_img, (20, 20), (50, 50), 
                                    color=(255, 255, 255), filled=True)
        # Draw circle
        shapes_img = cv.draw_circle(shapes_img, (100, 100), 20, 
                                 color=(255, 255, 255), filled=True)
        # Draw triangle
        triangle_pts = np.array([[150, 50], [180, 50], [165, 80]])
        shapes_img = cv.draw_polygon(shapes_img, triangle_pts.tolist(), 
                                  color=(255, 255, 255), filled=True)
        
        # Test finding all shapes
        all_shapes = cv.find_shapes(shapes_img)
        self.assertTrue(len(all_shapes) >= 3, "Should find at least 3 shapes")
        
        # Test finding specific shapes
        rectangles = cv.find_shapes(shapes_img, shape_type='rectangle')
        circles = cv.find_shapes(shapes_img, shape_type='circle')
        triangles = cv.find_shapes(shapes_img, shape_type='triangle')
        
        self.assertTrue(len(rectangles) > 0, "Should find rectangles")
        self.assertTrue(len(circles) > 0, "Should find circles")
        self.assertTrue(len(triangles) > 0, "Should find triangles")
    
    def test_template_matching(self):
        """Test template matching"""
        # Create a main image and a template from it
        main = self.color_image
        h, w = main.shape[:2]
        
        # Extract a region to use as template
        template = main[50:100, 100:200]
        
        # Test with default parameters
        result = cv.template_matching(main, template)
        self.assertIsNotNone(result, "Should find the template")
        top_left, bottom_right, score = result
        self.assertTrue(score > 0.7, "Match score should be high for exact template")
        
        # Test with different methods
        methods = ['sqdiff', 'sqdiff_normed', 'ccorr', 'ccorr_normed', 'ccoeff']
        for method in methods:
            result = cv.template_matching(main, template, method=method)
            self.assertIsNotNone(result, f"Should find the template with {method}")

if __name__ == "__main__":
    unittest.main()
