# Easy OpenCV Documentation

Easy OpenCV is a simplified wrapper for OpenCV functions that makes complex computer vision tasks accessible with intuitive one-liners.

## Table of Contents

1. [Image Operations](#image-operations)
2. [Video Operations](#video-operations)
3. [Image Processing](#image-processing)
4. [Feature Detection](#feature-detection)
5. [Object Detection](#object-detection)
6. [Drawing Operations](#drawing-operations)
7. [Filters](#filters)
8. [Transformations](#transformations)
9. [Utilities](#utilities)

## Image Operations

### `load_image(path, mode='color')`

Load an image from file with customizable color mode.

**Parameters:**

- `path` (str): Path to the image file
- `mode` (str): Color mode - 'color', 'gray', 'unchanged'

**Returns:**

- Image as NumPy array

**Example:**

```python
from easy_opencv import cv

# Load a color image (default)
image = cv.load_image('path/to/image.jpg')

# Load as grayscale
gray_image = cv.load_image('path/to/image.jpg', mode='gray')

# Load with alpha channel
alpha_image = cv.load_image('path/to/image.png', mode='unchanged')
```

### `save_image(image, path, quality=95)`

Save an image to file with customizable quality.

**Parameters:**

- `image` (numpy.ndarray): Image to save
- `path` (str): Output path
- `quality` (int): JPEG quality (0-100)

**Returns:**

- Boolean indicating success status

**Example:**

```python
from easy_opencv import cv

# Save image with default quality
success = cv.save_image(processed_image, 'output.jpg')

# Save with higher quality
success = cv.save_image(processed_image, 'high_quality.jpg', quality=100)

# Save in PNG format (quality parameter will be ignored)
success = cv.save_image(processed_image, 'output.png')
```

### `show_image(image, title='Image', wait=True, size=None)`

Display an image with customizable window properties.

**Parameters:**

- `image` (numpy.ndarray): Image to display
- `title` (str): Window title
- `wait` (bool): Whether to wait for a key press before continuing execution
- `size` (tuple): Optional (width, height) to resize window

**Returns:**

- None

**Example:**

```python
from easy_opencv import cv

# Display an image with default parameters (waits for key press)
cv.show_image(image, "My Image")

# Display without waiting (for animations/video processing)
cv.show_image(image, "Processing Frame", wait=False)

# Display with custom window size
cv.show_image(image, "Resized Window", size=(800, 600))
```

### `resize_image(image, width=None, height=None, scale=None, interpolation='linear')`

Resize an image with various options.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `width` (int): Target width in pixels
- `height` (int): Target height in pixels
- `scale` (float): Scale factor for both dimensions
- `interpolation` (str): Method - 'nearest', 'linear', 'cubic', 'area', 'lanczos'

**Returns:**

- Resized image

**Example:**

```python
from easy_opencv import cv

# Resize to specific dimensions
resized = cv.resize_image(image, width=800, height=600)

# Resize by scale factor
half_size = cv.resize_image(image, scale=0.5)

# Resize width only (maintain aspect ratio)
width_resized = cv.resize_image(image, width=800)

# Resize with different interpolation methods
quality_resize = cv.resize_image(image, width=1920, height=1080, interpolation='cubic')
fast_resize = cv.resize_image(image, width=1920, height=1080, interpolation='nearest')
```

### `crop_image(image, x, y, width, height)`

Crop a region from an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `x` (int): X-coordinate of top-left corner
- `y` (int): Y-coordinate of top-left corner
- `width` (int): Width of cropped region
- `height` (int): Height of cropped region

**Returns:**

- Cropped image

**Example:**

```python
from easy_opencv import cv

# Crop a region from the image
cropped = cv.crop_image(image, x=100, y=150, width=300, height=200)

# Crop the center of an image
info = cv.get_image_info(image)
center_x = info['width'] // 2 - 100  # 100px left of center
center_y = info['height'] // 2 - 100  # 100px above center
center_crop = cv.crop_image(image, center_x, center_y, 200, 200)
```

### `convert_color_space(image, target_space='RGB')`

Convert image between color spaces.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `target_space` (str): Target color space - 'RGB', 'BGR', 'HSV', 'GRAY', 'LAB', etc.

**Returns:**

- Converted image

**Example:**

```python
from easy_opencv import cv

# Convert to grayscale
gray = cv.convert_color_space(image, target_space='GRAY')

# Convert to HSV (useful for color-based detection)
hsv = cv.convert_color_space(image, target_space='HSV')

# Convert from BGR (OpenCV default) to RGB (for libraries like matplotlib)
rgb = cv.convert_color_space(image, target_space='RGB')

# Convert to LAB color space
lab = cv.convert_color_space(image, target_space='LAB')
```

### `get_image_info(image)`

Get basic information about an image.

**Parameters:**

- `image` (numpy.ndarray): Input image

**Returns:**

- Dictionary with image details (width, height, channels, dtype, etc.)

**Example:**

```python
from easy_opencv import cv

# Get image information
info = cv.get_image_info(image)

# Access specific properties
print(f"Image dimensions: {info['width']}x{info['height']}")
print(f"Number of channels: {info['channels']}")
print(f"Data type: {info['dtype']}")

# Use information for other operations
if info['channels'] == 3:
    print("This is a color image")
elif info['channels'] == 1:
    print("This is a grayscale image")
elif info['channels'] == 4:
    print("This image has an alpha channel")
```

## Video Operations

### `load_video(path)`

Load a video from file.

**Parameters:**

- `path` (str): Path to video file

**Returns:**

- Video capture object

**Example:**

```python
from easy_opencv import cv

# Load a video file
video = cv.load_video('path/to/video.mp4')

# Use with other video functions
info = cv.get_video_info(video)
print(f"Video has {info['frame_count']} frames at {info['fps']} FPS")

# Process the video
frames = cv.extract_frames(video, step=5)  # Extract every 5th frame
```

### `save_video(frames, output_path, fps=30, frame_size=None, codec='XVID')`

Save frames as a video file.

**Parameters:**

- `frames` (list): List of frames (numpy arrays)
- `output_path` (str): Output video path
- `fps` (int): Frames per second
- `frame_size` (tuple): Frame size (width, height)
- `codec` (str): Four-character codec code ('XVID', 'MJPG', 'H264', etc.)

**Returns:**

- Boolean indicating success status

### `extract_frames(video, step=1, start_frame=0, end_frame=None)`

Extract frames from a video.

**Parameters:**

- `video`: Video capture object or path
- `step` (int): Extract every Nth frame
- `start_frame` (int): Starting frame number
- `end_frame` (int): Ending frame number (None for all frames)

**Returns:**

- List of frames as numpy arrays

**Example:**

```python
from easy_opencv import cv

# Extract all frames
all_frames = cv.extract_frames('input_video.mp4')

# Extract every 10th frame (for faster processing of long videos)
sampled_frames = cv.extract_frames('input_video.mp4', step=10)

# Extract frames from a specific range
clip_frames = cv.extract_frames('input_video.mp4',
                              start_frame=30, end_frame=90)

# Process extracted frames
for i, frame in enumerate(sampled_frames):
    processed = cv.apply_cartoon_filter(frame)
    cv.save_image(processed, f"frame_{i:04d}.jpg")
```

### `create_video_from_frames(frames, output_path, fps=30, frame_size=None, codec='XVID')`

Create a video from a sequence of frames.

**Parameters:**

- `frames` (list): List of frames (numpy arrays)
- `output_path` (str): Output video path
- `fps` (int): Frames per second
- `frame_size` (tuple): Frame size (width, height)
- `codec` (str): Four-character codec code ('XVID', 'MJPG', 'H264', etc.)

**Returns:**

- Boolean indicating success status

### `get_video_info(video)`

Get information about a video.

**Parameters:**

- `video`: Video capture object or path

**Returns:**

- Dictionary with video details (frame count, fps, width, height, etc.)

### `play_video(video, window_name='Video', delay=30)`

Play a video in a window with adjustable speed.

**Parameters:**

- `video`: Video capture object or path
- `window_name` (str): Window title
- `delay` (int): Milliseconds to wait between frames (controls speed)

**Returns:**

- None

### `webcam_capture(camera_id=0, window_name='Webcam')`

Capture and display webcam feed.

**Parameters:**

- `camera_id` (int): Camera device index
- `window_name` (str): Window title

**Returns:**

- None (runs until user quits)

## Image Processing

### `apply_blur(image, method='gaussian', strength=5)`

Apply blur with different algorithms.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `method` (str): Blur method - 'gaussian', 'median', 'box', 'bilateral'
- `strength` (int): Blur intensity

**Returns:**

- Blurred image

**Example:**

```python
from easy_opencv import cv

# Apply default Gaussian blur
blurred = cv.apply_blur(image)

# Apply strong Gaussian blur
heavily_blurred = cv.apply_blur(image, strength=15)

# Apply median blur (good for salt-and-pepper noise)
median_blurred = cv.apply_blur(image, method='median', strength=7)

# Apply bilateral blur (preserves edges)
edge_preserving_blur = cv.apply_blur(image, method='bilateral', strength=10)

# Apply box blur (fastest)
box_blurred = cv.apply_blur(image, method='box', strength=5)
```

### `apply_sharpen(image, strength=1.0)`

Sharpen an image using unsharp masking.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `strength` (float): Sharpening intensity

**Returns:**

- Sharpened image

### `apply_edge_detection(image, method='canny', threshold1=100, threshold2=200)`

Detect edges in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `method` (str): Edge detection method - 'canny', 'sobel', 'laplacian'
- `threshold1` (int): First threshold for the hysteresis procedure (Canny)
- `threshold2` (int): Second threshold for the hysteresis procedure (Canny)

**Returns:**

- Image with detected edges

**Example:**

```python
from easy_opencv import cv

# Apply default Canny edge detection
edges = cv.apply_edge_detection(image)

# Apply Canny with custom thresholds (more or fewer edges)
sensitive_edges = cv.apply_edge_detection(image, threshold1=50, threshold2=150)
strong_edges = cv.apply_edge_detection(image, threshold1=150, threshold2=250)

# Use Sobel edge detector
sobel_edges = cv.apply_edge_detection(image, method='sobel')

# Use Laplacian edge detector
laplacian_edges = cv.apply_edge_detection(image, method='laplacian')

# Auto-detect edges with optimal thresholds
auto_edges = cv.auto_canny(image)
```

### `apply_threshold(image, threshold_value=127, max_value=255, threshold_type='binary')`

Apply image thresholding.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `threshold_value` (int): Threshold value
- `max_value` (int): Maximum value for binary methods
- `threshold_type` (str): Type - 'binary', 'binary_inv', 'trunc', 'tozero', 'tozero_inv', 'otsu', 'adaptive'

**Returns:**

- Thresholded image

**Example:**

```python
from easy_opencv import cv

# First convert to grayscale for better results with thresholding
gray = cv.convert_color_space(image, 'GRAY')

# Apply binary threshold (pixels > 127 become 255, others 0)
binary = cv.apply_threshold(gray, threshold_value=127, threshold_type='binary')

# Apply inverted binary threshold (pixels > 127 become 0, others 255)
binary_inv = cv.apply_threshold(gray, threshold_value=127, threshold_type='binary_inv')

# Apply Otsu's automatic thresholding (finds optimal threshold value)
otsu = cv.apply_threshold(gray, threshold_type='otsu')

# Apply adaptive thresholding (works better with varying lighting conditions)
adaptive = cv.apply_threshold(gray, threshold_type='adaptive')

# Truncate threshold (pixels > 127 become 127, others unchanged)
truncated = cv.apply_threshold(gray, threshold_type='trunc')
```

### `apply_morphology(image, operation='erode', kernel_size=5, iterations=1)`

Apply morphological operations.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `operation` (str): Operation type - 'erode', 'dilate', 'open', 'close', 'gradient', 'tophat', 'blackhat'
- `kernel_size` (int): Size of the structuring element
- `iterations` (int): Number of times to apply the operation

**Returns:**

- Processed image

### `apply_histogram_equalization(image, adaptive=False, clip_limit=2.0)`

Apply histogram equalization to improve contrast.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `adaptive` (bool): Whether to use adaptive histogram equalization (CLAHE)
- `clip_limit` (float): Threshold for contrast limiting (CLAHE only)

**Returns:**

- Contrast-enhanced image

### `adjust_brightness_contrast(image, brightness=0, contrast=1.0)`

Adjust image brightness and contrast.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `brightness` (int): Brightness adjustment (-255 to 255)
- `contrast` (float): Contrast adjustment (0.0 to 3.0)

**Returns:**

- Adjusted image

### `apply_gamma_correction(image, gamma=1.0)`

Apply gamma correction for lightness/darkness adjustment.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `gamma` (float): Gamma value (< 1 brightens, > 1 darkens)

**Returns:**

- Gamma-corrected image

## Feature Detection

### `detect_corners(image, max_corners=100, quality_level=0.01, min_distance=10)`

Detect corners in an image using Shi-Tomasi method.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `max_corners` (int): Maximum number of corners to detect
- `quality_level` (float): Minimum accepted quality of image corners
- `min_distance` (int): Minimum possible Euclidean distance between corners

**Returns:**

- Array of corner coordinates

### `detect_keypoints(image, method='sift', mask=None)`

Detect keypoints using different methods.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `method` (str): Detection method - 'sift', 'surf', 'orb', 'brisk', 'akaze'
- `mask` (numpy.ndarray): Optional mask specifying where to look for keypoints

**Returns:**

- Tuple of (keypoints, descriptors)

### `match_features(descriptors1, descriptors2, method='flann', ratio_test=0.75)`

Match features between two images.

**Parameters:**

- `descriptors1` (numpy.ndarray): Descriptors from first image
- `descriptors2` (numpy.ndarray): Descriptors from second image
- `method` (str): Matching method - 'flann' or 'bf' (brute force)
- `ratio_test` (float): Threshold for Lowe's ratio test

**Returns:**

- List of good matches

### `detect_contours(image, threshold_value=127, max_value=255, threshold_type='binary', min_area=0)`

Detect contours in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `threshold_value` (int): Threshold value for binary conversion
- `max_value` (int): Maximum value for thresholding
- `threshold_type` (str): Type of thresholding
- `min_area` (float): Minimum contour area to keep

**Returns:**

- List of detected contours

**Example:**

```python
from easy_opencv import cv

# Detect all contours in an image
contours = cv.detect_contours(image)

# Detect only larger contours (filter out small noise)
large_contours = cv.detect_contours(image, min_area=1000)

# Detect contours with custom threshold values
custom_contours = cv.detect_contours(image, threshold_value=200, threshold_type='binary_inv')

# Draw the detected contours on the original image
result = cv.draw_contour(image.copy(), contours, color=(0, 255, 255), thickness=2)

# Count and label objects
print(f"Found {len(contours)} objects")
for i, contour in enumerate(contours):
    # Get the center of the contour
    M = cv.moment(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # Label each object
        result = cv.draw_text(result, f"Object {i+1}", (cx, cy))
```

### `find_shapes(image, shape_type='all')`

Find specific shapes in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `shape_type` (str): Shape to detect - 'all', 'triangle', 'rectangle', 'square', 'circle'

**Returns:**

- List of contours matching the specified shape

### `template_matching(image, template, method='ccoeff_normed')`

Find a template in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image to search in
- `template` (numpy.ndarray): Template to search for
- `method` (str): Matching method - 'sqdiff', 'sqdiff_normed', 'ccorr', 'ccorr_normed', 'ccoeff', 'ccoeff_normed'

**Returns:**

- Tuple of (top_left_corner, bottom_right_corner, max_val)

## Object Detection

### `detect_faces(image, scale_factor=1.1, min_neighbors=5, min_size=(30, 30))`

Detect faces in an image using Haar cascades.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `scale_factor` (float): How much the image size is reduced at each scale
- `min_neighbors` (int): Minimum number of neighbors each candidate rectangle should have
- `min_size` (tuple): Minimum possible object size

**Returns:**

- List of rectangles where faces were detected

### `detect_eyes(image, scale_factor=1.1, min_neighbors=5)`

Detect eyes in an image using Haar cascades.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `scale_factor` (float): How much the image size is reduced at each scale
- `min_neighbors` (int): Minimum number of neighbors each candidate rectangle should have

**Returns:**

- List of rectangles where eyes were detected

### `detect_objects_cascade(image, cascade_path, scale_factor=1.1, min_neighbors=5)`

Detect objects using a custom cascade classifier.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `cascade_path` (str): Path to the cascade XML file
- `scale_factor` (float): How much the image size is reduced at each scale
- `min_neighbors` (int): Minimum number of neighbors each candidate rectangle should have

**Returns:**

- List of rectangles where objects were detected

### `background_subtraction(frames, method='mog2', learning_rate=-1)`

Perform background subtraction on a sequence of frames.

**Parameters:**

- `frames` (list): List of image frames
- `method` (str): Subtraction method - 'mog2', 'knn', 'gmg'
- `learning_rate` (float): Learning rate parameter (-1 for auto)

**Returns:**

- List of foreground masks

### `detect_motion(previous_frame, current_frame, threshold=25, min_area=500)`

Detect motion between two consecutive frames.

**Parameters:**

- `previous_frame` (numpy.ndarray): Previous frame
- `current_frame` (numpy.ndarray): Current frame
- `threshold` (int): Threshold for motion detection
- `min_area` (int): Minimum contour area to be considered motion

**Returns:**

- List of contours where motion was detected

### `detect_circles(image, dp=1, min_dist=50, param1=50, param2=30, min_radius=0, max_radius=0)`

Detect circles in an image using Hough transform.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `dp` (int): Inverse ratio of accumulator resolution
- `min_dist` (int): Minimum distance between detected centers
- `param1` (int): Higher threshold for the Canny edge detector
- `param2` (int): Accumulator threshold for circle centers
- `min_radius` (int): Minimum circle radius
- `max_radius` (int): Maximum circle radius

**Returns:**

- Array of detected circles (x, y, radius)

### `detect_lines(image, rho=1, theta=np.pi/180, threshold=100, min_line_length=100, max_line_gap=10)`

Detect lines using Hough transform.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `rho` (float): Distance resolution of the accumulator in pixels
- `theta` (float): Angle resolution of the accumulator in radians
- `threshold` (int): Accumulator threshold parameter
- `min_line_length` (int): Minimum line length
- `max_line_gap` (int): Maximum allowed gap between line segments

**Returns:**

- Array of detected lines (x1, y1, x2, y2)

### `color_detection(image, lower_range, upper_range)`

Detect a specific color range in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `lower_range` (numpy.ndarray): Lower bound color in the HSV color space
- `upper_range` (numpy.ndarray): Upper bound color in the HSV color space

**Returns:**

- Mask of the detected color regions

## Drawing Operations

### `draw_rectangle(image, start_point, end_point, color=(0, 255, 0), thickness=2, filled=False)`

Draw a rectangle on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `start_point` (tuple): Top-left corner (x, y)
- `end_point` (tuple): Bottom-right corner (x, y)
- `color` (tuple): Rectangle color (B, G, R)
- `thickness` (int): Line thickness
- `filled` (bool): Whether to fill the rectangle

**Returns:**

- Image with rectangle drawn

**Example:**

```python
from easy_opencv import cv

# Draw an outline rectangle
image_with_rect = cv.draw_rectangle(image,
                                   start_point=(100, 150),
                                   end_point=(300, 400),
                                   color=(0, 255, 0),  # Green in BGR
                                   thickness=2)

# Draw a filled rectangle
image_with_filled_rect = cv.draw_rectangle(image,
                                          start_point=(200, 250),
                                          end_point=(350, 350),
                                          color=(0, 0, 255),  # Red in BGR
                                          filled=True)

# Draw a semi-transparent rectangle (for highlighting regions)
overlay = image.copy()
overlay = cv.draw_rectangle(overlay, (50, 50), (200, 200),
                           color=(255, 0, 0), filled=True)
alpha = 0.4  # Transparency factor
image_with_transparent_rect = cv.apply_weighted_blend(image, overlay, alpha)
```

### `draw_circle(image, center, radius, color=(0, 255, 0), thickness=2, filled=False)`

Draw a circle on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `center` (tuple): Circle center (x, y)
- `radius` (int): Circle radius
- `color` (tuple): Circle color (B, G, R)
- `thickness` (int): Line thickness
- `filled` (bool): Whether to fill the circle

**Returns:**

- Image with circle drawn

### `draw_line(image, start_point, end_point, color=(0, 255, 0), thickness=2, line_type='aa')`

Draw a line on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `start_point` (tuple): Line start point (x, y)
- `end_point` (tuple): Line end point (x, y)
- `color` (tuple): Line color (B, G, R)
- `thickness` (int): Line thickness
- `line_type` (str): Line type - 'aa' (anti-aliased), '4' (4-connected), '8' (8-connected)

**Returns:**

- Image with line drawn

### `draw_text(image, text, position, font_scale=1.0, color=(0, 255, 0), thickness=2, font_face='simplex', background=False, bg_color=(0, 0, 0))`

Draw text on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `text` (str): Text to draw
- `position` (tuple): Bottom-left corner of the text (x, y)
- `font_scale` (float): Font scale factor
- `color` (tuple): Text color (B, G, R)
- `thickness` (int): Line thickness
- `font_face` (str): Font type - 'simplex', 'plain', 'duplex', 'complex', 'triplex', 'complex_small', 'script_simplex', 'script_complex'
- `background` (bool): Whether to add a background behind the text
- `bg_color` (tuple): Background color (B, G, R)

**Returns:**

- Image with text drawn

**Example:**

```python
from easy_opencv import cv

# Draw simple green text
image_with_text = cv.draw_text(image,
                              text="Hello, OpenCV!",
                              position=(50, 50),
                              color=(0, 255, 0))

# Draw larger text with a different font
image_with_large_text = cv.draw_text(image,
                                    text="Big Text",
                                    position=(100, 200),
                                    font_scale=2.0,
                                    color=(255, 255, 0),
                                    font_face='complex')

# Draw text with background for better visibility
image_with_text_bg = cv.draw_text(image,
                                 text="Text with background",
                                 position=(50, 300),
                                 color=(255, 255, 255),
                                 background=True,
                                 bg_color=(0, 0, 255))

# Add a title to an image
title = cv.draw_text(image.copy(),
                    text="Analysis Results",
                    position=(image.shape[1]//2 - 100, 30),
                    font_scale=1.5,
                    thickness=3,
                    background=True)
```

### `draw_polygon(image, points, color=(0, 255, 0), thickness=2, filled=False)`

Draw a polygon on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `points` (list): List of points [(x1, y1), (x2, y2), ...]
- `color` (tuple): Polygon color (B, G, R)
- `thickness` (int): Line thickness
- `filled` (bool): Whether to fill the polygon

**Returns:**

- Image with polygon drawn

### `draw_contour(image, contours, color=(0, 255, 0), thickness=2, contour_index=-1)`

Draw contours on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `contours` (list): List of contours or a single contour
- `color` (tuple): Contour color (B, G, R)
- `thickness` (int): Line thickness
- `contour_index` (int): Index of contour to draw (-1 for all)

**Returns:**

- Image with contours drawn

### `draw_arrow(image, start_point, end_point, color=(0, 255, 0), thickness=2, arrow_size=10)`

Draw an arrow on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `start_point` (tuple): Arrow start point (x, y)
- `end_point` (tuple): Arrow end point (x, y)
- `color` (tuple): Arrow color (B, G, R)
- `thickness` (int): Line thickness
- `arrow_size` (int): Size of the arrow head

**Returns:**

- Image with arrow drawn

### `draw_grid(image, grid_size=(10, 10), color=(128, 128, 128), thickness=1)`

Draw a grid on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `grid_size` (tuple): Number of grid cells (rows, cols)
- `color` (tuple): Grid color (B, G, R)
- `thickness` (int): Line thickness

**Returns:**

- Image with grid drawn

### `draw_crosshair(image, center, size=10, color=(0, 255, 0), thickness=1)`

Draw a crosshair on an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `center` (tuple): Center point (x, y)
- `size` (int): Size of the crosshair
- `color` (tuple): Crosshair color (B, G, R)
- `thickness` (int): Line thickness

**Returns:**

- Image with crosshair drawn

### `draw_bounding_boxes(image, boxes, labels=None, colors=None, thickness=2)`

Draw bounding boxes with optional labels.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `boxes` (list): List of boxes as [(x1, y1, x2, y2), ...]
- `labels` (list): Optional list of labels for each box
- `colors` (list): Optional list of colors for each box
- `thickness` (int): Line thickness

**Returns:**

- Image with bounding boxes drawn

## Filters

### `apply_gaussian_blur(image, kernel_size=15, sigma_x=0, sigma_y=0)`

Apply Gaussian blur filter.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `kernel_size` (int): Size of the Gaussian kernel
- `sigma_x` (float): Standard deviation in X direction
- `sigma_y` (float): Standard deviation in Y direction

**Returns:**

- Blurred image

**Example:**

```python
from easy_opencv import cv

# Apply default Gaussian blur
blurred = cv.apply_gaussian_blur(image)

# Apply light blur
light_blur = cv.apply_gaussian_blur(image, kernel_size=5)

# Apply strong blur
heavy_blur = cv.apply_gaussian_blur(image, kernel_size=31)

# Apply blur with custom sigma values for directional blur
directional_blur = cv.apply_gaussian_blur(image, kernel_size=15,
                                         sigma_x=10, sigma_y=1)

# Create a comparison grid
original_labeled = cv.draw_text(image.copy(), "Original", (10, 30))
default_labeled = cv.draw_text(blurred.copy(), "Default Blur", (10, 30))
light_labeled = cv.draw_text(light_blur.copy(), "Light Blur", (10, 30))
heavy_labeled = cv.draw_text(heavy_blur.copy(), "Heavy Blur", (10, 30))

grid = cv.create_image_grid([original_labeled, default_labeled,
                            light_labeled, heavy_labeled],
                           grid_size=(2, 2))
cv.show_image(grid, "Gaussian Blur Comparison")
```

### `apply_median_blur(image, kernel_size=5)`

Apply median blur filter (good for removing noise).

**Parameters:**

- `image` (numpy.ndarray): Input image
- `kernel_size` (int): Size of the kernel

**Returns:**

- Filtered image

### `apply_bilateral_filter(image, diameter=9, sigma_color=75, sigma_space=75)`

Apply bilateral filter (preserves edges while reducing noise).

**Parameters:**

- `image` (numpy.ndarray): Input image
- `diameter` (int): Diameter of each pixel neighborhood
- `sigma_color` (float): Filter sigma in the color space
- `sigma_space` (float): Filter sigma in the coordinate space

**Returns:**

- Filtered image

### `apply_custom_kernel(image, kernel)`

Apply a custom convolution kernel.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `kernel` (numpy.ndarray): Custom convolution kernel

**Returns:**

- Filtered image

### `apply_noise_reduction(image, method='nlm', strength=10)`

Apply noise reduction filters.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `method` (str): Method - 'nlm' (Non-Local Means), 'gaussian', 'median', 'bilateral'
- `strength` (int): Strength of noise reduction

**Returns:**

- Denoised image

### `apply_emboss_filter(image, direction='northeast')`

Apply an emboss effect filter.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `direction` (str): Emboss direction - 'north', 'northeast', 'east', etc.

**Returns:**

- Embossed image

### `apply_edge_enhance_filter(image, strength=1.0)`

Enhance edges in an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `strength` (float): Enhancement strength

**Returns:**

- Edge-enhanced image

### `apply_unsharp_mask(image, kernel_size=5, strength=1.0)`

Apply unsharp masking for edge enhancement.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `kernel_size` (int): Size of the Gaussian blur kernel
- `strength` (float): Strength of the effect

**Returns:**

- Enhanced image

### `apply_high_pass_filter(image, cutoff=50)`

Apply a high-pass filter to preserve edges.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `cutoff` (int): Cutoff frequency

**Returns:**

- Filtered image

### `apply_motion_blur(image, size=15, angle=45)`

Apply a motion blur effect.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `size` (int): Size of the motion blur kernel
- `angle` (float): Angle of motion in degrees

**Returns:**

- Motion-blurred image

### `apply_vintage_filter(image, intensity=1.0)`

Apply a vintage/retro filter effect.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `intensity` (float): Effect intensity (0.0 to 1.0)

**Returns:**

- Filtered image

**Example:**

```python
from easy_opencv import cv

# Apply vintage filter with default intensity
vintage = cv.apply_vintage_filter(image)

# Apply subtle vintage effect
light_vintage = cv.apply_vintage_filter(image, intensity=0.4)

# Apply strong vintage effect
strong_vintage = cv.apply_vintage_filter(image, intensity=1.5)

# Create a before/after comparison
comparison = cv.image_comparison(image, vintage, method='side_by_side')
cv.show_image(comparison, "Before / After Vintage Filter")

# Create multiple versions with different intensities
intensities = [0.2, 0.6, 1.0, 1.4]
filtered_images = []
for i, intensity in enumerate(intensities):
    result = cv.apply_vintage_filter(image, intensity=intensity)
    labeled = cv.draw_text(result, f"Intensity: {intensity}", (10, 30))
    filtered_images.append(labeled)

grid = cv.create_image_grid(filtered_images, grid_size=(2, 2))
cv.show_image(grid, "Vintage Filter Intensities")
```

### `apply_cartoon_filter(image, edges=1, bilateral=7)`

Apply a cartoon-like effect to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `edges` (int): Edge detection threshold
- `bilateral` (int): Bilateral filter iterations

**Returns:**

- Cartoon-like image

**Example:**

```python
from easy_opencv import cv

# Apply cartoon effect with default parameters
cartoon = cv.apply_cartoon_filter(image)

# Apply cartoon effect with subtle edges
subtle_cartoon = cv.apply_cartoon_filter(image, edges=0.5, bilateral=5)

# Apply cartoon effect with strong edges
strong_cartoon = cv.apply_cartoon_filter(image, edges=2, bilateral=9)

# Save the result
cv.save_image(cartoon, "cartoon_effect.jpg")

# Create a before/after comparison
comparison = cv.image_comparison(image, cartoon, method='side_by_side')
cv.show_image(comparison, "Original vs Cartoon")

# Apply to a series of video frames
video = cv.load_video("input.mp4")
frames = cv.extract_frames(video, step=5)  # Process every 5th frame for speed
cartoon_frames = []
for frame in frames:
    cartoon_frame = cv.apply_cartoon_filter(frame)
    cartoon_frames.append(cartoon_frame)

# Create a video from the cartoon frames
cv.create_video_from_frames(cartoon_frames, "cartoon_video.mp4", fps=6)
```

## Transformations

### `rotate_image(image, angle, center=None, scale=1.0, keep_size=False)`

Rotate an image around a point.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `angle` (float): Rotation angle in degrees
- `center` (tuple): Center of rotation (None for image center)
- `scale` (float): Isotropic scale factor
- `keep_size` (bool): Whether to maintain original image size

**Returns:**

- Rotated image

**Example:**

```python
from easy_opencv import cv

# Rotate image 45 degrees around the center
rotated = cv.rotate_image(image, angle=45)

# Rotate image 90 degrees
rotated_90 = cv.rotate_image(image, angle=90)

# Rotate and scale down simultaneously
rotated_scaled = cv.rotate_image(image, angle=30, scale=0.8)

# Rotate around a specific point
height, width = image.shape[:2]
custom_center = (width//4, height//4)  # Top-left quarter
rotated_custom = cv.rotate_image(image, angle=45, center=custom_center)

# Rotate but keep the original image dimensions (avoids cropping)
rotated_keep_size = cv.rotate_image(image, angle=45, keep_size=True)

# Create an animation with multiple rotation angles
frames = []
for angle in range(0, 360, 10):  # Rotate in 10-degree increments
    rotated_frame = cv.rotate_image(image, angle=angle)
    frames.append(rotated_frame)

# Save as a video
cv.create_video_from_frames(frames, "rotation_animation.mp4", fps=15)
```

### `flip_image(image, direction='horizontal')`

Flip an image horizontally or vertically.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `direction` (str): Flip direction - 'horizontal', 'vertical', 'both'

**Returns:**

- Flipped image

### `translate_image(image, x, y)`

Translate an image in x and y directions.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `x` (int): Pixels to shift horizontally (positive: right, negative: left)
- `y` (int): Pixels to shift vertically (positive: down, negative: up)

**Returns:**

- Translated image

### `apply_perspective_transform(image, source_points, destination_points)`

Apply perspective transformation to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `source_points` (list): List of source points [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
- `destination_points` (list): List of destination points [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]

**Returns:**

- Transformed image

### `apply_affine_transform(image, source_points, destination_points)`

Apply affine transformation to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `source_points` (list): List of 3 source points [(x1,y1), (x2,y2), (x3,y3)]
- `destination_points` (list): List of 3 destination points [(x1,y1), (x2,y2), (x3,y3)]

**Returns:**

- Transformed image

### `warp_image(image, transformation_matrix)`

Apply a custom transformation matrix to warp an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `transformation_matrix` (numpy.ndarray): 2x3 or 3x3 transformation matrix

**Returns:**

- Warped image

### `apply_barrel_distortion(image, k1=0.5, k2=0.5, center=None)`

Apply barrel (or pincushion) distortion to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `k1` (float): First radial distortion coefficient
- `k2` (float): Second radial distortion coefficient
- `center` (tuple): Center of distortion (None for image center)

**Returns:**

- Distorted image

### `apply_fisheye_effect(image, strength=1.5, center=None)`

Apply a fisheye lens effect to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `strength` (float): Strength of the effect
- `center` (tuple): Center of distortion (None for image center)

**Returns:**

- Image with fisheye effect

**Example:**

```python
from easy_opencv import cv

# Apply default fisheye effect
fisheye = cv.apply_fisheye_effect(image)

# Apply subtle fisheye effect
subtle_fisheye = cv.apply_fisheye_effect(image, strength=0.7)

# Apply extreme fisheye effect
extreme_fisheye = cv.apply_fisheye_effect(image, strength=2.5)

# Apply fisheye effect with custom center point
height, width = image.shape[:2]
custom_center = (width//2, height//3)  # Upper center
custom_fisheye = cv.apply_fisheye_effect(image, center=custom_center)

# Create a comparison grid
original_labeled = cv.draw_text(image.copy(), "Original", (10, 30))
default_labeled = cv.draw_text(fisheye.copy(), "Default (1.5)", (10, 30))
subtle_labeled = cv.draw_text(subtle_fisheye.copy(), "Subtle (0.7)", (10, 30))
extreme_labeled = cv.draw_text(extreme_fisheye.copy(), "Extreme (2.5)", (10, 30))

grid = cv.create_image_grid([original_labeled, default_labeled,
                           subtle_labeled, extreme_labeled],
                          grid_size=(2, 2))
cv.show_image(grid, "Fisheye Effect Comparison")
```

### `resize_with_aspect_ratio(image, width=None, height=None, inter='linear')`

Resize an image maintaining its aspect ratio.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `width` (int): Target width (None to calculate from height)
- `height` (int): Target height (None to calculate from width)
- `inter` (str): Interpolation method - 'nearest', 'linear', 'cubic', 'area'

**Returns:**

- Resized image maintaining aspect ratio

## Utilities

### `create_trackbar(name, window_name, min_val, max_val, initial_val, callback)`

Create a trackbar for interactive parameter adjustment.

**Parameters:**

- `name` (str): Trackbar name
- `window_name` (str): Name of the window to attach the trackbar to
- `min_val` (int): Minimum value
- `max_val` (int): Maximum value
- `initial_val` (int): Initial value
- `callback` (function): Callback function to handle trackbar changes

**Returns:**

- None

### `mouse_callback(event, x, y, flags, param)`

Template for mouse event handling.

**Parameters:**

- Standard OpenCV mouse callback parameters

**Returns:**

- None

### `set_mouse_callback(window_name, callback, param=None)`

Set a callback for mouse events in a window.

**Parameters:**

- `window_name` (str): Name of the window
- `callback` (function): Callback function
- `param` (any): Parameter to pass to the callback

**Returns:**

- None

### `fps_counter(frame, position=(10, 30), font_scale=1.0, color=(0, 255, 0), thickness=2)`

Add an FPS counter to a video frame.

**Parameters:**

- `frame` (numpy.ndarray): Input frame
- `position` (tuple): Position for the counter text
- `font_scale` (float): Size of the text
- `color` (tuple): Text color (B, G, R)
- `thickness` (int): Text thickness

**Returns:**

- Frame with FPS counter

### `color_picker(image, event, x, y, flags, param)`

Pick color from an image with mouse click.

**Parameters:**

- Standard OpenCV mouse callback parameters
- `image` (numpy.ndarray): Image to pick colors from

**Returns:**

- None (prints color values at click coordinates)

### `image_comparison(image1, image2, method='side_by_side')`

Create a comparison view of two images.

**Parameters:**

- `image1` (numpy.ndarray): First image
- `image2` (numpy.ndarray): Second image
- `method` (str): Comparison method - 'side_by_side', 'vertical', 'blend', 'diff'

**Returns:**

- Comparison image

### `create_image_grid(images, grid_size=(2, 2), image_size=None)`

Create a grid of images.

**Parameters:**

- `images` (list): List of images to include in the grid
- `grid_size` (tuple): Number of rows and columns in the grid
- `image_size` (tuple): Size to resize each image to before placing in grid

**Returns:**

- Grid image

**Example:**

```python
from easy_opencv import cv

# Create a basic 2x2 grid of the same image
grid = cv.create_image_grid([image] * 4)

# Create a grid with different images
processed_images = []
processed_images.append(image)  # Original
processed_images.append(cv.apply_gaussian_blur(image))  # Blurred
processed_images.append(cv.apply_edge_detection(image))  # Edges
processed_images.append(cv.apply_vintage_filter(image))  # Vintage

grid = cv.create_image_grid(processed_images, grid_size=(2, 2))
cv.show_image(grid, "Processing Effects")

# Create a grid with custom size for each cell
grid = cv.create_image_grid(processed_images,
                          grid_size=(2, 2),
                          image_size=(300, 200))

# Create a grid of different filters
filters = ["gaussian", "median", "bilateral", "box"]
filtered_images = []
for filter_name in filters:
    result = cv.apply_blur(image, method=filter_name)
    labeled = cv.draw_text(result, f"{filter_name} blur", (10, 30))
    filtered_images.append(labeled)

filter_grid = cv.create_image_grid(filtered_images, grid_size=(2, 2))
cv.save_image(filter_grid, "filter_comparison.jpg")
```

### `apply_watermark(image, text, position='bottom_right', opacity=0.4, font_scale=1.0, color=(255, 255, 255))`

Apply a text watermark to an image.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `text` (str): Watermark text
- `position` (str): Position - 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'
- `opacity` (float): Watermark opacity (0.0 to 1.0)
- `font_scale` (float): Font size
- `color` (tuple): Text color (B, G, R)

**Returns:**

- Image with watermark

**Example:**

```python
from easy_opencv import cv

# Apply default watermark
watermarked = cv.apply_watermark(image, "© My Company")

# Apply watermark at different positions
top_left = cv.apply_watermark(image.copy(), "Top Left Watermark",
                             position='top_left')

center = cv.apply_watermark(image.copy(), "CENTER",
                           position='center',
                           font_scale=2.0)

# Apply with custom opacity and color
subtle = cv.apply_watermark(image.copy(), "Subtle Watermark",
                           opacity=0.2,
                           color=(0, 0, 0))  # Black text

bold = cv.apply_watermark(image.copy(), "BOLD WATERMARK",
                         opacity=0.9,
                         font_scale=1.5,
                         color=(0, 0, 255))  # Red text

# Add watermark to all images in a folder
import os
input_folder = "input_images"
output_folder = "watermarked_images"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        img = cv.load_image(input_path)
        watermarked = cv.apply_watermark(img, "© Copyright 2025")
        cv.save_image(watermarked, output_path)
```

### `convert_to_sketch(image, pencil_mode=False, detail_level=3)`

Convert an image to a pencil sketch.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `pencil_mode` (bool): True for pencil sketch, False for ink sketch
- `detail_level` (int): Level of detail preservation (1-5)

**Returns:**

- Sketch image

**Example:**

```python
from easy_opencv import cv

# Default ink sketch
ink_sketch = cv.convert_to_sketch(image)

# Pencil sketch
pencil_sketch = cv.convert_to_sketch(image, pencil_mode=True)

# High detail ink sketch
detailed_ink = cv.convert_to_sketch(image, detail_level=5)

# Low detail pencil sketch
simple_pencil = cv.convert_to_sketch(image, pencil_mode=True, detail_level=1)

# Compare different sketch styles
original_labeled = cv.draw_text(image.copy(), "Original", (10, 30))
ink_labeled = cv.draw_text(ink_sketch, "Ink Sketch", (10, 30))
pencil_labeled = cv.draw_text(pencil_sketch, "Pencil Sketch", (10, 30))
detailed_labeled = cv.draw_text(detailed_ink, "Detailed Ink", (10, 30))

grid = cv.create_image_grid([original_labeled, ink_labeled,
                           pencil_labeled, detailed_labeled],
                          grid_size=(2, 2))
cv.show_image(grid, "Sketch Styles Comparison")
cv.save_image(grid, "sketch_comparison.jpg")
```

### `auto_canny(image, sigma=0.33)`

Apply Canny edge detection with automatic threshold calculation.

**Parameters:**

- `image` (numpy.ndarray): Input image
- `sigma` (float): Sigma value for threshold calculation

**Returns:**

- Edge image

**Example:**

```python
from easy_opencv import cv

# Get edges with automatic threshold calculation
edges = cv.auto_canny(image)

# More edges (lower thresholds)
more_edges = cv.auto_canny(image, sigma=0.20)

# Fewer edges (higher thresholds)
fewer_edges = cv.auto_canny(image, sigma=0.50)

# Create comparison grid
original_labeled = cv.draw_text(image.copy(), "Original", (10, 30))
auto_labeled = cv.draw_text(edges, "Auto Canny (sigma=0.33)", (10, 30))
more_labeled = cv.draw_text(more_edges, "More Edges (sigma=0.20)", (10, 30))
fewer_labeled = cv.draw_text(fewer_edges, "Fewer Edges (sigma=0.50)", (10, 30))

grid = cv.create_image_grid([original_labeled, auto_labeled,
                           more_labeled, fewer_labeled],
                          grid_size=(2, 2))
cv.show_image(grid, "Auto Canny Comparison")

# Practical application - find contours after edge detection
edges = cv.auto_canny(image)
contours = cv.detect_contours(edges)
result = cv.draw_contour(image.copy(), contours, color=(0, 255, 0))
cv.show_image(result, "Detected Contours")
```
