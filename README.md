# Easy OpenCV - Simplified Computer Vision Package

![Easy OpenCV](https://img.shields.io/badge/Easy-OpenCV-green)
![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenCV 4.5+](https://img.shields.io/badge/OpenCV-4.5%2B-blue)
[![PyPI version](https://img.shields.io/pypi/v/easy-opencv-wrapper.svg)](https://pypi.org/project/easy-opencv-wrapper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Downloads](https://static.pepy.tech/badge/easy-opencv-wrapper)](https://pepy.tech/projects/easy-opencv-wrapper)

<br>

A powerful yet user-friendly OpenCV wrapper that makes computer vision accessible for everyone. Easy OpenCV provides a streamlined interface to perform complex computer vision operations with simple, intuitive function calls.

> **"Computer vision simplified with human-readable function calls and sensible defaults"**

## 🚀 Installation

### Step 1: Install the Package

```bash
pip install easy-opencv-wrapper
```

### Step 2: Import and Use

```python
from easy_opencv import cv  # Note: underscores, not hyphens!
```

**Requirements**: Python 3.7+ • OpenCV 4.5+ • NumPy 1.19+ • Pillow 8.0+

> **📋 Critical**: The PyPI package name is `easy-opencv-wrapper` (with hyphens), but you import it as `easy_opencv` (with underscores). This is standard Python convention. See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for troubleshooting.

### ⚠️ Common Import Mistake

```python
# ❌ WRONG - These will cause ModuleNotFoundError
import easy_opencv_wrapper
import easy-opencv

# ✅ CORRECT - This is how you import Easy OpenCV
from easy_opencv import cv
```

### 🔍 Verify Your Installation

Run our verification script to test your installation:

```bash
python verify_import.py
```

This script will test both correct and incorrect imports and verify basic functionality.

## 🎯 Quick Start

```python
from easy_opencv import cv

# Load and enhance image (handles errors automatically)
image = cv.load_image('photo.jpg')
enhanced = cv.apply_noise_reduction(image)
enhanced = cv.adjust_brightness_contrast(enhanced, brightness=10, contrast=1.2)

# Detect faces and draw boxes
faces = cv.detect_faces(enhanced)
for (x, y, w, h) in faces:
    enhanced = cv.draw_rectangle(enhanced, (x, y), (x+w, y+h), color=(0, 255, 0))

# Save result
cv.save_image(enhanced, 'enhanced_photo.jpg')
```

## Why Choose Easy OpenCV?

Easy OpenCV dramatically reduces the complexity of computer vision code while maintaining all the power of OpenCV underneath. It helps you:

- **Write 50-70% less code** for common tasks
- **Eliminate boilerplate code** with smart defaults
- **Focus on your application** instead of OpenCV's complex API
- **Reduce errors** with built-in validation and clearer error messages
- **Learn computer vision concepts** with intuitive function names

### 🎯 Side-by-Side Comparison

```python
# OpenCV original:
img = cv2.imread('image.jpg')
if img is None:
    raise FileNotFoundError("Image not found")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
blurred = cv2.GaussianBlur(img_rgb, (15, 15), 0)
edges = cv2.Canny(blurred, 100, 200)

# Easy OpenCV equivalent:
img = cv.load_image('image.jpg', mode='rgb')  # Load and convert in one step
blurred = cv.apply_gaussian_blur(img, kernel_size=15)
edges = cv.apply_edge_detection(blurred)
```

📝 **See [DIFFERENCE.md](DIFFERENCE.md) for 22+ side-by-side code comparisons** and [EASY_OPENCV_BENEFITS.md](EASY_OPENCV_BENEFITS.md) for detailed benefits analysis.

## ✨ Key Features

- **Intuitive API Design**: Human-readable function names and parameters
- **Intelligent Defaults**: Functions work out-of-the-box with sensible parameters
- **Automatic Processing**: Many preprocessing steps are handled automatically
- **Built-in Error Handling**: Validation and clear error messages
- **Comprehensive Documentation**: Every function has detailed docstrings with examples

### 📦 Core Modules

- **Image Operations**: Load, save, resize, crop, and convert images with simple function calls
- **Video Processing**: Handle video files, extract frames, and create videos from image sequences
- **Image Processing**: Apply filters, enhance images, and perform various image transformations
- **Feature Detection**: Detect corners, keypoints, contours, and match features between images
- **Object Detection**: 🆕 **Class-based system with automatic webcam fallback** - Face, eye, motion, and DNN object detection
- **Drawing Operations**: Draw shapes, text, and annotations on images
- **Filters**: Apply various filters including blur, sharpen, vintage, cartoon effects
- **Transformations**: Rotate, flip, warp, and apply perspective transformations
- **Utilities**: Helper functions for FPS counting, color picking, and image comparison

### 🎥 NEW: Object Detection with Webcam Support

Easy OpenCV now features a powerful class-based object detection system with **automatic webcam fallback**:

```python
from easy_opencv import FaceDetector, EyeDetector, ColorDetector

# 🎯 Face detection with automatic webcam fallback
detector = FaceDetector()
results = detector.detect_from_source()  # Uses webcam if no source provided

# 🎨 Detect red objects from webcam
color_detector = ColorDetector(target_color='red')
results = color_detector.detect_from_source()

# 📹 Motion detection with live preview
motion_detector = MotionDetector()
results = motion_detector.detect_from_source(show_live=True)

# 🎥 Alternative webcam access methods
video = cv.load_video(0)  # Use camera index 0 (default webcam)
# Or use the WebcamCapture class for more control
webcam = cv.WebcamCapture()
webcam.capture(camera_id=0, save_path="recording.mp4")  # With optional recording
```

**Key Features:**

- 🎥 **Automatic webcam fallback** when no image/video path provided
- 📁 Support for images, videos, and live webcam streams
- 🎛️ Reusable detector objects with custom parameters
- 👀 Built-in live visualization with bounding boxes
- 🔄 Full backward compatibility with legacy functions

### 🔧 Webcam Usage Tips

For reliable webcam access, there are several approaches:

```python
# Method 1: Using the load_video function with camera index
video = cv.load_video(0)  # 0 = default webcam
while True:
    ret, frame = video.read()
    if not ret:
        break
    # Process frame
    cv.show_image(frame, 'Video', wait=False)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()

# Method 2: Using WebcamCapture class for interactive controls
webcam = cv.WebcamCapture()
webcam.capture(camera_id=0)  # Interactive session with keyboard controls

# Method 3: Using object detectors with built-in webcam support
detector = FaceDetector()
detector.detect_from_source(source=None)  # None defaults to webcam
```

> **⚠️ Note:** When using `cv.show_image()` in a video loop, set `wait=False` to prevent blocking.

## 🚀 Installation

### From PyPI (recommended)

```bash
pip install easy-opencv
```

### From Source

```bash
git clone https://github.com/yourusername/easy-opencv.git
cd easy-opencv
pip install -r requirements.txt
pip install -e .
```

### Requirements

- Python 3.7+
- OpenCV 4.5.0+
- NumPy 1.19.0+
- Pillow 8.0.0+

## 🏁 Quick Start

### Basic Usage

```python
from easy_opencv import cv

# Load an image (automatically handles errors and converts to preferred format)
image = cv.load_image('path/to/image.jpg', mode='rgb')

# Get image information
info = cv.get_image_info(image)
print(f"Image dimensions: {info['width']}x{info['height']}, channels: {info['channels']}")

# Resize with aspect ratio preservation
resized = cv.resize_image(image, width=800)  # Height calculated automatically

# Apply a filter with one simple function call
blurred = cv.apply_gaussian_blur(image, kernel_size=15)

# Show the result (handles window creation and keypress waiting)
cv.show_image(blurred, 'Blurred Image')

# Save the result with quality control
cv.save_image(blurred, 'output.jpg', quality=95)
```

### Face Detection Example

```python
from easy_opencv import cv

# Load image (handles errors automatically)
image = cv.load_image('portrait.jpg')

# Detect faces with simple parameters
faces = cv.detect_faces(image, scale_factor=1.1, min_neighbors=5)

# Process each face
for i, (x, y, w, h) in enumerate(faces):
    # Draw rectangle with built-in function
    image = cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)

    # Add label with customization options
    image = cv.draw_text(image, f"Face {i+1}", (x, y-10),
                         font_scale=0.5, color=(255, 255, 255),
                         background=True, bg_color=(0, 200, 0))

    # Extract face region for further processing
    face_img = cv.crop_image(image, x, y, w, h)

    # Detect eyes within the face
    eyes = cv.detect_eyes(face_img)
    print(f"Found {len(eyes)} eyes in face {i+1}")

# Save and display the result
cv.save_image(image, 'detected_faces.jpg')
cv.show_image(image, 'Face Detection Results')
```

### Creative Effects Pipeline

```python
from easy_opencv import cv

# Start with a single image
image = cv.load_image('scene.jpg')

# Create multiple processed versions
grayscale = cv.convert_color_space(image, 'rgb', 'gray')
blurred = cv.apply_gaussian_blur(image, kernel_size=15)
edges = cv.apply_edge_detection(image)
vintage = cv.apply_vintage_filter(image, intensity=0.7)
cartoon = cv.apply_cartoon_filter(image)

# Create a comparison grid with labels
images = [image, grayscale, blurred, edges, vintage, cartoon]
labels = ["Original", "Grayscale", "Blurred", "Edges", "Vintage", "Cartoon"]

# Add labels to images
labeled_images = []
for img, label in zip(images, labels):
    img_with_label = cv.draw_text(img.copy(), label, (10, 30),
                                  font_scale=0.8, color=(255, 255, 255),
                                  background=True)
    labeled_images.append(img_with_label)

# Create image grid (automatically handles different sized images)
grid = cv.create_image_grid(labeled_images, grid_size=(2, 3))

# Show the results
cv.show_image(grid, "Image Processing Effects")
```

## 📚 Module Overview

### 📷 Image Operations

| Function                                                       | Description                          | Key Features                                   |
| -------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| `load_image(path, mode='color')`                               | Load images in different color modes | Handles errors, auto-converts color spaces     |
| `save_image(image, path, quality=95)`                          | Save images with quality control     | Supports multiple formats, compression control |
| `resize_image(image, width=None, height=None, scale=None)`     | Flexible image resizing              | Preserves aspect ratio, multiple methods       |
| `crop_image(image, x, y, width, height)`                       | Crop images to specified regions     | Boundary checking, aspect ratio options        |
| `convert_color_space(image, src_space='bgr', dst_space='rgb')` | Convert between color spaces         | Intuitive naming ('rgb' vs 'COLOR_BGR2RGB')    |
| `merge_channels(channels)`                                     | Merge image channels                 | Automatic validation                           |
| `split_channels(image)`                                        | Split image into channels            | Returns named tuple for clarity                |

### 🎬 Video Operations

🆕 **NEW Class-Based API with Webcam Support:**

```python
# Import the new video operation classes
from easy_opencv import VideoLoader, VideoPlayer, WebcamCapture, VideoAnalyzer

# Load video files or webcam streams
loader = VideoLoader()
video = loader.load("video.mp4")  # or loader.load(0) for webcam

# Play videos with advanced controls
player = VideoPlayer(default_speed=1.0, default_loop=True)
player.play("video.mp4")  # Interactive playback with controls

# Analyze video content
analyzer = VideoAnalyzer()
info = analyzer.get_info("video.mp4")
motion_data = analyzer.analyze_motion("video.mp4")

# Capture from webcam with recording
webcam = WebcamCapture()
webcam.capture(camera_id=0, save_path="recording.mp4")
```

**Available Video Classes:**

- `VideoLoader` - Loading videos from files or webcam sources
- `VideoSaver` - Saving videos with customizable parameters
- `VideoPlayer` - Playing videos with advanced playback controls
- `FrameExtractor` - Extracting frames from videos
- `VideoAnalyzer` - Analyzing video properties and motion
- `WebcamCapture` - Capturing from webcams with interactive controls

**Legacy Functions (Still Supported):**

| Function                                                        | Description                        | Key Features                             |
| --------------------------------------------------------------- | ---------------------------------- | ---------------------------------------- |
| `load_video(path)`                                              | Load video files                   | Metadata extraction, error handling      |
| `extract_frames(video_path, output_dir, frame_interval=1)`      | Extract frames from videos         | Progress tracking, flexible naming       |
| `create_video_from_frames(frame_paths, output_path, fps=30.0)`  | Create videos from image sequences | Auto resolution detection, codec options |
| `webcam_capture(camera_id=0, save_path=None)`                   | Capture from webcam                | Interactive controls, recording options  |
| `get_video_info(video_path)`                                    | Get video metadata                 | FPS, resolution, duration, codec         |
| `apply_video_filter(video_path, filter_func, output_path=None)` | Process entire videos              | Progress bar, parallel processing        |

### 🖼️ Image Processing

| Function                                                        | Description                    | Key Features                                   |
| --------------------------------------------------------------- | ------------------------------ | ---------------------------------------------- |
| `apply_blur(image, blur_type='gaussian', strength=5)`           | Apply various blur effects     | Multiple algorithms, automatic kernel handling |
| `apply_edge_detection(image, method='canny')`                   | Edge detection algorithms      | Auto-threshold, pre-processing                 |
| `apply_threshold(image, threshold_type='binary')`               | Thresholding techniques        | Multiple methods, auto-threshold option        |
| `adjust_brightness_contrast(image, brightness=0, contrast=1.0)` | Brightness/contrast adjustment | Preview option, clip protection                |
| `equalize_histogram(image, adaptive=False)`                     | Enhance image contrast         | CLAHE adaptive option                          |
| `remove_noise(image, method='median')`                          | Noise removal                  | Multiple algorithms                            |
| `sharpen_image(image, strength=1.0)`                            | Sharpen images                 | Unsharp mask option                            |
| `invert_colors(image)`                                          | Invert image colors            | Handles all color spaces                       |

### 🔍 Feature Detection

| Function                                          | Description                    | Key Features                         |
| ------------------------------------------------- | ------------------------------ | ------------------------------------ |
| `detect_corners(image, method='harris')`          | Corner detection               | Multiple algorithms, filtration      |
| `detect_keypoints(image, detector='sift')`        | Keypoint detection             | Multiple detectors (SIFT, ORB, etc.) |
| `match_features(desc1, desc2, method='bf')`       | Feature matching               | Ratio test, RANSAC options           |
| `detect_contours(image, threshold_value=127)`     | Contour detection              | Hierarchy, filtering options         |
| `find_template(image, template, method='ccoeff')` | Template matching              | Multiple methods, threshold          |
| `find_lines(image, method='hough')`               | Line detection                 | Standard and probabilistic Hough     |
| `find_circles(image)`                             | Circle detection               | Parameter optimization               |
| `match_histograms(source, reference)`             | Match histogram between images | Channel-wise matching                |

### 🎯 Object Detection

🆕 **NEW Class-Based API with Webcam Support:**

```python
# Import the new detection classes
from easy_opencv import FaceDetector, EyeDetector, ColorDetector, MotionDetector

# Face detection with automatic webcam fallback
face_detector = FaceDetector(scale_factor=1.1, min_neighbors=5)
results = face_detector.detect_from_source()  # Uses webcam automatically

# Color detection from webcam
color_detector = ColorDetector(target_color='red', tolerance=20)
results = color_detector.detect_from_source(show_live=True)

# Motion detection with video output
motion_detector = MotionDetector(sensitivity=500)
results = motion_detector.detect_from_source(output_path="motion.mp4")
```

**Available Detector Classes:**

- `FaceDetector` - Face detection using Haar cascades
- `EyeDetector` - Eye detection using Haar cascades
- `CascadeDetector` - Generic cascade detector for custom XML files
- `MotionDetector` - Motion detection with background subtraction
- `CircleDetector` - Circle detection using Hough Transform
- `LineDetector` - Line detection using Hough Transform
- `ColorDetector` - Color-based object detection in HSV space
- `DNNObjectDetector` - Deep learning object detection (SSD MobileNet V2)

**Legacy Functions (Still Supported):**

| Function                                     | Description           | Key Features                             |
| -------------------------------------------- | --------------------- | ---------------------------------------- |
| `detect_faces(image, scale_factor=1.1)`      | Face detection        | Multiple models, confidence control      |
| `detect_eyes(image, scale_factor=1.1)`       | Eye detection         | Works within face regions                |
| `detect_motion(video_path, sensitivity=500)` | Motion detection      | ROI selection, threshold control         |
| `color_detection(image, target_color='red')` | Color-based detection | HSV/RGB support, tolerance setting       |
| `detect_objects_dnn(image)`                  | DNN object detection  | Pre-trained models, confidence threshold |

### 🎨 Drawing Operations

| Function                                                         | Description                  | Key Features                   |
| ---------------------------------------------------------------- | ---------------------------- | ------------------------------ |
| `draw_rectangle(image, start_point, end_point, color=(0,255,0))` | Draw rectangles              | Fill, opacity, rounded corners |
| `draw_circle(image, center, radius, color=(0,255,0))`            | Draw circles                 | Fill, opacity control          |
| `draw_text(image, text, position, font_scale=1.0)`               | Add text to images           | Background, auto-positioning   |
| `draw_bounding_boxes(image, boxes, labels=None)`                 | Draw multiple bounding boxes | Labels, confidence scores      |
| `draw_polygon(image, points, color=(0,255,0))`                   | Draw polygons                | Fill, antialiased              |
| `draw_arrow(image, start_point, end_point, color=(0,255,0))`     | Draw arrows                  | Width, head size control       |
| `draw_grid(image, grid_size, color=(128,128,128))`               | Draw grid lines              | Thickness, style options       |
| `draw_crosshair(image, position, size=20, color=(0,255,0))`      | Draw crosshair               | Thickness, style options       |

### 🌈 Filters

| Function                                     | Description              | Key Features            |
| -------------------------------------------- | ------------------------ | ----------------------- |
| `apply_gaussian_blur(image, kernel_size=15)` | Gaussian blur filter     | Auto odd kernel size    |
| `apply_vintage_filter(image, intensity=0.5)` | Vintage/sepia effect     | Adjustable intensity    |
| `apply_cartoon_filter(image)`                | Cartoon effect           | Style parameters        |
| `apply_motion_blur(image, size=15, angle=0)` | Motion blur effect       | Direction control       |
| `apply_emboss_filter(image)`                 | Emboss effect            | Strength, direction     |
| `apply_pencil_sketch(image, strength=0.5)`   | Pencil sketch effect     | Color/grayscale options |
| `apply_hdr_effect(image)`                    | HDR effect               | Intensity control       |
| `apply_custom_kernel(image, kernel)`         | Apply custom convolution | Border handling options |

### 🔄 Transformations

| Function                                                     | Description                   | Key Features                 |
| ------------------------------------------------------------ | ----------------------------- | ---------------------------- |
| `rotate_image(image, angle, center=None)`                    | Rotate images                 | Auto center, border handling |
| `flip_image(image, direction='horizontal')`                  | Flip images                   | Multiple directions          |
| `apply_perspective_transform(image, src_points, dst_points)` | Perspective transformation    | Auto size preservation       |
| `apply_fisheye_effect(image, strength=0.5)`                  | Fisheye lens effect           | Adjustable strength          |
| `warp_image(image, transform_matrix)`                        | Apply affine/perspective warp | Border handling              |
| `translate_image(image, x_shift, y_shift)`                   | Translate images              | Border handling              |
| `resize_with_padding(image, width, height)`                  | Resize with padding           | Border color, position       |
| `apply_barrel_distortion(image, strength=0.5)`               | Barrel distortion             | Center point, strength       |

### 🛠️ Utilities

| Function                                                  | Description               | Key Features                 |
| --------------------------------------------------------- | ------------------------- | ---------------------------- |
| `fps_counter()`                                           | FPS measurement           | Running average, display     |
| `color_picker(image)`                                     | Interactive color picking | RGB/HSV display, zoom        |
| `image_comparison(image1, image2, method='side_by_side')` | Compare images            | Multiple methods             |
| `create_image_grid(images, grid_size)`                    | Create image grids        | Auto-sizing, padding, titles |
| `apply_watermark(image, text)`                            | Add watermarks            | Position, opacity            |
| `get_dominant_colors(image, num_colors=5)`                | Extract dominant colors   | K-means clustering           |
| `auto_canny(image, sigma=0.33)`                           | Automatic edge detection  | Adaptive thresholds          |
| `get_image_hash(image, hash_method='phash')`              | Generate image hash       | Multiple algorithms          |

## 💻 Advanced Usage Examples

### Image Processing Workflow

```python
from easy_opencv import cv

# Load and process an image with error handling
try:
    image = cv.load_image('input.jpg', mode='rgb')
except Exception as e:
    print(f"Error loading image: {e}")
    image = cv.create_blank_image(800, 600, color=(240, 240, 240))  # Create blank image as fallback

# Get image information
info = cv.get_image_info(image)
print(f"Image size: {info['width']}x{info['height']}, {info['channels']} channels, {info['dtype']} type")

# Resize with aspect ratio preservation (multiple methods available)
resized = cv.resize_image(image, width=800, method='lanczos')  # Higher quality algorithm

# Apply enhancement pipeline
enhanced = image.copy()
enhanced = cv.remove_noise(enhanced, method='bilateral')  # Preserve edges while removing noise
enhanced = cv.adjust_brightness_contrast(enhanced, brightness=10, contrast=1.2)
enhanced = cv.apply_unsharp_mask(enhanced, radius=2.0, amount=1.0)  # Sharpen details

# Create side-by-side comparison with labels
comparison = cv.image_comparison(image, enhanced, method='side_by_side', labels=['Original', 'Enhanced'])
cv.save_image(comparison, 'comparison.jpg', quality=95)
```

### Advanced Object Detection

```python
from easy_opencv import cv
import time

# Start the FPS counter
fps = cv.fps_counter()

# Load an image with faces
image = cv.load_image('group_photo.jpg', mode='rgb')

# Face detection with confidence control
faces = cv.detect_faces(image, scale_factor=1.1, min_neighbors=5, min_size=(30, 30))
print(f"Found {len(faces)} faces in the image")

# For each face, detect features and add annotations
result = image.copy()
for i, (x, y, w, h) in enumerate(faces):
    # Extract the face region
    face_img = cv.crop_image(image, x, y, w, h)

    # Get the face region information
    face_info = f"Face {i+1}"

    # Detect eyes within this face
    eyes = cv.detect_eyes(face_img)
    if len(eyes) > 0:
        face_info += f" ({len(eyes)} eyes)"

    # Try to detect a smile
    smile_detected = cv.detect_smile(face_img)
    if smile_detected:
        face_info += ", smiling"

    # Draw enhanced bounding box with information
    result = cv.draw_rectangle(result, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    result = cv.draw_text(result, face_info, (x, y-10), font_scale=0.5,
                         color=(255, 255, 255), background=True, bg_color=(0, 128, 0))

# Color-based object detection in HSV space for more robust detection
red_mask = cv.color_detection(image, target_color='red', color_space='hsv', tolerance=15)
red_objects = cv.detect_contours(red_mask, min_area=100)
print(f"Found {len(red_objects)} red objects")

# Add red object outlines to the result
result = cv.draw_contour(result, red_objects, color=(0, 0, 255), thickness=2)

# Calculate and display FPS
fps_value = fps.get()
result = cv.draw_text(result, f"FPS: {fps_value:.1f}", (10, 30), font_scale=0.7,
                     color=(255, 255, 255), background=True)

# Save the final result
cv.save_image(result, 'detection_results.jpg')
```

### Feature Detection and Matching

```python
from easy_opencv import cv

# Load two images for feature matching
img1 = cv.load_image('scene.jpg', mode='rgb')
img2 = cv.load_image('object.jpg', mode='rgb')

# Detect keypoints and compute descriptors (SIFT by default)
keypoints1, descriptors1 = cv.detect_keypoints(img1, detector='sift')
keypoints2, descriptors2 = cv.detect_keypoints(img2, detector='sift')

print(f"Found {len(keypoints1)} keypoints in image 1")
print(f"Found {len(keypoints2)} keypoints in image 2")

# Match features between images
matches = cv.match_features(descriptors1, descriptors2, method='flann', ratio_threshold=0.7)
print(f"Found {len(matches)} good matches")

# Draw matches between images
match_img = cv.draw_matches(img1, keypoints1, img2, keypoints2, matches)

# Draw keypoints on original images
img1_kp = cv.draw_keypoints(img1, keypoints1)
img2_kp = cv.draw_keypoints(img2, keypoints2)

# Create a comparison grid
grid = cv.create_image_grid([img1_kp, img2_kp, match_img],
                           grid_size=(2, 2),
                           labels=["Image 1 Keypoints", "Image 2 Keypoints", "Matches"])

cv.show_image(grid, "Feature Matching")
```

### Video Processing and Analysis

```python
from easy_opencv import cv
import os

# Get information about a video file
video_info = cv.get_video_info('input_video.mp4')
print(f"Video dimensions: {video_info['width']}x{video_info['height']}")
print(f"Frame rate: {video_info['fps']:.2f} fps, Duration: {video_info['duration']:.2f} seconds")
print(f"Total frames: {video_info['frame_count']}, Codec: {video_info['codec']}")

# Extract frames with progress tracking
output_dir = 'extracted_frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Extract every 10th frame (10% of the video) with progress feedback
frame_paths = cv.extract_frames('input_video.mp4', output_dir,
                               frame_interval=10,
                               show_progress=True,
                               filename_format='frame_{:04d}.jpg')

print(f"Extracted {len(frame_paths)} frames to {output_dir}")

# Process extracted frames with a filter
processed_frames = []
for frame_path in frame_paths:
    frame = cv.load_image(frame_path)
    processed = cv.apply_vintage_filter(frame, intensity=0.6)
    output_path = frame_path.replace('.jpg', '_vintage.jpg')
    cv.save_image(processed, output_path)
    processed_frames.append(output_path)

# Create a new video from processed frames with custom settings
cv.create_video_from_frames(
    processed_frames,
    'vintage_video.mp4',
    fps=24.0,
    codec='mp4v',  # Codec options: 'mp4v', 'avc1', 'xvid', etc.
    size=None,     # Auto-detect from first frame
    is_color=True
)

# Motion detection with mask and visualization
cv.detect_motion(
    'input_video.mp4',
    'motion_output.mp4',
    sensitivity=500,
    min_area=500,
    blur_size=15,
    dilate_iterations=2,
    draw_bounding_boxes=True,
    show_progress=True
)
```

### Interactive Tools and Visualization

```python
from easy_opencv import cv
import numpy as np

# Create a blank canvas for drawing
canvas = cv.create_blank_image(800, 600, color=(240, 240, 240))

# Interactive color picker tool (click to get color values)
def on_color_pick(color, x, y):
    print(f"Picked color at ({x}, {y}): RGB={color}, HEX=#{color[0]:02x}{color[1]:02x}{color[2]:02x}")

cv.color_picker(image, window_name='Color Picker', callback=on_color_pick)

# Compare image processing methods with custom layout
original = cv.load_image('sample.jpg')
methods = {
    'Original': original,
    'Grayscale': cv.convert_color_space(original, 'rgb', 'gray'),
    'Blurred': cv.apply_gaussian_blur(original, kernel_size=15),
    'Edges': cv.apply_edge_detection(original),
    'Cartoon': cv.apply_cartoon_filter(original),
    'Vintage': cv.apply_vintage_filter(original)
}

# Create a comparison with multiple layouts
comparisons = {
    'Side by Side': cv.image_comparison(methods['Original'], methods['Cartoon'], method='side_by_side'),
    'Slider': cv.image_comparison(methods['Original'], methods['Vintage'], method='slider'),
    'Split': cv.image_comparison(methods['Original'], methods['Edges'], method='split'),
    'Blend': cv.image_comparison(methods['Original'], methods['Blurred'], method='blend', alpha=0.5)
}

# Create image grid with auto-sizing and labels
grid = cv.create_image_grid(
    list(methods.values()),
    grid_size=(2, 3),
    image_size=(300, 200),  # Target size for each grid cell
    padding=10,            # Padding between images
    background_color=(20, 20, 20),
    labels=list(methods.keys())
)

# Add watermark
grid = cv.apply_watermark(
    grid,
    text="Easy OpenCV Demo",
    position='bottom_right',
    font_scale=0.8,
    color=(255, 255, 255),
    opacity=0.7
)

cv.show_image(grid, 'Effect Comparison')

# Analyze image histograms
hist = cv.calculate_histogram(original)
hist_image = cv.draw_histogram(hist, size=(600, 400))
cv.show_image(hist_image, 'RGB Histogram')
```

### Real-Time Processing

```python
from easy_opencv import cv

# Start webcam capture with options
def frame_processor(frame):
    """Process each frame from the webcam"""
    # Apply real-time cartoon effect
    cartoon = cv.apply_cartoon_filter(frame)

    # Add FPS counter to the frame
    fps = cv.fps_counter().get()
    cartoon = cv.draw_text(cartoon, f"FPS: {fps:.1f}", (10, 30),
                          font_scale=0.7, color=(255, 255, 255), background=True)
    return cartoon

# Start webcam capture with the frame processor
cv.webcam_capture(
    camera_id=0,              # Use default camera
    frame_processor=frame_processor,
    window_name="Cartoon Webcam",
    save_path="webcam_recording.mp4",  # Optional recording
    record_fps=30.0,
    width=640,
    height=480
)
```

## 🔧 Troubleshooting

### Common Errors and Solutions

#### Module Import Issues

**Error:** `ModuleNotFoundError: No module named 'easy_opencv_wrapper'`  
**Solution:** Use the correct import statement: `from easy_opencv import cv`

**Error:** `ModuleNotFoundError: No module named 'easy-opencv'`  
**Solution:** The package name uses underscores in imports, not hyphens: `from easy_opencv import cv`

#### Webcam Access Problems

**Error:** `AttributeError: 'EasyCV' object has no attribute 'open_webcam'`  
**Solution:** Use `cv.load_video(0)` instead for webcam access, or the `WebcamCapture` class.

**Error:** Webcam freezes when using `show_image` in a loop  
**Solution:** Set `wait=False` in `cv.show_image()` when using it in a video loop.

```python
# Correct way to use show_image in a video loop
while True:
    ret, frame = video.read()
    if not ret:
        break

    cv.show_image(frame, 'Video', wait=False)  # Set wait=False to prevent blocking

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

#### Video Frame Processing

**Error:** No key detection when processing video frames  
**Solution:** Use direct OpenCV for keyboard detection:

```python
import cv2  # Import OpenCV directly for keyboard handling

# In your video loop
if cv2.waitKey(1) & 0xFF == ord('q'):
    break  # Exit on 'q' key press
```

### Getting Help

If you encounter problems not covered in this troubleshooting guide:

1. Check our [Documentation](./Documentation/) folder for more examples
2. See [DIFFERENCE.md](DIFFERENCE.md) for detailed code comparisons
3. File an issue on our GitHub repository
4. Join our community Discord server for live help

Remember that Easy OpenCV is a wrapper around OpenCV, so you can always mix both APIs when needed for specific functionality.

## 📋 Requirements

- **Python 3.7+**: Core language support
- **OpenCV 4.5.0+**: Core computer vision functionality
- **NumPy 1.19.0+**: Numerical processing
- **Pillow 8.0.0+**: Image processing support

## 📚 Additional Resources

| Resource                                           | Description                                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [DIFFERENCES.md](DIFFERENCES.md)                   | **22+ Side-by-side code comparisons** between OpenCV and Easy OpenCV for common tasks |
| [EASY_OPENCV_BENEFITS.md](EASY_OPENCV_BENEFITS.md) | Detailed analysis of **benefits and performance considerations**                      |
| [USAGE_GUIDE.md](USAGE_GUIDE.md)                   | Comprehensive guide with detailed explanations and **step-by-step tutorials**         |
| [WHY_EASY_OPENCV.md](WHY_EASY_OPENCV.md)           | In-depth explanation of **design philosophy** and technical benefits                  |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)       | **Package organization** and module overview for developers                           |
| [TEST_ANALYSIS_REPORT.md](TEST_ANALYSIS_REPORT.md) | Detailed test coverage analysis and recommendations                                   |
| [DEBUGGED_SUMMARY.md](DEBUGGED_SUMMARY.md)         | Summary of debugging processes and resolved issues                                    |

## 🚀 Getting Started in 60 Seconds

```python
# Install the package
pip install easy-opencv

# Import the library
from easy_opencv import cv

# Load an image and convert to RGB in one line
img = cv.load_image('photo.jpg', mode='rgb')

# Apply multiple effects sequentially
enhanced = cv.adjust_brightness_contrast(img, brightness=10, contrast=1.2)
cartoon = cv.apply_cartoon_filter(enhanced)

# Show the result and save
cv.show_image(cartoon, "Cartoon Effect")
cv.save_image(cartoon, "cartoon_result.jpg")
```

## 💡 Why Use Easy OpenCV?

- **Write 50-70% less code** for common computer vision tasks
- **Eliminate complex parameters** with intuitive function calls
- **Avoid common errors** with built-in validation
- **Improve readability** with consistent API design
- **Learn computer vision** with intuitive function names
- **Simplify color space handling** with semantic naming

For developers already familiar with OpenCV, Easy OpenCV makes your code cleaner and more maintainable. For newcomers to computer vision, it provides a gentle learning curve with powerful functionality.

See the [EASY_OPENCV_BENEFITS.md](EASY_OPENCV_BENEFITS.md) document for a detailed analysis of these benefits.

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  <em>Made with ❤️ for computer vision enthusiasts everywhere</em><br>
  <strong>Easy OpenCV - Computer vision made simple</strong>
</p>
