"""
Drawing Operations Module
Provides easy-to-use functions for drawing on images
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional

def draw_rectangle(image: np.ndarray, start_point: Tuple[int, int], 
                  end_point: Tuple[int, int], color: Tuple[int, int, int] = (0, 255, 0),
                  thickness: int = 2, filled: bool = False) -> np.ndarray:
    """
    Draw a rectangle on an image
    
    Args:
        image (np.ndarray): Input image
        start_point (tuple): Top-left corner (x, y)
        end_point (tuple): Bottom-right corner (x, y)
        color (tuple): Rectangle color (B, G, R)
        thickness (int): Line thickness (-1 for filled)
        filled (bool): Whether to fill the rectangle
    
    Returns:
        np.ndarray: Image with rectangle drawn
    """
    result = image.copy()
    thickness = -1 if filled else thickness
    cv2.rectangle(result, start_point, end_point, color, thickness)
    return result

def draw_circle(image: np.ndarray, center: Tuple[int, int], radius: int,
               color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2,
               filled: bool = False) -> np.ndarray:
    """
    Draw a circle on an image
    
    Args:
        image (np.ndarray): Input image
        center (tuple): Circle center (x, y)
        radius (int): Circle radius
        color (tuple): Circle color (B, G, R)
        thickness (int): Line thickness
        filled (bool): Whether to fill the circle
    
    Returns:
        np.ndarray: Image with circle drawn
    """
    result = image.copy()
    thickness = -1 if filled else thickness
    cv2.circle(result, center, radius, color, thickness)
    return result

def draw_line(image: np.ndarray, start_point: Tuple[int, int],
             end_point: Tuple[int, int], color: Tuple[int, int, int] = (0, 255, 0),
             thickness: int = 2) -> np.ndarray:
    """
    Draw a line on an image
    
    Args:
        image (np.ndarray): Input image
        start_point (tuple): Line start point (x, y)
        end_point (tuple): Line end point (x, y)
        color (tuple): Line color (B, G, R)
        thickness (int): Line thickness
    
    Returns:
        np.ndarray: Image with line drawn
    """
    result = image.copy()
    cv2.line(result, start_point, end_point, color, thickness)
    return result

def draw_text(image: np.ndarray, text: str, position: Tuple[int, int],
             font_scale: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255),
             thickness: int = 2, font: int = cv2.FONT_HERSHEY_SIMPLEX,
             background: bool = False, bg_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    """
    Draw text on an image
    
    Args:
        image (np.ndarray): Input image
        text (str): Text to draw
        position (tuple): Text position (x, y)
        font_scale (float): Font scale factor
        color (tuple): Text color (B, G, R)
        thickness (int): Text thickness
        font (int): Font type
        background (bool): Whether to draw background
        bg_color (tuple): Background color
    
    Returns:
        np.ndarray: Image with text drawn
    """
    result = image.copy()
    
    if background:
        # Get text size for background rectangle
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        cv2.rectangle(result, 
                     (position[0], position[1] - text_height - baseline),
                     (position[0] + text_width, position[1] + baseline),
                     bg_color, -1)
    
    cv2.putText(result, text, position, font, font_scale, color, thickness)
    return result

def draw_polygon(image: np.ndarray, points: List[Tuple[int, int]],
                color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2,
                filled: bool = False) -> np.ndarray:
    """
    Draw a polygon on an image
    
    Args:
        image (np.ndarray): Input image
        points (list): List of polygon vertices [(x, y), ...]
        color (tuple): Polygon color (B, G, R)
        thickness (int): Line thickness
        filled (bool): Whether to fill the polygon
    
    Returns:
        np.ndarray: Image with polygon drawn
    """
    result = image.copy()
    pts = np.array(points, np.int32)
    pts = pts.reshape((-1, 1, 2))
    
    if filled:
        cv2.fillPoly(result, [pts], color)
    else:
        cv2.polylines(result, [pts], True, color, thickness)
    
    return result

def draw_contour(image: np.ndarray, contours: List[np.ndarray],
                contour_idx: int = -1, color: Tuple[int, int, int] = (0, 255, 0),
                thickness: int = 2, filled: bool = False) -> np.ndarray:
    """
    Draw contours on an image
    
    Args:
        image (np.ndarray): Input image
        contours (list): List of contours
        contour_idx (int): Contour index (-1 for all)
        color (tuple): Contour color (B, G, R)
        thickness (int): Line thickness
        filled (bool): Whether to fill contours
    
    Returns:
        np.ndarray: Image with contours drawn
    """
    result = image.copy()
    thickness = -1 if filled else thickness
    cv2.drawContours(result, contours, contour_idx, color, thickness)
    return result

def draw_arrow(image: np.ndarray, start_point: Tuple[int, int],
              end_point: Tuple[int, int], color: Tuple[int, int, int] = (0, 255, 0),
              thickness: int = 2, tip_length: float = 0.1) -> np.ndarray:
    """
    Draw an arrow on an image
    
    Args:
        image (np.ndarray): Input image
        start_point (tuple): Arrow start point (x, y)
        end_point (tuple): Arrow end point (x, y)
        color (tuple): Arrow color (B, G, R)
        thickness (int): Line thickness
        tip_length (float): Arrow tip length as fraction of arrow length
    
    Returns:
        np.ndarray: Image with arrow drawn
    """
    result = image.copy()
    cv2.arrowedLine(result, start_point, end_point, color, thickness, tipLength=tip_length)
    return result

def draw_grid(image: np.ndarray, grid_size: int = 50,
             color: Tuple[int, int, int] = (128, 128, 128), thickness: int = 1) -> np.ndarray:
    """
    Draw a grid overlay on an image
    
    Args:
        image (np.ndarray): Input image
        grid_size (int): Grid cell size in pixels
        color (tuple): Grid color (B, G, R)
        thickness (int): Line thickness
    
    Returns:
        np.ndarray: Image with grid overlay
    """
    result = image.copy()
    height, width = image.shape[:2]
    
    # Draw vertical lines
    for x in range(0, width, grid_size):
        cv2.line(result, (x, 0), (x, height), color, thickness)
    
    # Draw horizontal lines
    for y in range(0, height, grid_size):
        cv2.line(result, (0, y), (width, y), color, thickness)
    
    return result

def draw_crosshair(image: np.ndarray, center: Tuple[int, int], size: int = 20,
                  color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> np.ndarray:
    """
    Draw a crosshair at specified position
    
    Args:
        image (np.ndarray): Input image
        center (tuple): Crosshair center (x, y)
        size (int): Crosshair size
        color (tuple): Crosshair color (B, G, R)
        thickness (int): Line thickness
    
    Returns:
        np.ndarray: Image with crosshair drawn
    """
    result = image.copy()
    x, y = center
    
    # Draw horizontal line
    cv2.line(result, (x - size, y), (x + size, y), color, thickness)
    # Draw vertical line
    cv2.line(result, (x, y - size), (x, y + size), color, thickness)
    
    return result

def draw_bounding_boxes(image: np.ndarray, boxes: List[Tuple[int, int, int, int]],
                       labels: Optional[List[str]] = None,
                       colors: Optional[List[Tuple[int, int, int]]] = None,
                       thickness: int = 2) -> np.ndarray:
    """
    Draw multiple bounding boxes with optional labels
    
    Args:
        image (np.ndarray): Input image
        boxes (list): List of bounding boxes [(x, y, w, h), ...]
        labels (list): Optional list of labels
        colors (list): Optional list of colors for each box
        thickness (int): Line thickness
    
    Returns:
        np.ndarray: Image with bounding boxes drawn
    """
    result = image.copy()
    
    for i, (x, y, w, h) in enumerate(boxes):
        # Use provided color or default
        if colors and i < len(colors):
            color = colors[i]
        else:
            color = (0, 255, 0)
        
        # Draw bounding box
        cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)
        
        # Draw label if provided
        if labels and i < len(labels):
            label = labels[i]
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            
            # Draw background rectangle for text
            cv2.rectangle(result, (x, y - text_height - baseline),
                         (x + text_width, y), color, -1)
            
            # Draw text
            cv2.putText(result, label, (x, y - baseline),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return result
