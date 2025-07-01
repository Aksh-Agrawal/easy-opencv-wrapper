# Easy OpenCV Package Structure

```
d:\Codes\python\py_lib\
├── easy_opencv/                    # Main package directory
│   ├── __init__.py                # Package initialization and main EasyCV class
│   ├── image_operations.py        # Basic image operations (load, save, resize, crop, etc.)
│   ├── video_operations.py        # Video processing (load, save, extract frames, etc.)
│   ├── image_processing.py        # Image processing (blur, sharpen, edge detection, etc.)
│   ├── feature_detection.py       # Feature detection (corners, keypoints, contours, etc.)
│   ├── object_detection.py        # Object detection (faces, eyes, motion, etc.)
│   ├── drawing_operations.py      # Drawing functions (shapes, text, annotations)
│   ├── filters.py                 # Various filters (blur, vintage, cartoon, etc.)
│   ├── transformations.py         # Image transformations (rotate, flip, warp, etc.)
│   └── utils.py                   # Utility functions (FPS counter, color picker, etc.)
│
├── examples/                      # Example scripts
│   ├── basic_examples.py          # Basic usage examples
│   └── advanced_examples.py       # Advanced usage examples
│
├── requirements.txt               # Package dependencies
├── setup.py                      # Package setup configuration
├── pyproject.toml                # Modern Python package configuration
├── README.md                     # Comprehensive package documentation
├── USAGE_GUIDE.md               # Detailed usage guide with examples
├── test_package.py              # Package functionality tests
└── quick_demo.py                # Quick demonstration script
```

## Package Features Summary

### 🎯 **Core Philosophy**

- **Simple**: Complex OpenCV operations become one-line function calls
- **Intuitive**: Function names and parameters that make sense
- **Customizable**: Extensive parameter options with sensible defaults
- **Reliable**: Built-in error handling and validation

### 📦 **Main Modules**

1. **Image Operations** - Basic image handling

   - Load/save images with quality control
   - Resize with aspect ratio preservation
   - Crop, flip, color space conversion
   - Get comprehensive image information

2. **Video Operations** - Video processing made easy

   - Extract frames from videos
   - Create videos from image sequences
   - Webcam capture with recording
   - Video information extraction

3. **Image Processing** - Enhancement and analysis

   - Multiple blur types and noise reduction
   - Edge detection with various algorithms
   - Thresholding and morphological operations
   - Brightness/contrast adjustment
   - Histogram equalization

4. **Feature Detection** - Find interesting points

   - Corner detection (Harris, Shi-Tomasi)
   - Keypoint detection (SIFT, ORB, FAST)
   - Feature matching between images
   - Contour detection and shape classification
   - Template matching

5. **Object Detection** - Find specific objects

   - Face and eye detection
   - Custom object detection with Haar cascades
   - Motion detection in videos
   - Color-based object detection
   - Circle and line detection

6. **Drawing Operations** - Annotations and graphics

   - Shapes (rectangles, circles, polygons)
   - Text with background options
   - Arrows, grids, crosshairs
   - Multiple bounding boxes with labels
   - Contour drawing

7. **Filters** - Creative and enhancement effects

   - Gaussian, median, bilateral filtering
   - Vintage/sepia effects
   - Cartoon and sketch effects
   - Motion blur with angle control
   - Emboss and edge enhancement
   - Custom kernel application

8. **Transformations** - Geometric modifications

   - Rotation with custom center and scale
   - Perspective and affine transformations
   - Fisheye and barrel distortion effects
   - Translation and warping
   - Resize with aspect ratio preservation

9. **Utilities** - Helper functions
   - FPS counter for real-time applications
   - Interactive color picker
   - Image comparison tools
   - Image grid creation
   - Watermark application
   - Automatic Canny edge detection

### 🚀 **Usage Examples**

**Simple Image Processing Pipeline:**

```python
from easy_opencv import cv

# Load and enhance image
image = cv.load_image('photo.jpg')
enhanced = cv.apply_noise_reduction(image, method='bilateral')
enhanced = cv.adjust_brightness_contrast(enhanced, brightness=10, contrast=1.2)
enhanced = cv.apply_unsharp_mask(enhanced, radius=1.0, amount=0.5)

# Detect faces and draw boxes
faces = cv.detect_faces(enhanced)
for (x, y, w, h) in faces:
    enhanced = cv.draw_rectangle(enhanced, (x, y), (x+w, y+h), color=(0, 255, 0))

# Save result
cv.save_image(enhanced, 'enhanced_photo.jpg', quality=95)
```

**Real-time Filter Application:**

```python
# Apply vintage filter with one line
vintage_image = cv.apply_vintage_filter(image, intensity=0.7)

# Create cartoon effect
cartoon_image = cv.apply_cartoon_filter(image)

# Edge detection
edges = cv.apply_edge_detection(image, method='canny')
```

### 🎨 **Key Benefits**

1. **Simplified API**: `cv.apply_blur(image, strength=15)` vs `cv2.GaussianBlur(image, (15,15), 0)`

2. **Intelligent Defaults**: Functions work out-of-the-box with sensible parameters

3. **Automatic Handling**:

   - Odd kernel sizes for filters
   - Color space conversions when needed
   - Input validation and error handling

4. **Comprehensive Documentation**: Every function has detailed docstrings with examples

5. **Modular Design**: Import only what you need, or use the unified `cv` interface

6. **Real-world Ready**: Includes utilities for FPS counting, interactive tools, and batch processing

### 📊 **Performance**

- Built on OpenCV for optimal performance
- Minimal overhead wrapper functions
- Efficient parameter handling
- Memory-conscious operations

### 🔧 **Installation & Usage**

```bash
pip install -r requirements.txt
```

```python
from easy_opencv import cv

# That's it! All OpenCV power with simple commands
image = cv.load_image('image.jpg')
result = cv.apply_cartoon_filter(image)
cv.save_image(result, 'cartoon.jpg')
```

This package makes computer vision accessible to everyone while maintaining the full power of OpenCV underneath.
