# OpenCV vs. Easy OpenCV: Code Comparison

This document provides side-by-side comparisons of common computer vision tasks using standard OpenCV versus the Easy OpenCV library. These examples clearly demonstrate how Easy OpenCV simplifies and streamlines your computer vision code.

## Basic Image Operations

### 1. Loading, Displaying, and Saving Images

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Loading an image
img = cv2.imread('image.jpg')
if img is None:
    raise FileNotFoundError("Image not found")

# Convert to RGB (OpenCV loads as BGR)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Display the image
cv2.imshow('Window Title', img_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save with quality control
cv2.imwrite('output.jpg', img_rgb,
            [cv2.IMWRITE_JPEG_QUALITY, 90])
```

</td>
<td>

```python
from easy_opencv import cv

# Loading an image directly in RGB mode
img = cv.load_image('image.jpg', mode='rgb')
# Error handling is built in

# Display the image
cv.show_image(img, 'Window Title')
# No need for waitKey or destroyAllWindows

# Save with quality control
cv.save_image(img, 'output.jpg', quality=90)
```

</td>
</tr>
</table>

### 2. Resizing Images

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load image
img = cv2.imread('image.jpg')

# Resize to specific dimensions
width, height = 800, 600
resized = cv2.resize(img, (width, height),
                    interpolation=cv2.INTER_LINEAR)

# Resize with aspect ratio
scale = 0.5
h, w = img.shape[:2]
new_height = int(h * scale)
new_width = int(w * scale)
resized_aspect = cv2.resize(img, (new_width, new_height),
                          interpolation=cv2.INTER_AREA)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Resize to specific dimensions
resized = cv.resize_image(img, width=800, height=600,
                         method='linear')

# Resize with aspect ratio - multiple approaches
resized_aspect = cv.resize_image(img, scale=0.5)
# OR
resized_aspect = cv.resize_image(img, width=800)  # Height auto-calculated
```

</td>
</tr>
</table>

### 3. Cropping Images

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load image
img = cv2.imread('image.jpg')

# Crop region (may fail silently if coordinates are invalid)
x, y, width, height = 100, 50, 300, 200
try:
    cropped = img[y:y+height, x:x+width]
except IndexError:
    print("Crop coordinates out of bounds")
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Crop with bounds checking
try:
    cropped = cv.crop_image(img, x=100, y=50, width=300, height=200)
except ValueError as e:
    print(f"Error: {e}")  # Shows clear error message
```

</td>
</tr>
</table>

## Image Processing

### 4. Applying Blur

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load image
img = cv2.imread('image.jpg')

# Different blur types
gaussian = cv2.GaussianBlur(img, (15, 15), 0)
median = cv2.medianBlur(img, 5)  # Must be odd kernel size
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# Box blur
box = cv2.blur(img, (10, 10))
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Different blur types with semantic parameters
gaussian = cv.apply_gaussian_blur(img, kernel_size=15)
median = cv.apply_median_blur(img, kernel_size=5)  # Auto-corrected if even
bilateral = cv.apply_bilateral_filter(img, diameter=9,
                                    sigma_color=75, sigma_space=75)
box = cv.apply_box_blur(img, kernel_size=10)
```

</td>
</tr>
</table>

### 5. Edge Detection

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Load and convert to grayscale
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny edge detection
edges = cv2.Canny(gray, threshold1=100, threshold2=200)

# Sobel edge detection
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
sobel = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)

# Laplacian edge detection
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
laplacian = np.uint8(np.absolute(laplacian))
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Canny edge detection (auto grayscale conversion)
edges = cv.apply_edge_detection(img, method='canny',
                              threshold1=100, threshold2=200)

# Sobel edge detection
sobel = cv.apply_edge_detection(img, method='sobel')

# Laplacian edge detection
laplacian = cv.apply_edge_detection(img, method='laplacian')
```

</td>
</tr>
</table>

### 6. Thresholding

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load and convert to grayscale
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Simple threshold
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Adaptive threshold
adaptive = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# Otsu's threshold
ret, otsu = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Simple threshold (auto grayscale conversion)
binary = cv.apply_threshold(img, value=127)

# Adaptive threshold
adaptive = cv.apply_adaptive_threshold(img, method='gaussian',
                                     block_size=11, offset=2)

# Otsu's threshold
otsu = cv.apply_threshold(img, method='otsu')
```

</td>
</tr>
</table>

## Drawing Operations

### 7. Drawing Shapes

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Create blank canvas
canvas = np.ones((300, 300, 3), dtype=np.uint8) * 255

# Draw shapes
# Note: OpenCV drawing functions modify image in-place
cv2.rectangle(canvas, (50, 50), (200, 200), (0, 0, 255), 2)
cv2.circle(canvas, (150, 150), 40, (0, 255, 0), -1)
cv2.line(canvas, (0, 0), (300, 300), (255, 0, 0), 2)
cv2.putText(canvas, "Hello", (50, 50),
           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Create polygon
points = np.array([[50, 50], [100, 25], [150, 50],
                   [100, 75]], np.int32)
points = points.reshape((-1, 1, 2))
cv2.polylines(canvas, [points], True, (255, 0, 255), 2)
```

</td>
<td>

```python
from easy_opencv import cv

# Create blank canvas
canvas = cv.create_blank_image(300, 300, color=(255, 255, 255))

# Draw shapes - functions return new images, not in-place
canvas = cv.draw_rectangle(canvas, (50, 50), (200, 200),
                         color=(0, 0, 255), thickness=2)
canvas = cv.draw_circle(canvas, (150, 150), 40,
                      color=(0, 255, 0), filled=True)
canvas = cv.draw_line(canvas, (0, 0), (300, 300),
                    color=(255, 0, 0), thickness=2)
canvas = cv.draw_text(canvas, "Hello", (50, 50),
                    color=(0, 0, 0), font_scale=1.0)

# Create polygon
points = [(50, 50), (100, 25), (150, 50), (100, 75)]
canvas = cv.draw_polygon(canvas, points, color=(255, 0, 255),
                       thickness=2, closed=True)
```

</td>
</tr>
</table>

## Feature Detection

### 8. Contour Detection

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load and preprocess
img = cv2.imread('shapes.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)[1]

# Find contours
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by area
min_area = 100
large_contours = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > min_area:
        large_contours.append(contour)

# Draw contours
result = img.copy()
cv2.drawContours(result, large_contours, -1, (0, 255, 0), 2)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('shapes.jpg')

# Find contours (automatically handles preprocessing)
contours = cv.detect_contours(img, threshold_value=127)

# Filter contours by area
large_contours = cv.filter_contours(contours, min_area=100)

# Draw contours
result = cv.draw_contours(img, large_contours,
                        color=(0, 255, 0), thickness=2)
```

</td>
</tr>
</table>

### 9. Face Detection

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load image and classifier
img = cv2.imread('people.jpg')
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw bounding boxes
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, "Face", (x, y-10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('people.jpg')

# Detect faces (automatically handles grayscale conversion)
faces = cv.detect_faces(img, scale_factor=1.1,
                      min_neighbors=5, min_size=(30, 30))

# Draw bounding boxes with labels
img = cv.draw_bounding_boxes(img, faces, labels=["Face"] * len(faces),
                           color=(0, 255, 0))
```

</td>
</tr>
</table>

## Video Processing

### 10. Reading Video Frames

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Open video file
cap = cv2.VideoCapture('video.mp4')
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frames = []
while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Store processed frame
    frames.append(blurred)

    # Display frame
    cv2.imshow('Frame', blurred)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Open and iterate through video file
video = cv.load_video('video.mp4')

frames = []
for frame in video:
    # Process frame
    blurred = cv.apply_gaussian_blur(
        cv.convert_color_space(frame, 'bgr', 'gray'),
        kernel_size=15
    )

    # Store processed frame
    frames.append(blurred)

    # Display frame
    cv.show_image(blurred, 'Frame', wait_ms=25)
    if cv.check_key('q'):
        break

# No need to manually release resources
```

</td>
</tr>
</table>

### 11. Extracting Video Frames and Creating Videos

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import os

# Extract frames from video
def extract_frames(video_path, output_dir, interval=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    frame_paths = []
    count = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(path, frame)
            frame_paths.append(path)
            frame_count += 1

        count += 1

    cap.release()
    return frame_paths

# Create video from frames
def create_video(frame_paths, output_path, fps=30.0):
    if not frame_paths:
        return False

    # Read first frame to get dimensions
    first_frame = cv2.imread(frame_paths[0])
    height, width = first_frame.shape[:2]

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Add frames to video
    for path in frame_paths:
        frame = cv2.imread(path)
        out.write(frame)

    out.release()
    return True

# Usage
frame_paths = extract_frames('input.mp4', 'frames/', 10)
create_video(frame_paths, 'output.mp4', 24.0)
```

</td>
<td>

```python
from easy_opencv import cv

# Extract frames from video
frame_paths = cv.extract_frames('input.mp4', 'frames/',
                              frame_interval=10)

# Create video from frames
cv.create_video_from_frames(frame_paths, 'output.mp4', fps=24.0)
```

</td>
</tr>
</table>

## Creative Effects

### 12. Applying Special Effects

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Load image
img = cv2.imread('image.jpg')

# Create cartoon effect
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
edges = cv2.adaptiveThreshold(gray, 255,
                            cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 9, 9)
color = cv2.bilateralFilter(img, 9, 300, 300)
cartoon = cv2.bitwise_and(color, color, mask=edges)

# Create sketch effect
gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
sketch = cv2.divide(gray, gray_blur, scale=256)

# Create vintage effect
kernel = np.ones((5,5),np.float32)/25
smoothed = cv2.filter2D(img, -1, kernel)
sepia = np.array(smoothed, dtype=np.float64)
sepia[:,:,0] = sepia[:,:,0] * 0.272
sepia[:,:,1] = sepia[:,:,1] * 0.534
sepia[:,:,2] = sepia[:,:,2] * 0.131
vintage = np.array(sepia, dtype=np.uint8)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Create cartoon effect
cartoon = cv.apply_cartoon_filter(img)

# Create sketch effect
sketch = cv.convert_to_sketch(img)

# Create vintage effect
vintage = cv.apply_vintage_filter(img)
```

</td>
</tr>
</table>

## Advanced Features

### 13. Creating an Image Grid

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

def create_image_grid(images, grid_size, image_size=None):
    rows, cols = grid_size

    # Resize images if needed
    if image_size:
        resized_images = []
        for img in images:
            resized = cv2.resize(img, image_size)
            # Convert grayscale to BGR if needed
            if len(resized.shape) == 2:
                resized = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
            resized_images.append(resized)
        images = resized_images

    # Make sure all images have the same size
    h, w = images[0].shape[:2]

    # Create empty grid
    grid = np.zeros((h * rows, w * cols, 3), dtype=np.uint8)

    # Fill grid with images
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if idx < len(images):
                grid[i*h:(i+1)*h, j*w:(j+1)*w] = images[idx]

    return grid

# Usage
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
img3 = cv2.imread('image3.jpg')
img4 = cv2.imread('image4.jpg')

grid = create_image_grid([img1, img2, img3, img4], (2, 2))
cv2.imshow('Grid', grid)
cv2.waitKey(0)
```

</td>
<td>

```python
from easy_opencv import cv

# Load images
img1 = cv.load_image('image1.jpg')
img2 = cv.load_image('image2.jpg')
img3 = cv.load_image('image3.jpg')
img4 = cv.load_image('image4.jpg')

# Create grid with a single function call
grid = cv.create_image_grid([img1, img2, img3, img4],
                           grid_size=(2, 2))
cv.show_image(grid, 'Grid')
```

</td>
</tr>
</table>

### 14. Performance Measurement with FPS Counter

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import time

class FPSCounter:
    def __init__(self, avg_frames=10):
        self.avg_frames = avg_frames
        self.times = []
        self.prev_time = time.time()

    def update(self):
        current_time = time.time()
        delta = current_time - self.prev_time
        self.prev_time = current_time

        self.times.append(delta)
        if len(self.times) > self.avg_frames:
            self.times.pop(0)

    def get_fps(self):
        if not self.times:
            return 0
        return len(self.times) / sum(self.times)

# Usage
cap = cv2.VideoCapture(0)
fps = FPSCounter()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update FPS counter
    fps.update()

    # Display FPS
    cv2.putText(frame, f"FPS: {fps.get_fps():.1f}",
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
               1.0, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Initialize webcam and FPS counter
video = cv.capture_video(0)
fps_counter = cv.fps_counter()

# Process frames
for frame in video:
    # FPS counter automatically updates
    fps = fps_counter.get()

    # Display FPS
    frame = cv.draw_text(frame, f"FPS: {fps:.1f}",
                       (10, 30), color=(0, 255, 0))

    cv.show_image(frame, 'Frame', wait_ms=1)
    if cv.check_key('q'):
        break
```

</td>
</tr>
</table>

## Additional Use Cases

### 15. Color Space Conversion

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2

# Load image
img = cv2.imread('image.jpg')

# Convert to different color spaces
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

# Convert back (need to remember exact constant)
bgr_from_hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Convert to different color spaces using intuitive names
gray = cv.convert_color_space(img, 'bgr', 'gray')
hsv = cv.convert_color_space(img, 'bgr', 'hsv')
lab = cv.convert_color_space(img, 'bgr', 'lab')
rgb = cv.convert_color_space(img, 'bgr', 'rgb')
hls = cv.convert_color_space(img, 'bgr', 'hls')

# Convert back (intuitive naming)
bgr_from_hsv = cv.convert_color_space(hsv, 'hsv', 'bgr')
```

</td>
</tr>
</table>

### 16. Morphological Operations

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Load and preprocess image
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Create kernel
kernel = np.ones((5, 5), np.uint8)

# Apply morphological operations
erosion = cv2.erode(binary, kernel, iterations=1)
dilation = cv2.dilate(binary, kernel, iterations=1)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
```

</td>
<td>

```python
from easy_opencv import cv

# Load image and convert to binary in one step
img = cv.load_image('image.jpg')
binary = cv.apply_threshold(img, value=127)

# Apply morphological operations with semantic names
erosion = cv.apply_morphology(binary, operation='erode', kernel_size=5)
dilation = cv.apply_morphology(binary, operation='dilate', kernel_size=5)
opening = cv.apply_morphology(binary, operation='open', kernel_size=5)
closing = cv.apply_morphology(binary, operation='close', kernel_size=5)
gradient = cv.apply_morphology(binary, operation='gradient', kernel_size=5)
```

</td>
</tr>
</table>

### 17. Image Histogram Analysis

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image and convert to appropriate color space
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Calculate histogram for grayscale image
hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])

# Calculate histograms for color channels
hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

# Calculate histogram for hue channel
hist_hue = cv2.calcHist([hsv], [0], None, [180], [0, 180])

# Visualize histograms
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.title('Gray Histogram')
plt.plot(hist_gray)
plt.subplot(2, 2, 2)
plt.title('BGR Histograms')
plt.plot(hist_b, color='b')
plt.plot(hist_g, color='g')
plt.plot(hist_r, color='r')
plt.tight_layout()
plt.show()
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Calculate histograms with a single function call
gray_hist = cv.calculate_histogram(img, channel='gray')
color_hists = cv.calculate_histogram(img, channel='all')
hue_hist = cv.calculate_histogram(img, channel='hue')

# Get histogram data for individual channels
b_hist, g_hist, r_hist = color_hists

# Visualize histograms
hist_visualization = cv.visualize_histograms(img)
cv.show_image(hist_visualization, 'Image Histograms')

# Alternative with specific options
custom_viz = cv.visualize_histograms(img, channels=['gray', 'rgb', 'hue'])
cv.show_image(custom_viz, 'Custom Histograms')
```

</td>
</tr>
</table>

### 18. Template Matching

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Load images
img = cv2.imread('image.jpg')
template = cv2.imread('template.jpg')
h, w = template.shape[:2]

# Apply template matching
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED',
           'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED',
           'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# Use the normalized correlation method
method = eval(methods[1])
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# If method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    top_left = min_loc
else:
    top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

# Draw rectangle on result
result = img.copy()
cv2.rectangle(result, top_left, bottom_right, (0, 255, 0), 2)

# Display result
cv2.imshow('Template Matching', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Load images
img = cv.load_image('image.jpg')
template = cv.load_image('template.jpg')

# Apply template matching with a single function
matches = cv.template_matching(img, template, method='correlation')

# Get the top match
top_match = matches[0]  # Returns (top_left, bottom_right, score)
top_left, bottom_right, score = top_match

# Draw rectangle on result
result = cv.draw_rectangle(img, top_left, bottom_right,
                         color=(0, 255, 0), thickness=2)

# Optionally, add match score text
result = cv.draw_text(result, f"Score: {score:.2f}",
                    position=(top_left[0], top_left[1] - 10),
                    color=(0, 255, 0))

# Display result
cv.show_image(result, 'Template Matching')
```

</td>
</tr>
</table>

### 19. Background Subtraction for Motion Detection

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Create background subtractor objects
mog = cv2.createBackgroundSubtractorMOG2()
knn = cv2.createBackgroundSubtractorKNN()

# Open video file
cap = cv2.VideoCapture('video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    mog_mask = mog.apply(frame)
    knn_mask = knn.apply(frame)

    # Apply morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    mog_mask = cv2.morphologyEx(mog_mask, cv2.MORPH_OPEN, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(mog_mask,
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original frame
    result = frame.copy()
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display results
    cv2.imshow('Original', frame)
    cv2.imshow('MOG2 Mask', mog_mask)
    cv2.imshow('Motion Detection', result)

    if cv2.waitKey(30) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Open video file with iterator pattern
video = cv.load_video('video.mp4')

# Initialize motion detector
motion_detector = cv.create_motion_detector(method='mog2')

for frame in video:
    # Apply background subtraction and get processed mask
    mask = motion_detector.process(frame)

    # Detect moving objects (returns bounding boxes)
    boxes = cv.detect_motion_objects(mask, min_area=500)

    # Draw boxes on original frame
    result = cv.draw_bounding_boxes(frame, boxes,
                                  color=(0, 255, 0))

    # Show results in multiple windows
    cv.show_images({
        'Original': frame,
        'Motion Mask': mask,
        'Motion Detection': result
    }, wait_ms=30)

    # Check for ESC key
    if cv.check_key(27):  # ESC key
        break
```

</td>
</tr>
</table>

### 20. Perspective Transformation

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

# Load image
img = cv2.imread('image.jpg')

# Define source points (the 4 corners of the object to transform)
src_pts = np.array([
    [56, 65],    # Top-left
    [368, 52],   # Top-right
    [28, 387],   # Bottom-left
    [389, 390]   # Bottom-right
], dtype=np.float32)

# Define destination points (where those points will end up)
width, height = 300, 400
dst_pts = np.array([
    [0, 0],              # Top-left
    [width - 1, 0],      # Top-right
    [0, height - 1],     # Bottom-left
    [width - 1, height - 1]  # Bottom-right
], dtype=np.float32)

# Calculate perspective transform matrix
matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Apply perspective transformation
warped = cv2.warpPerspective(img, matrix, (width, height))

# Show original and warped images
cv2.imshow('Original', img)
cv2.imshow('Warped', warped)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('image.jpg')

# Define source points and desired output size
src_points = [
    (56, 65),    # Top-left
    (368, 52),   # Top-right
    (28, 387),   # Bottom-left
    (389, 390)   # Bottom-right
]
output_size = (300, 400)  # width, height

# Apply perspective transformation in one step
warped = cv.apply_perspective_transform(
    img,
    src_points=src_points,
    output_size=output_size
)

# Show original and warped images side by side
comparison = cv.image_comparison(img, warped, method='side_by_side')
cv.show_image(comparison, 'Perspective Transform')
```

</td>
</tr>
</table>

### 21. Gamma Correction

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    # Build a lookup table mapping pixel values [0, 255] to adjusted values
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)
    ]).astype("uint8")

    # Apply gamma correction using the lookup table
    return cv2.LUT(image, table)

# Load image
img = cv2.imread('dark_image.jpg')

# Apply different gamma corrections
gamma_0_5 = adjust_gamma(img, gamma=0.5)  # Brighter
gamma_2_0 = adjust_gamma(img, gamma=2.0)  # Darker

# Display results
cv2.imshow('Original', img)
cv2.imshow('Gamma=0.5 (Brighter)', gamma_0_5)
cv2.imshow('Gamma=2.0 (Darker)', gamma_2_0)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

</td>
<td>

```python
from easy_opencv import cv

# Load image
img = cv.load_image('dark_image.jpg')

# Apply different gamma corrections with a single function
brighter = cv.apply_gamma_correction(img, gamma=0.5)
darker = cv.apply_gamma_correction(img, gamma=2.0)

# Display results with multiple images
cv.show_images({
    'Original': img,
    'Gamma=0.5 (Brighter)': brighter,
    'Gamma=2.0 (Darker)': darker
})
```

</td>
</tr>
</table>

### 22. Handling Image Channels

<table>
<tr>
<th>Standard OpenCV</th>
<th>Easy OpenCV</th>
</tr>
<tr>
<td>

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load a color image
img = cv2.imread('image.jpg')

# Split channels
b, g, r = cv2.split(img)

# Create images with only one channel
zeros = np.zeros(img.shape[:2], dtype=np.uint8)
blue_channel = cv2.merge([b, zeros, zeros])
green_channel = cv2.merge([zeros, g, zeros])
red_channel = cv2.merge([zeros, zeros, r])

# Merge specific channels
swapped_channels = cv2.merge([r, g, b])  # BGR -> RGB

# Display results
plt.figure(figsize=(12, 8))
plt.subplot(231), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('Original')
plt.subplot(232), plt.imshow(cv2.cvtColor(blue_channel, cv2.COLOR_BGR2RGB)), plt.title('Blue Channel')
plt.subplot(233), plt.imshow(cv2.cvtColor(green_channel, cv2.COLOR_BGR2RGB)), plt.title('Green Channel')
plt.subplot(234), plt.imshow(cv2.cvtColor(red_channel, cv2.COLOR_BGR2RGB)), plt.title('Red Channel')
plt.subplot(235), plt.imshow(swapped_channels), plt.title('RGB Swapped')
plt.tight_layout()
plt.show()
```

</td>
<td>

```python
from easy_opencv import cv

# Load a color image
img = cv.load_image('image.jpg')

# Get individual channels with semantic naming
channels = cv.split_channels(img)
blue_ch, green_ch, red_ch = channels

# Create visualizations of individual channels
blue_channel = cv.visualize_channel(img, 'blue')
green_channel = cv.visualize_channel(img, 'green')
red_channel = cv.visualize_channel(img, 'red')

# Create a channel swap (BGR -> RGB)
rgb = cv.convert_color_space(img, 'bgr', 'rgb')

# Create a grid of all channel visualizations
grid = cv.create_image_grid([
    img, blue_channel, green_channel,
    red_channel, rgb
], grid_size=(2, 3))

# Show the results
cv.show_image(grid, 'Channel Operations')
```

</td>
</tr>
</table>

## Conclusion

As demonstrated by the examples above, Easy OpenCV provides significant advantages over direct OpenCV usage:

1. **Reduced Code Volume**: Approximately 50-70% less code for the same functionality
2. **Intuitive Function Names**: Self-describing function names that explain their purpose
3. **Named Parameters**: Clear parameter names instead of positional arguments
4. **Automatic Processing**: Many preprocessing steps (grayscale conversion, etc.) are handled automatically
5. **Consistent Return Values**: Functions return new images rather than modifying in-place
6. **Error Handling**: Built-in validation and clear error messages
7. **Resource Management**: Automatic cleanup of resources
8. **Semantic Naming**: Color spaces, operations, and methods use plain English names
9. **Unified API Structure**: Similar operations follow consistent patterns

Easy OpenCV makes computer vision more accessible while maintaining all the power of OpenCV underneath.
