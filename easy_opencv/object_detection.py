"""
Object Detection Module
Provides easy-to-use functions for object detection
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

def detect_faces(image: np.ndarray, scale_factor: float = 1.1,
                min_neighbors: int = 5, min_size: Tuple[int, int] = (30, 30)) -> List[Tuple[int, int, int, int]]:
    """
    Detect faces in an image using Haar cascades
    
    Args:
        image (np.ndarray): Input image
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum face size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of face rectangles (x, y, w, h)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_size
    )
    
    return faces.tolist()

def detect_eyes(image: np.ndarray, scale_factor: float = 1.1,
               min_neighbors: int = 5, min_size: Tuple[int, int] = (20, 20)) -> List[Tuple[int, int, int, int]]:
    """
    Detect eyes in an image using Haar cascades
    
    Args:
        image (np.ndarray): Input image
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum eye size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of eye rectangles (x, y, w, h)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Load the eye cascade classifier
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_size
    )
    
    return eyes.tolist()

def detect_objects_cascade(image: np.ndarray, cascade_path: str,
                          scale_factor: float = 1.1, min_neighbors: int = 5,
                          min_size: Tuple[int, int] = (30, 30)) -> List[Tuple[int, int, int, int]]:
    """
    Detect objects using custom Haar cascade classifier
    
    Args:
        image (np.ndarray): Input image
        cascade_path (str): Path to cascade XML file
        scale_factor (float): Scale factor for detection
        min_neighbors (int): Minimum number of neighbor rectangles
        min_size (tuple): Minimum object size
    
    Returns:
        List[Tuple[int, int, int, int]]: List of object rectangles (x, y, w, h)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Load the custom cascade classifier
    cascade = cv2.CascadeClassifier(cascade_path)
    
    objects = cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_size
    )
    
    return objects.tolist()

def background_subtraction(video_path: str, method: str = 'mog2',
                          learning_rate: float = 0.01) -> cv2.BackgroundSubtractor:
    """
    Create a background subtractor for motion detection
    
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
    Detect motion in a video and optionally save the result
    
    Args:
        video_path (str): Input video path
        output_path (str): Output video path (optional)
        sensitivity (int): Motion detection sensitivity (minimum contour area)
    """
    cap = cv2.VideoCapture(video_path)
    
    # Create background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    
    # Setup video writer if output path is provided
    writer = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame)
        
        # Find contours of moving objects
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw bounding boxes around detected motion
        for contour in contours:
            if cv2.contourArea(contour) > sensitivity:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display or save the frame
        if writer:
            writer.write(frame)
        else:
            cv2.imshow('Motion Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

def detect_circles(image: np.ndarray, min_radius: int = 10, max_radius: int = 100,
                  sensitivity: int = 50) -> List[Tuple[int, int, int]]:
    """
    Detect circles in an image using Hough Circle Transform
    
    Args:
        image (np.ndarray): Input image
        min_radius (int): Minimum circle radius
        max_radius (int): Maximum circle radius
        sensitivity (int): Detection sensitivity
    
    Returns:
        List[Tuple[int, int, int]]: List of circles (x, y, radius)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=sensitivity,
        param1=50,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius
    )
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return [(x, y, r) for x, y, r in circles]
    
    return []

def detect_lines(image: np.ndarray, threshold: int = 100, min_line_length: int = 50,
                max_line_gap: int = 10) -> List[Tuple[int, int, int, int]]:
    """
    Detect lines in an image using Hough Line Transform
    
    Args:
        image (np.ndarray): Input image
        threshold (int): Accumulator threshold
        min_line_length (int): Minimum line length
        max_line_gap (int): Maximum allowed gap between line segments
    
    Returns:
        List[Tuple[int, int, int, int]]: List of lines (x1, y1, x2, y2)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )
    
    if lines is not None:
        return [tuple(line[0]) for line in lines]
    
    return []

def color_detection(image: np.ndarray, target_color: str = 'red',
                   tolerance: int = 20) -> np.ndarray:
    """
    Detect objects of a specific color
    
    Args:
        image (np.ndarray): Input image
        target_color (str): Target color name
        tolerance (int): Color tolerance
    
    Returns:
        np.ndarray: Binary mask of detected color
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color ranges in HSV
    color_ranges = {
        'red': [(0, 50, 50), (10, 255, 255)],
        'green': [(40, 50, 50), (80, 255, 255)],
        'blue': [(100, 50, 50), (130, 255, 255)],
        'yellow': [(20, 50, 50), (30, 255, 255)],
        'orange': [(10, 50, 50), (20, 255, 255)],
        'purple': [(130, 50, 50), (160, 255, 255)]
    }
    
    if target_color.lower() in color_ranges:
        lower, upper = color_ranges[target_color.lower()]
        lower = np.array([max(0, lower[0] - tolerance), lower[1], lower[2]])
        upper = np.array([min(179, upper[0] + tolerance), upper[1], upper[2]])
        
        mask = cv2.inRange(hsv, lower, upper)
        return mask
    
    return np.zeros(image.shape[:2], dtype=np.uint8)
