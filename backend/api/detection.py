"""
Detection API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from typing import List, Optional, Dict, Any
import cv2
import numpy as np
from pathlib import Path
import uuid
from datetime import datetime

from core.config import settings
from core.logger import log
from services.detection_service import detection_service
from services.fall_detection_service import get_fall_detection_service
from services.fire_smoke_detection_service import get_fire_smoke_detection_service
from services.ppe_detection_service import get_ppe_detection_service

router = APIRouter()


def detect_fall_pose_in_image(image: np.ndarray, confidence: float = 0.5) -> Dict[str, Any]:
    """
    Detect poses in a single image using YOLOv11-pose
    Note: Cannot do temporal fall detection (requires video), only pose detection

    Args:
        image: Input image
        confidence: Confidence threshold

    Returns:
        Detection results with pose keypoints
    """
    try:
        fall_service = get_fall_detection_service()

        # Detect poses
        results = fall_service.yolo_model(image, conf=confidence, verbose=False)[0]

        detections = []

        if results.keypoints is not None and results.keypoints.data.shape[0] > 0:
            num_persons = results.keypoints.data.shape[0]

            for person_idx in range(num_persons):
                # Get bounding box
                if results.boxes is not None and len(results.boxes) > person_idx:
                    box = results.boxes[person_idx]
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy().item()

                    # Get keypoints
                    keypoints_data = results.keypoints.data[person_idx].cpu().numpy()

                    # Calculate simple fall heuristic based on pose
                    # (person is more horizontal than vertical)
                    bbox_width = float(x2 - x1)
                    bbox_height = float(y2 - y1)
                    aspect_ratio = bbox_width / (bbox_height + 1e-6)

                    # Simple heuristic: if width > height, might be fallen
                    is_potential_fall = bool(aspect_ratio > 1.2)

                    detections.append({
                        "class": "person_with_pose",
                        "confidence": float(conf),
                        "bbox": {
                            "x1": float(x1),
                            "y1": float(y1),
                            "x2": float(x2),
                            "y2": float(y2)
                        },
                        "keypoints": keypoints_data.tolist(),
                        "num_keypoints": int(len(keypoints_data)),
                        "potential_fall": is_potential_fall,
                        "aspect_ratio": float(aspect_ratio),
                        "note": "Single image - temporal fall detection requires video (15 frames)"
                    })

        return {
            "type": "fall_pose_detection",
            "detections": detections,
            "yolo_results": results  # Keep for internal use (drawing), not serialized
        }

    except Exception as e:
        log.error(f"Error in fall pose detection: {e}")
        return {
            "type": "fall_pose_detection",
            "detections": [],
            "error": str(e)
        }


@router.post("/image")
async def detect_image(
    file: UploadFile = File(...),
    detection_types: str = Form(...),  # Comma-separated: "ppe,fall,fire"
    confidence: Optional[float] = Form(0.5),
    draw_boxes: bool = Form(True)
):
    """
    Detect objects in an uploaded image

    Args:
        file: Image file
        detection_types: Comma-separated detection types (ppe, fall, fire)
        confidence: Confidence threshold (default: 0.5)
        draw_boxes: Whether to draw bounding boxes on output image

    Returns:
        Detection results and optionally annotated image

    Note:
        - For 'fall' detection on images: Uses YOLOv11-pose for pose detection only
        - Temporal fall detection (GRU model) requires video with 15+ frames
        - For 'ppe' and 'fire': Uses YOLOv8n (requires trained models)
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Parse detection types
        det_types = [dt.strip().lower() for dt in detection_types.split(',')]

        log.info(f"Image detection requested for types: {det_types}")

        # Separate special detection types
        has_fall = 'fall' in det_types
        has_fire = 'fire' in det_types
        has_smoke = 'smoke' in det_types
        other_types = [dt for dt in det_types if dt not in ['fall', 'fire', 'smoke']]

        all_detections = []
        detection_counts = {}
        annotated_image = image.copy()

        # Handle fall detection with YOLOv11-pose
        if has_fall:
            log.info("Running YOLOv11-pose for fall/pose detection")
            fall_result = detect_fall_pose_in_image(image, confidence or 0.5)

            if fall_result['detections']:
                all_detections.extend(fall_result['detections'])
                detection_counts['fall_pose'] = len(fall_result['detections'])

                # Draw pose keypoints
                if draw_boxes and 'yolo_results' in fall_result:
                    annotated_image = fall_result['yolo_results'].plot(
                        img=annotated_image,
                        boxes=True,
                        kpt_radius=5,
                        line_width=2
                    )
            else:
                detection_counts['fall_pose'] = 0

        # Handle fire and smoke detection with specialized service
        if has_fire or has_smoke:
            try:
                log.info("Running fire/smoke detection service")
                fire_smoke_service = get_fire_smoke_detection_service()

                if has_fire and has_smoke:
                    # Detect both
                    fire_smoke_results = fire_smoke_service.detect_fire_and_smoke(
                        image, confidence
                    )

                    # Add fire detections
                    if fire_smoke_results['fire']:
                        all_detections.extend(fire_smoke_results['fire'])
                        detection_counts['fire'] = len(fire_smoke_results['fire'])
                    else:
                        detection_counts['fire'] = 0

                    # Add smoke detections
                    if fire_smoke_results['smoke']:
                        all_detections.extend(fire_smoke_results['smoke'])
                        detection_counts['smoke'] = len(fire_smoke_results['smoke'])
                    else:
                        detection_counts['smoke'] = 0

                    # Draw detections
                    if draw_boxes:
                        annotated_image = fire_smoke_service.draw_detections(
                            annotated_image, fire_smoke_results
                        )

                elif has_fire:
                    # Detect only fire
                    fire_detections = fire_smoke_service.detect_fire(image, confidence)
                    if fire_detections:
                        all_detections.extend(fire_detections)
                        detection_counts['fire'] = len(fire_detections)

                        if draw_boxes:
                            fire_smoke_results = {'fire': fire_detections, 'smoke': []}
                            annotated_image = fire_smoke_service.draw_detections(
                                annotated_image, fire_smoke_results
                            )
                    else:
                        detection_counts['fire'] = 0

                elif has_smoke:
                    # Detect only smoke
                    smoke_detections = fire_smoke_service.detect_smoke(image, confidence)
                    if smoke_detections:
                        all_detections.extend(smoke_detections)
                        detection_counts['smoke'] = len(smoke_detections)

                        if draw_boxes:
                            fire_smoke_results = {'fire': [], 'smoke': smoke_detections}
                            annotated_image = fire_smoke_service.draw_detections(
                                annotated_image, fire_smoke_results
                            )
                    else:
                        detection_counts['smoke'] = 0

            except Exception as e:
                log.error(f"Error in fire/smoke detection: {e}")
                if has_fire:
                    detection_counts['fire'] = 0
                if has_smoke:
                    detection_counts['smoke'] = 0

        # Handle other detection types (PPE) with old service
        if other_types:
            log.info(f"Running detection service for types: {other_types}")
            results = detection_service.detect_multiple_types(
                image, other_types, confidence
            )

            for det_type, detections in results.items():
                all_detections.extend(detections)
                detection_counts[det_type] = len(detections)

            # Draw boxes for other detections
            if draw_boxes and any(results.values()):
                flat_detections = []
                for dets in results.values():
                    flat_detections.extend(dets)
                annotated_image = detection_service.draw_detections(
                    annotated_image, flat_detections
                )

        response = {
            "success": True,
            "detections": all_detections,
            "total_detections": len(all_detections),
            "detection_counts": detection_counts,
            "note": "Fall detection on images shows pose only. For temporal fall detection, upload video."
        }

        # Save annotated image if requested
        if draw_boxes and all_detections:
            output_filename = f"detection_{uuid.uuid4().hex}.jpg"
            output_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
            cv2.imwrite(str(output_path), annotated_image)
            response["annotated_image_url"] = f"/results/{output_filename}"

        return response

    except Exception as e:
        log.error(f"Error in image detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def get_available_models():
    """Get list of available detection models"""
    models = []
    for model_name, model in detection_service.models.items():
        models.append({
            "name": model_name,
            "loaded": model is not None,
            "classes": list(model.names.values()) if model else []
        })
    
    return {
        "models": models,
        "device": detection_service.device
    }


@router.get("/classes/{model_name}")
async def get_model_classes(model_name: str):
    """Get classes for a specific model"""
    if model_name not in detection_service.models:
        raise HTTPException(status_code=404, detail="Model not found")

    model = detection_service.models[model_name]
    return {
        "model": model_name,
        "classes": list(model.names.values())
    }


@router.post("/fire-smoke")
async def detect_fire_smoke(
    file: UploadFile = File(...),
    detection_mode: str = Form("both"),  # "fire", "smoke", or "both"
    confidence: Optional[float] = Form(0.5),
    draw_boxes: bool = Form(True)
):
    """
    Dedicated endpoint for fire and smoke detection (supports images and videos)

    Args:
        file: Image or video file
        detection_mode: Detection mode - "fire", "smoke", or "both"
        confidence: Confidence threshold (default: 0.5)
        draw_boxes: Whether to draw bounding boxes on output

    Returns:
        Fire and smoke detection results with alert level
    """
    try:
        log.info(f"Fire/Smoke detection request received: {file.filename}, mode={detection_mode}, confidence={confidence}")

        # Read file contents
        contents = await file.read()

        # Check if it's an image or video
        is_video = file.content_type.startswith('video/') or file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv'))
        is_image = file.content_type.startswith('image/') or file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp'))

        if not is_image and not is_video:
            raise HTTPException(status_code=400, detail="File must be an image or video")

        if is_image:
            # Process image
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image file")

            # Get fire/smoke detection service
            fire_smoke_service = get_fire_smoke_detection_service()

            # Run detection based on mode
            if detection_mode == "both":
                results = fire_smoke_service.detect_fire_and_smoke(image, confidence)
            elif detection_mode == "fire":
                fire_detections = fire_smoke_service.detect_fire(image, confidence)
                results = {
                    'fire': fire_detections,
                    'smoke': [],
                    'total_detections': len(fire_detections),
                    'has_fire': len(fire_detections) > 0,
                    'has_smoke': False,
                    'alert_level': 'high' if len(fire_detections) > 0 else 'none'
                }
            elif detection_mode == "smoke":
                smoke_detections = fire_smoke_service.detect_smoke(image, confidence)
                results = {
                    'fire': [],
                    'smoke': smoke_detections,
                    'total_detections': len(smoke_detections),
                    'has_fire': False,
                    'has_smoke': len(smoke_detections) > 0,
                    'alert_level': 'medium' if len(smoke_detections) > 0 else 'none'
                }
            else:
                raise HTTPException(status_code=400, detail="Invalid detection_mode. Use 'fire', 'smoke', or 'both'")

            annotated_image = image.copy()

            # Draw detections if requested
            if draw_boxes:
                annotated_image = fire_smoke_service.draw_detections(
                    annotated_image, results
                )

            response = {
                "success": True,
                "file_type": "image",
                "detection_mode": detection_mode,
                "fire_detections": results['fire'],
                "smoke_detections": results['smoke'],
                "total_detections": results['total_detections'],
                "has_fire": results['has_fire'],
                "has_smoke": results['has_smoke'],
                "alert_level": results['alert_level'],
                "timestamp": datetime.now().isoformat()
            }

            # Save annotated image if detections found
            if draw_boxes and results['total_detections'] > 0:
                output_filename = f"fire_smoke_{uuid.uuid4().hex}.jpg"
                output_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
                cv2.imwrite(str(output_path), annotated_image)
                response["annotated_image_url"] = f"/results/{output_filename}"

            return response

        else:  # is_video
            # Process video
            # Save uploaded video temporarily
            temp_video_path = Path(settings.UPLOAD_DIR) / f"temp_{uuid.uuid4().hex}_{file.filename}"
            temp_video_path.parent.mkdir(parents=True, exist_ok=True)

            with open(temp_video_path, "wb") as f:
                f.write(contents)

            try:
                # Get fire/smoke detection service
                fire_smoke_service = get_fire_smoke_detection_service()

                # Open video
                cap = cv2.VideoCapture(str(temp_video_path))
                if not cap.isOpened():
                    raise HTTPException(status_code=400, detail="Invalid video file")

                # Get video properties
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Prepare output video if draw_boxes is enabled
                output_video_path = None
                video_writer = None
                if draw_boxes:
                    output_filename = f"fire_smoke_{uuid.uuid4().hex}.mp4"
                    output_video_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
                    output_video_path.parent.mkdir(parents=True, exist_ok=True)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

                # Process video frame by frame
                frame_detections = []
                fire_detected_frames = 0
                smoke_detected_frames = 0
                frame_count = 0

                log.info(f"Processing video for fire/smoke detection: {width}x{height}, {fps} fps, {total_frames} frames")
                log.info(f"Detection mode: {detection_mode}, Confidence threshold: {confidence}")

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1

                    # Run detection on frame
                    if detection_mode == "both":
                        frame_results = fire_smoke_service.detect_fire_and_smoke(frame, confidence)
                    elif detection_mode == "fire":
                        fire_detections = fire_smoke_service.detect_fire(frame, confidence)
                        frame_results = {
                            'fire': fire_detections,
                            'smoke': [],
                            'total_detections': len(fire_detections),
                            'has_fire': len(fire_detections) > 0,
                            'has_smoke': False,
                            'alert_level': 'high' if len(fire_detections) > 0 else 'none'
                        }
                    elif detection_mode == "smoke":
                        smoke_detections = fire_smoke_service.detect_smoke(frame, confidence)
                        frame_results = {
                            'fire': [],
                            'smoke': smoke_detections,
                            'total_detections': len(smoke_detections),
                            'has_fire': False,
                            'has_smoke': len(smoke_detections) > 0,
                            'alert_level': 'medium' if len(smoke_detections) > 0 else 'none'
                        }

                    # Count frames with detections
                    if frame_results['has_fire']:
                        fire_detected_frames += 1
                    if frame_results['has_smoke']:
                        smoke_detected_frames += 1

                    # Log detections when found
                    if frame_results['total_detections'] > 0:
                        log.info(f"Frame {frame_count}: Fire={len(frame_results['fire'])}, Smoke={len(frame_results['smoke'])}, Alert={frame_results['alert_level']}")
                        frame_detections.append({
                            'frame': frame_count,
                            'timestamp': frame_count / fps,
                            'fire_count': len(frame_results['fire']),
                            'smoke_count': len(frame_results['smoke']),
                            'alert_level': frame_results['alert_level']
                        })

                    # Log progress every 30 frames
                    if frame_count % 30 == 0:
                        progress = (frame_count / total_frames) * 100
                        log.info(f"Fire/Smoke detection progress: {progress:.1f}% ({frame_count}/{total_frames})")

                    # Draw detections and write frame
                    if draw_boxes and video_writer:
                        annotated_frame = fire_smoke_service.draw_detections(frame, frame_results)
                        video_writer.write(annotated_frame)

                # Release resources
                cap.release()
                if video_writer:
                    video_writer.release()

                # Calculate overall statistics
                has_fire = fire_detected_frames > 0
                has_smoke = smoke_detected_frames > 0

                if has_fire and has_smoke:
                    overall_alert = 'critical'
                elif has_fire:
                    overall_alert = 'high'
                elif has_smoke:
                    overall_alert = 'medium'
                else:
                    overall_alert = 'none'

                log.info(f"Fire/Smoke detection complete: {fire_detected_frames} frames with fire, {smoke_detected_frames} frames with smoke, Alert level: {overall_alert}")

                response = {
                    "success": True,
                    "file_type": "video",
                    "detection_mode": detection_mode,
                    "video_info": {
                        "total_frames": total_frames,
                        "fps": fps,
                        "duration_seconds": total_frames / fps if fps > 0 else 0,
                        "resolution": f"{width}x{height}"
                    },
                    "summary": {
                        "frames_with_fire": fire_detected_frames,
                        "frames_with_smoke": smoke_detected_frames,
                        "total_detection_events": len(frame_detections),
                        "has_fire": has_fire,
                        "has_smoke": has_smoke,
                        "alert_level": overall_alert
                    },
                    "frame_detections": frame_detections[:100],  # Limit to first 100 events
                    "timestamp": datetime.now().isoformat()
                }

                if output_video_path and output_video_path.exists():
                    response["annotated_video_url"] = f"/results/{output_video_path.name}"

                return response

            finally:
                # Clean up temporary video file
                if temp_video_path.exists():
                    temp_video_path.unlink()

    except Exception as e:
        log.error(f"Error in fire/smoke detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ppe")
async def detect_ppe(
    file: UploadFile = File(...),
    ppe_types: Optional[str] = Form(None),  # Comma-separated list of PPE types to detect
    confidence: Optional[float] = Form(0.5),
    draw_boxes: bool = Form(True)
):
    """
    Dedicated endpoint for PPE (Personal Protective Equipment) detection (supports images and videos)

    Args:
        file: Image or video file
        ppe_types: Comma-separated list of specific PPE types to detect (None = all)
                  Available: helmet, safety-vest, gloves, glasses, face-mask, shoes, etc.
        confidence: Confidence threshold (default: 0.5)
        draw_boxes: Whether to draw bounding boxes on output

    Returns:
        PPE detection results with compliance status
    """
    try:
        # Read file contents
        contents = await file.read()

        # Check if it's an image or video
        is_video = file.content_type.startswith('video/') or file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv'))
        is_image = file.content_type.startswith('image/') or file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp'))

        if not is_image and not is_video:
            raise HTTPException(status_code=400, detail="File must be an image or video")

        # Parse PPE types filter
        ppe_types_list = None
        if ppe_types:
            ppe_types_list = [t.strip() for t in ppe_types.split(',')]

        if is_image:
            # Process image
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image file")

            # Get PPE detection service
            ppe_service = get_ppe_detection_service()

            # Run detection
            results = ppe_service.detect_ppe(image, confidence, ppe_types_list)
            summary = ppe_service.get_ppe_summary(results)

            annotated_image = image.copy()

            # Draw detections if requested
            if draw_boxes:
                annotated_image = ppe_service.draw_detections(annotated_image, results)

            response = {
                "success": True,
                "file_type": "image",
                "detections": results['detections'],
                "total_detections": results['total_detections'],
                "ppe_counts": results['ppe_counts'],
                "persons_detected": results['persons_detected'],
                "compliance_status": results['compliance_status'],
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }

            # Save annotated image if detections found
            if draw_boxes and results['total_detections'] > 0:
                output_filename = f"ppe_{uuid.uuid4().hex}.jpg"
                output_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
                cv2.imwrite(str(output_path), annotated_image)
                response["annotated_image_url"] = f"/results/{output_filename}"

            return response

        else:  # is_video
            # Process video
            # Save uploaded video temporarily
            temp_video_path = Path(settings.UPLOAD_DIR) / f"temp_{uuid.uuid4().hex}_{file.filename}"
            temp_video_path.parent.mkdir(parents=True, exist_ok=True)

            with open(temp_video_path, "wb") as f:
                f.write(contents)

            try:
                # Get PPE detection service
                ppe_service = get_ppe_detection_service()

                # Open video
                cap = cv2.VideoCapture(str(temp_video_path))
                if not cap.isOpened():
                    raise HTTPException(status_code=400, detail="Invalid video file")

                # Get video properties
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                # Prepare output video if draw_boxes is enabled
                output_video_path = None
                video_writer = None
                if draw_boxes:
                    output_filename = f"ppe_{uuid.uuid4().hex}.mp4"
                    output_video_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
                    output_video_path.parent.mkdir(parents=True, exist_ok=True)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

                # Process video frame by frame
                frame_detections = []
                compliant_frames = 0
                partial_frames = 0
                non_compliant_frames = 0
                frame_count = 0

                total_ppe_items = {}

                log.info(f"Processing PPE video: {total_frames} frames at {fps} FPS")

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1

                    # Run detection on frame
                    frame_results = ppe_service.detect_ppe(frame, confidence, ppe_types_list)

                    # Count compliance status
                    if frame_results['compliance_status'] == 'compliant':
                        compliant_frames += 1
                    elif frame_results['compliance_status'] == 'partial':
                        partial_frames += 1
                    elif frame_results['compliance_status'] == 'non-compliant':
                        non_compliant_frames += 1

                    # Aggregate PPE counts
                    for ppe_item, count in frame_results['ppe_counts'].items():
                        if ppe_item in total_ppe_items:
                            total_ppe_items[ppe_item] += count
                        else:
                            total_ppe_items[ppe_item] = count

                    # Store frame detection summary
                    if frame_results['total_detections'] > 0:
                        frame_detections.append({
                            'frame': frame_count,
                            'timestamp': frame_count / fps,
                            'ppe_count': frame_results['total_detections'],
                            'persons': frame_results['persons_detected'],
                            'compliance': frame_results['compliance_status']
                        })

                    # Draw detections and write frame
                    if draw_boxes and video_writer:
                        annotated_frame = ppe_service.draw_detections(frame, frame_results)
                        video_writer.write(annotated_frame)

                # Release resources
                cap.release()
                if video_writer:
                    video_writer.release()

                # Calculate overall compliance
                if compliant_frames > non_compliant_frames:
                    overall_compliance = 'compliant'
                elif partial_frames > 0 or compliant_frames > 0:
                    overall_compliance = 'partial'
                else:
                    overall_compliance = 'non-compliant'

                response = {
                    "success": True,
                    "file_type": "video",
                    "video_info": {
                        "total_frames": total_frames,
                        "fps": fps,
                        "duration_seconds": total_frames / fps if fps > 0 else 0,
                        "resolution": f"{width}x{height}"
                    },
                    "summary": {
                        "compliant_frames": compliant_frames,
                        "partial_frames": partial_frames,
                        "non_compliant_frames": non_compliant_frames,
                        "overall_compliance": overall_compliance,
                        "total_ppe_items_detected": total_ppe_items,
                        "detection_events": len(frame_detections)
                    },
                    "frame_detections": frame_detections[:100],  # Limit to first 100 events
                    "timestamp": datetime.now().isoformat()
                }

                if output_video_path and output_video_path.exists():
                    response["annotated_video_url"] = f"/results/{output_video_path.name}"

                return response

            finally:
                # Clean up temporary video file
                if temp_video_path.exists():
                    temp_video_path.unlink()

    except Exception as e:
        log.error(f"Error in PPE detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fall")
async def detect_fall(
    file: UploadFile = File(...),
    confidence: Optional[float] = Form(0.5),
    draw_boxes: bool = Form(True)
):
    """
    Dedicated endpoint for fall detection (supports images and videos)

    For images: Uses YOLOv11-pose for pose detection only
    For videos: Uses YOLOv11-pose + GRU for temporal fall detection

    Args:
        file: Image or video file
        confidence: Confidence threshold (default: 0.5)
        draw_boxes: Whether to draw bounding boxes/keypoints on output

    Returns:
        Fall detection results
    """
    try:
        # Read file contents
        contents = await file.read()

        # Check if it's an image or video
        is_video = file.content_type.startswith('video/') or file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv'))
        is_image = file.content_type.startswith('image/') or file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp'))

        if not is_image and not is_video:
            raise HTTPException(status_code=400, detail="File must be an image or video")

        if is_image:
            # Process image with pose detection
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image file")

            log.info("Running fall/pose detection on image")
            fall_result = detect_fall_pose_in_image(image, confidence or 0.5)

            annotated_image = image.copy()

            # Draw pose keypoints if requested
            if draw_boxes and 'yolo_results' in fall_result and fall_result['detections']:
                annotated_image = fall_result['yolo_results'].plot(
                    img=annotated_image,
                    boxes=True,
                    kpt_radius=5,
                    line_width=2
                )

            response = {
                "success": True,
                "file_type": "image",
                "detections": fall_result['detections'],
                "total_detections": len(fall_result['detections']),
                "note": "Image analysis shows pose only. For temporal fall detection, upload a video.",
                "timestamp": datetime.now().isoformat()
            }

            # Save annotated image if detections found
            if draw_boxes and fall_result['detections']:
                output_filename = f"fall_pose_{uuid.uuid4().hex}.jpg"
                output_path = Path(settings.DETECTION_RESULTS_DIR) / output_filename
                cv2.imwrite(str(output_path), annotated_image)
                response["annotated_image_url"] = f"/results/{output_filename}"

            return response

        else:
            # Process video with temporal fall detection
            log.info("Processing video for fall detection")

            # Save temporary video file
            temp_video_path = Path(settings.UPLOAD_DIR) / f"temp_fall_{uuid.uuid4().hex}{Path(file.filename).suffix}"
            temp_video_path.parent.mkdir(parents=True, exist_ok=True)

            with temp_video_path.open("wb") as f:
                f.write(contents)

            try:
                fall_service = get_fall_detection_service()
                cap = cv2.VideoCapture(str(temp_video_path))

                # Get video properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # Setup output video
                output_video_path = None
                video_writer = None

                if draw_boxes:
                    output_video_path = Path(settings.DETECTION_RESULTS_DIR) / f"fall_detection_{uuid.uuid4().hex}.mp4"
                    output_video_path.parent.mkdir(parents=True, exist_ok=True)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

                frame_count = 0
                falls_detected = []
                frames_with_falls = 0

                log.info(f"Processing fall detection: {width}x{height}, {fps} fps, {total_frames} frames")

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1

                    # Process frame for fall detection
                    result = fall_service.process_frame(frame)

                    # Check for falls
                    if result['falls_detected']:
                        frames_with_falls += 1
                        for fall in result['falls_detected']:
                            falls_detected.append({
                                'frame': frame_count,
                                'timestamp': frame_count / fps if fps > 0 else 0,
                                'probability': fall['probability'],
                                'person_idx': fall['person_idx']
                            })

                    # Draw results on frame
                    if draw_boxes and video_writer:
                        # Draw pose keypoints
                        if 'yolo_results' in result and result['yolo_results'] is not None:
                            annotated_frame = result['yolo_results'].plot(
                                img=frame.copy(),
                                boxes=True,
                                kpt_radius=3,
                                line_width=1
                            )
                        else:
                            annotated_frame = frame.copy()

                        # Add fall detection text
                        if result['falls_detected']:
                            cv2.putText(
                                annotated_frame,
                                "FALL DETECTED!",
                                (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.5,
                                (0, 0, 255),
                                3
                            )

                            for fall in result['falls_detected']:
                                cv2.putText(
                                    annotated_frame,
                                    f"Fall Prob: {fall['probability']:.2f}",
                                    (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (0, 0, 255),
                                    2
                                )

                        video_writer.write(annotated_frame)

                    # Log progress every 30 frames
                    if frame_count % 30 == 0:
                        progress = (frame_count / total_frames) * 100
                        log.info(f"Fall detection progress: {progress:.1f}% ({frame_count}/{total_frames})")

                # Release resources
                cap.release()
                if video_writer:
                    video_writer.release()

                log.info(f"Fall detection complete: {len(falls_detected)} fall events detected in {frames_with_falls} frames")

                response = {
                    "success": True,
                    "file_type": "video",
                    "video_info": {
                        "total_frames": total_frames,
                        "fps": fps,
                        "duration_seconds": total_frames / fps if fps > 0 else 0,
                        "resolution": f"{width}x{height}"
                    },
                    "summary": {
                        "total_fall_events": len(falls_detected),
                        "frames_with_falls": frames_with_falls,
                        "has_falls": len(falls_detected) > 0
                    },
                    "fall_events": falls_detected[:50],  # Limit to first 50 events
                    "timestamp": datetime.now().isoformat()
                }

                if output_video_path and output_video_path.exists():
                    response["annotated_video_url"] = f"/results/{output_video_path.name}"

                return response

            finally:
                # Clean up temporary video file
                if temp_video_path.exists():
                    temp_video_path.unlink()

    except Exception as e:
        log.error(f"Error in fall detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

