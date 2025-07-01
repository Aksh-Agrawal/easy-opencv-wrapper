"""
Video Operations Module
Provides easy-to-use classes and functions for video processing with webcam support
"""

import cv2
import numpy as np
import os
from typing import Optional, List, Tuple, Union, Dict, Any


class VideoLoader:
    """Class for loading videos from files or webcam sources"""
    
    def __init__(self, default_api_preference: int = cv2.CAP_ANY):
        """
        Initialize VideoLoader
        
        Args:
            default_api_preference: Default API preference backend
        """
        self.default_api_preference = default_api_preference
    
    def load(self, path: Union[str, int], api_preference: Optional[int] = None) -> cv2.VideoCapture:
        """
        Load a video from file or webcam
        
        Args:
            path: Path to video file or webcam index (0, 1, etc.)
            api_preference: Backend API preference
            
        Returns:
            VideoCapture object
            
        Raises:
            ValueError: If video source cannot be opened
        """
        api_preference = api_preference or self.default_api_preference
        cap = cv2.VideoCapture(path, api_preference)
        
        if not cap.isOpened():
            source_type = "webcam" if isinstance(path, int) else "file"
            raise ValueError(f"Could not open video {source_type} at {path}")
        
        return cap
    
    def release(self, video: cv2.VideoCapture) -> None:
        """
        Release video resources
        
        Args:
            video: VideoCapture object to release
        """
        if video and video.isOpened():
            video.release()


class VideoSaver:
    """Class for saving videos with customizable parameters"""
    
    def __init__(self, default_codec: str = 'mp4v', default_fps: float = 30.0):
        """
        Initialize VideoSaver
        
        Args:
            default_codec: Default video codec
            default_fps: Default frames per second
        """
        self.default_codec = default_codec
        self.default_fps = default_fps
    
    def save(self, frames: List[np.ndarray], output_path: str,
             fps: Optional[float] = None, codec: Optional[str] = None) -> bool:
        """
        Save frames as a video file
        
        Args:
            frames: List of frames
            output_path: Output video path
            fps: Frames per second
            codec: Video codec
        
        Returns:
            Success status
        """
        if not frames:
            return False
        
        fps = fps or self.default_fps
        codec = codec or self.default_codec
        
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        return True
    
    def create_from_frame_paths(self, frame_paths: List[str], output_path: str,
                               fps: Optional[float] = None, codec: Optional[str] = None) -> bool:
        """
        Create a video from a list of frame image paths
        
        Args:
            frame_paths: List of frame image paths
            output_path: Output video path
            fps: Frames per second
            codec: Video codec
        
        Returns:
            Success status
        """
        if not frame_paths:
            return False
            
        fps = fps or self.default_fps
        codec = codec or self.default_codec
        
        # Read first frame to get dimensions
        first_frame = cv2.imread(frame_paths[0])
        if first_frame is None:
            return False
            
        height, width = first_frame.shape[:2]
        
        fourcc = cv2.VideoWriter_fourcc(*codec)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for frame_path in frame_paths:
            frame = cv2.imread(frame_path)
            if frame is not None:
                out.write(frame)
        
        out.release()
        return True


class FrameExtractor:
    """Class for extracting frames from videos"""
    
    def __init__(self, default_output_format: str = 'jpg', default_quality: int = 95):
        """
        Initialize FrameExtractor
        
        Args:
            default_output_format: Default image format for extracted frames
            default_quality: Default image quality (0-100)
        """
        self.default_output_format = default_output_format
        self.default_quality = default_quality
        self.video_loader = VideoLoader()
    
    def extract(self, video_path: Union[str, int], output_dir: str = '.', 
                frame_interval: int = 1, max_frames: Optional[int] = None,
                output_format: Optional[str] = None, quality: Optional[int] = None) -> List[str]:
        """
        Extract frames from a video
        
        Args:
            video_path: Input video path or webcam index
            output_dir: Directory to save frames
            frame_interval: Extract every nth frame
            max_frames: Maximum number of frames to extract
            output_format: Image format (jpg, png, etc)
            quality: Image quality (0-100)
        
        Returns:
            List of saved frame paths
        """
        output_format = output_format or self.default_output_format
        quality = quality or self.default_quality
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        cap = self.video_loader.load(video_path)
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
                
                frame_path = f"{output_dir}/frame_{saved_count:06d}.{output_format}"
                
                # Save with quality parameter if jpg/jpeg
                if output_format.lower() in ('jpg', 'jpeg'):
                    cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
                elif output_format.lower() == 'png':
                    compression = max(0, min(9, int(9 * (100 - quality) / 100)))
                    cv2.imwrite(frame_path, frame, [cv2.IMWRITE_PNG_COMPRESSION, compression])
                else:
                    cv2.imwrite(frame_path, frame)
                
                frame_paths.append(frame_path)
                saved_count += 1
            
            frame_count += 1
        
        self.video_loader.release(cap)
        return frame_paths


class VideoAnalyzer:
    """Class for analyzing video properties and metadata"""
    
    def __init__(self):
        """Initialize VideoAnalyzer"""
        self.video_loader = VideoLoader()
    
    def get_info(self, video_path: Union[str, int]) -> Dict[str, Any]:
        """
        Get comprehensive information about a video
        
        Args:
            video_path: Path to video file or webcam index
        
        Returns:
            Dictionary with video information
        """
        cap = self.video_loader.load(video_path)
        
        # Get basic properties
        info = {
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'codec': int(cap.get(cv2.CAP_PROP_FOURCC)),
            'is_webcam': isinstance(video_path, int)
        }
        
        # Calculate duration (not applicable for webcams)
        if not info['is_webcam'] and info['frame_count'] > 0 and info['fps'] > 0:
            info['duration_sec'] = info['frame_count'] / info['fps']
            mins, secs = divmod(info['duration_sec'], 60)
            hours, mins = divmod(mins, 60)
            info['duration_formatted'] = f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
        
        # Get codec as four-character code
        codec_int = info['codec']
        info['codec_fourcc'] = ''.join([chr((codec_int >> 8 * i) & 0xFF) for i in range(4)])
        
        # Read first frame to get more information
        ret, first_frame = cap.read()
        if ret:
            info['channels'] = 1 if len(first_frame.shape) == 2 else first_frame.shape[2]
            info['is_color'] = info['channels'] == 3
            
            # Calculate average brightness of first frame
            if info['is_color']:
                gray_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
            else:
                gray_frame = first_frame
            info['first_frame_avg_brightness'] = float(np.mean(gray_frame))
        
        self.video_loader.release(cap)
        return info
    
    def analyze_motion(self, video_path: Union[str, int], sample_size: int = 50) -> Dict[str, Any]:
        """
        Analyze motion in a video
        
        Args:
            video_path: Path to video file or webcam index
            sample_size: Number of frames to sample for analysis
        
        Returns:
            Dictionary with motion analysis metrics
        """
        cap = self.video_loader.load(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # For webcam or unknown frame count, use sampling
        if frame_count <= 0:
            frame_count = 1000  # arbitrary large number
        
        # Calculate sampling interval
        interval = max(1, frame_count // sample_size)
        
        # Initialize variables
        prev_frame = None
        diffs = []
        frames_analyzed = 0
        
        # Process frames
        for i in range(0, frame_count, interval):
            if isinstance(video_path, int):  # For webcam, we can't seek
                ret, frame = cap.read()
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
            
            if not ret:
                break
                
            # Convert to grayscale for motion analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate absolute difference between frames
                diff = cv2.absdiff(gray, prev_frame)
                avg_diff = np.mean(diff)
                diffs.append(avg_diff)
            
            prev_frame = gray
            frames_analyzed += 1
            
            # For webcam, limit number of frames to analyze
            if isinstance(video_path, int) and frames_analyzed >= sample_size:
                break
        
        self.video_loader.release(cap)
        
        # Calculate motion metrics
        result = {
            'frames_analyzed': frames_analyzed,
            'avg_motion': 0,
            'max_motion': 0,
            'min_motion': 0,
            'motion_variability': 0,
            'has_significant_motion': False
        }
        
        if diffs:
            result['avg_motion'] = float(np.mean(diffs))
            result['max_motion'] = float(np.max(diffs))
            result['min_motion'] = float(np.min(diffs))
            result['motion_variability'] = float(np.std(diffs))
            result['has_significant_motion'] = result['avg_motion'] > 10.0
        
        return result


class VideoPlayer:
    """Class for playing videos with customizable playback controls"""
    
    def __init__(self, default_speed: float = 1.0, default_loop: bool = False):
        """
        Initialize VideoPlayer
        
        Args:
            default_speed: Default playback speed multiplier
            default_loop: Whether to loop the video by default
        """
        self.default_speed = default_speed
        self.default_loop = default_loop
        self.video_loader = VideoLoader()
    
    def play(self, video_path: Union[str, int], window_name: str = 'Video', 
             speed: Optional[float] = None, loop: Optional[bool] = None,
             start_frame: int = 0, end_frame: Optional[int] = None) -> None:
        """
        Play a video with customizable options
        
        Args:
            video_path: Path to video file or webcam index
            window_name: Window title
            speed: Playback speed multiplier
            loop: Whether to loop the video
            start_frame: Starting frame index
            end_frame: Ending frame index
        """
        speed = speed or self.default_speed
        loop = loop if loop is not None else self.default_loop
        
        cap = self.video_loader.load(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / (fps * speed)) if fps > 0 else 30
        
        # Initialize controls
        playing = True
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = start_frame
        
        # For webcams, ignore frame indices
        is_webcam = isinstance(video_path, int)
        if is_webcam:
            start_frame = 0
            end_frame = None
        else:
            # Set to start frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Set end frame if not provided
        if end_frame is None and frame_count > 0:
            end_frame = frame_count - 1
            
        print("Video Player Controls:")
        print("  Space - Play/Pause")
        print("  → - Forward 10 frames")
        print("  ← - Backward 10 frames")
        print("  + - Increase speed")
        print("  - - Decrease speed")
        print("  r - Restart video")
        print("  l - Toggle loop")
        print("  q or ESC - Quit")
        
        while True:
            if playing or is_webcam:
                ret, frame = cap.read()
                current_frame += 1
                
                if not ret or (end_frame is not None and current_frame > end_frame):
                    if loop and not is_webcam:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                        current_frame = start_frame
                        continue
                    else:
                        break
                        
                # Display frame
                cv2.imshow(window_name, frame)
                
                # Display progress bar for non-webcam videos
                if not is_webcam and frame_count > 0:
                    progress = int((current_frame - start_frame) * 100 / (end_frame - start_frame + 1))
                    progress_bar = f"[{'█' * (progress // 5)}{' ' * (20 - progress // 5)}] {progress}%"
                    print(f"\rPlaying: {progress_bar} (Speed: {speed:.1f}x, Frame: {current_frame})", end='')
            
            # Handle key events
            key = cv2.waitKey(0 if not playing else delay) & 0xFF
            
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord(' '):  # Space to pause/play
                playing = not playing
            elif key == ord('+') or key == ord('='):  # Increase speed
                speed = min(10.0, speed + 0.1)
                delay = int(1000 / (fps * speed)) if fps > 0 else 30
            elif key == ord('-'):  # Decrease speed
                speed = max(0.1, speed - 0.1)
                delay = int(1000 / (fps * speed)) if fps > 0 else 30
            elif key == ord('r'):  # Restart
                if not is_webcam:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                    current_frame = start_frame
            elif key == ord('l'):  # Toggle loop
                loop = not loop
            elif key == 83:  # Right arrow - forward 10 frames
                if not is_webcam:
                    current_frame = min(end_frame or frame_count - 1, current_frame + 10)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            elif key == 81:  # Left arrow - backward 10 frames
                if not is_webcam:
                    current_frame = max(start_frame, current_frame - 10)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        
        self.video_loader.release(cap)
        cv2.destroyWindow(window_name)
        
        # Clear progress bar line
        if not is_webcam:
            print()


class WebcamCapture:
    """Class for capturing video from webcam with recording capability"""
    
    def __init__(self, default_codec: str = 'mp4v', default_fps: float = 20.0):
        """
        Initialize WebcamCapture
        
        Args:
            default_codec: Default video codec for recording
            default_fps: Default frames per second for recording
        """
        self.default_codec = default_codec
        self.default_fps = default_fps
        self.video_loader = VideoLoader()
    
    def capture(self, camera_id: int = 0, save_path: Optional[str] = None,
                fps: Optional[float] = None, codec: Optional[str] = None,
                width: Optional[int] = None, height: Optional[int] = None) -> None:
        """
        Capture video from webcam with optional recording
        
        Args:
            camera_id: Camera device ID
            save_path: Path to save recorded video (None for no recording)
            fps: Frames per second for recording
            codec: Video codec for recording
            width: Force webcam width resolution
            height: Force webcam height resolution
        """
        fps = fps or self.default_fps
        codec = codec or self.default_codec
        
        cap = self.video_loader.load(camera_id)
        
        # Set custom resolution if specified
        if width and height:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Get actual dimensions (may differ from requested)
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize video writer if saving
        out = None
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(save_path, fourcc, fps, (actual_width, actual_height))
        
        print("Webcam Capture Controls:")
        print("  r - Start/Stop recording")
        print("  s - Take screenshot")
        print("  q or ESC - Quit")
        
        recording = False
        frame_count = 0
        screenshot_count = 0
        start_time = cv2.getTickCount()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Calculate actual FPS
            if frame_count % 10 == 0:
                current_time = cv2.getTickCount()
                elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
                actual_fps = frame_count / elapsed_time
            
            # Add status text
            status_text = f"Resolution: {actual_width}x{actual_height}"
            if frame_count % 10 == 0:
                status_text += f", FPS: {actual_fps:.1f}"
            if recording:
                status_text += ", RECORDING"
                
                # Add red recording indicator
                cv2.circle(frame, (20, 20), 10, (0, 0, 255), -1)
            
            cv2.putText(frame, status_text, (10, actual_height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display frame
            cv2.imshow('Webcam Capture', frame)
            
            # Save frame if recording
            if recording and out:
                out.write(frame)
            
            # Handle key events
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord('r') and save_path:  # Toggle recording
                recording = not recording
                print(f"Recording: {'ON' if recording else 'OFF'}")
            elif key == ord('s'):  # Take screenshot
                screenshot_path = f"webcam_screenshot_{screenshot_count:03d}.jpg"
                cv2.imwrite(screenshot_path, frame)
                print(f"Screenshot saved to {screenshot_path}")
                screenshot_count += 1
        
        # Clean up
        self.video_loader.release(cap)
        if out:
            out.release()
        cv2.destroyAllWindows()
    
    def multi_camera_capture(self, camera_ids: List[int], save_paths: Optional[List[str]] = None) -> None:
        """
        Capture video from multiple webcams simultaneously
        
        Args:
            camera_ids: List of camera device IDs
            save_paths: Optional list of paths to save recorded videos (None for no recording)
        """
        if save_paths and len(camera_ids) != len(save_paths):
            raise ValueError("If save_paths is provided, it must have the same length as camera_ids")
        
        # Initialize camera captures
        caps = []
        outs = []
        
        try:
            for i, camera_id in enumerate(camera_ids):
                cap = self.video_loader.load(camera_id)
                caps.append(cap)
                
                # Initialize video writer if saving
                if save_paths:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fourcc = cv2.VideoWriter_fourcc(*self.default_codec)
                    out = cv2.VideoWriter(save_paths[i], fourcc, self.default_fps, (width, height))
                    outs.append(out)
                else:
                    outs.append(None)
            
            print("Multi-Camera Capture Controls:")
            print("  q or ESC - Quit")
            
            while True:
                frames = []
                
                # Capture frames from all cameras
                for i, cap in enumerate(caps):
                    ret, frame = cap.read()
                    if not ret:
                        continue
                    
                    # Add camera ID label
                    cv2.putText(frame, f"Camera {camera_ids[i]}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    frames.append(frame)
                    
                    # Save frame if recording
                    if outs[i]:
                        outs[i].write(frame)
                    
                    # Display individual camera
                    cv2.imshow(f"Camera {camera_ids[i]}", frame)
                
                # Handle key events
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    break
        
        finally:
            # Clean up
            for cap in caps:
                self.video_loader.release(cap)
            
            for out in outs:
                if out:
                    out.release()
            
            cv2.destroyAllWindows()


# Legacy function wrappers for backward compatibility
def load_video(path: str) -> cv2.VideoCapture:
    """
    Load a video file (Legacy function)
    
    Args:
        path (str): Path to video file
    
    Returns:
        cv2.VideoCapture: Video capture object
    """
    loader = VideoLoader()
    return loader.load(path)


def save_video(frames: List[np.ndarray], output_path: str, fps: float = 30.0,
               codec: str = 'mp4v') -> bool:
    """
    Save frames as a video file (Legacy function)
    
    Args:
        frames (List[np.ndarray]): List of frames
        output_path (str): Output video path
        fps (float): Frames per second
        codec (str): Video codec
    
    Returns:
        bool: Success status
    """
    saver = VideoSaver(default_codec=codec, default_fps=fps)
    return saver.save(frames, output_path)


def extract_frames(video_path: str, output_dir: str = '.', 
                  frame_interval: int = 1, max_frames: Optional[int] = None) -> List[str]:
    """
    Extract frames from a video (Legacy function)
    
    Args:
        video_path (str): Input video path
        output_dir (str): Directory to save frames
        frame_interval (int): Extract every nth frame
        max_frames (int): Maximum number of frames to extract
    
    Returns:
        List[str]: List of saved frame paths
    """
    extractor = FrameExtractor()
    return extractor.extract(video_path, output_dir, frame_interval, max_frames)


def create_video_from_frames(frame_paths: List[str], output_path: str, 
                           fps: float = 30.0, codec: str = 'mp4v') -> bool:
    """
    Create a video from a list of frame images (Legacy function)
    
    Args:
        frame_paths (List[str]): List of frame image paths
        output_path (str): Output video path
        fps (float): Frames per second
        codec (str): Video codec
    
    Returns:
        bool: Success status
    """
    saver = VideoSaver(default_codec=codec, default_fps=fps)
    return saver.create_from_frame_paths(frame_paths, output_path)


def get_video_info(video_path: str) -> dict:
    """
    Get comprehensive information about a video (Legacy function)
    
    Args:
        video_path (str): Path to video file
    
    Returns:
        dict: Video information
    """
    analyzer = VideoAnalyzer()
    return analyzer.get_info(video_path)


def play_video(video_path: str, window_name: str = 'Video', 
               speed: float = 1.0, loop: bool = False) -> None:
    """
    Play a video with customizable options (Legacy function)
    
    Args:
        video_path (str): Path to video file
        window_name (str): Window title
        speed (float): Playback speed multiplier
        loop (bool): Whether to loop the video
    """
    player = VideoPlayer(default_speed=speed, default_loop=loop)
    player.play(video_path, window_name)


def webcam_capture(camera_id: int = 0, save_path: Optional[str] = None) -> None:
    """
    Capture video from webcam (Legacy function)
    
    Args:
        camera_id (int): Camera device ID
        save_path (str): Path to save recorded video
    """
    capture = WebcamCapture()
    capture.capture(camera_id, save_path)

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
