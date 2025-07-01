# Easy OpenCV - Quick Start Guide

## Installation

1. Clone or download this package to your project directory
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Import and use:

```python
from easy_opencv import cv
```

## Quick Examples

### 1. Basic Image Operations

```python
from easy_opencv import cv

# Load an image
image = cv.load_image('path/to/your/image.jpg')

# Resize image
resized = cv.resize_image(image, width=800)  # Height automatically calculated

# Crop image
cropped = cv.crop_image(image, x=100, y=100, width=200, height=150)

# Convert color space
gray = cv.convert_color_space(image, 'bgr', 'gray')

# Save image
cv.save_image(resized, 'output.jpg', quality=95)

# Display image
cv.show_image(image, 'My Image')
```

### 2. Apply Filters

```python
# Blur effects
gaussian_blur = cv.apply_gaussian_blur(image, kernel_size=21)
median_blur = cv.apply_median_blur(image, kernel_size=15)

# Artistic effects
vintage = cv.apply_vintage_filter(image, intensity=0.7)
cartoon = cv.apply_cartoon_filter(image)
sketch = cv.convert_to_sketch(image, blur_value=21)

# Edge detection
edges = cv.apply_edge_detection(image, method='canny', threshold1=100, threshold2=200)

# Enhancement
sharpened = cv.apply_unsharp_mask(image, radius=1.0, amount=1.0)
enhanced = cv.adjust_brightness_contrast(image, brightness=20, contrast=1.2)
```

### 3. Drawing Operations

```python
# Start with a blank canvas or existing image
canvas = cv.load_image('image.jpg')  # or create blank: np.zeros((height, width, 3), dtype=np.uint8)

# Draw shapes
canvas = cv.draw_rectangle(canvas, (50, 50), (200, 150), color=(255, 0, 0), thickness=3)
canvas = cv.draw_circle(canvas, (300, 100), radius=50, color=(0, 255, 0), filled=True)
canvas = cv.draw_line(canvas, (0, 200), (400, 200), color=(0, 0, 255), thickness=5)

# Add text
canvas = cv.draw_text(canvas, "Hello OpenCV!", (50, 250),
                     font_scale=2.0, color=(255, 255, 255), thickness=3)

# Draw polygon
points = [(400, 50), (450, 100), (400, 150), (350, 100)]
canvas = cv.draw_polygon(canvas, points, color=(255, 255, 0), thickness=2)

cv.show_image(canvas, 'Drawing Example')
```

### 4. Object Detection

```python
# Face detection
faces = cv.detect_faces(image, scale_factor=1.1, min_neighbors=5)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    image = cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    image = cv.draw_text(image, "Face", (x, y-10), color=(0, 255, 0))

# Color detection
red_mask = cv.color_detection(image, target_color='red', tolerance=30)

# Circle detection
circles = cv.detect_circles(image, min_radius=20, max_radius=100)
for (x, y, r) in circles:
    image = cv.draw_circle(image, (x, y), r, color=(255, 0, 255), thickness=2)

cv.show_image(image, 'Detection Results')
```

### 5. Feature Detection

```python
# Corner detection
corners = cv.detect_corners(image, method='shi_tomasi', max_corners=50)

# Draw detected corners
for corner in corners:
    x, y = corner.ravel()
    image = cv.draw_circle(image, (int(x), int(y)), 5, color=(0, 255, 0), filled=True)

# Contour detection
contours = cv.detect_contours(image, threshold_value=127, min_area=500)
image = cv.draw_contour(image, contours, color=(255, 0, 0), thickness=2)

# Shape detection
shapes = cv.find_shapes(image, min_area=1000)
for shape in shapes:
    x, y, w, h = shape['bounding_box']
    image = cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 255))
    image = cv.draw_text(image, shape['name'], (x, y-10), color=(0, 255, 255))

cv.show_image(image, 'Feature Detection')
```

### 6. Image Transformations

```python
# Rotate image
rotated = cv.rotate_image(image, angle=45, scale=1.0)

# Flip image
flipped_h = cv.flip_image(image, direction='horizontal')
flipped_v = cv.flip_image(image, direction='vertical')

# Apply perspective transformation
src_points = [(0, 0), (400, 0), (400, 300), (0, 300)]
dst_points = [(50, 50), (350, 100), (300, 250), (100, 200)]
warped = cv.apply_perspective_transform(image, src_points, dst_points)

# Fisheye effect
fisheye = cv.apply_fisheye_effect(image, strength=0.5)

# Show transformations
cv.show_image(rotated, 'Rotated', wait=False)
cv.show_image(warped, 'Perspective Transform', wait=False)
cv.show_image(fisheye, 'Fisheye Effect')
```

### 7. Video Processing

```python
# Extract frames from video
frame_paths = cv.extract_frames('input_video.mp4', 'frames/', frame_interval=30)
print(f"Extracted {len(frame_paths)} frames")

# Create video from images
image_list = ['frame1.jpg', 'frame2.jpg', 'frame3.jpg']  # Your image files
cv.create_video_from_frames(image_list, 'output_video.mp4', fps=24)

# Get video information
video_info = cv.get_video_info('video.mp4')
print(f"Video: {video_info['width']}x{video_info['height']}, {video_info['fps']} fps")

# Webcam capture
cv.webcam_capture(camera_id=0, save_path='recorded_video.mp4')  # Press 'q' to quit, 'r' to record
```

### 8. Utility Functions

```python
# Get image information
info = cv.get_image_info(image)
print(f"Image size: {info['width']}x{info['height']}, Channels: {info['channels']}")

# Compare images
comparison = cv.image_comparison(image1, image2, method='side_by_side')
cv.show_image(comparison, 'Comparison')

# Create image grid
images = [img1, img2, img3, img4]
grid = cv.create_image_grid(images, grid_size=(2, 2), image_size=(300, 200))
cv.show_image(grid, 'Image Grid')

# Add watermark
watermarked = cv.apply_watermark(image, "© My Company",
                                position='bottom_right', opacity=0.7)

# Interactive color picker
cv.color_picker(image, 'Click to pick colors')  # Click on image to get color values

# FPS counter for real-time applications
fps = cv.fps_counter()
while True:
    # Your processing loop
    fps_text = fps.get_fps_text()
    # Use fps_text to display current FPS
    break  # Remove this in actual loop
```

### 9. Complete Image Processing Pipeline

```python
from easy_opencv import cv

def process_image(input_path, output_path):
    """Complete image processing pipeline example"""

    # Load image
    image = cv.load_image(input_path)

    # Step 1: Resize if too large
    if image.shape[1] > 1920:  # If width > 1920
        image = cv.resize_image(image, width=1920)

    # Step 2: Noise reduction
    image = cv.apply_noise_reduction(image, method='bilateral', strength=10)

    # Step 3: Enhance contrast
    image = cv.adjust_brightness_contrast(image, brightness=10, contrast=1.2)

    # Step 4: Sharpen
    image = cv.apply_unsharp_mask(image, radius=1.0, amount=0.5)

    # Step 5: Detect and highlight objects (example: faces)
    faces = cv.detect_faces(image)
    for (x, y, w, h) in faces:
        image = cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)

    # Step 6: Add watermark
    image = cv.apply_watermark(image, "Processed with Easy OpenCV",
                              position='bottom_right', opacity=0.6)

    # Step 7: Save result
    cv.save_image(image, output_path, quality=95)

    print(f"Processed image saved to: {output_path}")

# Usage
process_image('input.jpg', 'processed_output.jpg')
```

## Testing the Package

Run the test script to verify everything works:

```bash
python test_package.py
```

Or run the examples:

```bash
python examples/basic_examples.py
python examples/advanced_examples.py
```

## Common Use Cases

1. **Photo Enhancement**: Noise reduction, contrast adjustment, sharpening
2. **Object Detection**: Faces, shapes, colors
3. **Image Analysis**: Feature detection, contour analysis
4. **Creative Effects**: Vintage, cartoon, sketch filters
5. **Video Processing**: Frame extraction, video creation
6. **Real-time Processing**: Webcam applications with filters
7. **Batch Processing**: Process multiple images with consistent operations

## Tips for Best Results

1. **Image Quality**: Higher quality input images give better results
2. **Parameter Tuning**: Experiment with function parameters for optimal results
3. **Color Spaces**: Convert to appropriate color space for specific operations
4. **Error Handling**: Always check if images loaded successfully before processing
5. **Performance**: Use appropriate image sizes for real-time applications

## Function Reference

All functions include detailed docstrings with parameter descriptions and examples. Use Python's help system:

```python
help(cv.apply_gaussian_blur)
help(cv.detect_faces)
```

This package makes OpenCV accessible with simple, intuitive function calls while maintaining the power and flexibility of the underlying OpenCV library.
