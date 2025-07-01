# Object Detection Classes Usage Guide

## Overview

The Easy OpenCV library now provides a comprehensive class-based object detection system with automatic webcam fallback. When no image or video path is provided, the system automatically uses the default webcam as input.

## Key Features

- **Automatic Webcam Fallback**: If no source is provided, uses webcam automatically
- **Multiple Input Sources**: Support for images, videos, and webcam streams
- **Object-Oriented Design**: Clean, reusable classes for each detection type
- **Live Visualization**: Real-time detection display with bounding boxes
- **Legacy Function Support**: All old functions still work for backward compatibility

## Available Classes

### 1. ImageSource

Base class for handling different image/video sources with automatic webcam fallback.

```python
from easy_opencv.object_detection import ImageSource

# Use default webcam (source=None)
with ImageSource() as source:
    frame = source.get_frame()

# Use specific webcam (source=0, 1, 2, etc.)
with ImageSource(0) as source:
    frame = source.get_frame()

# Use image file
with ImageSource("path/to/image.jpg") as source:
    frame = source.get_frame()

# Use video file
with ImageSource("path/to/video.mp4") as source:
    while True:
        frame = source.get_frame()
        if frame is None:
            break
```

### 2. FaceDetector

Detects faces using Haar cascades with webcam support.

```python
from easy_opencv.object_detection import FaceDetector

# Create detector
face_detector = FaceDetector(scale_factor=1.1, min_neighbors=5, min_size=(30, 30))

# Detect from webcam (auto-fallback)
results = face_detector.detect_from_source()

# Detect from specific webcam
results = face_detector.detect_from_source(source=0)

# Detect from image file
results = face_detector.detect_from_source(source="image.jpg")

# Detect from video file
results = face_detector.detect_from_source(source="video.mp4")

# Programmatic detection (single frame)
import cv2
image = cv2.imread("image.jpg")
faces = face_detector.detect(image)
print(f"Found {len(faces)} faces: {faces}")
```

### 3. EyeDetector

Detects eyes using Haar cascades with webcam support.

```python
from easy_opencv.object_detection import EyeDetector

# Create detector
eye_detector = EyeDetector(scale_factor=1.1, min_neighbors=5, min_size=(20, 20))

# Detect from webcam (auto-fallback)
results = eye_detector.detect_from_source()

# Disable live display
results = eye_detector.detect_from_source(show_live=False)
```

### 4. CascadeDetector

Generic cascade detector for custom Haar cascade files.

```python
from easy_opencv.object_detection import CascadeDetector

# Create detector with custom cascade
cascade_detector = CascadeDetector(
    cascade_path="path/to/custom_cascade.xml",
    scale_factor=1.1,
    min_neighbors=5,
    min_size=(30, 30)
)

# Detect from webcam
results = cascade_detector.detect_from_source()
```

### 5. MotionDetector

Detects motion in video streams with background subtraction.

```python
from easy_opencv.object_detection import MotionDetector

# Create detector
motion_detector = MotionDetector(
    method='mog2',  # or 'knn'
    learning_rate=0.01,
    sensitivity=500
)

# Detect from webcam and save output
results = motion_detector.detect_from_source(
    source=None,  # webcam
    show_live=True,
    output_path="motion_output.mp4"  # optional
)
```

### 6. CircleDetector

Detects circles using Hough Circle Transform.

```python
from easy_opencv.object_detection import CircleDetector

# Create detector
circle_detector = CircleDetector(
    min_radius=10,
    max_radius=100,
    sensitivity=50
)

# Detect from webcam
results = circle_detector.detect_from_source()
```

### 7. LineDetector

Detects lines using Hough Line Transform.

```python
from easy_opencv.object_detection import LineDetector

# Create detector
line_detector = LineDetector(
    threshold=100,
    min_line_length=50,
    max_line_gap=10
)

# Detect from webcam
results = line_detector.detect_from_source()
```

### 8. ColorDetector

Detects objects based on color in HSV color space.

```python
from easy_opencv.object_detection import ColorDetector

# Create detector for red objects
color_detector = ColorDetector(target_color='red', tolerance=20)

# Supported colors: 'red', 'green', 'blue', 'yellow', 'orange', 'purple'
green_detector = ColorDetector(target_color='green', tolerance=15)

# Detect from webcam
results = color_detector.detect_from_source()
```

### 9. DNNObjectDetector

Detects objects using pre-trained deep neural networks (SSD MobileNet V2).

```python
from easy_opencv.object_detection import DNNObjectDetector

# Create detector (downloads model on first use)
dnn_detector = DNNObjectDetector(
    confidence_threshold=0.5,
    nms_threshold=0.4
)

# Detect from webcam
results = dnn_detector.detect_from_source()

# Returns: List[List[Tuple[str, float, Tuple[int, int, int, int]]]]
# Each detection: (class_name, confidence, (x, y, w, h))
```

## Usage Patterns

### 1. Automatic Webcam Fallback

```python
# All these will use webcam if no source specified
face_detector = FaceDetector()
results = face_detector.detect_from_source()  # Uses default webcam

eye_detector = EyeDetector()
results = eye_detector.detect_from_source(source=None)  # Explicit webcam

motion_detector = MotionDetector()
results = motion_detector.detect_from_source()  # Uses webcam for motion detection
```

### 2. Multiple Source Types

```python
detector = FaceDetector()

# Image file
results = detector.detect_from_source("photo.jpg")

# Video file
results = detector.detect_from_source("video.mp4")

# Webcam index
results = detector.detect_from_source(0)  # First webcam
results = detector.detect_from_source(1)  # Second webcam

# Default webcam
results = detector.detect_from_source(None)
results = detector.detect_from_source()  # Same as above
```

### 3. Programmatic Detection

```python
import cv2
from easy_opencv.object_detection import FaceDetector

# Load image
image = cv2.imread("image.jpg")

# Create detector
detector = FaceDetector()

# Detect faces (returns list of (x, y, w, h) tuples)
faces = detector.detect(image)

# Draw rectangles
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Display result
cv2.imshow("Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 4. Batch Processing

```python
import cv2
import os
from easy_opencv.object_detection import FaceDetector

detector = FaceDetector()

# Process all images in a directory
image_dir = "path/to/images"
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)

        faces = detector.detect(image)
        print(f"{filename}: {len(faces)} faces detected")
```

### 5. Real-time Processing with Custom Logic

```python
import cv2
from easy_opencv.object_detection import FaceDetector

detector = FaceDetector()

cap = cv2.VideoCapture(0)  # Use webcam
face_count_history = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces
        faces = detector.detect(frame)
        face_count_history.append(len(faces))

        # Keep only last 10 frames
        if len(face_count_history) > 10:
            face_count_history.pop(0)

        # Calculate average face count
        avg_faces = sum(face_count_history) / len(face_count_history)

        # Draw faces and info
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(frame, f"Faces: {len(faces)} (Avg: {avg_faces:.1f})",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
```

## Error Handling

```python
from easy_opencv.object_detection import FaceDetector

detector = FaceDetector()

try:
    # This will automatically fallback to webcam if image doesn't exist
    results = detector.detect_from_source("nonexistent_image.jpg")
except ValueError as e:
    print(f"Error: {e}")
    # Fallback to webcam
    results = detector.detect_from_source()
```

## Performance Tips

1. **Adjust Detection Parameters**: Lower `scale_factor` and higher `min_neighbors` for better accuracy but slower performance.

2. **Use Appropriate Sensitivity**: For motion detection, adjust `sensitivity` based on your use case.

3. **Process Every Nth Frame**: For real-time applications, process every 2nd or 3rd frame to improve performance.

```python
frame_count = 0
detector = FaceDetector()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Process every 3rd frame
    if frame_count % 3 == 0:
        faces = detector.detect(frame)
        # Draw faces...

    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

## Legacy Function Support

All original functions still work for backward compatibility:

```python
import cv2
from easy_opencv.object_detection import detect_faces, detect_eyes, detect_objects_dnn

# Load image
image = cv2.imread("image.jpg")

# Legacy functions still work
faces = detect_faces(image)
eyes = detect_eyes(image)
objects = detect_objects_dnn(image)
```

## Complete Example

```python
"""
Complete object detection example with webcam fallback
"""
import cv2
from easy_opencv.object_detection import FaceDetector, DNNObjectDetector

def main():
    # Try to detect faces from an image, fallback to webcam
    face_detector = FaceDetector()

    # If you have an image file, specify it; otherwise uses webcam
    image_path = "your_image.jpg"  # Change this or set to None for webcam

    try:
        print("Starting face detection...")
        results = face_detector.detect_from_source(
            source=image_path,  # Will use webcam if file doesn't exist
            show_live=True
        )
        print(f"Detection completed. Processed {len(results)} frames/images.")

    except KeyboardInterrupt:
        print("Detection interrupted by user.")
    except Exception as e:
        print(f"Error during detection: {e}")

if __name__ == "__main__":
    main()
```

This new class-based system provides a much more flexible and user-friendly way to perform object detection while maintaining full backward compatibility with existing code.
