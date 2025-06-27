"""
Filters Module
Provides easy-to-use functions for image filtering
"""

import cv2
import numpy as np
from typing import Optional, Tuple

def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 15,
                       sigma_x: float = 0, sigma_y: float = 0) -> np.ndarray:
    """
    Apply Gaussian blur filter
    
    Args:
        image (np.ndarray): Input image
        kernel_size (int): Size of the Gaussian kernel
        sigma_x (float): Gaussian kernel standard deviation in X direction
        sigma_y (float): Gaussian kernel standard deviation in Y direction
    
    Returns:
        np.ndarray: Blurred image
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure odd kernel size
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma_x, sigmaY=sigma_y)

def apply_median_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply median blur filter (good for removing noise)
    
    Args:
        image (np.ndarray): Input image
        kernel_size (int): Size of the kernel
    
    Returns:
        np.ndarray: Filtered image
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure odd kernel size
    
    return cv2.medianBlur(image, kernel_size)

def apply_bilateral_filter(image: np.ndarray, diameter: int = 9,
                          sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
    """
    Apply bilateral filter (preserves edges while reducing noise)
    
    Args:
        image (np.ndarray): Input image
        diameter (int): Diameter of each pixel neighborhood
        sigma_color (float): Filter sigma in the color space
        sigma_space (float): Filter sigma in the coordinate space
    
    Returns:
        np.ndarray: Filtered image
    """
    return cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)

def apply_custom_kernel(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Apply a custom convolution kernel
    
    Args:
        image (np.ndarray): Input image
        kernel (np.ndarray): Custom convolution kernel
    
    Returns:
        np.ndarray: Filtered image
    """
    return cv2.filter2D(image, -1, kernel)

def apply_noise_reduction(image: np.ndarray, method: str = 'bilateral',
                         strength: int = 10) -> np.ndarray:
    """
    Apply noise reduction filters
    
    Args:
        image (np.ndarray): Input image
        method (str): Noise reduction method - 'bilateral', 'nlmeans', 'gaussian'
        strength (int): Filter strength
    
    Returns:
        np.ndarray: Denoised image
    """
    if method == 'bilateral':
        return cv2.bilateralFilter(image, strength, strength * 2, strength * 2)
    elif method == 'nlmeans':
        if len(image.shape) == 3:
            return cv2.fastNlMeansDenoisingColored(image, None, strength, strength, 7, 21)
        else:
            return cv2.fastNlMeansDenoising(image, None, strength, 7, 21)
    elif method == 'gaussian':
        return cv2.GaussianBlur(image, (strength, strength), 0)
    else:
        return image

def apply_emboss_filter(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Apply emboss filter to create 3D effect
    
    Args:
        image (np.ndarray): Input image
        strength (float): Emboss strength
    
    Returns:
        np.ndarray: Embossed image
    """
    kernel = np.array([[-2, -1, 0],
                      [-1,  1, 1],
                      [ 0,  1, 2]]) * strength
    
    embossed = cv2.filter2D(image, -1, kernel)
    # Normalize to 0-255 range
    embossed = np.clip(embossed + 128, 0, 255).astype(np.uint8)
    return embossed

def apply_edge_enhance_filter(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Apply edge enhancement filter
    
    Args:
        image (np.ndarray): Input image
        strength (float): Enhancement strength
    
    Returns:
        np.ndarray: Edge enhanced image
    """
    kernel = np.array([[ 0, -1,  0],
                      [-1,  5, -1],
                      [ 0, -1,  0]]) * strength
    
    return cv2.filter2D(image, -1, kernel)

def apply_unsharp_mask(image: np.ndarray, radius: float = 1.0,
                      amount: float = 1.0, threshold: int = 0) -> np.ndarray:
    """
    Apply unsharp mask for image sharpening
    
    Args:
        image (np.ndarray): Input image
        radius (float): Blur radius
        amount (float): Sharpening amount
        threshold (int): Threshold for sharpening
    
    Returns:
        np.ndarray: Sharpened image
    """
    # Create blurred version
    blurred = cv2.GaussianBlur(image, (0, 0), radius)
    
    # Create sharpened image
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    
    # Apply threshold if specified
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    
    return sharpened

def apply_high_pass_filter(image: np.ndarray, radius: int = 10) -> np.ndarray:
    """
    Apply high-pass filter to enhance details
    
    Args:
        image (np.ndarray): Input image
        radius (int): Filter radius
    
    Returns:
        np.ndarray: High-pass filtered image
    """
    # Create low-pass version
    low_pass = cv2.GaussianBlur(image, (2*radius+1, 2*radius+1), 0)
    
    # Subtract low-pass from original to get high-pass
    high_pass = cv2.subtract(image, low_pass)
    
    # Add 128 to center the values
    high_pass = cv2.add(high_pass, 128)
    
    return high_pass

def apply_motion_blur(image: np.ndarray, size: int = 15, angle: float = 0) -> np.ndarray:
    """
    Apply motion blur effect
    
    Args:
        image (np.ndarray): Input image
        size (int): Blur size
        angle (float): Motion angle in degrees
    
    Returns:
        np.ndarray: Motion blurred image
    """
    # Create motion blur kernel
    kernel = np.zeros((size, size))
    
    # Calculate kernel based on angle
    if angle == 0:
        kernel[int((size-1)/2), :] = np.ones(size)
    elif angle == 90:
        kernel[:, int((size-1)/2)] = np.ones(size)
    else:
        # For other angles, create diagonal kernel
        radian = np.deg2rad(angle)
        for i in range(size):
            offset = int((i - size/2) * np.tan(radian))
            if 0 <= offset < size:
                kernel[i, offset] = 1
    
    kernel = kernel / kernel.sum()
    
    return cv2.filter2D(image, -1, kernel)

def apply_vintage_filter(image: np.ndarray, intensity: float = 0.5) -> np.ndarray:
    """
    Apply vintage/sepia effect
    
    Args:
        image (np.ndarray): Input image
        intensity (float): Effect intensity (0.0 to 1.0)
    
    Returns:
        np.ndarray: Vintage filtered image
    """
    # Sepia transformation matrix
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                            [0.349, 0.686, 0.168],
                            [0.393, 0.769, 0.189]])
    
    sepia_img = cv2.transform(image, sepia_kernel)
    
    # Blend with original based on intensity
    vintage = cv2.addWeighted(image, 1 - intensity, sepia_img, intensity, 0)
    
    return np.clip(vintage, 0, 255).astype(np.uint8)

def apply_cartoon_filter(image: np.ndarray, num_down: int = 2, num_bilateral: int = 7) -> np.ndarray:
    """
    Apply cartoon effect to image
    
    Args:
        image (np.ndarray): Input image
        num_down (int): Number of downsampling steps
        num_bilateral (int): Number of bilateral filter applications
    
    Returns:
        np.ndarray: Cartoon filtered image
    """
    # Downsample image
    img_small = image
    for _ in range(num_down):
        img_small = cv2.pyrDown(img_small)
    
    # Apply bilateral filter multiple times
    for _ in range(num_bilateral):
        img_small = cv2.bilateralFilter(img_small, 9, 200, 200)
    
    # Upsample image back to original size
    img_rgb = img_small
    for _ in range(num_down):
        img_rgb = cv2.pyrUp(img_rgb)
    
    # Resize to match original dimensions
    img_rgb = cv2.resize(img_rgb, (image.shape[1], image.shape[0]))
    
    # Create edge mask
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)
    img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    
    # Convert edge mask to 3-channel
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2BGR)
    
    # Combine color reduction and edge mask
    cartoon = cv2.bitwise_and(img_rgb, img_edge)
    
    return cartoon
