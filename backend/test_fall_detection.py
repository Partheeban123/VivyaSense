"""
Test script for fall detection service
"""
import cv2
import sys
from services.fall_detection_service import get_fall_detection_service

def test_fall_detection(video_path: str):
    """Test fall detection on a video"""
    print(f"Testing fall detection on: {video_path}")
    
    # Initialize service
    service = get_fall_detection_service()
    print("✅ Fall detection service initialized")
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video {video_path}")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {fps} fps, {total_frames} frames")
    
    frame_count = 0
    falls_detected = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        result = service.process_frame(frame, person_id=0)
        
        frame_count += 1
        
        # Log progress
        if frame_count % 30 == 0:
            print(f"Frame {frame_count}/{total_frames}: "
                  f"Persons={result['persons_detected']}, "
                  f"Falls={len(result['falls_detected'])}")
        
        # Track falls
        if result['falls_detected']:
            falls_detected.append({
                'frame': frame_count,
                'timestamp': frame_count / fps,
                'falls': result['falls_detected']
            })
            print(f"⚠️  FALL DETECTED at frame {frame_count} "
                  f"({frame_count/fps:.2f}s)")
    
    cap.release()
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total frames processed: {frame_count}")
    print(f"Total fall events: {len(falls_detected)}")
    
    if falls_detected:
        print("\nFall Events:")
        for i, event in enumerate(falls_detected, 1):
            print(f"  {i}. Frame {event['frame']} "
                  f"({event['timestamp']:.2f}s) - "
                  f"{len(event['falls'])} person(s)")
    else:
        print("\n✅ No falls detected")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_fall_detection.py <video_path>")
        sys.exit(1)
    
    test_fall_detection(sys.argv[1])

