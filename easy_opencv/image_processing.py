"""
Image Processing Module
Provides easy-to-use functions for image processing operations
"""

import cv2
import numpy as np
from typing import Optional, Tuple

def apply_blur(image: np.ndarray, blur_type: str = 'gaussian', 
               strength: int = 5) -> np.ndarray:
    """
    Apply different types of blur to an image
    
    Args:
        image (np.ndarray): Input image
        blur_type (str): Type of blur - 'gaussian', 'median', 'average'
        strength (int): Blur strength (kernel size)
    
    Returns:
        np.ndarray: Blurred image
    """
    if strength % 2 == 0:
        strength += 1  # Ensure odd kernel size
    
    if blur_type == 'gaussian':
        return cv2.GaussianBlur(image, (strength, strength), 0)
    elif blur_type == 'median':
        return cv2.medianBlur(image, strength)
    elif blur_type == 'average':
        return cv2.blur(image, (strength, strength))
    else:
        return image

def apply_sharpen(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Apply sharpening filter to an image
    
    Args:
        image (np.ndarray): Input image
        strength (float): Sharpening strength
    
    Returns:
        np.ndarray: Sharpened image
    """
    kernel = np.array([[-1, -1, -1],
                      [-1, 9, -1],
                      [-1, -1, -1]]) * strength
    return cv2.filter2D(image, -1, kernel)

def apply_edge_detection(image: np.ndarray, method: str = 'canny',
                        threshold1: int = 100, threshold2: int = 200) -> np.ndarray:
    """
    Apply edge detection algorithms
    
    Args:
        image (np.ndarray): Input image
        method (str): Edge detection method - 'canny', 'sobel', 'laplacian'
        threshold1 (int): First threshold for Canny
        threshold2 (int): Second threshold for Canny
    
    Returns:
        np.ndarray: Edge detected image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    if method == 'canny':
        return cv2.Canny(gray, threshold1, threshold2)
    elif method == 'sobel':
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        return cv2.magnitude(sobelx, sobely)
    elif method == 'laplacian':
        return cv2.Laplacian(gray, cv2.CV_64F)
    else:
        return gray

def apply_threshold(image: np.ndarray, threshold_type: str = 'binary',
                   threshold_value: int = 127, max_value: int = 255) -> np.ndarray:
    """
    Apply different thresholding techniques
    
    Args:
        image (np.ndarray): Input image
        threshold_type (str): Type of threshold - 'binary', 'adaptive', 'otsu'
        threshold_value (int): Threshold value
        max_value (int): Maximum value for binary threshold
    
    Returns:
        np.ndarray: Thresholded image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    if threshold_type == 'binary':
        _, thresh = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
        return thresh
    elif threshold_type == 'adaptive':
        return cv2.adaptiveThreshold(gray, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    elif threshold_type == 'otsu':
        _, thresh = cv2.threshold(gray, 0, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    else:
        return gray

def apply_morphology(image: np.ndarray, operation: str = 'opening',
                    kernel_size: int = 5, iterations: int = 1) -> np.ndarray:
    """
    Apply morphological operations
    
    Args:
        image (np.ndarray): Input image
        operation (str): Morphological operation - 'opening', 'closing', 'erosion', 'dilation'
        kernel_size (int): Size of morphological kernel
        iterations (int): Number of iterations
    
    Returns:
        np.ndarray: Processed image
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    operations = {
        'erosion': cv2.MORPH_ERODE,
        'dilation': cv2.MORPH_DILATE,
        'opening': cv2.MORPH_OPEN,
        'closing': cv2.MORPH_CLOSE,
        'gradient': cv2.MORPH_GRADIENT,
        'tophat': cv2.MORPH_TOPHAT,
        'blackhat': cv2.MORPH_BLACKHAT
    }
    
    if operation in ['erosion', 'dilation']:
        return cv2.morphologyEx(image, operations[operation], kernel, iterations=iterations)
    else:
        return cv2.morphologyEx(image, operations.get(operation, cv2.MORPH_OPEN), kernel)

def apply_histogram_equalization(image: np.ndarray, method: str = 'global') -> np.ndarray:
    """
    Apply histogram equalization for contrast enhancement
    
    Args:
        image (np.ndarray): Input image
        method (str): Equalization method - 'global', 'adaptive'
    
    Returns:
        np.ndarray: Enhanced image
    """
    if len(image.shape) == 3:
        # Convert to YUV and equalize Y channel
        yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        if method == 'global':
            yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        elif method == 'adaptive':
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            yuv[:,:,0] = clahe.apply(yuv[:,:,0])
        return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    else:
        if method == 'global':
            return cv2.equalizeHist(image)
        elif method == 'adaptive':
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            return clahe.apply(image)
    
    return image

def adjust_brightness_contrast(image: np.ndarray, brightness: int = 0, 
                             contrast: float = 1.0) -> np.ndarray:
    """
    Adjust brightness and contrast of an image
    
    Args:
        image (np.ndarray): Input image
        brightness (int): Brightness adjustment (-100 to 100)
        contrast (float): Contrast multiplier (0.5 to 3.0)
    
    Returns:
        np.ndarray: Adjusted image
    """
    adjusted = cv2.addWeighted(image, contrast, image, 0, brightness)
    return np.clip(adjusted, 0, 255).astype(np.uint8)

def apply_gamma_correction(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """
    Apply gamma correction to an image
    
    Args:
        image (np.ndarray): Input image
        gamma (float): Gamma value
    
    Returns:
        np.ndarray: Gamma corrected image
    """
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                     for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)
