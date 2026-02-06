"""
Screen Capture Module
Handles continuous screen capture at ~3 FPS with a rolling 1-minute buffer.
"""

import mss
import time
import threading
from collections import deque
from datetime import datetime
from typing import Optional, Callable
import numpy as np
from PIL import Image
import io


class ScreenCapture:
    """
    Captures screen content continuously and maintains a rolling buffer.
    """
    
    def __init__(self, fps: float = 3.0, buffer_duration: int = 60):
        """
        Initialize the screen capture system.
        
        Args:
            fps: Target frames per second for capture
            buffer_duration: Duration in seconds to keep in rolling buffer
        """
        self.fps = fps
        self.buffer_duration = buffer_duration
        self.frame_interval = 1.0 / fps
        
        # Rolling buffer: stores (timestamp, image_data) tuples
        max_frames = int(fps * buffer_duration)
        self.frame_buffer = deque(maxlen=max_frames)
        
        # Thread control
        self._running = False
        self._capture_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Callback for new frames
        self._frame_callback: Optional[Callable] = None
        
        # Screen capture instance
        self._sct = None
    
    def set_frame_callback(self, callback: Callable):
        """
        Set a callback function to be called when a new frame is captured.
        Callback receives (timestamp, pil_image) as arguments.
        """
        self._frame_callback = callback
    
    def start(self):
        """Start the continuous screen capture."""
        if self._running:
            return
        
        self._running = True
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._capture_thread.start()
        print("[ScreenCapture] Started capturing at {} FPS".format(self.fps))
    
    def stop(self):
        """Stop the screen capture."""
        self._running = False
        if self._capture_thread:
            self._capture_thread.join(timeout=2.0)
            self._capture_thread = None
        print("[ScreenCapture] Stopped capturing")
    
    def _capture_loop(self):
        """Main capture loop running in a separate thread."""
        with mss.mss() as sct:
            # Get primary monitor
            monitor = sct.monitors[1]  # Primary monitor (0 is all monitors combined)
            
            while self._running:
                start_time = time.time()
                
                try:
                    # Capture the screen
                    screenshot = sct.grab(monitor)
                    
                    # Convert to PIL Image
                    img = Image.frombytes(
                        'RGB',
                        (screenshot.width, screenshot.height),
                        screenshot.rgb
                    )
                    
                    # Resize for faster OCR processing (optional, can be adjusted)
                    # Keep aspect ratio, max dimension 1920
                    max_dim = 1920
                    if img.width > max_dim or img.height > max_dim:
                        ratio = min(max_dim / img.width, max_dim / img.height)
                        new_size = (int(img.width * ratio), int(img.height * ratio))
                        img = img.resize(new_size, Image.LANCZOS)
                    
                    timestamp = datetime.now()
                    
                    # Add to buffer
                    with self._lock:
                        self.frame_buffer.append((timestamp, img))
                    
                    # Call callback if set
                    if self._frame_callback:
                        try:
                            self._frame_callback(timestamp, img)
                        except Exception as e:
                            print(f"[ScreenCapture] Callback error: {e}")
                    
                except Exception as e:
                    print(f"[ScreenCapture] Capture error: {e}")
                
                # Maintain target FPS
                elapsed = time.time() - start_time
                sleep_time = max(0, self.frame_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
    
    def get_latest_frame(self) -> Optional[tuple]:
        """
        Get the most recent captured frame.
        
        Returns:
            Tuple of (timestamp, PIL.Image) or None if buffer is empty
        """
        with self._lock:
            if self.frame_buffer:
                return self.frame_buffer[-1]
            return None
    
    def get_frames_since(self, seconds: float) -> list:
        """
        Get all frames from the last N seconds.
        
        Args:
            seconds: Number of seconds to look back
            
        Returns:
            List of (timestamp, PIL.Image) tuples
        """
        cutoff = datetime.now().timestamp() - seconds
        
        with self._lock:
            return [
                (ts, img) for ts, img in self.frame_buffer
                if ts.timestamp() >= cutoff
            ]
    
    def get_buffer_stats(self) -> dict:
        """Get statistics about the current buffer."""
        with self._lock:
            if not self.frame_buffer:
                return {
                    'frame_count': 0,
                    'duration_seconds': 0,
                    'oldest_timestamp': None,
                    'newest_timestamp': None
                }
            
            oldest = self.frame_buffer[0][0]
            newest = self.frame_buffer[-1][0]
            
            return {
                'frame_count': len(self.frame_buffer),
                'duration_seconds': (newest - oldest).total_seconds(),
                'oldest_timestamp': oldest,
                'newest_timestamp': newest
            }


# Test function
if __name__ == "__main__":
    print("Testing Screen Capture Module...")
    
    capture = ScreenCapture(fps=3.0, buffer_duration=10)
    
    def on_frame(timestamp, image):
        print(f"Frame captured at {timestamp}, size: {image.size}")
    
    capture.set_frame_callback(on_frame)
    capture.start()
    
    # Run for 5 seconds
    time.sleep(5)
    
    stats = capture.get_buffer_stats()
    print(f"Buffer stats: {stats}")
    
    capture.stop()
    print("Test complete!")
