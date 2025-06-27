"""
Video Operations Module
Provides easy-to-use functions for video processing
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple

def load_video(path: str) -> cv2.VideoCapture:
    """
    Load a video file
    
    Args:
        path (str): Path to video file
    
    Returns:
        cv2.VideoCapture: Video capture object
    """
    return cv2.VideoCapture(path)

def save_video(frames: List[np.ndarray], output_path: str, fps: float = 30.0,
               codec: str = 'mp4v') -> bool:
    """
    Save frames as a video file
    
    Args:
        frames (List[np.ndarray]): List of frames
        output_path (str): Output video path
        fps (float): Frames per second
        codec (str): Video codec
    
    Returns:
        bool: Success status
    """
    if not frames:
        return False
    
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    return True

def extract_frames(video_path: str, output_dir: str = '.', 
                  frame_interval: int = 1, max_frames: Optional[int] = None) -> List[str]:
    """
    Extract frames from a video
    
    Args:
        video_path (str): Input video path
        output_dir (str): Directory to save frames
        frame_interval (int): Extract every nth frame
        max_frames (int): Maximum number of frames to extract
    
    Returns:
        List[str]: List of saved frame paths
    """
    cap = cv2.VideoCapture(video_path)
    frame_paths = []
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            if max_frames and saved_count >= max_frames:
                break
            
            frame_path = f"{output_dir}/frame_{saved_count:06d}.jpg"
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    return frame_paths

def create_video_from_frames(frame_paths: List[str], output_path: str, 
                           fps: float = 30.0, codec: str = 'mp4v') -> bool:
    """
    Create a video from a list of frame images
    
    Args:
        frame_paths (List[str]): List of frame image paths
        output_path (str): Output video path
        fps (float): Frames per second
        codec (str): Video codec
    
    Returns:
        bool: Success status
    """
    if not frame_paths:
        return False
    
    # Read first frame to get dimensions
    first_frame = cv2.imread(frame_paths[0])
    height, width = first_frame.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        if frame is not None:
            out.write(frame)
    
    out.release()
    return True

def get_video_info(video_path: str) -> dict:
    """
    Get comprehensive information about a video
    
    Args:
        video_path (str): Path to video file
    
    Returns:
        dict: Video information
    """
    cap = cv2.VideoCapture(video_path)
    
    info = {
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS),
        'codec': int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    
    cap.release()
    return info

def play_video(video_path: str, window_name: str = 'Video', 
               speed: float = 1.0, loop: bool = False) -> None:
    """
    Play a video with customizable options
    
    Args:
        video_path (str): Path to video file
        window_name (str): Window title
        speed (float): Playback speed multiplier
        loop (bool): Whether to loop the video
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / (fps * speed))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            if loop:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break
        
        cv2.imshow(window_name, frame)
        
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
        elif key == ord(' '):  # Space to pause
            cv2.waitKey(0)
    
    cap.release()
    cv2.destroyAllWindows()

def webcam_capture(camera_id: int = 0, save_path: Optional[str] = None) -> None:
    """
    Capture video from webcam
    
    Args:
        camera_id (int): Camera device ID
        save_path (str): Path to save recorded video
    """
    cap = cv2.VideoCapture(camera_id)
    
    if save_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 20.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
    
    print("Press 'q' to quit, 'r' to start/stop recording")
    recording = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Webcam', frame)
        
        if save_path and recording:
            out.write(frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and save_path:
            recording = not recording
            print(f"Recording: {'ON' if recording else 'OFF'}")
    
    cap.release()
    if save_path:
        out.release()
    cv2.destroyAllWindows()
