"""
Threaded Video Capture for RTSP Streams

Provides minimal latency video capture by continuously grabbing frames
in a separate thread, ensuring the main thread always gets the most
recent frame without buffering delay.
"""
import cv2
import threading
from typing import Optional, Tuple
from core.logger import log


class ThreadedVideoCapture:
    """
    Threaded video capture for RTSP streams with minimal latency.
    
    Uses a separate thread to continuously grab frames, ensuring
    the main thread always gets the most recent frame without buffering delay.
    """
    
    def __init__(self, source: str, name: str = "VideoCapture"):
        """
        Initialize threaded video capture.
        
        Args:
            source: Video source (RTSP URL, file path, or camera index)
            name: Name for logging purposes
        """
        self.source = source
        self.name = name
        self.cap = cv2.VideoCapture(source)
        
        # Configure for low latency
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer
        
        # For RTSP streams, use TCP for reliability or UDP for speed
        if source.startswith('rtsp://'):
            # Try UDP first for lower latency
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
        
        self.frame = None
        self.ret = False
        self.stopped = False
        self.lock = threading.Lock()
        
        # Start the thread
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        
        log.info(f"ThreadedVideoCapture '{self.name}' started for source: {source}")
    
    def _update(self):
        """
        Continuously grab frames in a separate thread.
        
        This method runs in a background thread and continuously grabs
        the latest frame, discarding old frames to minimize latency.
        """
        while not self.stopped:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                
                with self.lock:
                    self.ret = ret
                    if ret:
                        self.frame = frame
            else:
                # Try to reconnect if connection is lost
                log.warning(f"ThreadedVideoCapture '{self.name}' connection lost, attempting to reconnect...")
                self.cap.release()
                self.cap = cv2.VideoCapture(self.source)
                
                # Reconfigure for low latency
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                if self.source.startswith('rtsp://'):
                    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
    
    def read(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """
        Read the most recent frame.
        
        Returns:
            Tuple of (success, frame) where success is True if frame was read successfully
        """
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None
    
    def isOpened(self) -> bool:
        """
        Check if video capture is opened.
        
        Returns:
            True if capture is opened and has received at least one frame
        """
        return self.cap.isOpened() and self.frame is not None
    
    def get(self, prop_id: int):
        """
        Get video capture property.
        
        Args:
            prop_id: Property identifier (cv2.CAP_PROP_*)
            
        Returns:
            Property value
        """
        return self.cap.get(prop_id)
    
    def set(self, prop_id: int, value) -> bool:
        """
        Set video capture property.
        
        Args:
            prop_id: Property identifier (cv2.CAP_PROP_*)
            value: Property value
            
        Returns:
            True if property was set successfully
        """
        return self.cap.set(prop_id, value)
    
    def release(self):
        """
        Release video capture and stop the thread.
        """
        self.stopped = True
        
        # Wait for thread to finish
        if self.thread.is_alive():
            self.thread.join(timeout=2.0)
        
        # Release the capture
        if self.cap.isOpened():
            self.cap.release()
        
        log.info(f"ThreadedVideoCapture '{self.name}' released")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.release()

