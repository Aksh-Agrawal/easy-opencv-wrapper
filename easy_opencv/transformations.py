"""
Transformations Module
Provides easy-to-use functions for image transformations
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List

def rotate_image(image: np.ndarray, angle: float, center: Optional[Tuple[int, int]] = None,
                scale: float = 1.0, border_mode: str = 'constant',
                border_value: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Rotate an image by a specified angle
    
    Args:
        image (np.ndarray): Input image
        angle (float): Rotation angle in degrees (positive = counterclockwise)
        center (tuple): Center of rotation (x, y). If None, uses image center
        scale (float): Scaling factor
        border_mode (str): Border handling mode - 'constant', 'reflect', 'wrap'
        border_value (tuple): Fill value for constant border mode
    
    Returns:
        np.ndarray: Rotated image
    """
    height, width = image.shape[:2]
    
    if center is None:
        center = (width // 2, height // 2)
    
    # Get rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Map border modes
    border_modes = {
        'constant': cv2.BORDER_CONSTANT,
        'reflect': cv2.BORDER_REFLECT,
        'wrap': cv2.BORDER_WRAP,
        'replicate': cv2.BORDER_REPLICATE
    }
    
    border_mode_cv = border_modes.get(border_mode, cv2.BORDER_CONSTANT)
    
    # Apply rotation
    rotated = cv2.warpAffine(image, rotation_matrix, (width, height),
                           borderMode=border_mode_cv, borderValue=border_value)
    
    return rotated

def flip_image(image: np.ndarray, direction: str = 'horizontal') -> np.ndarray:
    """
    Flip an image horizontally, vertically, or both
    
    Args:
        image (np.ndarray): Input image
        direction (str): Flip direction - 'horizontal', 'vertical', 'both'
    
    Returns:
        np.ndarray: Flipped image
        
    Raises:
        ValueError: If direction is not one of the supported values
    """
    directions = {
        'horizontal': 1,
        'vertical': 0,
        'both': -1
    }
    
    if direction.lower() not in directions:
        raise ValueError(f"Invalid flip direction: {direction}. Choose from: horizontal, vertical, both")
        
    flip_code = directions.get(direction.lower(), 1)
    return cv2.flip(image, flip_code)

def translate_image(image: np.ndarray, tx: int, ty: int,
                   border_mode: str = 'constant',
                   border_value: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Translate (shift) an image by specified offsets
    
    Args:
        image (np.ndarray): Input image
        tx (int): Translation in x direction (pixels)
        ty (int): Translation in y direction (pixels)
        border_mode (str): Border handling mode
        border_value (tuple): Fill value for constant border mode
    
    Returns:
        np.ndarray: Translated image
    """
    height, width = image.shape[:2]
    
    # Create translation matrix
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    
    # Map border modes
    border_modes = {
        'constant': cv2.BORDER_CONSTANT,
        'reflect': cv2.BORDER_REFLECT,
        'wrap': cv2.BORDER_WRAP,
        'replicate': cv2.BORDER_REPLICATE
    }
    
    border_mode_cv = border_modes.get(border_mode, cv2.BORDER_CONSTANT)
    
    # Apply translation
    translated = cv2.warpAffine(image, translation_matrix, (width, height),
                              borderMode=border_mode_cv, borderValue=border_value)
    
    return translated

def apply_perspective_transform(image: np.ndarray, src_points: List[Tuple[int, int]],
                              dst_points: List[Tuple[int, int]],
                              output_size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    """
    Apply perspective transformation to an image
    
    Args:
        image (np.ndarray): Input image
        src_points (list): Source points [(x, y), ...] (4 points)
        dst_points (list): Destination points [(x, y), ...] (4 points)
        output_size (tuple): Output image size (width, height)
    
    Returns:
        np.ndarray: Perspective transformed image
    """
    if output_size is None:
        output_size = (image.shape[1], image.shape[0])
    
    # Convert points to numpy arrays
    src_pts = np.float32(src_points)
    dst_pts = np.float32(dst_points)
    
    # Get perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    # Apply perspective transformation
    warped = cv2.warpPerspective(image, matrix, output_size)
    
    return warped

def apply_affine_transform(image: np.ndarray, src_points: List[Tuple[int, int]],
                         dst_points: List[Tuple[int, int]],
                         output_size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    """
    Apply affine transformation to an image
    
    Args:
        image (np.ndarray): Input image
        src_points (list): Source points [(x, y), ...] (3 points)
        dst_points (list): Destination points [(x, y), ...] (3 points)
        output_size (tuple): Output image size (width, height)
    
    Returns:
        np.ndarray: Affine transformed image
    """
    if output_size is None:
        output_size = (image.shape[1], image.shape[0])
    
    # Convert points to numpy arrays
    src_pts = np.float32(src_points)
    dst_pts = np.float32(dst_points)
    
    # Get affine transformation matrix
    matrix = cv2.getAffineTransform(src_pts, dst_pts)
    
    # Apply affine transformation
    warped = cv2.warpAffine(image, matrix, output_size)
    
    return warped

def warp_image(image: np.ndarray, transformation_matrix: np.ndarray,
              output_size: Optional[Tuple[int, int]] = None,
              interpolation: str = 'linear') -> np.ndarray:
    """
    Warp an image using a custom transformation matrix
    
    Args:
        image (np.ndarray): Input image
        transformation_matrix (np.ndarray): 2x3 or 3x3 transformation matrix
        output_size (tuple): Output image size (width, height)
        interpolation (str): Interpolation method
    
    Returns:
        np.ndarray: Warped image
    """
    if output_size is None:
        output_size = (image.shape[1], image.shape[0])
    
    # Map interpolation methods
    interpolations = {
        'nearest': cv2.INTER_NEAREST,
        'linear': cv2.INTER_LINEAR,
        'cubic': cv2.INTER_CUBIC,
        'lanczos': cv2.INTER_LANCZOS4
    }
    
    interp_method = interpolations.get(interpolation, cv2.INTER_LINEAR)
    
    # Apply transformation based on matrix size
    if transformation_matrix.shape == (2, 3):
        # Affine transformation
        warped = cv2.warpAffine(image, transformation_matrix, output_size,
                              flags=interp_method)
    elif transformation_matrix.shape == (3, 3):
        # Perspective transformation
        warped = cv2.warpPerspective(image, transformation_matrix, output_size,
                                   flags=interp_method)
    else:
        raise ValueError("Transformation matrix must be 2x3 or 3x3")
    
    return warped

def apply_barrel_distortion(image: np.ndarray, k1: float = -0.2, k2: float = 0.0) -> np.ndarray:
    """
    Apply barrel distortion effect to an image
    
    Args:
        image (np.ndarray): Input image
        k1 (float): Radial distortion coefficient
        k2 (float): Additional radial distortion coefficient
    
    Returns:
        np.ndarray: Distorted image
    """
    height, width = image.shape[:2]
    
    # Camera matrix (assuming centered principal point)
    camera_matrix = np.array([[width, 0, width/2],
                             [0, height, height/2],
                             [0, 0, 1]], dtype=np.float32)
    
    # Distortion coefficients
    dist_coeffs = np.array([k1, k2, 0, 0], dtype=np.float32)
    
    # Apply distortion
    distorted = cv2.undistort(image, camera_matrix, -dist_coeffs)
    
    return distorted

def apply_fisheye_effect(image: np.ndarray, strength: float = 0.5) -> np.ndarray:
    """
    Apply fisheye lens effect to an image
    
    Args:
        image (np.ndarray): Input image
        strength (float): Effect strength (0.0 to 1.0)
    
    Returns:
        np.ndarray: Image with fisheye effect
    """
    height, width = image.shape[:2]
    
    # Create coordinate matrices
    x = np.arange(width)
    y = np.arange(height)
    x_map, y_map = np.meshgrid(x, y)
    
    # Convert to normalized coordinates (-1 to 1)
    x_norm = (x_map - width/2) / (width/2)
    y_norm = (y_map - height/2) / (height/2)
    
    # Calculate radius from center
    radius = np.sqrt(x_norm**2 + y_norm**2)
    
    # Apply fisheye transformation
    radius_new = radius * (1 + strength * radius**2)
    
    # Convert back to image coordinates
    x_new = x_norm * radius_new / (radius + 1e-10) * (width/2) + width/2
    y_new = y_norm * radius_new / (radius + 1e-10) * (height/2) + height/2
    
    # Ensure coordinates are within bounds
    x_new = np.clip(x_new, 0, width-1)
    y_new = np.clip(y_new, 0, height-1)
    
    # Remap the image
    fisheye = cv2.remap(image, x_new.astype(np.float32), y_new.astype(np.float32),
                       cv2.INTER_LINEAR)
    
    return fisheye

def resize_with_aspect_ratio(image: np.ndarray, target_size: Tuple[int, int],
                           padding_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio, with padding if necessary
    
    Args:
        image (np.ndarray): Input image
        target_size (tuple): Target size (width, height)
        padding_color (tuple): Color for padding areas
    
    Returns:
        np.ndarray: Resized image with padding
    """
    height, width = image.shape[:2]
    target_width, target_height = target_size
    
    # Calculate scaling factor
    scale = min(target_width / width, target_height / height)
    
    # Calculate new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize image
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Create canvas with target size
    canvas = np.full((target_height, target_width, image.shape[2]), padding_color, dtype=np.uint8)
    
    # Calculate position to center the resized image
    start_x = (target_width - new_width) // 2
    start_y = (target_height - new_height) // 2
    
    # Place resized image on canvas
    canvas[start_y:start_y + new_height, start_x:start_x + new_width] = resized
    
    return canvas
