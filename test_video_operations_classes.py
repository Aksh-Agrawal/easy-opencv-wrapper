"""
Test script for the refactored video operations classes
"""

import os
import cv2
import numpy as np
from easy_opencv import cv  # Import the global EasyCV instance
from easy_opencv.video_operations import (
    VideoLoader, VideoSaver, VideoPlayer, FrameExtractor,
    VideoAnalyzer, WebcamCapture
)

def test_video_loader():
    """Test VideoLoader class"""
    print("\nTesting VideoLoader...")
    
    try:
        # Create a test video
        frames = []
        for i in range(30):  # 1 second at 30fps
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add frame number text
            cv2.putText(frame, f"Frame {i}", (50, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            frames.append(frame)
        
        # Save test video
        test_video_path = "test_video.mp4"
        cv.save_video(frames, test_video_path)
        
        # Test loader
        loader = VideoLoader()
        video = loader.load(test_video_path)
        
        # Check properties
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"  Video loaded successfully: {test_video_path}")
        print(f"  Frame count: {frame_count}")
        print(f"  Resolution: {width}x{height}")
        
        # Release resources
        loader.release(video)
        
        # Clean up
        os.remove(test_video_path)
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_video_analyzer():
    """Test VideoAnalyzer class"""
    print("\nTesting VideoAnalyzer...")
    
    try:
        # Create a test video
        frames = []
        for i in range(30):  # 1 second at 30fps
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add frame number text
            cv2.putText(frame, f"Frame {i}", (50, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # Add moving object
            cv2.circle(frame, (100 + i*10, 100), 20, (0, 0, 255), -1)
            frames.append(frame)
        
        # Save test video
        test_video_path = "test_video_analysis.mp4"
        cv.save_video(frames, test_video_path)
        
        # Test analyzer
        analyzer = VideoAnalyzer()
        info = analyzer.get_info(test_video_path)
        motion = analyzer.analyze_motion(test_video_path)
        
        # Print info
        print("  Video information:")
        for key, value in info.items():
            print(f"    {key}: {value}")
        
        print("  Motion analysis:")
        for key, value in motion.items():
            print(f"    {key}: {value}")
        
        # Clean up
        os.remove(test_video_path)
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_frame_extractor():
    """Test FrameExtractor class"""
    print("\nTesting FrameExtractor...")
    
    try:
        # Create a test video
        frames = []
        for i in range(10):  # 10 frames
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add frame number text
            cv2.putText(frame, f"Frame {i}", (50, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            frames.append(frame)
        
        # Save test video
        test_video_path = "test_video_extract.mp4"
        cv.save_video(frames, test_video_path)
        
        # Create output directory
        output_dir = "test_frames"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test extractor
        extractor = FrameExtractor()
        frame_paths = extractor.extract(test_video_path, output_dir, 
                                      frame_interval=2, max_frames=3)
        
        print(f"  Extracted {len(frame_paths)} frames")
        for path in frame_paths:
            print(f"    {path}")
        
        # Clean up
        os.remove(test_video_path)
        for path in frame_paths:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(output_dir) and len(os.listdir(output_dir)) == 0:
            os.rmdir(output_dir)
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def manual_test_video_player():
    """Manual test for VideoPlayer class"""
    print("\nTesting VideoPlayer (Manual Test)...")
    
    try:
        # Create a test video
        frames = []
        for i in range(60):  # 2 seconds at 30fps
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add frame number text
            cv2.putText(frame, f"Frame {i}", (50, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # Add a moving object
            x = i * 10 % 600
            cv2.circle(frame, (x + 20, 100), 30, (0, 0, 255), -1)
            frames.append(frame)
        
        # Save test video
        test_video_path = "test_video_player.mp4"
        cv.save_video(frames, test_video_path)
        
        print("  Playing video... (press 'q' to exit)")
        print("  Try using space to pause/play, and arrow keys to navigate")
        
        # Test player
        player = VideoPlayer(default_speed=1.0, default_loop=True)
        player.play(test_video_path, "Video Player Test")
        
        # Clean up
        os.remove(test_video_path)
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def manual_test_webcam_capture():
    """Manual test for WebcamCapture class"""
    print("\nTesting WebcamCapture (Manual Test)...")
    
    try:
        print("  Do you want to run webcam capture test? (y/n)")
        response = input("  > ")
        
        if response.lower() != 'y':
            print("  Skipping webcam test...")
            return True
        
        # Test path for saving
        test_video_path = "webcam_test.mp4"
        
        print("  Starting webcam capture... (press 'q' to exit, 'r' to toggle recording)")
        
        # Test webcam capture
        capture = WebcamCapture()
        capture.capture(camera_id=0, save_path=test_video_path)
        
        # Check if file was created
        if os.path.exists(test_video_path):
            print(f"  Webcam video saved to {test_video_path}")
            
            # Offer to play the recorded video
            print("  Do you want to play the recorded video? (y/n)")
            response = input("  > ")
            
            if response.lower() == 'y':
                player = VideoPlayer()
                player.play(test_video_path)
            
            # Clean up
            os.remove(test_video_path)
        
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Running Video Operations Classes Tests")
    print("=" * 40)
    
    tests = [
        ("VideoLoader", test_video_loader),
        ("VideoAnalyzer", test_video_analyzer),
        ("FrameExtractor", test_frame_extractor),
        ("VideoPlayer", manual_test_video_player),
        ("WebcamCapture", manual_test_webcam_capture)
    ]
    
    results = {}
    
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        success = test_func()
        results[name] = "PASSED" if success else "FAILED"
    
    print("\nTest Results:")
    print("=" * 40)
    for name, result in results.items():
        print(f"{name.ljust(20)}: {result}")
    
    if all(result == "PASSED" for result in results.values()):
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    run_all_tests()
