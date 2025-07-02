# Easy OpenCV Project Pipeline

## Overview

Easy OpenCV is a simplified wrapper library that makes computer vision operations more accessible by providing an intuitive interface to OpenCV functions. The library follows a modular design and offers both function-based and class-based APIs for different use cases.

## Project Structure and Dependencies

```
Easy OpenCV Project
├── easy_opencv/                    # Main package directory
│   ├── __init__.py                # Package initialization and EasyCV class
│   ├── image_operations.py        # Basic image operations
│   ├── video_operations.py        # Video processing
│   ├── image_processing.py        # Image enhancement and filters
│   ├── feature_detection.py       # Feature detection
│   ├── object_detection.py        # Object detection with various detectors
│   ├── drawing_operations.py      # Drawing and annotation
│   ├── filters.py                 # Creative filters
│   ├── transformations.py         # Image transformations
│   └── utils.py                   # Utility functions
├── examples/                       # Example scripts
├── demo_object_detection.py        # Demo application
├── requirements.txt                # Package dependencies
└── setup.py                        # Package setup configuration
```

**Dependencies:**

- opencv-python
- numpy
- pillow (optional)

## Core Components

1. **EasyCV Class**: Central access point that provides a unified interface to all module functions
2. **Object Detection Classes**: Set of specialized detector classes with a common interface
3. **Image/Video Handling Classes**: Classes for loading, processing, and saving visual data
4. **Utility Functions**: Helper functions for common tasks

## Data Flow Pipeline

1. **Input Source Resolution**:

   - The library can accept images, video files, or webcam streams
   - The `ImageSource` class handles source determination and resource management
   - Automatic webcam fallback when no source is specified

2. **Processing Pipeline**:

   - **Pre-processing**: Format conversion, resizing, normalization (as needed)
   - **Core Operation**: Detection, transformation, or filtering algorithm
   - **Post-processing**: Drawing, annotation, result formatting

3. **Output Handling**:
   - Live visualization (optional)
   - Return processed results
   - Save to file (optional)

## Usage Patterns

### 1. Direct Function Access (Legacy Style)

```python
from easy_opencv import cv

image = cv.load_image('photo.jpg')
faces = cv.detect_faces(image)
result = cv.draw_bounding_boxes(image, faces, color=(0, 255, 0))
cv.show_image(result, 'Face Detection')
```

### 2. Class-Based API (Modern Style)

```python
from easy_opencv import FaceDetector

detector = FaceDetector(min_neighbors=5)
results = detector.detect_from_source('photo.jpg', show_live=True)
```

### 3. Module-Specific Imports

```python
from easy_opencv.object_detection import detect_faces
from easy_opencv.image_operations import load_image

image = load_image('photo.jpg')
faces = detect_faces(image)
```

## Demo Application Flow

The `demo_object_detection.py` file showcases the library's capabilities:

1. **Main Menu**: Options to demonstrate different aspects of the library
2. **Webcam Fallback**: Shows how detectors automatically use webcam when no source is specified
3. **Different Sources**: Demonstrates using various input sources
4. **Class vs. Legacy**: Compares the class-based and function-based APIs

## Object Detection Pipeline

The object detection pipeline is a prime example of the library's design:

1. **Source Selection**:

   - `ImageSource` class determines if input is webcam, video, or image
   - Context manager (`__enter__` and `__exit__`) handles resource cleanup

2. **Detector Classes**:

   - Each detector implements a common interface
   - `detect()` method processes a single image
   - `detect_from_source()` method handles any input source

3. **Result Processing**:
   - Detection results are standardized across detectors
   - Optional live visualization
   - Results returned for further processing

## Key Design Patterns

1. **Facade Pattern**: EasyCV class provides simplified access to complex functionality
2. **Strategy Pattern**: Different detector classes implement the same interface
3. **Context Manager**: ImageSource manages resource lifecycle
4. **Factory Methods**: Methods that create and configure OpenCV objects

## Best Practices for Extension

1. Follow the existing class structure for new detectors
2. Implement both `detect()` and `detect_from_source()` methods
3. Use the `ImageSource` class for input handling
4. Maintain backward compatibility with legacy functions
