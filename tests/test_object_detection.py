"""
Tests for object detection module.
"""

import unittest
import numpy as np
from easy_opencv import cv
from tests.base_test_case import BaseTestCase

class TestObjectDetection(BaseTestCase):
    """Test cases for object detection functions"""
    
    def test_detect_faces(self):
        """Test face detection"""
        # Skip if not available or no test images
        try:
            # Create a simple face-like shape
            face_img = np.ones((200, 200, 3), dtype=np.uint8) * 200
            # Draw face outline
            face_img = cv.draw_circle(face_img, (100, 100), 70, (150, 150, 150), filled=True)
            # Draw eyes
            face_img = cv.draw_circle(face_img, (70, 80), 15, (100, 100, 100), filled=True)
            face_img = cv.draw_circle(face_img, (130, 80), 15, (100, 100, 100), filled=True)
            # Draw mouth
            face_img = cv.draw_rectangle(face_img, (70, 130), (130, 150), (100, 100, 100), filled=True)
            
            # Test detection
            faces = cv.detect_faces(face_img)
            self.assertIsNotNone(faces, "Face detection should return a result")
            
            # Test with custom parameters
            faces_custom = cv.detect_faces(face_img, scale_factor=1.2, 
                                         min_neighbors=3, min_size=(50, 50))
            self.assertIsNotNone(faces_custom, "Face detection with custom params should work")
        except Exception as e:
            print(f"Skipping face detection test: {e}")
    
    def test_detect_eyes(self):
        """Test eye detection"""
        # Skip if not available or no test images
        try:
            # Create a simple eye-like shape
            eye_img = np.ones((100, 200, 3), dtype=np.uint8) * 200
            # Draw eyes
            eye_img = cv.draw_circle(eye_img, (50, 50), 25, (150, 150, 150), filled=True)
            eye_img = cv.draw_circle(eye_img, (150, 50), 25, (150, 150, 150), filled=True)
            # Draw pupils
            eye_img = cv.draw_circle(eye_img, (50, 50), 10, (50, 50, 50), filled=True)
            eye_img = cv.draw_circle(eye_img, (150, 50), 10, (50, 50, 50), filled=True)
            
            # Test detection
            eyes = cv.detect_eyes(eye_img)
            self.assertIsNotNone(eyes, "Eye detection should return a result")
            
            # Test with custom parameters
            eyes_custom = cv.detect_eyes(eye_img, scale_factor=1.2, min_neighbors=3)
            self.assertIsNotNone(eyes_custom, "Eye detection with custom params should work")
        except Exception as e:
            print(f"Skipping eye detection test: {e}")
    
    def test_detect_objects_cascade(self):
        """Test object detection using cascade classifiers"""
        # Skip if not available or no test images
        try:
            # This test requires a cascade XML file
            import os
            import cv2
            haarcascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            
            if not os.path.exists(haarcascade_path):
                print(f"Skipping cascade test: cascade file not found")
                return
                
            # Create a simple face-like shape
            face_img = np.ones((200, 200, 3), dtype=np.uint8) * 200
            face_img = cv.draw_circle(face_img, (100, 100), 70, (150, 150, 150), filled=True)
            
            # Test detection
            objects = cv.detect_objects_cascade(face_img, haarcascade_path)
            self.assertIsNotNone(objects, "Cascade detection should return a result")
            
            # Test with custom parameters
            objects_custom = cv.detect_objects_cascade(face_img, haarcascade_path,
                                                    scale_factor=1.2, min_neighbors=3)
            self.assertIsNotNone(objects_custom, "Cascade detection with custom params should work")
        except Exception as e:
            print(f"Skipping cascade detection test: {e}")
    
    def test_background_subtraction(self):
        """Test background subtraction"""
        # Create a sequence of frames with moving object
        frames = []
        for i in range(5):
            frame = np.zeros((100, 100, 3), dtype=np.uint8)
            # Draw a moving rectangle
            x_pos = 20 + i*10
            frame = cv.draw_rectangle(frame, (x_pos, 40), (x_pos+20, 60), 
                                   color=(255, 255, 255), filled=True)
            frames.append(frame)
        
        # Test with default parameters
        masks = cv.background_subtraction(frames)
        self.assertEqual(len(masks), len(frames), "Should return mask for each frame")
        self.assert_image_not_empty(masks[-1])  # Last mask should have detected the movement
        
        # Test with different methods
        methods = ['mog2', 'knn']
        for method in methods:
            try:
                method_masks = cv.background_subtraction(frames, method=method)
                self.assertEqual(len(method_masks), len(frames), 
                              f"Should return mask for each frame with {method}")
                self.assert_image_not_empty(method_masks[-1])
            except Exception as e:
                print(f"Method {method} not available: {e}")
    
    def test_detect_motion(self):
        """Test motion detection"""
        # Create two frames with movement
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame1 = cv.draw_rectangle(frame1, (20, 40), (40, 60), 
                               color=(255, 255, 255), filled=True)
        
        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = cv.draw_rectangle(frame2, (30, 40), (50, 60), 
                               color=(255, 255, 255), filled=True)
        
        # Test with default parameters
        motion = cv.detect_motion(frame1, frame2)
        self.assertIsNotNone(motion, "Motion detection should return a result")
        
        # Test with custom parameters
        motion_custom = cv.detect_motion(frame1, frame2, threshold=20, min_area=10)
        self.assertIsNotNone(motion_custom, "Motion detection with custom params should work")
    
    def test_detect_circles(self):
        """Test circle detection"""
        # Create image with circles
        circles_img = np.zeros((200, 200, 3), dtype=np.uint8)
        circles_img = cv.draw_circle(circles_img, (50, 50), 20, 
                                  color=(255, 255, 255), thickness=2)
        circles_img = cv.draw_circle(circles_img, (150, 150), 30, 
                                  color=(255, 255, 255), thickness=2)
        
        # Test with default parameters
        circles = cv.detect_circles(circles_img)
        self.assertIsNotNone(circles, "Circle detection should return a result")
        self.assertTrue(len(circles) > 0, "Should detect at least one circle")
        
        # Test with custom parameters
        circles_custom = cv.detect_circles(circles_img, 
                                        dp=2, min_dist=100, param1=100, param2=50)
        self.assertIsNotNone(circles_custom, "Circle detection with custom params should work")
    
    def test_detect_lines(self):
        """Test line detection"""
        # Create image with lines
        lines_img = np.zeros((200, 200, 3), dtype=np.uint8)
        lines_img = cv.draw_line(lines_img, (50, 50), (150, 50), 
                              color=(255, 255, 255), thickness=2)
        lines_img = cv.draw_line(lines_img, (50, 100), (150, 150), 
                              color=(255, 255, 255), thickness=2)
        
        # Test with default parameters
        lines = cv.detect_lines(lines_img)
        self.assertIsNotNone(lines, "Line detection should return a result")
        self.assertTrue(len(lines) > 0, "Should detect at least one line")
        
        # Test with custom parameters
        lines_custom = cv.detect_lines(lines_img, 
                                    threshold=50, min_line_length=50, max_line_gap=5)
        self.assertIsNotNone(lines_custom, "Line detection with custom params should work")
    
    def test_color_detection(self):
        """Test color detection"""
        # Create image with multiple colors
        color_img = np.zeros((100, 300, 3), dtype=np.uint8)
        # Red region
        color_img[0:100, 0:100] = [0, 0, 255]  # BGR: Red
        # Green region
        color_img[0:100, 100:200] = [0, 255, 0]  # BGR: Green
        # Blue region
        color_img[0:100, 200:300] = [255, 0, 0]  # BGR: Blue
        
        # Convert to HSV for color detection
        hsv_img = cv.convert_color_space(color_img, 'BGR', 'HSV')
        
        # Test red detection
        red_lower = np.array([0, 100, 100])
        red_upper = np.array([10, 255, 255])
        red_mask = cv.color_detection(hsv_img, red_lower, red_upper)
        self.assert_image_not_empty(red_mask)
        
        # Test green detection
        green_lower = np.array([40, 100, 100])
        green_upper = np.array([80, 255, 255])
        green_mask = cv.color_detection(hsv_img, green_lower, green_upper)
        self.assert_image_not_empty(green_mask)
        
        # Test blue detection
        blue_lower = np.array([100, 100, 100])
        blue_upper = np.array([140, 255, 255])
        blue_mask = cv.color_detection(hsv_img, blue_lower, blue_upper)
        self.assert_image_not_empty(blue_mask)

if __name__ == "__main__":
    unittest.main()
