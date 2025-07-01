"""
Object Detection Examples
Demonstrates how to use the new class-based object detection system with webcam support
"""

import cv2
import numpy as np
from easy_opencv.object_detection import (
    FaceDetector, EyeDetector, CascadeDetector, MotionDetector,
    CircleDetector, LineDetector, ColorDetector, DNNObjectDetector
)

def face_detection_example():
    """Example of face detection from webcam"""
    print("Starting face detection from webcam...")
    print("Press 'q' to quit")
    
    # Create face detector
    face_detector = FaceDetector(scale_factor=1.1, min_neighbors=5, min_size=(30, 30))
    
    # Detect faces from webcam (source=None uses default webcam)
    # You can also pass a specific webcam index like source=0, source=1, etc.
    # Or pass an image/video path like source="path/to/image.jpg"
    results = face_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected faces in {len(results)} frames")


def eye_detection_example():
    """Example of eye detection from webcam"""
    print("Starting eye detection from webcam...")
    print("Press 'q' to quit")
    
    # Create eye detector
    eye_detector = EyeDetector(scale_factor=1.1, min_neighbors=5, min_size=(20, 20))
    
    # Detect eyes from webcam
    results = eye_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected eyes in {len(results)} frames")


def motion_detection_example():
    """Example of motion detection from webcam"""
    print("Starting motion detection from webcam...")
    print("Press 'q' to quit")
    
    # Create motion detector
    motion_detector = MotionDetector(method='mog2', sensitivity=500)
    
    # Detect motion from webcam and optionally save to file
    results = motion_detector.detect_from_source(
        source=None, 
        show_live=True, 
        output_path="motion_detection_output.mp4"  # Optional: save output
    )
    
    print(f"Detected motion in {len(results)} frames")


def circle_detection_example():
    """Example of circle detection from webcam"""
    print("Starting circle detection from webcam...")
    print("Press 'q' to quit")
    
    # Create circle detector
    circle_detector = CircleDetector(min_radius=10, max_radius=100, sensitivity=50)
    
    # Detect circles from webcam
    results = circle_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected circles in {len(results)} frames")


def line_detection_example():
    """Example of line detection from webcam"""
    print("Starting line detection from webcam...")
    print("Press 'q' to quit")
    
    # Create line detector
    line_detector = LineDetector(threshold=100, min_line_length=50, max_line_gap=10)
    
    # Detect lines from webcam
    results = line_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected lines in {len(results)} frames")


def color_detection_example():
    """Example of color detection from webcam"""
    print("Starting red color detection from webcam...")
    print("Press 'q' to quit")
    
    # Create color detector for red objects
    color_detector = ColorDetector(target_color='red', tolerance=20)
    
    # Detect red objects from webcam
    results = color_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected red objects in {len(results)} frames")


def dnn_object_detection_example():
    """Example of DNN object detection from webcam"""
    print("Starting DNN object detection from webcam...")
    print("This will download the model files on first run...")
    print("Press 'q' to quit")
    
    # Create DNN object detector
    dnn_detector = DNNObjectDetector(confidence_threshold=0.5, nms_threshold=0.4)
    
    # Detect objects from webcam
    results = dnn_detector.detect_from_source(source=None, show_live=True)
    
    print(f"Detected objects in {len(results)} frames")


def single_image_detection_example():
    """Example of detecting objects in a single image"""
    print("Example: Detecting faces in a single image...")
    
    # You can replace this with your actual image path
    image_path = "path/to/your/image.jpg"
    
    # Check if image exists, otherwise use webcam
    import os
    if not os.path.exists(image_path):
        print(f"Image {image_path} not found. Using webcam instead.")
        image_path = None  # This will use webcam
    
    # Create face detector
    face_detector = FaceDetector()
    
    # Detect faces from image or webcam
    results = face_detector.detect_from_source(source=image_path, show_live=True)
    
    if image_path:
        print(f"Detected {len(results[0]) if results else 0} faces in the image")
    else:
        print(f"Detected faces in {len(results)} frames from webcam")


def video_file_detection_example():
    """Example of detecting objects in a video file"""
    print("Example: Detecting motion in a video file...")
    
    # You can replace this with your actual video path
    video_path = "path/to/your/video.mp4"
    
    # Check if video exists, otherwise use webcam
    import os
    if not os.path.exists(video_path):
        print(f"Video {video_path} not found. Using webcam instead.")
        video_path = None  # This will use webcam
    
    # Create motion detector
    motion_detector = MotionDetector(sensitivity=1000)
    
    # Detect motion from video or webcam
    results = motion_detector.detect_from_source(source=video_path, show_live=True)
    
    if video_path:
        print(f"Detected motion in {len(results)} frames of the video")
    else:
        print(f"Detected motion in {len(results)} frames from webcam")


def programmatic_detection_example():
    """Example of programmatic detection without GUI"""
    print("Example: Programmatic detection from webcam...")
    
    # Create face detector
    face_detector = FaceDetector()
    
    # Manually capture and process frames
    cap = cv2.VideoCapture(0)  # Use default webcam
    
    frame_count = 0
    total_faces = 0
    
    try:
        while frame_count < 30:  # Process 30 frames
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces in the frame
            faces = face_detector.detect(frame)
            total_faces += len(faces)
            frame_count += 1
            
            print(f"Frame {frame_count}: Detected {len(faces)} faces")
    
    finally:
        cap.release()
    
    print(f"Total faces detected across {frame_count} frames: {total_faces}")


def main():
    """Main function to run examples"""
    print("Object Detection Examples")
    print("=" * 50)
    print("1. Face Detection from Webcam")
    print("2. Eye Detection from Webcam")
    print("3. Motion Detection from Webcam")
    print("4. Circle Detection from Webcam")
    print("5. Line Detection from Webcam")
    print("6. Color Detection from Webcam")
    print("7. DNN Object Detection from Webcam")
    print("8. Single Image Detection")
    print("9. Video File Detection")
    print("10. Programmatic Detection")
    print("=" * 50)
    
    try:
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            face_detection_example()
        elif choice == '2':
            eye_detection_example()
        elif choice == '3':
            motion_detection_example()
        elif choice == '4':
            circle_detection_example()
        elif choice == '5':
            line_detection_example()
        elif choice == '6':
            color_detection_example()
        elif choice == '7':
            dnn_object_detection_example()
        elif choice == '8':
            single_image_detection_example()
        elif choice == '9':
            video_file_detection_example()
        elif choice == '10':
            programmatic_detection_example()
        else:
            print("Invalid choice. Please run the script again.")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
