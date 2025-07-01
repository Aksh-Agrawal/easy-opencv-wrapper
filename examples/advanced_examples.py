"""
Advanced Examples for Easy OpenCV Package
This file demonstrates more complex use cases and real-world applications.
"""

from easy_opencv import cv
import numpy as np
import os

def face_detection_demo():
    """Demonstrate face detection with webcam or image"""
    print("=== Face Detection Demo ===")
    
    # Create a sample image with face-like shapes (since we don't have actual photos)
    image = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Draw face-like oval shapes for demonstration
    image = cv.draw_circle(image, (200, 200), 80, (220, 180, 150), filled=True)  # Face
    image = cv.draw_circle(image, (180, 180), 8, (50, 50, 50), filled=True)      # Eye
    image = cv.draw_circle(image, (220, 180), 8, (50, 50, 50), filled=True)      # Eye
    image = cv.draw_circle(image, (200, 210), 5, (100, 50, 50), filled=True)     # Nose
    
    # Another face
    image = cv.draw_circle(image, (450, 300), 70, (210, 170, 140), filled=True)  # Face
    image = cv.draw_circle(image, (435, 285), 7, (40, 40, 40), filled=True)      # Eye
    image = cv.draw_circle(image, (465, 285), 7, (40, 40, 40), filled=True)      # Eye
    
    # Try to detect faces (may not work on artificial faces, but demonstrates the function)
    faces = cv.detect_faces(image, scale_factor=1.1, min_neighbors=3, min_size=(50, 50))
    
    # Draw rectangles around detected areas
    result = image.copy()
    for (x, y, w, h) in faces:
        result = cv.draw_rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), thickness=3)
        result = cv.draw_text(result, "Face", (x, y-10), color=(0, 255, 0))
    
    if len(faces) == 0:
        # If no faces detected, draw manual bounding boxes for demo
        result = cv.draw_rectangle(result, (120, 120), (280, 280), (0, 255, 0), thickness=3)
        result = cv.draw_text(result, "Face Area", (120, 110), color=(0, 255, 0))
        
        result = cv.draw_rectangle(result, (380, 230), (520, 370), (0, 255, 0), thickness=3)
        result = cv.draw_text(result, "Face Area", (380, 220), color=(0, 255, 0))
    
    cv.show_image(result, "Face Detection Demo")
    
    return result

def real_time_filter_application():
    """Demonstrate real-time filter application (simulated)"""
    print("=== Real-time Filter Application ===")
    
    # Create base image
    base_image = np.ones((400, 600, 3), dtype=np.uint8) * 150
    base_image = cv.draw_circle(base_image, (200, 200), 80, (100, 150, 200), filled=True)
    base_image = cv.draw_rectangle(base_image, (350, 150), (550, 250), (200, 100, 150), filled=True)
    
    # Simulate different filter applications
    filters = [
        ("Original", lambda img: img),
        ("Gaussian Blur", lambda img: cv.apply_gaussian_blur(img, kernel_size=15)),
        ("Vintage", lambda img: cv.apply_vintage_filter(img, intensity=0.8)),
        ("Cartoon", lambda img: cv.apply_cartoon_filter(img)),
        ("Edge Detection", lambda img: cv.apply_edge_detection(img, method='canny')),
        ("Motion Blur", lambda img: cv.apply_motion_blur(img, size=15, angle=45))
    ]
    
    # Apply each filter and show
    filtered_images = []
    for name, filter_func in filters:
        filtered = filter_func(base_image.copy())
        # Convert single channel to 3-channel for consistency
        if len(filtered.shape) == 2:
            filtered = cv.convert_color_space(filtered, 'gray', 'bgr')
        
        # Add filter name to image
        filtered = cv.draw_text(filtered, name, (10, 30), 
                              font_scale=1.0, color=(255, 255, 0), thickness=2)
        filtered_images.append(filtered)
    
    # Create grid of filtered images
    grid = cv.create_image_grid(filtered_images, grid_size=(2, 3), image_size=(300, 200))
    cv.show_image(grid, "Real-time Filter Effects")
    
    return grid

def object_tracking_simulation():
    """Simulate object tracking across multiple frames"""
    print("=== Object Tracking Simulation ===")
    
    frames = []
    
    # Create sequence of frames with moving object
    for i in range(6):
        frame = np.zeros((300, 500, 3), dtype=np.uint8)
        
        # Moving circle (simulated object)
        x_pos = 50 + i * 70
        y_pos = 150 + int(30 * np.sin(i * 0.5))  # Add some vertical movement
        
        frame = cv.draw_circle(frame, (x_pos, y_pos), 25, (0, 255, 255), filled=True)
        
        # Add tracking box
        frame = cv.draw_rectangle(frame, (x_pos-35, y_pos-35), (x_pos+35, y_pos+35), 
                                (255, 0, 0), thickness=2)
        
        # Add frame number
        frame = cv.draw_text(frame, f"Frame {i+1}", (10, 30), 
                           font_scale=0.8, color=(255, 255, 255))
        
        # Add trajectory line
        if i > 0:
            prev_x = 50 + (i-1) * 70
            prev_y = 150 + int(30 * np.sin((i-1) * 0.5))
            frame = cv.draw_line(frame, (prev_x, prev_y), (x_pos, y_pos), 
                               (0, 255, 0), thickness=2)
        
        frames.append(frame)
    
    # Show tracking sequence
    grid = cv.create_image_grid(frames, grid_size=(2, 3), image_size=(250, 150))
    cv.show_image(grid, "Object Tracking Simulation")
    
    return grid

def image_enhancement_pipeline():
    """Demonstrate a complete image enhancement pipeline"""
    print("=== Image Enhancement Pipeline ===")
    
    # Create a noisy, low-contrast image
    image = np.random.randint(80, 120, (300, 400, 3), dtype=np.uint8)  # Low contrast base
    
    # Add some structure
    image = cv.draw_rectangle(image, (50, 50), (150, 150), (140, 140, 140), filled=True)
    image = cv.draw_circle(image, (250, 200), 40, (160, 160, 160), filled=True)
    
    # Add noise
    noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
    noisy_image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Enhancement pipeline steps
    steps = []
    current = noisy_image.copy()
    
    # Step 1: Noise reduction
    current = cv.apply_noise_reduction(current, method='bilateral', strength=10)
    steps.append(("1. Noise Reduction", current.copy()))
    
    # Step 2: Contrast enhancement
    current = cv.adjust_brightness_contrast(current, brightness=10, contrast=1.3)
    steps.append(("2. Contrast Enhancement", current.copy()))
    
    # Step 3: Sharpening
    current = cv.apply_unsharp_mask(current, radius=1.0, amount=0.5)
    steps.append(("3. Sharpening", current.copy()))
    
    # Step 4: Color enhancement (histogram equalization)
    current = cv.apply_histogram_equalization(current, method='adaptive')
    steps.append(("4. Color Enhancement", current.copy()))
    
    # Create comparison
    all_images = [("Original (Noisy)", noisy_image)] + steps
    
    # Show each step
    for name, img in all_images:
        labeled_img = cv.draw_text(img.copy(), name, (10, 25), 
                                 font_scale=0.7, color=(255, 255, 0), 
                                 background=True, bg_color=(0, 0, 0))
        cv.show_image(labeled_img, name, wait=False)
    
    # Show final comparison
    comparison = cv.image_comparison(noisy_image, current, method='side_by_side')
    comparison = cv.draw_text(comparison, "BEFORE vs AFTER", (10, 25), 
                            font_scale=1.0, color=(255, 255, 0), thickness=2)
    cv.show_image(comparison, "Enhancement Results")
    
    return comparison

def color_space_analysis():
    """Demonstrate color space analysis and manipulation"""
    print("=== Color Space Analysis ===")
    
    # Create a colorful image
    image = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Add colored regions
    image[50:150, 50:150] = [255, 0, 0]    # Red
    image[50:150, 200:300] = [0, 255, 0]   # Green
    image[150:250, 50:150] = [0, 0, 255]   # Blue
    image[150:250, 200:300] = [255, 255, 0] # Yellow
    
    # Convert to different color spaces
    hsv = cv.convert_color_space(image, 'bgr', 'hsv')
    lab = cv.convert_color_space(image, 'bgr', 'lab')
    gray = cv.convert_color_space(image, 'bgr', 'gray')
    gray_bgr = cv.convert_color_space(gray, 'gray', 'bgr')  # Convert back for display
    
    # Color detection for each primary color
    red_mask = cv.color_detection(image, 'red', tolerance=50)
    green_mask = cv.color_detection(image, 'green', tolerance=50)
    blue_mask = cv.color_detection(image, 'blue', tolerance=50)
    
    # Convert masks to BGR for display
    red_mask_bgr = cv.convert_color_space(red_mask, 'gray', 'bgr')
    green_mask_bgr = cv.convert_color_space(green_mask, 'gray', 'bgr')
    blue_mask_bgr = cv.convert_color_space(blue_mask, 'gray', 'bgr')
    
    # Create analysis grid
    images = [
        image, hsv, lab, gray_bgr,
        red_mask_bgr, green_mask_bgr, blue_mask_bgr, image
    ]
    
    labels = [
        "Original (BGR)", "HSV", "LAB", "Grayscale",
        "Red Detection", "Green Detection", "Blue Detection", "Combined"
    ]
    
    # Add labels to images
    labeled_images = []
    for img, label in zip(images, labels):
        labeled = cv.draw_text(img.copy(), label, (5, 20), 
                             font_scale=0.5, color=(255, 255, 255), 
                             background=True, bg_color=(0, 0, 0))
        labeled_images.append(labeled)
    
    grid = cv.create_image_grid(labeled_images, grid_size=(2, 4), image_size=(200, 150))
    cv.show_image(grid, "Color Space Analysis")
    
    return grid

def geometric_shape_detection():
    """Demonstrate detection and classification of geometric shapes"""
    print("=== Geometric Shape Detection ===")
    
    # Create image with various shapes
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Draw different shapes
    # Triangle
    triangle_pts = [(100, 100), (150, 200), (50, 200)]
    image = cv.draw_polygon(image, triangle_pts, (255, 255, 255), filled=True)
    
    # Rectangle
    image = cv.draw_rectangle(image, (200, 100), (350, 200), (255, 255, 255), filled=True)
    
    # Circle
    image = cv.draw_circle(image, (450, 150), 50, (255, 255, 255), filled=True)
    
    # Pentagon (approximate)
    pentagon_pts = [(100, 250), (140, 230), (160, 270), (120, 310), (80, 290)]
    image = cv.draw_polygon(image, pentagon_pts, (255, 255, 255), filled=True)
    
    # Hexagon (approximate)
    hexagon_pts = [(250, 250), (290, 230), (330, 250), (330, 290), (290, 310), (250, 290)]
    image = cv.draw_polygon(image, hexagon_pts, (255, 255, 255), filled=True)
    
    # Detect shapes
    shapes = cv.find_shapes(image, min_area=500)
    
    # Draw detection results
    result = image.copy()
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    for i, shape in enumerate(shapes):
        color = colors[i % len(colors)]
        
        # Draw contour
        result = cv.draw_contour(result, [shape['contour']], color=color, thickness=3)
        
        # Draw bounding box
        x, y, w, h = shape['bounding_box']
        result = cv.draw_rectangle(result, (x, y), (x+w, y+h), color, thickness=2)
        
        # Add label
        center_x, center_y = shape['center']
        result = cv.draw_text(result, shape['name'], (center_x-20, center_y), 
                            font_scale=0.6, color=color, thickness=2)
    
    # Add title
    result = cv.draw_text(result, "Shape Detection Results", (10, 30), 
                        font_scale=1.0, color=(255, 255, 255), thickness=2)
    
    cv.show_image(result, "Geometric Shape Detection")
    
    return result

def dnn_object_detection_demo():
    """Demonstrate object detection using a pre-trained DNN model."""
    print("=== DNN Object Detection Demo ===")

    # Create a sample image for detection
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    # Draw a green circle (could be a 'bottle')
    image = cv.draw_circle(image, (150, 200), 50, (0, 255, 0), filled=True)
    # Draw a red rectangle (could be a 'tvmonitor')
    image = cv.draw_rectangle(image, (350, 150), (500, 300), (0, 0, 255), filled=True)

    # Detect objects using the DNN model
    detected_objects = cv.detect_objects_dnn(image, confidence_threshold=0.2)

    result = image.copy()
    # Draw bounding boxes and labels
    for (label, confidence, (startX, startY, endX, endY)) in detected_objects:
        result = cv.draw_rectangle(result, (startX, startY), (endX, endY), (255, 255, 0), thickness=2)
        text = f"{label}: {confidence:.2f}"
        result = cv.draw_text(result, text, (startX, startY - 10), font_scale=0.6, color=(255, 255, 0))

    cv.show_image(result, "DNN Object Detection Demo")
    return result

def advanced_demo():
    """Run all advanced demos"""
    print("Welcome to Easy OpenCV Advanced Demo!")
    print("This demonstrates more complex computer vision applications.\n")
    
    try:
        face_detection_demo()
        real_time_filter_application()
        object_tracking_simulation()
        image_enhancement_pipeline()
        color_space_analysis()
        geometric_shape_detection()
        dnn_object_detection_demo()

        print("\n=== Advanced Demo Completed! ===")
        print("These examples show how Easy OpenCV can handle complex tasks with simple calls.")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("Make sure all dependencies are properly installed.")

if __name__ == "__main__":
    advanced_demo()
