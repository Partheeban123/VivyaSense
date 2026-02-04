"""
Video Processing Service
"""
import cv2
import asyncio
from typing import Optional, Callable, Dict, Any, List
from pathlib import Path
import numpy as np
from datetime import datetime
from core.config import settings
from core.logger import log

# Import specialized detection services
from services.fall_detection_service import get_fall_detection_service
from services.fire_smoke_detection_service import get_fire_smoke_detection_service
from services.ppe_detection_service import get_ppe_detection_service

# Import threaded video capture for low-latency RTSP streaming
from services.threaded_video_capture import ThreadedVideoCapture


class VideoProcessor:
    """Process video streams and files"""
    
    def __init__(self):
        self.active_streams = {}
    
    async def process_video_file(
        self,
        video_path: str,
        detection_types: list,
        callback: Optional[Callable] = None,
        save_output: bool = True
    ) -> Dict[str, Any]:
        """
        Process a video file with AI detection
        
        Args:
            video_path: Path to video file
            detection_types: List of detection types to run
            callback: Callback function for each frame result
            save_output: Whether to save output video
        
        Returns:
            Processing results summary
        """
        if not Path(video_path).exists():
            log.error(f"Video file not found: {video_path}")
            return {"error": "Video file not found"}
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            log.error(f"Failed to open video: {video_path}")
            return {"error": "Failed to open video"}
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        log.info(f"Processing video: {video_path} ({width}x{height}, {fps} fps, {total_frames} frames)")
        
        # Setup output video writer if needed
        output_writer = None
        output_path = None
        if save_output:
            output_path = Path(settings.DETECTION_RESULTS_DIR) / f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Processing statistics
        stats = {
            'total_frames': total_frames,
            'processed_frames': 0,
            'detections': [],
            'detection_counts': {dt: 0 for dt in detection_types}
        }
        
        frame_count = 0
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                timestamp = frame_count / fps
                
                # Run detection on frame
                detections = detection_service.detect_multiple_types(
                    frame, detection_types
                )
                
                # Flatten detections and add timestamp
                all_detections = []
                for det_type, dets in detections.items():
                    for det in dets:
                        det['timestamp'] = timestamp
                        det['frame_number'] = frame_count
                        all_detections.append(det)
                        stats['detection_counts'][det_type] += 1
                
                stats['detections'].extend(all_detections)
                stats['processed_frames'] = frame_count
                
                # Draw detections on frame
                if all_detections:
                    frame = detection_service.draw_detections(frame, all_detections)
                
                # Save frame to output video
                if output_writer:
                    output_writer.write(frame)
                
                # Call callback if provided
                if callback:
                    await callback({
                        'frame_number': frame_count,
                        'timestamp': timestamp,
                        'detections': all_detections,
                        'progress': (frame_count / total_frames) * 100
                    })
                
                # Allow other tasks to run
                if frame_count % 10 == 0:
                    await asyncio.sleep(0)
        
        except Exception as e:
            log.error(f"Error processing video: {e}")
            stats['error'] = str(e)
        
        finally:
            cap.release()
            if output_writer:
                output_writer.release()
        
        stats['output_path'] = str(output_path) if output_path else None
        log.info(f"Video processing complete: {frame_count} frames processed")
        
        return stats
    
    async def process_rtsp_stream(
        self,
        stream_url: str,
        detection_types: List[str],
        callback: Callable,
        stream_id: str,
        confidence: float = 0.5
    ):
        """
        Process RTSP stream in real-time with AI detection

        Args:
            stream_url: RTSP stream URL
            detection_types: List of detection types ('fall', 'fire', 'smoke', 'ppe')
            callback: Callback for each frame
            stream_id: Unique stream identifier
            confidence: Confidence threshold for detections
        """
        # Use threaded video capture for minimal latency
        cap = ThreadedVideoCapture(stream_url, name=stream_id)

        # Wait a moment for the thread to grab the first frame
        await asyncio.sleep(0.5)

        if not cap.isOpened():
            log.error(f"Failed to open RTSP stream: {stream_url}")
            await callback({
                'type': 'error',
                'message': 'Failed to open RTSP stream'
            })
            cap.release()
            return

        self.active_streams[stream_id] = True
        log.info(f"Started processing RTSP stream: {stream_id} with detections: {detection_types}")
        log.info(f"Using threaded video capture for minimal latency")

        # Initialize detection services based on requested types
        fall_service = None
        fire_smoke_service = None
        ppe_service = None

        if 'fall' in detection_types:
            fall_service = get_fall_detection_service()
            log.info(f"Fall detection enabled for stream {stream_id}")

        if 'fire' in detection_types or 'smoke' in detection_types:
            fire_smoke_service = get_fire_smoke_detection_service()
            log.info(f"Fire/Smoke detection enabled for stream {stream_id}")

        if 'ppe' in detection_types:
            ppe_service = get_ppe_detection_service()
            log.info(f"PPE detection enabled for stream {stream_id}")

        # Performance optimization settings
        frame_count = 0
        target_width = 640  # Reduce resolution for faster processing

        # All detection types now process EVERY frame for maximum accuracy
        # PPE: EVERY frame (accurate real-time detection)
        # Fall: EVERY frame (needs continuous sequence for GRU model)
        # Fire/Smoke: EVERY frame (accurate real-time fire/smoke detection)
        ppe_frequency = 1  # Every frame - accurate real-time detection
        fall_frequency = 1  # Every frame - fall detection needs continuous frames
        fire_smoke_frequency = 1  # Every frame - accurate real-time fire/smoke detection

        # FPS calculation
        import time
        fps_start_time = time.time()
        fps_frame_count = 0
        current_fps = 0

        # No caching needed - all detections process every frame

        try:
            while self.active_streams.get(stream_id, False):
                ret, frame = cap.read()
                if not ret:
                    log.warning(f"Failed to read frame from stream: {stream_id}")
                    await asyncio.sleep(1)
                    continue

                frame_count += 1

                # Calculate FPS
                fps_frame_count += 1
                if fps_frame_count >= 30:  # Update FPS every 30 frames
                    elapsed = time.time() - fps_start_time
                    current_fps = fps_frame_count / elapsed
                    fps_start_time = time.time()
                    fps_frame_count = 0

                # Resize frame for faster processing
                original_frame = frame.copy()
                height, width = frame.shape[:2]
                if width > target_width:
                    scale = target_width / width
                    new_height = int(height * scale)
                    frame = cv2.resize(frame, (target_width, new_height))

                annotated_frame = frame.copy()
                all_detections = []

                # Run Fall Detection (EVERY frame - needs continuous keypoint sequence)
                if fall_service:
                    try:
                        fall_result = fall_service.process_frame(frame)

                        # Draw pose keypoints
                        if 'yolo_results' in fall_result and fall_result['yolo_results'] is not None:
                            annotated_frame = fall_result['yolo_results'].plot(
                                img=annotated_frame,
                                boxes=True,
                                kpt_radius=3,
                                line_width=1
                            )

                        # Add fall detections
                        if fall_result.get('falls_detected'):
                            for fall in fall_result['falls_detected']:
                                all_detections.append({
                                    'type': 'fall',
                                    'probability': fall['probability'],
                                    'person_idx': fall['person_idx'],
                                    'alert': True
                                })

                                # Draw fall alert
                                cv2.putText(
                                    annotated_frame,
                                    "FALL DETECTED!",
                                    (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.5,
                                    (0, 0, 255),
                                    3
                                )
                    except Exception as e:
                        log.error(f"Fall detection error: {e}")

                # Run Fire/Smoke Detection (EVERY frame - no caching needed)
                if fire_smoke_service:
                    try:
                        # Use detect_fire_and_smoke method for combined detection
                        fire_smoke_result = fire_smoke_service.detect_fire_and_smoke(
                            frame,
                            confidence=confidence
                        )

                        # Draw fire/smoke detections
                        if fire_smoke_result['fire'] or fire_smoke_result['smoke']:
                            annotated_frame = fire_smoke_service.draw_detections(
                                annotated_frame,
                                fire_smoke_result
                            )

                            # Add to detections list
                            for fire_det in fire_smoke_result['fire']:
                                all_detections.append({
                                    'type': 'fire',
                                    'confidence': fire_det['confidence'],
                                    'bbox': fire_det['bbox'],
                                    'alert': True
                                })

                            for smoke_det in fire_smoke_result['smoke']:
                                all_detections.append({
                                    'type': 'smoke',
                                    'confidence': smoke_det['confidence'],
                                    'bbox': smoke_det['bbox'],
                                    'alert': True
                                })
                    except Exception as e:
                        log.error(f"Fire/Smoke detection error: {e}")

                # Run PPE Detection (EVERY frame - no caching needed)
                if ppe_service:
                    try:
                        # Use detect_ppe method
                        ppe_result = ppe_service.detect_ppe(
                            frame,
                            confidence=confidence
                        )

                        # Draw PPE detections
                        if ppe_result['detections']:
                            annotated_frame = ppe_service.draw_detections(
                                annotated_frame,
                                ppe_result
                            )

                            # Add to detections list
                            for ppe_det in ppe_result['detections']:
                                all_detections.append({
                                    'type': 'ppe',
                                    'class': ppe_det['class_name'],  # Fixed: use 'class_name' not 'class'
                                    'confidence': ppe_det['confidence'],
                                    'bbox': ppe_det['bbox']
                                })
                    except Exception as e:
                        log.error(f"PPE detection error: {e}")

                # Resize annotated frame back to original size for display
                if width > target_width:
                    annotated_frame = cv2.resize(annotated_frame, (width, height))

                # Send frame to callback with FPS info
                await callback({
                    'type': 'frame',
                    'stream_id': stream_id,
                    'frame_number': frame_count,
                    'frame': annotated_frame,
                    'detections': all_detections,
                    'has_alerts': any(d.get('alert', False) for d in all_detections),
                    'fps': round(current_fps, 1)
                })

                # Small delay to prevent overwhelming the WebSocket
                await asyncio.sleep(0.01)

        except Exception as e:
            log.error(f"Error processing RTSP stream {stream_id}: {e}")
            await callback({
                'type': 'error',
                'message': str(e)
            })

        finally:
            cap.release()
            if stream_id in self.active_streams:
                del self.active_streams[stream_id]
            log.info(f"Stopped processing RTSP stream: {stream_id}")
    
    def stop_stream(self, stream_id: str):
        """Stop processing a stream"""
        if stream_id in self.active_streams:
            self.active_streams[stream_id] = False
            log.info(f"Stopping stream: {stream_id}")


# Global video processor instance
video_processor = VideoProcessor()

