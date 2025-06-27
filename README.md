# Easy OpenCV - Simplified Computer Vision Package

A comprehensive and easy-to-use OpenCV wrapper that provides simplified functions for common computer vision tasks. This package allows you to perform complex OpenCV operations with simple, intuitive arguments.

## Why Choose Easy OpenCV?

Easy OpenCV makes computer vision more accessible by wrapping OpenCV's complex API in a user-friendly interface:

```python
# OpenCV original:
img = cv2.imread('image.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
blurred = cv2.GaussianBlur(img_rgb, (15, 15), 0)
edges = cv2.Canny(blurred, 100, 200)

# Easy OpenCV equivalent:
img = cv.load_image('image.jpg', mode='rgb')  # Load and convert in one step
blurred = cv.apply_gaussian_blur(img, kernel_size=15)
edges = cv.apply_edge_detection(blurred)
```

📝 **See [EASY_OPENCV_BENEFITS.md](EASY_OPENCV_BENEFITS.md) for detailed comparisons and benefits** of using Easy OpenCV over direct OpenCV usage.

## Features

- **Image Operations**: Load, save, resize, crop, and convert images with simple function calls
- **Video Processing**: Handle video files, extract frames, and create videos from image sequences
- **Image Processing**: Apply filters, enhance images, and perform various image transformations
- **Feature Detection**: Detect corners, keypoints, contours, and match features between images
- **Object Detection**: Face detection, eye detection, and custom object detection using Haar cascades
- **Drawing Operations**: Draw shapes, text, and annotations on images
- **Filters**: Apply various filters including blur, sharpen, vintage, cartoon effects
- **Transformations**: Rotate, flip, warp, and apply perspective transformations
- **Utilities**: Helper functions for FPS counting, color picking, and image comparison

## Installation

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Quick Start

```python
from easy_opencv import cv

# Load and display an image
image = cv.load_image('path/to/image.jpg')
cv.show_image(image, 'My Image')

# Apply a filter
blurred = cv.apply_blur(image, 'gaussian', strength=15)

# Detect faces
faces = cv.detect_faces(image)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    image = cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0))

# Save the result
cv.save_image(image, 'output.jpg')
```

## Module Overview

### Image Operations

- `load_image(path, mode='color')` - Load images in different color modes
- `save_image(image, path, quality=95)` - Save images with quality control
- `resize_image(image, width=None, height=None, scale=None)` - Flexible image resizing
- `crop_image(image, x, y, width, height)` - Crop images to specified regions

### Video Operations

- `load_video(path)` - Load video files
- `extract_frames(video_path, output_dir, frame_interval=1)` - Extract frames from videos
- `create_video_from_frames(frame_paths, output_path, fps=30.0)` - Create videos from image sequences
- `webcam_capture(camera_id=0, save_path=None)` - Capture from webcam

### Image Processing

- `apply_blur(image, blur_type='gaussian', strength=5)` - Various blur effects
- `apply_edge_detection(image, method='canny')` - Edge detection algorithms
- `apply_threshold(image, threshold_type='binary')` - Thresholding techniques
- `adjust_brightness_contrast(image, brightness=0, contrast=1.0)` - Brightness/contrast adjustment

### Feature Detection

- `detect_corners(image, method='harris')` - Corner detection
- `detect_keypoints(image, detector='sift')` - Keypoint detection and description
- `match_features(desc1, desc2, method='bf')` - Feature matching
- `detect_contours(image, threshold_value=127)` - Contour detection

### Object Detection

- `detect_faces(image, scale_factor=1.1)` - Face detection using Haar cascades
- `detect_eyes(image, scale_factor=1.1)` - Eye detection
- `detect_motion(video_path, sensitivity=500)` - Motion detection in videos
- `color_detection(image, target_color='red')` - Color-based object detection

### Drawing Operations

- `draw_rectangle(image, start_point, end_point, color=(0,255,0))` - Draw rectangles
- `draw_circle(image, center, radius, color=(0,255,0))` - Draw circles
- `draw_text(image, text, position, font_scale=1.0)` - Add text to images
- `draw_bounding_boxes(image, boxes, labels=None)` - Draw multiple bounding boxes

### Filters

- `apply_gaussian_blur(image, kernel_size=15)` - Gaussian blur filter
- `apply_vintage_filter(image, intensity=0.5)` - Vintage/sepia effect
- `apply_cartoon_filter(image)` - Cartoon effect
- `apply_motion_blur(image, size=15, angle=0)` - Motion blur effect

### Transformations

- `rotate_image(image, angle, center=None)` - Rotate images
- `flip_image(image, direction='horizontal')` - Flip images
- `apply_perspective_transform(image, src_points, dst_points)` - Perspective transformation
- `apply_fisheye_effect(image, strength=0.5)` - Fisheye lens effect

### Utilities

- `fps_counter()` - FPS measurement for real-time applications
- `color_picker(image)` - Interactive color picking tool
- `image_comparison(image1, image2, method='side_by_side')` - Compare images
- `create_image_grid(images, grid_size)` - Create image grids

## Usage Examples

### Basic Image Processing

```python
from easy_opencv import cv

# Load and process an image
image = cv.load_image('input.jpg')

# Resize with aspect ratio preservation
resized = cv.resize_image(image, width=800)

# Apply filters
blurred = cv.apply_gaussian_blur(image, kernel_size=21)
vintage = cv.apply_vintage_filter(image, intensity=0.7)
cartoon = cv.apply_cartoon_filter(image)

# Edge detection
edges = cv.apply_edge_detection(image, method='canny', threshold1=100, threshold2=200)
```

### Object Detection

```python
# Face detection
faces = cv.detect_faces(image, scale_factor=1.1, min_neighbors=5)

# Draw bounding boxes around faces
result = cv.draw_bounding_boxes(image, faces, labels=['Face']*len(faces))

# Color-based detection
red_mask = cv.color_detection(image, target_color='red', tolerance=30)
```

### Video Processing

```python
# Extract frames from video
frame_paths = cv.extract_frames('input_video.mp4', 'frames/', frame_interval=10)

# Create video from images
cv.create_video_from_frames(frame_paths, 'output_video.mp4', fps=24)

# Motion detection
cv.detect_motion('input_video.mp4', 'motion_output.mp4', sensitivity=500)
```

### Interactive Features

```python
# Color picker tool
cv.color_picker(image, 'Color Picker Window')

# Compare two images
comparison = cv.image_comparison(image1, image2, method='side_by_side')
cv.show_image(comparison, 'Comparison')

# Create image grid
grid = cv.create_image_grid([img1, img2, img3, img4], grid_size=(2, 2))
```

## Requirements

- Python 3.7+
- OpenCV 4.5.0+
- NumPy 1.19.0+
- Pillow 8.0.0+

## Additional Resources

- [EASY_OPENCV_BENEFITS.md](EASY_OPENCV_BENEFITS.md) - Detailed comparison of Easy OpenCV vs direct OpenCV usage
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Comprehensive guide with examples
- [WHY_EASY_OPENCV.md](WHY_EASY_OPENCV.md) - In-depth explanation of the benefits of this wrapper library
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Overview of the package organization
