"""
Quick Demo - Shows how easy it is to use the Easy OpenCV package
"""

from easy_opencv import cv
import numpy as np

print("🎨 Easy OpenCV - Quick Demo")
print("=" * 40)

# Create a sample image (in real use, you'd load with cv.load_image('path/to/image.jpg'))
print("1. Creating a sample image...")
image = np.ones((400, 600, 3), dtype=np.uint8) * 240  # Light gray background

# Draw some shapes with simple function calls
print("2. Drawing shapes with simple commands...")
image = cv.draw_rectangle(image, (50, 50), (200, 150), color=(255, 100, 100), filled=True)
image = cv.draw_circle(image, (400, 100), radius=60, color=(100, 255, 100), filled=True)
image = cv.draw_text(image, "Easy OpenCV!", (50, 250), font_scale=2.0, color=(50, 50, 255), thickness=3)

# Apply filters with one line each
print("3. Applying filters...")
blurred = cv.apply_gaussian_blur(image, kernel_size=21)
vintage = cv.apply_vintage_filter(image, intensity=0.8)
cartoon = cv.apply_cartoon_filter(image)

# Image transformations
print("4. Applying transformations...")
rotated = cv.rotate_image(image, angle=15)
fisheye = cv.apply_fisheye_effect(image, strength=0.3)

# Object detection (finding shapes we drew)
print("5. Detecting objects...")
contours = cv.detect_contours(image, threshold_value=200, min_area=1000)
print(f"   Found {len(contours)} objects!")

# Add detection results to image
detected = image.copy()
detected = cv.draw_contour(detected, contours, color=(0, 255, 255), thickness=3)
detected = cv.draw_text(detected, f"Detected {len(contours)} objects", (50, 320), 
                       font_scale=1.0, color=(0, 255, 255), thickness=2)

# Create a comparison grid
print("6. Creating comparison grid...")
images = [image, blurred, vintage, cartoon, rotated, fisheye, detected, image]
labels = ["Original", "Blurred", "Vintage", "Cartoon", "Rotated", "Fisheye", "Detected", "Final"]

# Add labels to images
labeled_images = []
for img, label in zip(images, labels):
    labeled = cv.draw_text(img.copy(), label, (10, 30), 
                          font_scale=0.8, color=(255, 255, 255), 
                          background=True, bg_color=(0, 0, 0))
    labeled_images.append(labeled)

# Create final grid
grid = cv.create_image_grid(labeled_images, grid_size=(2, 4), image_size=(300, 200))

# Add watermark
grid = cv.apply_watermark(grid, "Made with Easy OpenCV", 
                         position='bottom_right', opacity=0.7)

print("7. Displaying results...")
cv.show_image(grid, "Easy OpenCV Demo - All Effects in One Grid!")

print("\n✅ Demo complete!")
print("🚀 With Easy OpenCV, complex computer vision tasks become simple one-liners!")
print("\nKey benefits:")
print("   • Simple function names (cv.apply_blur vs cv2.GaussianBlur)")
print("   • Intuitive parameters (strength=15 vs kernel_size=(15,15), sigmaX=0)")
print("   • Automatic parameter handling (odd kernel sizes, color conversions)")
print("   • Built-in error handling and validation")
print("   • Comprehensive documentation and examples")

# Get image information easily
info = cv.get_image_info(image)
print(f"\n📊 Image Info: {info['width']}x{info['height']} pixels, {info['channels']} channels")

print("\n🎯 Ready to use in your projects!")
print("   from easy_opencv import cv")
print("   image = cv.load_image('your_image.jpg')")
print("   result = cv.apply_cartoon_filter(image)")
print("   cv.save_image(result, 'output.jpg')")
