"""
Object Detection Module
Provides easy-to-use classes and functions for object detection with webcam support
"""

import cv2
import numpy as np
import os
import tarfile
from typing import List, Tuple, Optional, Union
from .utils import download_file

class ImageSource:
    """Base class for handling different image/video sources"""
    
    def __init__(self, source: Optional[Union[str, int]] = None):
        """
        Initialize image source
        
        Args:
            source: Path to image/video file, webcam index (0, 1, etc), or None for default webcam
        """
        self.source = source
        self.cap = None
        self.is_video = False
        self.is_webcam = False
        
    def __enter__(self):
        if self.source is None or isinstance(self.source, int):
            # Use webcam
            self.cap = cv2.VideoCapture(self.source or 0)
            self.is_webcam = True
            if not self.cap.isOpened():
                raise ValueError(f"Could not open webcam {self.source or 0}")
        elif isinstance(self.source, str):
            if self.source.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                # Single image
                self.is_video = False
            else:
                # Video file
                self.cap = cv2.VideoCapture(self.source)
                self.is_video = True
                if not self.cap.isOpened():
                    raise ValueError(f"Could not open video file: {self.source}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get a frame from the source"""
        if self.cap is not None:
            ret, frame = self.cap.read()
            return frame if ret else None
        elif isinstance(self.source, str) and not self.is_video:
            # Load single image
            return cv2.imread(self.source)
        return None


class FaceDetector:
    """Face detection using Haar cascades with webcam support"""
    
    def __init__(self, scale_factor: float = 1.1, min_neighbors: int = 5, 
                 min_size: Tuple[int, int] = (30, 30)):
        """
        Initialize face detector
        
        Args:
            scale_factor: Scale factor for detection
            min_neighbors: Minimum number of neighbor rectangles
            min_size: Minimum face size
        """
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image
        
        Args:
            image: Input image
            
        Returns:
            List of face rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size
        )
        
        return faces.tolist() if isinstance(faces, np.ndarray) and len(faces) > 0 else []
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None, 
                          show_live: bool = True) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect faces from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    faces = self.detect(frame)
                    results.append(faces)
                    
                    if show_live:
                        # Draw rectangles around faces
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        
                        cv2.imshow('Face Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    faces = self.detect(frame)
                    results.append(faces)
                    
                    if show_live:
                        # Draw rectangles around faces
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        
                        cv2.imshow('Face Detection', frame)
                        cv2.waitKey(0)
        
        return results


class EyeDetector:
    """Eye detection using Haar cascades with webcam support"""
    
    def __init__(self, scale_factor: float = 1.1, min_neighbors: int = 5,
                 min_size: Tuple[int, int] = (20, 20)):
        """
        Initialize eye detector
        
        Args:
            scale_factor: Scale factor for detection
            min_neighbors: Minimum number of neighbor rectangles
            min_size: Minimum eye size
        """
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect eyes in an image
        
        Args:
            image: Input image
            
        Returns:
            List of eye rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        eyes = self.eye_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size
        )
        
        return eyes.tolist() if isinstance(eyes, np.ndarray) and len(eyes) > 0 else []
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect eyes from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    eyes = self.detect(frame)
                    results.append(eyes)
                    
                    if show_live:
                        # Draw rectangles around eyes
                        for (x, y, w, h) in eyes:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        cv2.imshow('Eye Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    eyes = self.detect(frame)
                    results.append(eyes)
                    
                    if show_live:
                        # Draw rectangles around eyes
                        for (x, y, w, h) in eyes:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        cv2.imshow('Eye Detection', frame)
                        cv2.waitKey(0)
        
        return results


class CascadeDetector:
    """Generic cascade detector with webcam support"""
    
    def __init__(self, cascade_path: str, scale_factor: float = 1.1,
                 min_neighbors: int = 5, min_size: Tuple[int, int] = (30, 30)):
        """
        Initialize cascade detector
        
        Args:
            cascade_path: Path to cascade XML file
            scale_factor: Scale factor for detection
            min_neighbors: Minimum number of neighbor rectangles
            min_size: Minimum object size
        """
        self.cascade_path = cascade_path
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.cascade = cv2.CascadeClassifier(cascade_path)
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect objects in an image
        
        Args:
            image: Input image
            
        Returns:
            List of object rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        objects = self.cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size
        )
        
        return objects.tolist() if isinstance(objects, np.ndarray) and len(objects) > 0 else []
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect objects from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    objects = self.detect(frame)
                    results.append(objects)
                    
                    if show_live:
                        # Draw rectangles around detected objects
                        for (x, y, w, h) in objects:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        
                        cv2.imshow('Object Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    objects = self.detect(frame)
                    results.append(objects)
                    
                    if show_live:
                        # Draw rectangles around detected objects
                        for (x, y, w, h) in objects:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        
                        cv2.imshow('Object Detection', frame)
                        cv2.waitKey(0)
        
        return results


class MotionDetector:
    """Motion detection with webcam support"""
    
    def __init__(self, method: str = 'mog2', learning_rate: float = 0.01,
                 sensitivity: int = 500):
        """
        Initialize motion detector
        
        Args:
            method: Background subtraction method - 'mog2', 'knn'
            learning_rate: Learning rate for background model
            sensitivity: Motion detection sensitivity (minimum contour area)
        """
        self.method = method
        self.learning_rate = learning_rate
        self.sensitivity = sensitivity
        
        if method == 'mog2':
            self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
        elif method == 'knn':
            self.bg_subtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        else:
            self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    
    def detect(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect motion in a frame
        
        Args:
            frame: Input frame
            
        Returns:
            List of motion bounding boxes (x, y, w, h)
        """
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame, learningRate=self.learning_rate)
        
        # Find contours of moving objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_boxes = []
        for contour in contours:
            if cv2.contourArea(contour) > self.sensitivity:
                x, y, w, h = cv2.boundingRect(contour)
                motion_boxes.append((x, y, w, h))
        
        return motion_boxes
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True, output_path: Optional[str] = None) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect motion from video file or webcam
        
        Args:
            source: Video path or webcam index (None for default webcam)
            show_live: Whether to show live detection
            output_path: Path to save output video (optional)
            
        Returns:
            List of motion detection results for each frame
        """
        results = []
        writer = None
        
        with ImageSource(source) as img_source:
            if output_path and (img_source.is_webcam or img_source.is_video):
                # Setup video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = img_source.cap.get(cv2.CAP_PROP_FPS) if img_source.cap else 30.0
                
                # Get first frame to determine dimensions
                first_frame = img_source.get_frame()
                if first_frame is not None:
                    height, width = first_frame.shape[:2]
                    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    # Process first frame
                    motion_boxes = self.detect(first_frame)
                    results.append(motion_boxes)
                    
                    if show_live:
                        for (x, y, w, h) in motion_boxes:
                            cv2.rectangle(first_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.imshow('Motion Detection', first_frame)
                    
                    if writer:
                        writer.write(first_frame)
            
            # Process remaining frames
            while True:
                frame = img_source.get_frame()
                if frame is None:
                    break
                
                motion_boxes = self.detect(frame)
                results.append(motion_boxes)
                
                if show_live:
                    # Draw bounding boxes around detected motion
                    for (x, y, w, h) in motion_boxes:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    cv2.imshow('Motion Detection', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                if writer:
                    writer.write(frame)
        
        if writer:
            writer.release()
        
        return results


class CircleDetector:
    """Circle detection using Hough Transform with webcam support"""
    
    def __init__(self, min_radius: int = 10, max_radius: int = 100,
                 sensitivity: int = 50):
        """
        Initialize circle detector
        
        Args:
            min_radius: Minimum circle radius
            max_radius: Maximum circle radius
            sensitivity: Detection sensitivity
        """
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.sensitivity = sensitivity
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int]]:
        """
        Detect circles in an image
        
        Args:
            image: Input image
            
        Returns:
            List of circles (x, y, radius)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=self.sensitivity,
            param1=50,
            param2=30,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            return [(x, y, r) for x, y, r in circles]
        
        return []
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[List[Tuple[int, int, int]]]:
        """
        Detect circles from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    circles = self.detect(frame)
                    results.append(circles)
                    
                    if show_live:
                        # Draw circles
                        for (x, y, r) in circles:
                            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                        
                        cv2.imshow('Circle Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    circles = self.detect(frame)
                    results.append(circles)
                    
                    if show_live:
                        # Draw circles
                        for (x, y, r) in circles:
                            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
                        
                        cv2.imshow('Circle Detection', frame)
                        cv2.waitKey(0)
        
        return results


class LineDetector:
    """Line detection using Hough Transform with webcam support"""
    
    def __init__(self, threshold: int = 100, min_line_length: int = 50,
                 max_line_gap: int = 10):
        """
        Initialize line detector
        
        Args:
            threshold: Accumulator threshold
            min_line_length: Minimum line length
            max_line_gap: Maximum allowed gap between line segments
        """
        self.threshold = threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect lines in an image
        
        Args:
            image: Input image
            
        Returns:
            List of lines (x1, y1, x2, y2)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=self.threshold,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap
        )
        
        if lines is not None:
            return [tuple(line[0]) for line in lines]
        
        return []
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[List[Tuple[int, int, int, int]]]:
        """
        Detect lines from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    lines = self.detect(frame)
                    results.append(lines)
                    
                    if show_live:
                        # Draw lines
                        for (x1, y1, x2, y2) in lines:
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        cv2.imshow('Line Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    lines = self.detect(frame)
                    results.append(lines)
                    
                    if show_live:
                        # Draw lines
                        for (x1, y1, x2, y2) in lines:
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        cv2.imshow('Line Detection', frame)
                        cv2.waitKey(0)
        
        return results


class ColorDetector:
    """Color-based object detection with webcam support"""
    
    def __init__(self, target_color: str = 'red', tolerance: int = 20):
        """
        Initialize color detector
        
        Args:
            target_color: Target color name
            tolerance: Color tolerance
        """
        self.target_color = target_color
        self.tolerance = tolerance
        
        # Define color ranges in HSV
        self.color_ranges = {
            'red': [(0, 50, 50), (10, 255, 255)],
            'green': [(40, 50, 50), (80, 255, 255)],
            'blue': [(100, 50, 50), (130, 255, 255)],
            'yellow': [(20, 50, 50), (30, 255, 255)],
            'orange': [(10, 50, 50), (20, 255, 255)],
            'purple': [(130, 50, 50), (160, 255, 255)]
        }
    
    def detect(self, image: np.ndarray) -> np.ndarray:
        """
        Detect objects of a specific color
        
        Args:
            image: Input image
            
        Returns:
            Binary mask of detected color
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        if self.target_color.lower() in self.color_ranges:
            lower, upper = self.color_ranges[self.target_color.lower()]
            lower = np.array([max(0, lower[0] - self.tolerance), lower[1], lower[2]])
            upper = np.array([min(179, upper[0] + self.tolerance), upper[1], upper[2]])
            
            mask = cv2.inRange(hsv, lower, upper)
            return mask
        
        return np.zeros(image.shape[:2], dtype=np.uint8)
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[np.ndarray]:
        """
        Detect color from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection masks for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    mask = self.detect(frame)
                    results.append(mask)
                    
                    if show_live:
                        # Apply mask to original image
                        result = cv2.bitwise_and(frame, frame, mask=mask)
                        
                        # Show both original and masked image
                        display = np.hstack([frame, result])
                        cv2.imshow(f'{self.target_color.title()} Detection', display)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    mask = self.detect(frame)
                    results.append(mask)
                    
                    if show_live:
                        # Apply mask to original image
                        result = cv2.bitwise_and(frame, frame, mask=mask)
                        
                        # Show both original and masked image
                        display = np.hstack([frame, result])
                        cv2.imshow(f'{self.target_color.title()} Detection', display)
                        cv2.waitKey(0)
        
        return results


class DNNObjectDetector:
    """Deep neural network object detection with webcam support"""
    
    def __init__(self, confidence_threshold: float = 0.5, nms_threshold: float = 0.4):
        """
        Initialize DNN object detector
        
        Args:
            confidence_threshold: Minimum confidence for a detection
            nms_threshold: Non-Maximum Suppression threshold
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        
        # Model file paths
        self.model_url = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"
        self.config_url = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
        self.names_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/dnn/object_detection_classes_coco.txt"
        
        self.model_path = "ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb"
        self.config_path = "ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
        self.names_path = "object_detection_classes_coco.txt"
        
        self.net = None
        self.classes = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Download and initialize the model"""
        # Download and extract the model files if they don't exist
        if not os.path.exists(self.model_path):
            print("Downloading and extracting model...")
            download_file(self.model_url, "ssd_mobilenet_v2_coco_2018_03_29.tar.gz", 
                         description="SSD MobileNet V2 Model")
            with tarfile.open("ssd_mobilenet_v2_coco_2018_03_29.tar.gz", "r:gz") as tar:
                tar.extractall()
            os.remove("ssd_mobilenet_v2_coco_2018_03_29.tar.gz")

        download_file(self.config_url, self.config_path, description="Model Config")
        download_file(self.names_url, self.names_path, description="Class Names")

        # Load the COCO class labels
        with open(self.names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # Load the serialized model from disk
        self.net = cv2.dnn.readNetFromTensorflow(self.model_path, self.config_path)
    
    def detect(self, image: np.ndarray) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
        """
        Detect objects in an image
        
        Args:
            image: Input image
            
        Returns:
            List of detected objects: (class_name, confidence, (x, y, w, h))
        """
        if self.net is None:
            self._initialize_model()
        
        # Get image dimensions
        (H, W) = image.shape[:2]

        # Construct a blob from the input image and perform forward pass
        blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
        self.net.setInput(blob)
        detections = self.net.forward()

        boxes = []
        confidences = []
        classIDs = []

        # Loop over the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence_threshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")

                x = startX
                y = startY
                w = endX - startX
                h = endY - startY

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classIDs.append(idx)

        # Apply non-maxima suppression
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

        detected_objects = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                label = str(self.classes[classIDs[i]])
                confidence = confidences[i]
                detected_objects.append((label, confidence, (x, y, w, h)))

        return detected_objects
    
    def detect_from_source(self, source: Optional[Union[str, int]] = None,
                          show_live: bool = True) -> List[List[Tuple[str, float, Tuple[int, int, int, int]]]]:
        """
        Detect objects from image file, video file, or webcam
        
        Args:
            source: Image/video path or webcam index (None for default webcam)
            show_live: Whether to show live detection (for video/webcam)
            
        Returns:
            List of detection results for each frame
        """
        results = []
        
        with ImageSource(source) as img_source:
            if img_source.is_webcam or img_source.is_video:
                # Process video/webcam frames
                while True:
                    frame = img_source.get_frame()
                    if frame is None:
                        break
                    
                    objects = self.detect(frame)
                    results.append(objects)
                    
                    if show_live:
                        # Draw bounding boxes and labels
                        for label, confidence, (x, y, w, h) in objects:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            text = f"{label}: {confidence:.2f}"
                            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.5, (0, 255, 0), 2)
                        
                        cv2.imshow('DNN Object Detection', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                # Process single image
                frame = img_source.get_frame()
                if frame is not None:
                    objects = self.detect(frame)
                    results.append(objects)
                    
                    if show_live:
                        # Draw bounding boxes and labels
                        for label, confidence, (x, y, w, h) in objects:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            text = f"{label}: {confidence:.2f}"
                            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.5, (0, 255, 0), 2)
                        
                        cv2.imshow('DNN Object Detection', frame)
                        cv2.waitKey(0)
        
        return results


# Legacy function wrappers for backward compatibility
def detect_faces(image: np.ndarray, scale_factor: float = 1.1,
                min_neighbors: int = 5, min_size: Tuple[int, int] = (30, 30)) -> List[Tuple[int, int, int, int]]:
    """
    Detect faces in an image using Haar cascades (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum face size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of face rectangles (x, y, w, h)
    """
    detector = FaceDetector(scale_factor, min_neighbors, min_size)
    return detector.detect(image)


def detect_eyes(image: np.ndarray, scale_factor: float = 1.1,
               min_neighbors: int = 5, min_size: Tuple[int, int] = (20, 20)) -> List[Tuple[int, int, int, int]]:
    """
    Detect eyes in an image using Haar cascades (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum eye size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of eye rectangles (x, y, w, h)
    """
    detector = EyeDetector(scale_factor, min_neighbors, min_size)
    return detector.detect(image)


def detect_objects_cascade(image: np.ndarray, cascade_path: str,
                          scale_factor: float = 1.1, min_neighbors: int = 5,
                          min_size: Tuple[int, int] = (30, 30)) -> List[Tuple[int, int, int, int]]:
    """
    Detect objects using custom Haar cascade classifier (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        cascade_path (str): Path to cascade XML file
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum object size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of object rectangles (x, y, w, h)
    """
    detector = CascadeDetector(cascade_path, scale_factor, min_neighbors, min_size)
    return detector.detect(image)


def background_subtraction(video_path: str, method: str = 'mog2',
                          learning_rate: float = 0.01) -> cv2.BackgroundSubtractor:
    """
    Create a background subtractor for motion detection (Legacy function)
    
    Args:
        video_path (str): Path to video file
        method (str): Background subtraction method - 'mog2', 'knn', 'gmm'
        learning_rate (float): Learning rate for background model
    
    Returns:
        cv2.BackgroundSubtractor: Background subtractor object
    """
    if method == 'mog2':
        return cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    elif method == 'knn':
        return cv2.createBackgroundSubtractorKNN(detectShadows=True)
    else:
        return cv2.createBackgroundSubtractorMOG2(detectShadows=True)


def detect_motion(video_path: str, output_path: Optional[str] = None,
                 sensitivity: int = 500) -> None:
    """
    Detect motion in a video and optionally save the result (Legacy function)
    
    Args:
        video_path (str): Input video path
        output_path (str): Output video path (optional)
        sensitivity (int): Motion detection sensitivity (minimum contour area)
    """
    detector = MotionDetector(sensitivity=sensitivity)
    detector.detect_from_source(video_path, output_path=output_path)


def detect_circles(image: np.ndarray, min_radius: int = 10, max_radius: int = 100,
                  sensitivity: int = 50) -> List[Tuple[int, int, int]]:
    """
    Detect circles in an image using Hough Circle Transform (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        min_radius (int): Minimum circle radius
        max_radius (int): Maximum circle radius
        sensitivity (int): Detection sensitivity
    
    Returns:
        List[Tuple[int, int, int]]: List of circles (x, y, radius)
    """
    detector = CircleDetector(min_radius, max_radius, sensitivity)
    return detector.detect(image)


def detect_lines(image: np.ndarray, threshold: int = 100, min_line_length: int = 50,
                max_line_gap: int = 10) -> List[Tuple[int, int, int, int]]:
    """
    Detect lines in an image using Hough Line Transform (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        threshold (int): Accumulator threshold
        min_line_length (int): Minimum line length
        max_line_gap (int): Maximum allowed gap between line segments
    
    Returns:
        List[Tuple[int, int, int, int]]: List of lines (x1, y1, x2, y2)
    """
    detector = LineDetector(threshold, min_line_length, max_line_gap)
    return detector.detect(image)


def color_detection(image: np.ndarray, target_color: str = 'red',
                   tolerance: int = 20) -> np.ndarray:
    """
    Detect objects of a specific color (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        target_color (str): Target color name
        tolerance (int): Color tolerance
    
    Returns:
        np.ndarray: Binary mask of detected color
    """
    detector = ColorDetector(target_color, tolerance)
    return detector.detect(image)


def detect_objects_dnn(image: np.ndarray, confidence_threshold: float = 0.5, 
                      nms_threshold: float = 0.4) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
    """
    Detect objects using a pre-trained SSD MobileNet V2 model (Legacy function)

    Args:
        image (np.ndarray): Input image.
        confidence_threshold (float): Minimum confidence for a detection to be considered.
        nms_threshold (float): Non-Maximum Suppression threshold to remove overlapping boxes.

    Returns:
        List[Tuple[str, float, Tuple[int, int, int, int]]]: A list of detected objects.
        Each tuple contains (class_name, confidence, (x, y, w, h)).
    """
    detector = DNNObjectDetector(confidence_threshold, nms_threshold)
    return detector.detect(image)
