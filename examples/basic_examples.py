"""
Basic Examples for Easy OpenCV Package
This file demonstrates the most common use cases with simple examples.
"""

from easy_opencv import cv
import numpy as np

def basic_image_operations():
    """Demonstrate basic image operations"""
    print("=== Basic Image Operations ===")
    
    # Create a sample image (you can replace with cv.load_image('your_image.jpg'))
    image = np.ones((400, 600, 3), dtype=np.uint8) * 128  # Gray image
    
    # Add some content to make it interesting
    image = cv.draw_rectangle(image, (50, 50), (200, 150), (255, 0, 0), filled=True)
    image = cv.draw_circle(image, (300, 200), 50, (0, 255, 0), filled=True)
    image = cv.draw_text(image, "Easy OpenCV Demo", (50, 300), font_scale=1.5, color=(255, 255, 255))
    
    # Basic operations
    resized = cv.resize_image(image, width=300)
    cropped = cv.crop_image(image, 100, 100, 200, 150)
    flipped = cv.flip_image(image, 'horizontal')
    
    # Show results
    cv.show_image(image, "Original", wait=False)
    cv.show_image(resized, "Resized", wait=False)
    cv.show_image(cropped, "Cropped", wait=False)
    cv.show_image(flipped, "Flipped")
    
    return image

def apply_filters_demo():
    """Demonstrate various filters"""
    print("=== Filters Demo ===")
    
    # Create sample image
    image = np.ones((400, 600, 3), dtype=np.uint8) * 255
    image = cv.draw_circle(image, (150, 200), 80, (100, 50, 200), filled=True)
    image = cv.draw_rectangle(image, (300, 100), (500, 300), (50, 200, 100), filled=True)
    
    # Apply different filters
    gaussian_blur = cv.apply_gaussian_blur(image, kernel_size=15)
    vintage = cv.apply_vintage_filter(image, intensity=0.8)
    cartoon = cv.apply_cartoon_filter(image)
    edges = cv.apply_edge_detection(image, method='canny')
    
    # Create comparison grid
    images = [image, gaussian_blur, vintage, cartoon]
    grid = cv.create_image_grid(images, grid_size=(2, 2), image_size=(300, 200))
    
    cv.show_image(grid, "Filters Comparison")
    
    return image

def drawing_operations_demo():
    """Demonstrate drawing operations"""
    print("=== Drawing Operations Demo ===")
    
    # Create blank canvas
    canvas = np.zeros((500, 700, 3), dtype=np.uint8)
    
    # Draw various shapes
    canvas = cv.draw_rectangle(canvas, (50, 50), (200, 150), (255, 0, 0), thickness=3)
    canvas = cv.draw_circle(canvas, (350, 100), 60, (0, 255, 0), filled=True)
    canvas = cv.draw_line(canvas, (50, 200), (650, 200), (255, 255, 0), thickness=5)
    canvas = cv.draw_arrow(canvas, (100, 300), (300, 400), (0, 255, 255), thickness=3)
    
    # Draw polygon (triangle)
    triangle_points = [(450, 250), (550, 250), (500, 350)]
    canvas = cv.draw_polygon(canvas, triangle_points, (255, 0, 255), thickness=3)
    
    # Add text
    canvas = cv.draw_text(canvas, "Drawing Demo", (50, 450), 
                         font_scale=2.0, color=(255, 255, 255), thickness=3)
    
    # Add crosshair
    canvas = cv.draw_crosshair(canvas, (600, 400), size=30, color=(255, 255, 255))
    
    cv.show_image(canvas, "Drawing Operations")
    
    return canvas

def transformations_demo():
    """Demonstrate image transformations"""
    print("=== Transformations Demo ===")
    
    # Create sample image
    image = np.ones((300, 400, 3), dtype=np.uint8) * 100
    image = cv.draw_rectangle(image, (50, 50), (150, 150), (255, 100, 0), filled=True)
    image = cv.draw_text(image, "TRANSFORM", (60, 200), color=(255, 255, 255))
    
    # Apply transformations
    rotated = cv.rotate_image(image, angle=45)
    translated = cv.translate_image(image, tx=50, ty=30)
    fisheye = cv.apply_fisheye_effect(image, strength=0.3)
    
    # Create comparison
    images = [image, rotated, translated, fisheye]
    labels = ["Original", "Rotated 45°", "Translated", "Fisheye"]
    
    # Show each transformation
    for img, label in zip(images, labels):
        cv.show_image(img, label, wait=False)
    
    # Wait for any key to close all windows
    cv.show_image(image, "Press any key to continue", wait=True)

def feature_detection_demo():
    """Demonstrate feature detection"""
    print("=== Feature Detection Demo ===")
    
    # Create sample image with features
    image = np.ones((400, 600, 3), dtype=np.uint8) * 50
    
    # Add some geometric shapes to detect
    image = cv.draw_rectangle(image, (100, 100), (200, 200), (255, 255, 255), filled=True)
    image = cv.draw_circle(image, (400, 150), 50, (200, 200, 200), filled=True)
    image = cv.draw_polygon(image, [(300, 250), (400, 250), (350, 350)], (180, 180, 180), filled=True)
    
    # Detect corners
    corners = cv.detect_corners(image, method='shi_tomasi', max_corners=50)
    
    # Draw detected corners
    result = image.copy()
    for corner in corners:
        x, y = corner.ravel()
        result = cv.draw_circle(result, (int(x), int(y)), 5, (0, 255, 0), filled=True)
    
    # Detect contours
    contours = cv.detect_contours(image, threshold_value=100, min_area=500)
    
    # Draw contours
    result = cv.draw_contour(result, contours, color=(255, 0, 0), thickness=2)
    
    cv.show_image(result, "Feature Detection: Corners (Green) & Contours (Red)")
    
    return result

def utility_functions_demo():
    """Demonstrate utility functions"""
    print("=== Utility Functions Demo ===")
    
    # Create sample images
    image1 = np.ones((300, 400, 3), dtype=np.uint8) * 100
    image1 = cv.draw_circle(image1, (200, 150), 50, (255, 0, 0), filled=True)
    
    image2 = np.ones((300, 400, 3), dtype=np.uint8) * 120
    image2 = cv.draw_rectangle(image2, (150, 100), (250, 200), (0, 255, 0), filled=True)
    
    # Image comparison
    comparison = cv.image_comparison(image1, image2, method='side_by_side')
    cv.show_image(comparison, "Image Comparison", wait=False)
    
    # Blend comparison
    blend = cv.image_comparison(image1, image2, method='blend')
    cv.show_image(blend, "Blended Images", wait=False)
    
    # Apply watermark
    watermarked = cv.apply_watermark(image1, "© Easy OpenCV", 
                                   position='bottom_right', opacity=0.7)
    cv.show_image(watermarked, "Watermarked Image")
    
    return comparison

def comprehensive_demo():
    """Run all demos in sequence"""
    print("Welcome to Easy OpenCV Comprehensive Demo!")
    print("This will demonstrate various features of the package.\n")
    
    try:
        # Run all demos
        basic_image_operations()
        apply_filters_demo()
        drawing_operations_demo()
        transformations_demo()
        feature_detection_demo()
        utility_functions_demo()
        
        print("\n=== Demo Completed Successfully! ===")
        print("You can now use Easy OpenCV in your projects with simple function calls.")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("Make sure OpenCV and dependencies are properly installed.")

if __name__ == "__main__":
    comprehensive_demo()
