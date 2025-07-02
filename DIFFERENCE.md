# Easy OpenCV vs. Traditional OpenCV: Code Comparisons

This document provides side-by-side comparisons showing how Easy OpenCV simplifies computer vision tasks compared to traditional OpenCV code. Each comparison demonstrates the reduction in code complexity and the benefits of our wrapper.

## Table of Contents

1. [Basic Image Operations](#basic-image-operations)
2. [Image Processing](#image-processing)
3. [Object Detection](#object-detection)
4. [Video Operations](#video-operations)
5. [Drawing Operations](#drawing-operations)
6. [Feature Detection](#feature-detection)
7. [Filters](#filters)
8. [Transformations](#transformations)
9. [Utility Functions](#utility-functions)

## Basic Image Operations

### Loading Images

**Traditional OpenCV:**

```python
import cv2
import numpy as np

# Load image with error handling
try:
    img = cv2.imread('image.jpg')
    if img is None:
        raise FileNotFoundError("Image not found")
    # Convert to RGB from BGR
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
except Exception as e:
    print(f"Error: {e}")
```

**Easy OpenCV:**

```python
from easy_opencv import cv

# Load image with automatic error handling and optional color conversion
img = cv.load_image('image.jpg', mode='rgb')
```

### Saving Images

**Traditional OpenCV:**

```python
try:
    success = cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    if not success:
        print("Failed to save image")
except Exception as e:
    print(f"Error: {e}")
```

**Easy OpenCV:**

```python
cv.save_image(img, 'output.jpg', quality=95)
```

### Displaying Images

**Traditional OpenCV:**

```python
cv2.namedWindow('Image Display', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image Display', 800, 600)
cv2.imshow('Image Display', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Easy OpenCV:**

```python
cv.show_image(img, 'Image Display', size=(800, 600))
```

### Resizing Images

**Traditional OpenCV:**

```python
# Resize with calculated height to maintain aspect ratio
width = 800
aspect_ratio = img.shape[1] / img.shape[0]
height = int(width / aspect_ratio)
resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
```

**Easy OpenCV:**

```python
# Resize with automatic aspect ratio preservation
resized = cv.resize_image(img, width=800, method='linear')
```

### Image Information

**Traditional OpenCV:**

```python
height, width = img.shape[:2]
channels = img.shape[2] if len(img.shape) > 2 else 1
pixel_count = height * width
print(f"Image size: {width}x{height}, Channels: {channels}")
```

**Easy OpenCV:**

```python
info = cv.get_image_info(img)
print(f"Image size: {info['width']}x{info['height']}, Channels: {info['channels']}")
```

## Image Processing

### Edge Detection

**Traditional OpenCV:**

```python
# Convert to grayscale first
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# Apply Canny edge detection
edges = cv2.Canny(blurred, 100, 200)
```

**Easy OpenCV:**

```python
edges = cv.apply_edge_detection(img, method='canny')
```

### Thresholding

**Traditional OpenCV:**

```python
# Convert to grayscale first
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply threshold
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

**Easy OpenCV:**

```python
thresh = cv.apply_threshold(img, threshold=127, method='binary')
```

### Histogram Equalization

**Traditional OpenCV:**

```python
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply histogram equalization
equalized = cv2.equalizeHist(gray)
```

**Easy OpenCV:**

```python
equalized = cv.apply_histogram_equalization(img)
```

### Brightness and Contrast Adjustment

**Traditional OpenCV:**

```python
alpha = 1.5  # Contrast control
beta = 30    # Brightness control
adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
```

**Easy OpenCV:**

```python
adjusted = cv.adjust_brightness_contrast(img, brightness=30, contrast=1.5)
```

## Object Detection

### Face Detection

**Traditional OpenCV:**

```python
# Load the cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

**Easy OpenCV (Legacy Function):**

```python
faces = cv.detect_faces(img)
for (x, y, w, h) in faces:
    img = cv.draw_rectangle(img, (x, y), (x+w, y+h), color=(0, 255, 0))
```

**Easy OpenCV (Class-Based API with Webcam Support):**

```python
from easy_opencv import FaceDetector

detector = FaceDetector()
results = detector.detect_from_source('image.jpg', show_live=True)
# Or use webcam by default:
# results = detector.detect_from_source(show_live=True)
```

### Color Detection

**Traditional OpenCV:**

```python
# Convert to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define range for red color
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Create mask
mask = cv2.inRange(hsv, lower_red, upper_red)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 500:  # Filter by area
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
```

**Easy OpenCV (Class-Based API):**

```python
from easy_opencv import ColorDetector

detector = ColorDetector(target_color='red', min_area=500)
results = detector.detect_from_source('image.jpg', show_live=True)
```

### Motion Detection

**Traditional OpenCV:**

```python
# Create background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Apply background subtraction
fg_mask = bg_subtractor.apply(frame)

# Filter noise
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

# Find contours
contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Process contours
for contour in contours:
    if cv2.contourArea(contour) > 500:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

**Easy OpenCV (Class-Based API):**

```python
from easy_opencv import MotionDetector

detector = MotionDetector(method='mog2', sensitivity=500)
results = detector.detect_from_source(source=0, show_live=True)  # 0 = default webcam
```

## Video Operations

### Opening a Video

**Traditional OpenCV:**

```python
cap = cv2.VideoCapture('video.mp4')
if not cap.isOpened():
    print("Error: Could not open video.")
```

**Easy OpenCV:**

```python
video = cv.load_video('video.mp4')  # Handles errors automatically
```

### Reading Video Frames

**Traditional OpenCV:**

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    # ...

    cv2.imshow('Video', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Easy OpenCV (VideoPlayer Class):**

```python
player = cv.VideoPlayer()
player.play(video_path='video.mp4', processing_func=my_processing_function)
```

### Webcam Capture

**Traditional OpenCV:**

```python
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Easy OpenCV (WebcamCapture Class):**

```python
webcam = cv.WebcamCapture()
webcam.capture(camera_id=0, save_path="recording.mp4")  # With optional recording
```

### Frame Extraction

**Traditional OpenCV:**

```python
cap = cv2.VideoCapture('video.mp4')
count = 0
frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save every 10th frame
    if count % 10 == 0:
        cv2.imwrite(f'frame_{count}.jpg', frame)
    count += 1

cap.release()
```

**Easy OpenCV:**

```python
cv.extract_frames('video.mp4', output_dir='frames', step=10)
```

## Drawing Operations

### Drawing Shapes

**Traditional OpenCV:**

```python
# Copy image to avoid modifying original
result = img.copy()

# Draw rectangle
cv2.rectangle(result, (50, 50), (200, 200), (0, 255, 0), 2)

# Draw circle
cv2.circle(result, (300, 150), 50, (0, 0, 255), -1)

# Draw text
cv2.putText(result, "OpenCV", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
```

**Easy OpenCV:**

```python
# Each drawing operation returns a new image (non-destructive)
result = img.copy()
result = cv.draw_rectangle(result, (50, 50), (200, 200), color=(0, 255, 0))
result = cv.draw_circle(result, (300, 150), 50, color=(0, 0, 255), filled=True)
result = cv.draw_text(result, "OpenCV", (100, 300), color=(255, 255, 255))
```

## Feature Detection

### Corner Detection

**Traditional OpenCV:**

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
corners = cv2.cornerHarris(gray, 2, 3, 0.04)
corners = cv2.dilate(corners, None)

# Threshold for corner detection
img[corners > 0.01*corners.max()] = [0, 0, 255]
```

**Easy OpenCV:**

```python
corners = cv.detect_corners(img, method='harris')
result = cv.draw_corners(img, corners)
```

### Keypoint Detection

**Traditional OpenCV:**

```python
# Create SIFT detector
sift = cv2.SIFT_create()

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find keypoints and descriptors
keypoints, descriptors = sift.detectAndCompute(gray, None)

# Draw keypoints
result = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0),
                          flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
```

**Easy OpenCV:**

```python
keypoints, descriptors = cv.detect_keypoints(img, detector='sift')
result = cv.draw_keypoints(img, keypoints)
```

## Filters

### Gaussian Blur

**Traditional OpenCV:**

```python
blurred = cv2.GaussianBlur(img, (15, 15), 0)
```

**Easy OpenCV:**

```python
blurred = cv.apply_gaussian_blur(img, kernel_size=15)
```

### Custom Filters

**Traditional OpenCV:**

```python
kernel = np.array([[-1, -1, -1],
                  [-1,  9, -1],
                  [-1, -1, -1]])
sharpened = cv2.filter2D(img, -1, kernel)
```

**Easy OpenCV:**

```python
sharpened = cv.apply_custom_kernel(img, kernel_type='sharpen')
```

### Cartoon Effect

**Traditional OpenCV:**

```python
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply median blur
gray = cv2.medianBlur(gray, 5)

# Detect edges
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                             cv2.THRESH_BINARY, 9, 9)

# Apply bilateral filter
color = cv2.bilateralFilter(img, 9, 300, 300)

# Combine edges and color
cartoon = cv2.bitwise_and(color, color, mask=edges)
```

**Easy OpenCV:**

```python
cartoon = cv.apply_cartoon_filter(img)
```

## Transformations

### Image Rotation

**Traditional OpenCV:**

```python
rows, cols = img.shape[:2]
center = (cols/2, rows/2)
rotation_matrix = cv2.getRotationMatrix2D(center, angle=45, scale=1)
rotated = cv2.warpAffine(img, rotation_matrix, (cols, rows))
```

**Easy OpenCV:**

```python
rotated = cv.rotate_image(img, angle=45, keep_size=True)
```

### Perspective Transform

**Traditional OpenCV:**

```python
# Define source and destination points
pts1 = np.float32([[50, 50], [200, 50], [50, 200], [200, 200]])
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

# Calculate transformation matrix
matrix = cv2.getPerspectiveTransform(pts1, pts2)

# Apply perspective transformation
result = cv2.warpPerspective(img, matrix, (300, 300))
```

**Easy OpenCV:**

```python
source_points = [(50, 50), (200, 50), (50, 200), (200, 200)]
dest_points = [(0, 0), (300, 0), (0, 300), (300, 300)]
result = cv.apply_perspective_transform(img, source_points, dest_points, output_size=(300, 300))
```

## Utility Functions

### FPS Counter

**Traditional OpenCV:**

```python
import time

start_time = time.time()
frame_count = 0

while True:
    # Process frames
    frame_count += 1

    # Calculate FPS every second
    elapsed = time.time() - start_time
    if elapsed > 1:
        fps = frame_count / elapsed
        print(f"FPS: {fps:.2f}")
        start_time = time.time()
        frame_count = 0
```

**Easy OpenCV:**

```python
fps_counter = cv.fps_counter()

while True:
    # Process frames
    fps = fps_counter.update()
    print(f"FPS: {fps:.2f}")
```

### Image Comparison

**Traditional OpenCV:**

```python
# Calculate structural similarity index
import skimage.metrics

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

ssim_index = skimage.metrics.structural_similarity(gray1, gray2)
print(f"SSIM: {ssim_index}")

# Calculate mean squared error
mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
print(f"MSE: {mse}")
```

**Easy OpenCV:**

```python
comparison = cv.image_comparison(img1, img2, methods=['ssim', 'mse'])
print(f"SSIM: {comparison['ssim']}")
print(f"MSE: {comparison['mse']}")
```

### Auto Canny

**Traditional OpenCV:**

```python
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Calculate median pixel intensity
v = np.median(gray)

# Determine thresholds based on intensity
sigma = 0.33
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))

# Apply Canny edge detection
edges = cv2.Canny(gray, lower, upper)
```

**Easy OpenCV:**

```python
edges = cv.auto_canny(img, sigma=0.33)
```
