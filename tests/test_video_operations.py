"""
Tests for video operations module
"""
import os
import unittest
import tempfile
import numpy as np
import cv2
from easy_opencv.video_operations import (
    load_video, save_video, extract_frames, create_video_from_frames,
    get_video_info, play_video, webcam_capture
)
from tests.base_test_case import BaseTestCase


class TestVideoOperations(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a temporary directory to save test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a simple test video (small, fast to generate)
        self.test_frames = []
        for i in range(30):  # 30 frames
            # Create a black frame with a number on it
            frame = np.zeros((200, 200, 3), dtype=np.uint8)
            cv2.putText(frame, str(i), (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 255, 255), 2)
            self.test_frames.append(frame)
        
        # Save test video
        self.test_video_path = os.path.join(self.temp_dir, "test_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.test_video_path, fourcc, 30.0, (200, 200))
        for frame in self.test_frames:
            out.write(frame)
        out.release()

    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
        super().tearDown()

    def test_load_video(self):
        """Test loading a video file"""
        cap = load_video(self.test_video_path)
        self.assertTrue(cap.isOpened())
        
        # Check video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.assertEqual(width, 200)
        self.assertEqual(height, 200)
        cap.release()

    def test_save_video(self):
        """Test saving frames to a video file"""
        output_path = os.path.join(self.temp_dir, "output_video.mp4")
        result = save_video(self.test_frames, output_path, fps=30.0)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify the video contains the expected frames
        cap = cv2.VideoCapture(output_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.assertEqual(frame_count, len(self.test_frames))
        cap.release()

    def test_extract_frames(self):
        """Test extracting frames from a video file"""
        output_dir = os.path.join(self.temp_dir, "frames")
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract every 5th frame
        frame_paths = extract_frames(self.test_video_path, output_dir, frame_interval=5)
        
        # Verify frames were extracted correctly
        self.assertGreater(len(frame_paths), 0)
        self.assertTrue(all(os.path.exists(path) for path in frame_paths))
        self.assertEqual(len(frame_paths), 30 // 5 + (1 if 30 % 5 > 0 else 0))
        
        # Verify with max_frames limit
        frame_paths = extract_frames(self.test_video_path, output_dir, 
                                    frame_interval=1, max_frames=10)
        self.assertEqual(len(frame_paths), 10)

    def test_create_video_from_frames(self):
        """Test creating a video from image files"""
        output_dir = os.path.join(self.temp_dir, "frames")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save frames as images
        frame_paths = []
        for i, frame in enumerate(self.test_frames[:10]):
            path = os.path.join(output_dir, f"frame_{i:03d}.jpg")
            cv2.imwrite(path, frame)
            frame_paths.append(path)
        
        output_path = os.path.join(self.temp_dir, "recreated_video.mp4")
        result = create_video_from_frames(frame_paths, output_path, fps=15.0)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify video contains correct number of frames
        cap = cv2.VideoCapture(output_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.assertEqual(frame_count, len(frame_paths))
        cap.release()

    def test_get_video_info(self):
        """Test getting video information"""
        info = get_video_info(self.test_video_path)
        
        self.assertIsInstance(info, dict)
        self.assertEqual(info['width'], 200)
        self.assertEqual(info['height'], 200)
        self.assertEqual(info['fps'], 30.0)
        self.assertEqual(info['frame_count'], 30)
        
    # These tests are disabled by default as they require GUI
    def _test_play_video(self):
        """Test playing a video (requires GUI)"""
        # This is more of a visual test, so we just check it doesn't crash
        try:
            play_video(self.test_video_path, delay=1)
            self.assertTrue(True)  # If we get here without exception, it worked
        except Exception as e:
            self.fail(f"play_video raised an exception: {e}")

    def _test_webcam_capture(self):
        """Test webcam capture (requires camera hardware)"""
        # This is more of a visual test and requires hardware
        # So we just check it doesn't crash when capturing a few frames
        try:
            frames = webcam_capture(num_frames=5, delay=1)
            self.assertIsInstance(frames, list)
            self.assertGreater(len(frames), 0)
        except Exception as e:
            self.fail(f"webcam_capture raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
