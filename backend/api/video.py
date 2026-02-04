"""
Video processing API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path
import uuid
import shutil

from core.config import settings
from core.logger import log
from services.video_service import video_processor
from services.fall_detection_service import get_fall_detection_service

router = APIRouter()


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    detection_types: str = Form(...),
    confidence: Optional[float] = Form(None),
    background_tasks: BackgroundTasks = None
):
    """
    Upload and process a video file
    
    Args:
        file: Video file
        detection_types: Comma-separated detection types
        confidence: Confidence threshold
        background_tasks: Background task handler
    
    Returns:
        Processing job information
    """
    try:
        # Validate file
        file_ext = Path(file.filename).suffix.lower().replace('.', '')
        if file_ext not in settings.SUPPORTED_VIDEO_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported video format. Supported: {settings.SUPPORTED_VIDEO_FORMATS}"
            )
        
        # Save uploaded file
        job_id = uuid.uuid4().hex
        upload_path = Path(settings.UPLOAD_DIR) / f"{job_id}_{file.filename}"
        
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        log.info(f"Video uploaded: {upload_path}")
        
        # Parse detection types
        det_types = [dt.strip() for dt in detection_types.split(',')]
        
        # Process video in background
        async def process_callback(result):
            """Callback for processing progress"""
            # Here you can emit progress via WebSocket or save to database
            log.info(f"Processing progress: {result.get('progress', 0):.1f}%")
        
        # Start processing
        background_tasks.add_task(
            video_processor.process_video_file,
            str(upload_path),
            det_types,
            process_callback,
            True
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "message": "Video processing started",
            "status": "processing"
        }
    
    except Exception as e:
        log.error(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}")
async def get_processing_status(job_id: str):
    """Get video processing status"""
    # In production, this would query a database or cache
    # For now, return a placeholder
    return {
        "job_id": job_id,
        "status": "processing",
        "progress": 50,
        "message": "Processing video..."
    }


@router.get("/result/{job_id}")
async def get_processing_result(job_id: str):
    """Get video processing results"""
    # In production, query database for results
    return {
        "job_id": job_id,
        "status": "completed",
        "detections": [],
        "output_video_url": f"/results/output_{job_id}.mp4"
    }


@router.get("/download/{filename}")
async def download_result(filename: str):
    """Download processed video"""
    file_path = Path(settings.DETECTION_RESULTS_DIR) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=str(file_path),
        media_type="video/mp4",
        filename=filename
    )


@router.post("/fall-detection/upload")
async def upload_video_fall_detection(
    file: UploadFile = File(...),
    show_pose: bool = Form(True),
    fall_threshold: Optional[float] = Form(None),
    background_tasks: BackgroundTasks = None
):
    """
    Upload and process video for fall detection using YOLOv11-pose + GRU

    Args:
        file: Video file
        show_pose: Whether to show pose keypoints
        fall_threshold: Fall detection threshold (default: 0.95)
        background_tasks: Background task handler

    Returns:
        Processing job information
    """
    try:
        # Validate file
        file_ext = Path(file.filename).suffix.lower().replace('.', '')
        if file_ext not in settings.SUPPORTED_VIDEO_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported video format. Supported: {settings.SUPPORTED_VIDEO_FORMATS}"
            )

        # Save uploaded file
        job_id = uuid.uuid4().hex
        upload_path = Path(settings.UPLOAD_DIR) / f"fall_{job_id}_{file.filename}"

        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        log.info(f"Video uploaded for fall detection: {upload_path}")

        # Process video with fall detection
        async def process_fall_detection():
            """Process video for fall detection"""
            import cv2

            try:
                fall_service = get_fall_detection_service()
                cap = cv2.VideoCapture(str(upload_path))

                # Get video properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # Setup output video
                output_path = Path(settings.DETECTION_RESULTS_DIR) / f"fall_output_{job_id}.mp4"
                output_path.parent.mkdir(parents=True, exist_ok=True)

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

                frame_count = 0
                falls_detected = []

                log.info(f"Processing fall detection: {width}x{height}, {fps} fps, {total_frames} frames")

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Process frame
                    result = fall_service.process_frame(frame, person_id=0)

                    # Draw detections
                    annotated_frame = fall_service.draw_detections(
                        result['frame'],
                        result,
                        show_pose=show_pose,
                        show_fall_info=True
                    )

                    # Write frame
                    out.write(annotated_frame)

                    # Track falls
                    if result['falls_detected']:
                        falls_detected.append({
                            'frame': frame_count,
                            'timestamp': frame_count / fps,
                            'falls': result['falls_detected']
                        })

                    frame_count += 1

                    if frame_count % 30 == 0:
                        progress = (frame_count / total_frames) * 100
                        log.info(f"Fall detection progress: {progress:.1f}%")

                cap.release()
                out.release()

                log.info(f"Fall detection complete: {len(falls_detected)} fall events detected")

                return {
                    'success': True,
                    'output_path': str(output_path),
                    'falls_detected': len(falls_detected),
                    'fall_events': falls_detected
                }

            except Exception as e:
                log.error(f"Fall detection processing error: {e}")
                return {'success': False, 'error': str(e)}

        # Start processing in background
        background_tasks.add_task(process_fall_detection)

        return {
            "success": True,
            "job_id": job_id,
            "message": "Fall detection processing started",
            "status": "processing",
            "output_url": f"/api/video/download/fall_output_{job_id}.mp4"
        }

    except Exception as e:
        log.error(f"Fall detection upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

