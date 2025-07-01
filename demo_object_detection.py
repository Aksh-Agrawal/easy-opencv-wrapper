"""
Quick Demo: Object Detection with Automatic Webcam Fallback
This demonstrates the key feature where if no image source is provided,
the system automatically uses the webcam.
"""

import sys
import os

# Add the parent directory to the path so we can import easy_opencv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_webcam_fallback():
    """Demonstrate automatic webcam fallback"""
    print("=== Object Detection with Automatic Webcam Fallback ===")
    print()
    
    # Import the new classes
    from easy_opencv import FaceDetector, ColorDetector, EyeDetector
    
    print("Available detection options:")
    print("1. Face Detection")
    print("2. Eye Detection") 
    print("3. Red Color Detection")
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n🔍 Starting Face Detection...")
                print("💡 No image provided - automatically using webcam!")
                print("📹 Press 'q' to quit the webcam feed")
                print("⏳ Initializing...")
                
                # Create face detector
                detector = FaceDetector()
                
                # This will automatically use webcam since no source is provided
                try:
                    results = detector.detect_from_source(show_live=True)
                    print(f"✅ Face detection completed. Processed {len(results)} frames.")
                except Exception as e:
                    print(f"❌ Error during face detection: {e}")
                    if "Could not open webcam" in str(e):
                        print("💡 Make sure your webcam is connected and not being used by another application.")
                
            elif choice == '2':
                print("\n👀 Starting Eye Detection...")
                print("💡 No image provided - automatically using webcam!")
                print("📹 Press 'q' to quit the webcam feed")
                print("⏳ Initializing...")
                
                # Create eye detector
                detector = EyeDetector()
                
                try:
                    results = detector.detect_from_source(show_live=True)
                    print(f"✅ Eye detection completed. Processed {len(results)} frames.")
                except Exception as e:
                    print(f"❌ Error during eye detection: {e}")
                    if "Could not open webcam" in str(e):
                        print("💡 Make sure your webcam is connected and not being used by another application.")
                
            elif choice == '3':
                print("\n🔴 Starting Red Color Detection...")
                print("💡 No image provided - automatically using webcam!")
                print("📹 Press 'q' to quit the webcam feed")
                print("⏳ Initializing...")
                
                # Create color detector for red objects
                detector = ColorDetector(target_color='red', tolerance=20)
                
                try:
                    results = detector.detect_from_source(show_live=True)
                    print(f"✅ Red color detection completed. Processed {len(results)} frames.")
                except Exception as e:
                    print(f"❌ Error during color detection: {e}")
                    if "Could not open webcam" in str(e):
                        print("💡 Make sure your webcam is connected and not being used by another application.")
                
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            
            print()
            
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def demo_different_sources():
    """Demonstrate using different image sources"""
    print("\n=== Demonstrating Different Image Sources ===")
    print()
    
    from easy_opencv import FaceDetector
    
    # Create detector
    detector = FaceDetector()
    
    # Example of different source types
    print("🎯 Different ways to use the same detector:")
    print()
    
    print("1. Automatic webcam (no source specified):")
    print("   detector.detect_from_source()")
    print("   # Uses default webcam automatically")
    print()
    
    print("2. Explicit webcam index:")
    print("   detector.detect_from_source(source=0)  # First webcam")
    print("   detector.detect_from_source(source=1)  # Second webcam")
    print()
    
    print("3. Image file:")
    print("   detector.detect_from_source(source='photo.jpg')")
    print("   # If file doesn't exist, will show error")
    print()
    
    print("4. Video file:")
    print("   detector.detect_from_source(source='video.mp4')")
    print("   # If file doesn't exist, will show error")
    print()
    
    print("5. Programmatic detection (single image):")
    print("   import cv2")
    print("   image = cv2.imread('photo.jpg')")
    print("   faces = detector.detect(image)")
    print("   print(f'Found {len(faces)} faces')")

def demo_class_vs_legacy():
    """Show the difference between new classes and legacy functions"""
    print("\n=== New Classes vs Legacy Functions ===")
    print()
    
    print("🆕 NEW CLASS-BASED APPROACH (Recommended):")
    print("```python")
    print("from easy_opencv import FaceDetector")
    print()
    print("# Create detector with custom parameters")
    print("detector = FaceDetector(scale_factor=1.1, min_neighbors=5)")
    print()
    print("# Detect from webcam (automatic fallback)")
    print("results = detector.detect_from_source()")
    print()
    print("# Detect from specific source")
    print("results = detector.detect_from_source(source='image.jpg')")
    print()
    print("# Programmatic detection")
    print("import cv2")
    print("image = cv2.imread('image.jpg')")
    print("faces = detector.detect(image)")
    print("```")
    print()
    
    print("🔄 LEGACY FUNCTION APPROACH (Still works):")
    print("```python")
    print("from easy_opencv.object_detection import detect_faces")
    print("import cv2")
    print()
    print("# Load image manually")
    print("image = cv2.imread('image.jpg')")
    print()
    print("# Detect faces")
    print("faces = detect_faces(image, scale_factor=1.1, min_neighbors=5)")
    print("```")
    print()
    
    print("✨ ADVANTAGES OF NEW APPROACH:")
    print("• 🎥 Automatic webcam fallback")
    print("• 📁 Support for multiple input sources")
    print("• 🎛️ Reusable detector objects")
    print("• 👀 Built-in live visualization")
    print("• 🧹 Cleaner, object-oriented API")
    print("• 🔒 Better error handling")

def main():
    """Main demo function"""
    print("🚀 Easy OpenCV Object Detection Demo")
    print("=====================================")
    print()
    print("This demo shows the new class-based object detection system")
    print("with automatic webcam fallback functionality.")
    print()
    
    print("Choose demo type:")
    print("1. Interactive Webcam Demo")
    print("2. Show Different Source Types")
    print("3. Compare New vs Legacy Approach")
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                demo_webcam_fallback()
            elif choice == '2':
                demo_different_sources()
            elif choice == '3':
                demo_class_vs_legacy()
            elif choice == '4':
                print("👋 Thanks for trying the demo!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            
            print()
            
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted. Exiting...")
            break
        except Exception as e:
            print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    main()
