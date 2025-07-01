# Video Operations Classes Guide

This guide explains the new class-based API for video operations in the Easy OpenCV library. These classes provide a more object-oriented approach to video processing while maintaining backward compatibility with the existing function-based API.

## Video Operations Classes Overview

The following classes are now available:

### VideoLoader

Class for loading videos from files or webcam sources.

```python
from easy_opencv import cv

# Creating a loader instance
loader = cv.VideoLoader()

# Loading a video file
video = loader.load("video.mp4")

# Loading from webcam
webcam = loader.load(0)  # 0 is the default webcam

# Don't forget to release when done
loader.release(video)
loader.release(webcam)
```

### VideoSaver

Class for saving videos with customizable parameters.

```python
from easy_opencv import cv

# Creating a saver instance with custom defaults
saver = cv.VideoSaver(default_codec='mp4v', default_fps=30.0)

# Saving frames as a video
frames = [...]  # List of image frames
saver.save(frames, "output_video.mp4")

# Creating a video from image files
frame_paths = ["frame1.jpg", "frame2.jpg", "frame3.jpg"]
saver.create_from_frame_paths(frame_paths, "output_video.mp4", fps=24.0)
```

### VideoPlayer

Class for playing videos with advanced playback controls.

```python
from easy_opencv import cv

# Creating a player instance
player = cv.VideoPlayer(default_speed=1.0, default_loop=False)

# Playing a video
player.play("video.mp4")

# Customizing playback
player.play("video.mp4",
          window_name="My Video",
          speed=1.5,
          loop=True,
          start_frame=30,
          end_frame=90)

# Controls available during playback:
# - Space: Play/Pause
# - →: Forward 10 frames
# - ←: Backward 10 frames
# - +: Increase speed
# - -: Decrease speed
# - r: Restart video
# - l: Toggle loop
# - q or ESC: Quit
```

### FrameExtractor

Class for extracting frames from videos.

```python
from easy_opencv import cv

# Creating an extractor instance
extractor = cv.FrameExtractor(default_output_format='jpg', default_quality=95)

# Extracting frames
frame_paths = extractor.extract(
    "video.mp4",
    output_dir="frames",
    frame_interval=5,     # Extract every 5th frame
    max_frames=20,        # Extract at most 20 frames
    output_format='png',  # Save as PNG
    quality=90            # PNG compression quality
)

# Extracted frame paths are returned
for path in frame_paths:
    print(path)
```

### VideoAnalyzer

Class for analyzing video properties and metadata.

```python
from easy_opencv import cv

# Creating an analyzer instance
analyzer = cv.VideoAnalyzer()

# Getting basic video information
info = analyzer.get_info("video.mp4")
print(f"Resolution: {info['width']}x{info['height']}")
print(f"Duration: {info['duration_formatted']}")
print(f"FPS: {info['fps']}")

# Analyzing motion in the video
motion_info = analyzer.analyze_motion("video.mp4", sample_size=50)
print(f"Average motion: {motion_info['avg_motion']}")
print(f"Has significant motion: {motion_info['has_significant_motion']}")
```

### WebcamCapture

Class for capturing video from webcams with recording capability.

```python
from easy_opencv import cv

# Creating a capture instance
capture = cv.WebcamCapture(default_codec='mp4v', default_fps=30.0)

# Simple webcam capture with recording
capture.capture(
    camera_id=0,                # Default webcam
    save_path="webcam_video.mp4" # Optional path to save recording
)

# Advanced webcam capture
capture.capture(
    camera_id=1,                # External webcam
    save_path="webcam_video.mp4",
    fps=60.0,                   # 60 FPS recording
    codec='avc1',               # H.264 codec
    width=1280,                 # Force 720p resolution
    height=720
)

# Multi-camera capture
capture.multi_camera_capture(
    camera_ids=[0, 1],          # Main and external webcam
    save_paths=["cam1.mp4", "cam2.mp4"]
)

# Controls available during webcam capture:
# - r: Start/Stop recording
# - s: Take screenshot
# - q or ESC: Quit
```

## Backward Compatibility

The original function-based API is still available and now uses these new classes internally. For example:

```python
# Legacy function (still works)
video = cv.load_video("video.mp4")

# New class-based approach
loader = cv.VideoLoader()
video = loader.load("video.mp4")
loader.release(video)
```

## Benefits of the Class-Based Approach

1. **Reusability**: Create a loader, player, or analyzer once and reuse it for multiple videos
2. **Configuration**: Set default parameters when creating the class instance
3. **Resource management**: Classes provide better methods for cleanup and resource release
4. **Extensibility**: Easier to extend with new features or customize for specific use cases
5. **Consistency**: Matches the object-oriented pattern used in other modules
6. **Webcam support**: Better handling of both file and webcam sources

## Implementation Notes

The video operations classes handle both video files and webcam streams with the same interface. All classes support error handling, default parameters, and comprehensive documentation.
