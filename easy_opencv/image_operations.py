"""
Image Operations Module
Provides easy-to-use classes and functions for basic image operations with webcam support
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Union, List

class ImageLoader:
    """Class for loading images with various modes and error handling"""
    
    def __init__(self, default_mode: str = 'color'):
        """
        Initialize ImageLoader
        
        Args:
            default_mode: Default color mode for loading images
        """
        self.default_mode = default_mode
        self.mode_map = {
            'color': cv2.IMREAD_COLOR,
            'gray': cv2.IMREAD_GRAYSCALE,
            'unchanged': cv2.IMREAD_UNCHANGED
        }
    
    def load(self, path: Union[str, int], mode: Optional[str] = None) -> np.ndarray:
        """
        Load an image from file or webcam with customizable color mode
        
        Args:
            path: Path to image file or webcam index (0, 1, etc)
            mode: Color mode - 'color', 'gray', 'unchanged'
        
        Returns:
            Loaded image
        """
        mode = mode or self.default_mode
        
        if isinstance(path, int):
            # Load from webcam
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                raise ValueError(f"Could not open webcam {path}")
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                raise ValueError(f"Could not read frame from webcam {path}")
            
            # Convert color mode if needed
            if mode == 'gray':
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            return frame
        else:
            # Load from file
            cv_mode = self.mode_map.get(mode, cv2.IMREAD_COLOR)
            image = cv2.imread(path, cv_mode)
            
            if image is None:
                raise ValueError(f"Could not load image from {path}")
            
            return image
    
    def load_multiple(self, paths: List[Union[str, int]], 
                     mode: Optional[str] = None) -> List[np.ndarray]:
        """
        Load multiple images
        
        Args:
            paths: List of image paths or webcam indices
            mode: Color mode for all images
            
        Returns:
            List of loaded images
        """
        return [self.load(path, mode) for path in paths]


class ImageSaver:
    """Class for saving images with quality control and format options"""
    
    def __init__(self, default_quality: int = 95):
        """
        Initialize ImageSaver
        
        Args:
            default_quality: Default JPEG quality (0-100)
        """
        self.default_quality = default_quality
    
    def save(self, image: np.ndarray, path: str, 
             quality: Optional[int] = None) -> bool:
        """
        Save an image to file with customizable quality
        
        Args:
            image: Image to save
            path: Output path
            quality: JPEG quality (0-100)
        
        Returns:
            Success status
        """
        quality = quality or self.default_quality
        
        if path.lower().endswith(('.jpg', '.jpeg')):
            return cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        elif path.lower().endswith('.png'):
            # PNG compression level (0-9)
            compression = max(0, min(9, int(9 * (100 - quality) / 100)))
            return cv2.imwrite(path, image, [cv2.IMWRITE_PNG_COMPRESSION, compression])
        else:
            return cv2.imwrite(path, image)
    
    def save_multiple(self, images: List[np.ndarray], paths: List[str],
                     quality: Optional[int] = None) -> List[bool]:
        """
        Save multiple images
        
        Args:
            images: List of images to save
            paths: List of output paths
            quality: JPEG quality for all images
            
        Returns:
            List of success statuses
        """
        if len(images) != len(paths):
            raise ValueError("Number of images must match number of paths")
        
        return [self.save(img, path, quality) for img, path in zip(images, paths)]


class ImageDisplayer:
    """Class for displaying images with customizable window properties"""
    
    def __init__(self, default_wait: bool = True):
        """
        Initialize ImageDisplayer
        
        Args:
            default_wait: Whether to wait for key press by default
        """
        self.default_wait = default_wait
        self.active_windows = set()
    
    def show(self, image: np.ndarray, title: str = 'Image', 
             wait: Optional[bool] = None, size: Optional[Tuple[int, int]] = None,
             position: Optional[Tuple[int, int]] = None) -> None:
        """
        Display an image with customizable window properties
        
        Args:
            image: Image to display
            title: Window title
            wait: Whether to wait for key press
            size: Window size (width, height)
            position: Window position (x, y)
        """
        wait = wait if wait is not None else self.default_wait
        
        if size:
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, size[0], size[1])
        else:
            cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
        
        if position:
            cv2.moveWindow(title, position[0], position[1])
        
        cv2.imshow(title, image)
        self.active_windows.add(title)
        
        if wait:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.active_windows.clear()
    
    def show_multiple(self, images: List[np.ndarray], titles: Optional[List[str]] = None,
                     grid_size: Optional[Tuple[int, int]] = None,
                     wait: Optional[bool] = None) -> None:
        """
        Display multiple images in separate windows or grid
        
        Args:
            images: List of images to display
            titles: List of window titles
            grid_size: If provided, arrange windows in grid (cols, rows)
            wait: Whether to wait for key press
        """
        wait = wait if wait is not None else self.default_wait
        titles = titles or [f"Image {i+1}" for i in range(len(images))]
        
        if len(images) != len(titles):
            raise ValueError("Number of images must match number of titles")
        
        if grid_size:
            cols, rows = grid_size
            for i, (img, title) in enumerate(zip(images, titles)):
                row = i // cols
                col = i % cols
                x = col * 300  # Window spacing
                y = row * 300
                self.show(img, title, wait=False, position=(x, y))
        else:
            for img, title in zip(images, titles):
                self.show(img, title, wait=False)
        
        if wait:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.active_windows.clear()
    
    def close_all(self) -> None:
        """Close all active windows"""
        cv2.destroyAllWindows()
        self.active_windows.clear()


class ImageResizer:
    """Class for resizing images with multiple sizing options"""
    
    def __init__(self, default_method: str = 'linear'):
        """
        Initialize ImageResizer
        
        Args:
            default_method: Default interpolation method
        """
        self.default_method = default_method
        self.method_map = {
            'linear': cv2.INTER_LINEAR,
            'cubic': cv2.INTER_CUBIC,
            'nearest': cv2.INTER_NEAREST,
            'area': cv2.INTER_AREA,
            'lanczos': cv2.INTER_LANCZOS4
        }
    
    def resize(self, image: np.ndarray, width: Optional[int] = None,
               height: Optional[int] = None, scale: Optional[float] = None,
               method: Optional[str] = None, maintain_aspect: bool = True) -> np.ndarray:
        """
        Resize an image with multiple sizing options
        
        Args:
            image: Input image
            width: Target width
            height: Target height
            scale: Scale factor
            method: Interpolation method
            maintain_aspect: Whether to maintain aspect ratio
        
        Returns:
            Resized image
        """
        method = method or self.default_method
        h, w = image.shape[:2]
        
        if scale:
            width = int(w * scale)
            height = int(h * scale)
        elif width and not height and maintain_aspect:
            height = int(h * (width / w))
        elif height and not width and maintain_aspect:
            width = int(w * (height / h))
        elif not width and not height and not scale:
            raise ValueError("At least one of width, height, or scale must be provided")
        
        if method.lower() not in self.method_map:
            raise ValueError(f"Invalid resize method: {method}. Choose from: {', '.join(self.method_map.keys())}")
        
        return cv2.resize(image, (width, height), 
                         interpolation=self.method_map.get(method.lower(), cv2.INTER_LINEAR))
    
    def resize_to_fit(self, image: np.ndarray, max_width: int, max_height: int,
                     method: Optional[str] = None) -> np.ndarray:
        """
        Resize image to fit within specified dimensions while maintaining aspect ratio
        
        Args:
            image: Input image
            max_width: Maximum width
            max_height: Maximum height
            method: Interpolation method
            
        Returns:
            Resized image
        """
        h, w = image.shape[:2]
        
        # Calculate scaling factor
        scale_w = max_width / w
        scale_h = max_height / h
        scale = min(scale_w, scale_h)
        
        if scale >= 1:
            return image  # No need to resize
        
        return self.resize(image, scale=scale, method=method)


class ImageCropper:
    """Class for cropping images with various options"""
    
    def __init__(self):
        """Initialize ImageCropper"""
        pass
    
    def crop(self, image: np.ndarray, x: int, y: int, width: int, height: int,
             safe_mode: bool = True) -> np.ndarray:
        """
        Crop an image to specified dimensions
        
        Args:
            image: Input image
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of crop area
            height: Height of crop area
            safe_mode: Whether to adjust coordinates if out of bounds
        
        Returns:
            Cropped image
        """
        img_height, img_width = image.shape[:2]
        
        if safe_mode:
            # Adjust coordinates to stay within bounds
            x = max(0, min(x, img_width - 1))
            y = max(0, min(y, img_height - 1))
            width = min(width, img_width - x)
            height = min(height, img_height - y)
        else:
            # Check if crop is out of bounds
            if x < 0 or y < 0 or x + width > img_width or y + height > img_height:
                raise ValueError(f"Crop dimensions ({x},{y},{width},{height}) out of bounds for image of size {img_width}x{img_height}")
        
        return image[y:y+height, x:x+width]
    
    def crop_center(self, image: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Crop image from center
        
        Args:
            image: Input image
            width: Crop width
            height: Crop height
            
        Returns:
            Center-cropped image
        """
        img_height, img_width = image.shape[:2]
        
        x = (img_width - width) // 2
        y = (img_height - height) // 2
        
        return self.crop(image, x, y, width, height)
    
    def crop_multiple_regions(self, image: np.ndarray, 
                             regions: List[Tuple[int, int, int, int]]) -> List[np.ndarray]:
        """
        Crop multiple regions from the same image
        
        Args:
            image: Input image
            regions: List of (x, y, width, height) tuples
            
        Returns:
            List of cropped images
        """
        return [self.crop(image, x, y, w, h) for x, y, w, h in regions]


class ColorSpaceConverter:
    """Class for converting images between different color spaces"""
    
    def __init__(self):
        """Initialize ColorSpaceConverter"""
        self.conversion_map = {
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
            ('bgr', 'yuv'): cv2.COLOR_BGR2YUV,
            ('yuv', 'bgr'): cv2.COLOR_YUV2BGR,
        }
    
    def convert(self, image: np.ndarray, from_space: str = 'bgr',
                to_space: str = 'rgb') -> np.ndarray:
        """
        Convert image between different color spaces
        
        Args:
            image: Input image
            from_space: Source color space
            to_space: Target color space
        
        Returns:
            Converted image
        """
        key = (from_space.lower(), to_space.lower())
        
        if key == (from_space.lower(), from_space.lower()):
            return image.copy()  # No conversion needed
        
        if key in self.conversion_map:
            return cv2.cvtColor(image, self.conversion_map[key])
        else:
            raise ValueError(f"Unsupported color space conversion: {from_space} -> {to_space}")
    
    def convert_multiple(self, images: List[np.ndarray], from_space: str = 'bgr',
                        to_space: str = 'rgb') -> List[np.ndarray]:
        """
        Convert multiple images to the same color space
        
        Args:
            images: List of input images
            from_space: Source color space
            to_space: Target color space
            
        Returns:
            List of converted images
        """
        return [self.convert(img, from_space, to_space) for img in images]


class ImageAnalyzer:
    """Class for analyzing image properties and statistics"""
    
    def __init__(self):
        """Initialize ImageAnalyzer"""
        pass
    
    def get_info(self, image: np.ndarray) -> dict:
        """
        Get comprehensive information about an image
        
        Args:
            image: Input image
        
        Returns:
            Image information dictionary
        """
        info = {
            'shape': image.shape,
            'height': image.shape[0],
            'width': image.shape[1],
            'channels': 1 if len(image.shape) == 2 else image.shape[2],
            'dtype': str(image.dtype),
            'size': image.size,
            'min_value': float(image.min()),
            'max_value': float(image.max()),
            'mean_value': float(image.mean()),
            'std_value': float(image.std()),
            'memory_mb': image.nbytes / (1024 * 1024)
        }
        return info
    
    def get_histogram(self, image: np.ndarray, bins: int = 256) -> dict:
        """
        Calculate histogram for each channel
        
        Args:
            image: Input image
            bins: Number of histogram bins
            
        Returns:
            Dictionary containing histograms for each channel
        """
        if len(image.shape) == 2:
            # Grayscale image
            hist = cv2.calcHist([image], [0], None, [bins], [0, 256])
            return {'gray': hist.flatten()}
        else:
            # Color image
            histograms = {}
            for i in range(image.shape[2]):
                hist = cv2.calcHist([image], [i], None, [bins], [0, 256])
                channel_name = ['blue', 'green', 'red'][i] if image.shape[2] == 3 else f'channel_{i}'
                histograms[channel_name] = hist.flatten()
            return histograms
    
    def compare_images(self, image1: np.ndarray, image2: np.ndarray) -> dict:
        """
        Compare two images and return similarity metrics
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Dictionary with comparison metrics
        """
        if image1.shape != image2.shape:
            raise ValueError("Images must have the same dimensions for comparison")
        
        # Mean Squared Error
        mse = np.mean((image1 - image2) ** 2)
        
        # Peak Signal-to-Noise Ratio
        if mse == 0:
            psnr = float('inf')
        else:
            max_pixel = 255.0
            psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
        # Structural Similarity Index (simplified version)
        mean1, mean2 = image1.mean(), image2.mean()
        var1, var2 = image1.var(), image2.var()
        covar = np.mean((image1 - mean1) * (image2 - mean2))
        
        c1, c2 = 0.01 ** 2, 0.03 ** 2
        ssim = ((2 * mean1 * mean2 + c1) * (2 * covar + c2)) / \
               ((mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2))
        
        return {
            'mse': float(mse),
            'psnr': float(psnr),
            'ssim': float(ssim),
            'are_identical': mse == 0
        }


# Legacy function wrappers for backward compatibility
def load_image(path: str, mode: str = 'color') -> np.ndarray:
    """
    Load an image from file with customizable color mode (Legacy function)
    
    Args:
        path (str): Path to the image file
        mode (str): Color mode - 'color', 'gray', 'unchanged'
    
    Returns:
        np.ndarray: Loaded image
    """
    loader = ImageLoader(default_mode=mode)
    return loader.load(path)


def save_image(image: np.ndarray, path: str, quality: int = 95) -> bool:
    """
    Save an image to file with customizable quality (Legacy function)
    
    Args:
        image (np.ndarray): Image to save
        path (str): Output path
        quality (int): JPEG quality (0-100)
    
    Returns:
        bool: Success status
    """
    saver = ImageSaver(default_quality=quality)
    return saver.save(image, path)


def show_image(image: np.ndarray, title: str = 'Image', wait: bool = True, 
               size: Optional[Tuple[int, int]] = None) -> None:
    """
    Display an image with customizable window properties (Legacy function)
    
    Args:
        image (np.ndarray): Image to display
        title (str): Window title
        wait (bool): Whether to wait for key press
        size (tuple): Window size (width, height)
    """
    displayer = ImageDisplayer(default_wait=wait)
    displayer.show(image, title, size=size)


def resize_image(image: np.ndarray, width: Optional[int] = None, 
                height: Optional[int] = None, scale: Optional[float] = None,
                method: str = 'linear') -> np.ndarray:
    """
    Resize an image with multiple sizing options (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        width (int): Target width
        height (int): Target height
        scale (float): Scale factor
        method (str): Interpolation method - 'linear', 'cubic', 'nearest'
    
    Returns:
        np.ndarray: Resized image
    """
    resizer = ImageResizer(default_method=method)
    return resizer.resize(image, width, height, scale)


def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """
    Crop an image to specified dimensions (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        x (int): X coordinate of top-left corner
        y (int): Y coordinate of top-left corner
        width (int): Width of crop area
        height (int): Height of crop area
    
    Returns:
        np.ndarray: Cropped image
    """
    cropper = ImageCropper()
    return cropper.crop(image, x, y, width, height, safe_mode=False)


def convert_color_space(image: np.ndarray, from_space: str = 'bgr', 
                       to_space: str = 'rgb') -> np.ndarray:
    """
    Convert image between different color spaces (Legacy function)
    
    Args:
        image (np.ndarray): Input image
        from_space (str): Source color space
        to_space (str): Target color space
    
    Returns:
        np.ndarray: Converted image
    """
    converter = ColorSpaceConverter()
    return converter.convert(image, from_space, to_space)


def get_image_info(image: np.ndarray) -> dict:
    """
    Get comprehensive information about an image (Legacy function)
    
    Args:
        image (np.ndarray): Input image
    
    Returns:
        dict: Image information
    """
    analyzer = ImageAnalyzer()
    return analyzer.get_info(image)
