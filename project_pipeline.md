# Easy OpenCV Pipeline Diagram

## Project Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Easy OpenCV Project Structure                   │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Package Dependencies                          │
│                                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐               │
│  │ OpenCV-    │     │ NumPy      │     │ Pillow     │               │
│  │ Python     │     │            │     │            │               │
│  └────────────┘     └────────────┘     └────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Core Module Structure                         │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐    │
│   │                      easy_opencv/__init__.py                │    │
│   │                                                             │    │
│   │  - Imports all modules                                      │    │
│   │  - Exposes main classes for direct access                   │    │
│   │  - Creates global 'cv' instance of EasyCV class             │    │
│   │  - Package metadata                                         │    │
│   └─────────────────────────────────────────────────────────────┘    │
│                                   │                                  │
│                                   ▼                                  │
│   ┌─────────────────────────────────────────────────────────────┐    │
│   │                      EasyCV Main Class                      │    │
│   │                                                             │    │
│   │  - Provides access to all module functions                  │    │
│   │  - Creates global 'cv' instance                             │    │
│   └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       Functional Module Layers                       │
└──────────────────────────────────────────────────────────────────────┘
          │                 │                  │                 │
          ▼                 ▼                  ▼                 ▼
┌──────────────┐   ┌───────────────┐   ┌───────────────┐  ┌────────────┐
│ Input/Output │   │ Processing &  │   │ Detection &   │  │ Utilities  │
│ Layer        │   │ Filtering     │   │ Drawing       │  │ Layer      │
└──────────────┘   └───────────────┘   └───────────────┘  └────────────┘
       │                  │                   │                 │
       ▼                  ▼                   ▼                 ▼
┌──────────────┐   ┌───────────────┐   ┌───────────────┐  ┌────────────┐
│- image_ops   │   │- image_proc   │   │- object_det   │  │- utils.py  │
│- video_ops   │   │- transforms   │   │- feature_det  │  │            │
│              │   │- filters      │   │- drawing_ops  │  │            │
└──────────────┘   └───────────────┘   └───────────────┘  └────────────┘
```

## Class Hierarchies and Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                     Object Detection Pipeline                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          ImageSource                            │
│                                                                 │
│  - Base class for handling different image/video inputs         │
│  - Automatic webcam fallback when no source provided            │
│  - Context manager pattern for resource cleanup                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
     ┌──────────────┬─────────┴──────────┬───────────────┐
     │              │                    │               │
     ▼              ▼                    ▼               ▼
┌────────────┐ ┌────────────┐     ┌────────────┐  ┌────────────┐
│FaceDetector│ │EyeDetector │     │ColorDetector│  │DNNDetector │
└────────────┘ └────────────┘     └────────────┘  └────────────┘
     │              │                    │               │
     └──────────────┴─────────┬─────────┴───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    detect_from_source() Method                  │
│                                                                 │
│  - Common pattern across all detector classes                   │
│  - Takes optional source parameter                              │
│  - Handles both image and video/webcam inputs                   │
│  - Returns detection results                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Demo Application Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    demo_object_detection.py                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          main()                                 │
│  - Entry point that displays menu of demo options               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
    ┌───────────────┬─────────┴──────────┬─────────────────┐
    │               │                    │                 │
    ▼               ▼                    ▼                 ▼
┌───────────┐ ┌────────────┐     ┌───────────────┐ ┌───────────────┐
│demo_webcam │ │demo_sources│     │demo_class_vs_ │ │exit           │
│_fallback() │ │()          │     │legacy()       │ │               │
└───────────┘ └────────────┘     └───────────────┘ └───────────────┘
    │
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│              Interactive Object Detection Options               │
│                                                                 │
│  1. Face Detection                                              │
│  2. Eye Detection                                               │
│  3. Red Color Detection                                         │
│  4. Exit                                                        │
└─────────────────────────────────────────────────────────────────┘
    │
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Detector Pattern Usage                       │
│                                                                 │
│  1. Create detector instance                                    │
│  2. Call detect_from_source() with show_live=True               │
│  3. Process results                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                        User Input / API Call                         │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Input Source Resolution                         │
│                                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐               │
│  │ Image      │     │ Video      │     │ Webcam     │               │
│  │ File       │     │ File       │     │            │               │
│  └────────────┘     └────────────┘     └────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Processing Pipeline                          │
│                                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐               │
│  │Pre-process │     │Run         │     │Post-process│               │
│  │(as needed) │ ──► │Detection   │ ──► │Results     │               │
│  └────────────┘     └────────────┘     └────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                             Output Options                           │
│                                                                      │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐               │
│  │Live        │     │Return      │     │Save to     │               │
│  │Display     │     │Results     │     │File        │               │
│  └────────────┘     └────────────┘     └────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
```

## API Usage Patterns

### 1. Legacy Function Style

```python
from easy_opencv import cv

# Load an image
image = cv.load_image('photo.jpg')

# Detect faces
faces = cv.detect_faces(image)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv.draw_rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0))

# Show the result
cv.show_image(image, 'Face Detection')
```

### 2. Modern Class-Based Style

```python
from easy_opencv import FaceDetector

# Create detector
detector = FaceDetector()

# Automatically uses webcam if no source provided
results = detector.detect_from_source(show_live=True)
```

### 3. Direct Module Import

```python
from easy_opencv.object_detection import detect_faces
from easy_opencv.image_operations import load_image, show_image
from easy_opencv.drawing_operations import draw_rectangle

# Load image
image = load_image('photo.jpg')

# Detect faces
faces = detect_faces(image)

# Draw and display
for face in faces:
    draw_rectangle(image, (face[0], face[1]),
                  (face[0]+face[2], face[1]+face[3]),
                  color=(0, 255, 0))
show_image(image, 'Face Detection')
```
