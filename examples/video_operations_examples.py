"""
Examples demonstrating the use of video operations classes
"""

import os
import cv2
import numpy as np
from easy_opencv import cv

def create_sample_video(output_path, duration_sec=5, fps=30):
    """Create a sample video for testing"""
    frames = []
    frame_count = duration_sec * fps
    
    for i in range(frame_count):
        # Create a black canvas
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add frame number
        cv2.putText(frame, f"Frame {i+1}/{frame_count}", (50, 50), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Add moving circle
        x = int(320 + 250 * np.sin(i * 2 * np.pi / frame_count))
        y = int(240 + 150 * np.cos(i * 2 * np.pi / frame_count))
        cv2.circle(frame, (x, y), 30, (0, 0, 255), -1)
        
        # Add timestamp
        seconds = i / fps
        timestamp = f"{int(seconds // 60):02d}:{seconds % 60:05.2f}"
        cv2.putText(frame, timestamp, (500, 450), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        frames.append(frame)
    
    # Save video using legacy function
    cv.save_video(frames, output_path, fps=fps)
    print(f"Created sample video: {output_path} ({duration_sec}s at {fps}fps)")
    return output_path

def example_video_loader():
    """Example using VideoLoader class"""
    print("\nExample: VideoLoader")
    print("-" * 40)
    
    # Create sample video
    sample_video = create_sample_video("sample_video.mp4")
    
    # Create loader instance
    loader = cv.VideoLoader()
    
    # Load video
    video = loader.load(sample_video)
    
    # Get basic information
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Loaded video: {sample_video}")
    print(f"Resolution: {width}x{height}")
    print(f"FPS: {fps}")
    print(f"Frame count: {frame_count}")
    
    # Read first frame
    ret, first_frame = video.read()
    if ret:
        print("Successfully read first frame")
    
    # Release resources
    loader.release(video)
    
    print("VideoLoader example completed")

def example_frame_extractor():
    """Example using FrameExtractor class"""
    print("\nExample: FrameExtractor")
    print("-" * 40)
    
    # Create sample video
    sample_video = "sample_video.mp4"
    if not os.path.exists(sample_video):
        create_sample_video(sample_video)
    
    # Create output directory
    output_dir = "extracted_frames"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create extractor instance
    extractor = cv.FrameExtractor(default_output_format='jpg', default_quality=95)
    
    # Extract frames
    print("Extracting frames from video...")
    frame_paths = extractor.extract(
        sample_video,
        output_dir=output_dir,
        frame_interval=15,      # Extract every 15th frame
        max_frames=10,          # Maximum 10 frames
        output_format='jpg'     # Save as JPEG
    )
    
    print(f"Extracted {len(frame_paths)} frames to {output_dir}/")
    for i, path in enumerate(frame_paths):
        print(f"  Frame {i+1}: {os.path.basename(path)}")
    
    print("FrameExtractor example completed")

def example_video_analyzer():
    """Example using VideoAnalyzer class"""
    print("\nExample: VideoAnalyzer")
    print("-" * 40)
    
    # Create sample video
    sample_video = "sample_video.mp4"
    if not os.path.exists(sample_video):
        create_sample_video(sample_video)
    
    # Create analyzer instance
    analyzer = cv.VideoAnalyzer()
    
    # Get basic information
    print("Analyzing video...")
    info = analyzer.get_info(sample_video)
    
    print("Video information:")
    print(f"  Resolution: {info['width']}x{info['height']}")
    print(f"  FPS: {info['fps']}")
    print(f"  Duration: {info.get('duration_sec', 0):.2f} seconds")
    print(f"  Frame count: {info['frame_count']}")
    print(f"  Codec: {info['codec_fourcc']}")
    
    # Analyze motion
    print("\nAnalyzing motion...")
    motion = analyzer.analyze_motion(sample_video)
    
    print("Motion analysis:")
    print(f"  Frames analyzed: {motion['frames_analyzed']}")
    print(f"  Average motion: {motion['avg_motion']:.2f}")
    print(f"  Motion variability: {motion['motion_variability']:.2f}")
    print(f"  Significant motion: {'Yes' if motion['has_significant_motion'] else 'No'}")
    
    print("VideoAnalyzer example completed")

def example_video_player():
    """Example using VideoPlayer class"""
    print("\nExample: VideoPlayer")
    print("-" * 40)
    
    # Create sample video
    sample_video = "sample_video.mp4"
    if not os.path.exists(sample_video):
        create_sample_video(sample_video)
    
    # Create player instance
    player = cv.VideoPlayer(default_speed=1.0, default_loop=True)
    
    print("Playing video. Try these controls:")
    print("  Space - Play/Pause")
    print("  → - Forward 10 frames")
    print("  ← - Backward 10 frames")
    print("  + - Increase speed")
    print("  - - Decrease speed")
    print("  r - Restart video")
    print("  l - Toggle loop")
    print("  q or ESC - Quit")
    
    # Play video
    player.play(sample_video, window_name="VideoPlayer Example")
    
    print("VideoPlayer example completed")

def example_webcam_capture():
    """Example using WebcamCapture class"""
    print("\nExample: WebcamCapture")
    print("-" * 40)
    
    # Ask before running webcam example
    print("Do you want to run the webcam capture example? (y/n)")
    response = input("> ")
    if response.lower() != 'y':
        print("Skipping webcam example")
        return
    
    # Create capture instance
    capture = cv.WebcamCapture()
    
    # Output path
    output_path = "webcam_recording.mp4"
    
    print("Starting webcam capture. Try these controls:")
    print("  r - Start/Stop recording")
    print("  s - Take screenshot")
    print("  q or ESC - Quit")
    
    # Start capture
    capture.capture(
        camera_id=0,           # Default webcam
        save_path=output_path  # Save recording
    )
    
    # Check if video was recorded
    if os.path.exists(output_path):
        print(f"\nRecording saved to {output_path}")
        
        # Ask if user wants to play the recording
        print("Do you want to play the recording? (y/n)")
        response = input("> ")
        if response.lower() == 'y':
            # Play recording
            player = cv.VideoPlayer()
            player.play(output_path, window_name="Webcam Recording")
    
    print("WebcamCapture example completed")

def run_all_examples():
    """Run all examples"""
    print("Video Operations Classes Examples")
    print("=" * 50)
    
    # Run examples
    example_video_loader()
    example_frame_extractor()
    example_video_analyzer()
    example_video_player()
    example_webcam_capture()
    
    # Clean up files
    cleanup_files = [
        "sample_video.mp4",
        "webcam_recording.mp4"
    ]
    
    print("\nCleaning up...")
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"  Removed {file}")
    
    # Remove extracted frames
    extracted_frames_dir = "extracted_frames"
    if os.path.exists(extracted_frames_dir):
        frame_files = os.listdir(extracted_frames_dir)
        for file in frame_files:
            file_path = os.path.join(extracted_frames_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        os.rmdir(extracted_frames_dir)
        print(f"  Removed {extracted_frames_dir}/ directory and {len(frame_files)} files")
    
    print("\nAll examples completed!")

if __name__ == "__main__":
    run_all_examples()
