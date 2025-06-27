"""
Image Operations Module
Provides easy-to-use functions for basic image operations
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Union

def load_image(path: str, mode: str = 'color') -> np.ndarray:
    """
    Load an image from file with customizable color mode
    
    Args:
        path (str): Path to the image file
        mode (str): Color mode - 'color', 'gray', 'unchanged'
    
    Returns:
        np.ndarray: Loaded image
    """
    mode_map = {
        'color': cv2.IMREAD_COLOR,
        'gray': cv2.IMREAD_GRAYSCALE,
        'unchanged': cv2.IMREAD_UNCHANGED
    }
    
    return cv2.imread(path, mode_map.get(mode, cv2.IMREAD_COLOR))

def save_image(image: np.ndarray, path: str, quality: int = 95) -> bool:
    """
    Save an image to file with customizable quality
    
    Args:
        image (np.ndarray): Image to save
        path (str): Output path
        quality (int): JPEG quality (0-100)
    
    Returns:
        bool: Success status
    """
    if path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
        return cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    else:
        return cv2.imwrite(path, image)

def show_image(image: np.ndarray, title: str = 'Image', wait: bool = True, 
               size: Optional[Tuple[int, int]] = None) -> None:
    """
    Display an image with customizable window properties
    
    Args:
        image (np.ndarray): Image to display
        title (str): Window title
        wait (bool): Whether to wait for key press
        size (tuple): Window size (width, height)
    """
    if size:
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(title, size[0], size[1])
    else:
        cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    
    cv2.imshow(title, image)
    
    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def resize_image(image: np.ndarray, width: Optional[int] = None, 
                height: Optional[int] = None, scale: Optional[float] = None,
                method: str = 'linear') -> np.ndarray:
    """
    Resize an image with multiple sizing options
    
    Args:
        image (np.ndarray): Input image
        width (int): Target width
        height (int): Target height
        scale (float): Scale factor
        method (str): Interpolation method - 'linear', 'cubic', 'nearest'
    
    Returns:
        np.ndarray: Resized image
    """
    h, w = image.shape[:2]
    
    method_map = {
        'linear': cv2.INTER_LINEAR,
        'cubic': cv2.INTER_CUBIC,
        'nearest': cv2.INTER_NEAREST,
        'area': cv2.INTER_AREA,
        'lanczos': cv2.INTER_LANCZOS4
    }
    
    if scale:
        width = int(w * scale)
        height = int(h * scale)
    elif width and not height:
        height = int(h * (width / w))
    elif height and not width:
        width = int(w * (height / h))
    elif not width and not height and not scale:
        raise ValueError("At least one of width, height, or scale must be provided")
    
    # Check for valid method
    if method.lower() not in method_map:
        raise ValueError(f"Invalid resize method: {method}. Choose from: {', '.join(method_map.keys())}")
    
    return cv2.resize(image, (width, height), interpolation=method_map.get(method.lower(), cv2.INTER_LINEAR))

def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """
    Crop an image to specified dimensions
    
    Args:
        image (np.ndarray): Input image
        x (int): X coordinate of top-left corner
        y (int): Y coordinate of top-left corner
        width (int): Width of crop area
        height (int): Height of crop area
    
    Returns:
        np.ndarray: Cropped image
        
    Raises:
        ValueError: If crop dimensions are out of image bounds
    """
    img_height, img_width = image.shape[:2]
    
    # Check if crop is out of bounds
    if x < 0 or y < 0 or x + width > img_width or y + height > img_height:
        raise ValueError(f"Crop dimensions ({x},{y},{width},{height}) out of bounds for image of size {img_width}x{img_height}")
        
    return image[y:y+height, x:x+width]

def convert_color_space(image: np.ndarray, from_space: str = 'bgr', 
                       to_space: str = 'rgb') -> np.ndarray:
    """
    Convert image between different color spaces
    
    Args:
        image (np.ndarray): Input image
        from_space (str): Source color space
        to_space (str): Target color space
    
    Returns:
        np.ndarray: Converted image
    """
    conversion_map = {
        ('bgr', 'rgb'): cv2.COLOR_BGR2RGB,
        ('rgb', 'bgr'): cv2.COLOR_RGB2BGR,
        ('bgr', 'gray'): cv2.COLOR_BGR2GRAY,
        ('rgb', 'gray'): cv2.COLOR_RGB2GRAY,
        ('gray', 'bgr'): cv2.COLOR_GRAY2BGR,
        ('gray', 'rgb'): cv2.COLOR_GRAY2RGB,
        ('bgr', 'hsv'): cv2.COLOR_BGR2HSV,
        ('hsv', 'bgr'): cv2.COLOR_HSV2BGR,
        ('bgr', 'lab'): cv2.COLOR_BGR2LAB,
        ('lab', 'bgr'): cv2.COLOR_LAB2BGR,
    }
    
    key = (from_space.lower(), to_space.lower())
    if key in conversion_map:
        return cv2.cvtColor(image, conversion_map[key])
    else:
        raise ValueError(f"Unsupported color space conversion: {from_space} -> {to_space}")

def get_image_info(image: np.ndarray) -> dict:
    """
    Get comprehensive information about an image
    
    Args:
        image (np.ndarray): Input image
    
    Returns:
        dict: Image information
    """
    info = {
        'shape': image.shape,
        'height': image.shape[0],
        'width': image.shape[1],
        'channels': 1 if len(image.shape) == 2 else image.shape[2],  # Grayscale = 1 channel
        'dtype': str(image.dtype),
        'size': image.size,
        'min_value': image.min(),
        'max_value': image.max(),
        'mean_value': image.mean()
    }
    return info
