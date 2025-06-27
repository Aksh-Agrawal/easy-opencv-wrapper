"""
Feature Detection Module
Provides easy-to-use functions for feature detection and matching
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple

def detect_corners(image: np.ndarray, method: str = 'harris', 
                  max_corners: int = 100, quality: float = 0.01) -> np.ndarray:
    """
    Detect corners in an image
    
    Args:
        image (np.ndarray): Input image
        method (str): Corner detection method - 'harris', 'shi_tomasi'
        max_corners (int): Maximum number of corners to detect
        quality (float): Quality level parameter
    
    Returns:
        np.ndarray: Array of corner coordinates
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    if method == 'harris':
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        corners = np.where(dst > 0.01 * dst.max())
        return np.column_stack((corners[1], corners[0]))
    
    elif method == 'shi_tomasi':
        corners = cv2.goodFeaturesToTrack(gray, max_corners, quality, 10)
        return corners.reshape(-1, 2) if corners is not None else np.array([])
    
    return np.array([])

def detect_keypoints(image: np.ndarray, detector: str = 'sift', 
                    max_features: int = 1000) -> Tuple[List, np.ndarray]:
    """
    Detect keypoints and compute descriptors
    
    Args:
        image (np.ndarray): Input image
        detector (str): Detector type - 'sift', 'orb', 'surf', 'fast'
        max_features (int): Maximum number of features
    
    Returns:
        Tuple[List, np.ndarray]: Keypoints and descriptors
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    if detector == 'sift':
        detector_obj = cv2.SIFT_create(nfeatures=max_features)
    elif detector == 'orb':
        detector_obj = cv2.ORB_create(nfeatures=max_features)
    elif detector == 'fast':
        detector_obj = cv2.FastFeatureDetector_create()
        keypoints = detector_obj.detect(gray, None)
        return keypoints, None
    else:
        detector_obj = cv2.ORB_create(nfeatures=max_features)
    
    keypoints, descriptors = detector_obj.detectAndCompute(gray, None)
    return keypoints, descriptors

def match_features(desc1: np.ndarray, desc2: np.ndarray, 
                  method: str = 'bf', ratio_threshold: float = 0.75) -> List:
    """
    Match features between two images
    
    Args:
        desc1 (np.ndarray): Descriptors from first image
        desc2 (np.ndarray): Descriptors from second image
        method (str): Matching method - 'bf' (brute force), 'flann'
        ratio_threshold (float): Ratio threshold for Lowe's test
    
    Returns:
        List: Good matches
    """
    if desc1 is None or desc2 is None:
        return []
    
    if method == 'bf':
        # Determine if descriptors are binary (ORB) or float (SIFT)
        if desc1.dtype == np.uint8:
            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        else:
            matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        
        matches = matcher.knnMatch(desc1, desc2, k=2)
        
        # Apply ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < ratio_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    elif method == 'flann':
        # FLANN parameters
        if desc1.dtype == np.uint8:
            # For ORB descriptors
            FLANN_INDEX_LSH = 6
            index_params = dict(algorithm=FLANN_INDEX_LSH,
                              table_number=6,
                              key_size=12,
                              multi_probe_level=1)
        else:
            # For SIFT descriptors
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(desc1, desc2, k=2)
        
        # Apply ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < ratio_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    return []

def detect_contours(image: np.ndarray, threshold_value: int = 127,
                   min_area: int = 100) -> List[np.ndarray]:
    """
    Detect contours in an image
    
    Args:
        image (np.ndarray): Input image
        threshold_value (int): Threshold value for binarization
        min_area (int): Minimum contour area
    
    Returns:
        List[np.ndarray]: List of contours
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    return filtered_contours

def find_shapes(image: np.ndarray, min_area: int = 100) -> List[dict]:
    """
    Detect and classify shapes in an image
    
    Args:
        image (np.ndarray): Input image
        min_area (int): Minimum shape area
    
    Returns:
        List[dict]: List of detected shapes with properties
    """
    contours = detect_contours(image, min_area=min_area)
    shapes = []
    
    for contour in contours:
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            continue
        
        # Approximate contour to polygon
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        
        # Classify shape based on number of vertices
        vertices = len(approx)
        shape_name = "unknown"
        
        if vertices == 3:
            shape_name = "triangle"
        elif vertices == 4:
            # Check if it's a square or rectangle
            aspect_ratio = w / float(h)
            if 0.95 <= aspect_ratio <= 1.05:
                shape_name = "square"
            else:
                shape_name = "rectangle"
        elif vertices == 5:
            shape_name = "pentagon"
        elif vertices > 5:
            # Check if it's a circle
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            if circularity > 0.85:
                shape_name = "circle"
            else:
                shape_name = "polygon"
        
        shape_info = {
            'name': shape_name,
            'vertices': vertices,
            'area': area,
            'perimeter': perimeter,
            'contour': contour,
            'bounding_box': (x, y, w, h),
            'center': (x + w//2, y + h//2)
        }
        
        shapes.append(shape_info)
    
    return shapes

def template_matching(image: np.ndarray, template: np.ndarray, 
                     method: str = 'normalized', threshold: float = 0.8) -> List[Tuple[int, int]]:
    """
    Perform template matching to find template in image
    
    Args:
        image (np.ndarray): Input image
        template (np.ndarray): Template to search for
        method (str): Matching method
        threshold (float): Match threshold
    
    Returns:
        List[Tuple[int, int]]: List of match locations
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template
    
    methods = {
        'squared_difference': cv2.TM_SQDIFF_NORMED,
        'correlation': cv2.TM_CCORR_NORMED,
        'normalized': cv2.TM_CCOEFF_NORMED
    }
    
    method_cv = methods.get(method, cv2.TM_CCOEFF_NORMED)
    result = cv2.matchTemplate(gray_image, gray_template, method_cv)
    
    locations = []
    if method == 'squared_difference':
        # For SQDIFF, lower values are better matches
        loc = np.where(result <= (1 - threshold))
    else:
        # For other methods, higher values are better matches
        loc = np.where(result >= threshold)
    
    for pt in zip(*loc[::-1]):
        locations.append(pt)
    
    return locations
