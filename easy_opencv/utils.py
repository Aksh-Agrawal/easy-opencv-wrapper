"""
Utilities Module
Provides helpful utility functions for OpenCV operations
"""

import cv2
import numpy as np
from typing import Optional, Callable, Tuple, Any
import time

def create_trackbar(window_name: str, trackbar_name: str, initial_value: int = 0,
                   max_value: int = 255, callback: Optional[Callable] = None) -> None:
    """
    Create a trackbar for interactive parameter adjustment
    
    Args:
        window_name (str): Name of the window to attach trackbar to
        trackbar_name (str): Name of the trackbar
        initial_value (int): Initial value
        max_value (int): Maximum value
        callback (callable): Callback function when trackbar changes
    """
    def dummy_callback(val):
        pass
    
    cb = callback if callback else dummy_callback
    cv2.createTrackbar(trackbar_name, window_name, initial_value, max_value, cb)

def mouse_callback(event: int, x: int, y: int, flags: int, param: Any) -> None:
    """
    Default mouse callback function for handling mouse events
    
    Args:
        event (int): Mouse event type
        x (int): X coordinate
        y (int): Y coordinate
        flags (int): Event flags
        param (Any): Additional parameters
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left click at ({x}, {y})")
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(f"Right click at ({x}, {y})")
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print(f"Dragging at ({x}, {y})")

def set_mouse_callback(window_name: str, callback: Callable) -> None:
    """
    Set mouse callback for a window
    
    Args:
        window_name (str): Name of the window
        callback (callable): Mouse callback function
    """
    cv2.setMouseCallback(window_name, callback)

class FPSCounter:
    """
    Class for measuring and displaying FPS in real-time applications
    """
    
    def __init__(self, window_size: int = 30):
        """
        Initialize FPS counter
        
        Args:
            window_size (int): Number of frames to average over
        """
        self.window_size = window_size
        self.frame_times = []
        self.last_time = time.time()
    
    def update(self) -> float:
        """
        Update FPS calculation
        
        Returns:
            float: Current FPS
        """
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
        
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        return 0.0
    
    def get_fps_text(self) -> str:
        """
        Get formatted FPS text
        
        Returns:
            str: Formatted FPS string
        """
        fps = self.update()
        return f"FPS: {fps:.1f}"

def fps_counter(show_on_image: bool = True) -> FPSCounter:
    """
    Create and return an FPS counter instance
    
    Args:
        show_on_image (bool): Whether to display FPS on image
    
    Returns:
        FPSCounter: FPS counter instance
    """
    return FPSCounter()

def color_picker(image: np.ndarray, window_name: str = 'Color Picker') -> None:
    """
    Interactive color picker tool
    
    Args:
        image (np.ndarray): Input image
        window_name (str): Window name for display
    """
    def pick_color(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get color at clicked position
            if len(image.shape) == 3:
                b, g, r = image[y, x]
                print(f"Position: ({x}, {y})")
                print(f"BGR: ({b}, {g}, {r})")
                print(f"RGB: ({r}, {g}, {b})")
                print(f"Hex: #{r:02x}{g:02x}{b:02x}")
            else:
                gray_value = image[y, x]
                print(f"Position: ({x}, {y})")
                print(f"Gray value: {gray_value}")
    
    cv2.imshow(window_name, image)
    cv2.setMouseCallback(window_name, pick_color)
    
    print("Click on the image to pick colors. Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def image_comparison(image1: np.ndarray, image2: np.ndarray,
                    method: str = 'side_by_side') -> np.ndarray:
    """
    Compare two images using different visualization methods
    
    Args:
        image1 (np.ndarray): First image
        image2 (np.ndarray): Second image
        method (str): Comparison method - 'side_by_side', 'difference', 'blend'
    
    Returns:
        np.ndarray: Comparison result
    """
    # Ensure images have the same size
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    if (h1, w1) != (h2, w2):
        image2 = cv2.resize(image2, (w1, h1))
    
    if method == 'side_by_side':
        # Concatenate images horizontally
        return np.hstack((image1, image2))
    
    elif method == 'difference':
        # Show absolute difference
        diff = cv2.absdiff(image1, image2)
        return diff
    
    elif method == 'blend':
        # Blend images with 50% opacity
        return cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
    
    else:
        return image1

def create_image_grid(images: list, grid_size: Tuple[int, int],
                     image_size: Optional[Tuple[int, int]] = None) -> np.ndarray:
    """
    Create a grid of images
    
    Args:
        images (list): List of images
        grid_size (tuple): Grid dimensions (rows, cols)
        image_size (tuple): Size to resize each image to
    
    Returns:
        np.ndarray: Grid image
    """
    rows, cols = grid_size
    
    if len(images) > rows * cols:
        images = images[:rows * cols]
        
    # Make sure all images have same number of channels
    processed_images = []
    for img in images:
        if len(img.shape) == 2:  # Grayscale image
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        processed_images.append(img)
    
    images = processed_images
    
    # Determine a common image size for all images
    if image_size:
        common_size = image_size
    elif images:
        # If no size specified, use the first image's size
        common_size = (images[0].shape[1], images[0].shape[0])
    else:
        return np.zeros((100, 100, 3), dtype=np.uint8)  # Default empty image
    
    # Resize all images to the common size
    images = [cv2.resize(img, common_size) for img in images]
    
    # Create empty slots for missing images
    while len(images) < rows * cols:
        empty_img = np.zeros((common_size[1], common_size[0], 3), dtype=np.uint8)
        images.append(empty_img)
    
    # Arrange images in grid
    grid_rows = []
    for i in range(rows):
        row_images = images[i * cols:(i + 1) * cols]
        grid_row = np.hstack(row_images)
        grid_rows.append(grid_row)
    
    grid = np.vstack(grid_rows)
    return grid

def apply_watermark(image: np.ndarray, watermark_text: str,
                   position: str = 'bottom_right', opacity: float = 0.5,
                   font_scale: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
    """
    Add a text watermark to an image
    
    Args:
        image (np.ndarray): Input image
        watermark_text (str): Watermark text
        position (str): Position of watermark
        opacity (float): Watermark opacity
        font_scale (float): Font scale
        color (tuple): Text color
    
    Returns:
        np.ndarray: Watermarked image
    """
    result = image.copy()
    height, width = image.shape[:2]
    
    # Get text size
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    (text_width, text_height), baseline = cv2.getTextSize(watermark_text, font, font_scale, thickness)
    
    # Calculate position
    positions = {
        'top_left': (10, text_height + 10),
        'top_right': (width - text_width - 10, text_height + 10),
        'bottom_left': (10, height - 10),
        'bottom_right': (width - text_width - 10, height - 10),
        'center': ((width - text_width) // 2, (height + text_height) // 2)
    }
    
    text_position = positions.get(position, positions['bottom_right'])
    
    # Create overlay for transparency
    overlay = image.copy()
    cv2.putText(overlay, watermark_text, text_position, font, font_scale, color, thickness)
    
    # Blend with original
    watermarked = cv2.addWeighted(result, 1 - opacity, overlay, opacity, 0)
    
    return watermarked

def convert_to_sketch(image: np.ndarray, blur_value: int = 21, intensity: int = 256) -> np.ndarray:
    """
    Convert image to pencil sketch style
    
    Args:
        image (np.ndarray): Input image
        blur_value (int): Blur intensity
        intensity (int): Sketch intensity
    
    Returns:
        np.ndarray: Sketch-style image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert the image
    inverted = 255 - gray
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(inverted, (blur_value, blur_value), 0)
    
    # Invert the blurred image
    inverted_blurred = 255 - blurred
    
    # Create the sketch by dividing
    sketch = cv2.divide(gray, inverted_blurred, scale=intensity)
    
    return sketch

def auto_canny(image: np.ndarray, sigma: float = 0.33) -> np.ndarray:
    """
    Automatic Canny edge detection with optimal thresholds
    
    Args:
        image (np.ndarray): Input image
        sigma (float): Sigma value for threshold calculation
    
    Returns:
        np.ndarray: Edge detected image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Calculate median of pixel intensities
    median = np.median(gray)
    
    # Calculate optimal thresholds
    lower = int(max(0, (1.0 - sigma) * median))
    upper = int(min(255, (1.0 + sigma) * median))
    
    # Apply Canny edge detection
    edged = cv2.Canny(gray, lower, upper)
    
    return edged
