"""
Fall Detection Service
Uses YOLOv11 model (best_fall.pt) for direct fall detection - Fine-tuned model
"""
# ============================================================================
# GRU-BASED FALL DETECTION (COMMENTED OUT - KEPT FOR REFERENCE)
# ============================================================================
# from collections import defaultdict
# from models.fall_detection_gru import load_fall_detection_model
# ============================================================================

from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import cv2
import numpy as np
import torch
from ultralytics import YOLO

from core.config import settings
from core.logger import log


class FallDetectionService:
    """
    Fall detection using YOLOv11 model for direct fall detection

    Pipeline:
    1. YOLOv11 (best_fall.pt) detects falls directly from frames - Fine-tuned model

    Note: GRU-based pose detection code is commented out below for reference
    """

    def __init__(
        self,
        yolo_model_path: str = None,
        confidence_threshold: float = 0.5
    ):
        """
        Initialize fall detection service

        Args:
            yolo_model_path: Path to YOLOv11 fall detection model (best_fall.pt - fine-tuned)
            confidence_threshold: YOLO confidence threshold
        """
        # Device selection: CUDA > MPS (Apple Silicon) > CPU
        if torch.cuda.is_available():
            self.device = 'cuda'
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            self.device = 'mps'  # Apple Silicon GPU
        else:
            self.device = 'cpu'

        self.confidence_threshold = confidence_threshold

        log.info(f"Fall detection service initializing on device: {self.device}")

        # Load YOLO fall detection model (best_fall.pt - fine-tuned)
        yolo_path = yolo_model_path or "./models/best_fall.pt"
        if Path(yolo_path).exists():
            self.yolo_model = YOLO(yolo_path)
            self.yolo_model.to(self.device)
            log.info(f"Loaded YOLOv11 fine-tuned fall detection model from {yolo_path}")
        else:
            log.error(f"YOLO fall detection model not found: {yolo_path}")
            raise FileNotFoundError(f"YOLO fall detection model not found: {yolo_path}")

    # ========================================================================
    # GRU-BASED INITIALIZATION (COMMENTED OUT)
    # ========================================================================
    # def __init__(
    #     self,
    #     yolo_model_path: str = None,
    #     gru_model_path: str = None,
    #     sequence_length: int = 15,
    #     fall_threshold: float = 0.90,
    #     confidence_threshold: float = 0.5
    # ):
    #     """Initialize fall detection service with GRU model"""
    #     if torch.cuda.is_available():
    #         self.device = 'cuda'
    #     elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    #         self.device = 'mps'
    #     else:
    #         self.device = 'cpu'
    #
    #     self.sequence_length = sequence_length
    #     self.fall_threshold = fall_threshold
    #     self.confidence_threshold = confidence_threshold
    #     self.keypoints_buffers = defaultdict(list)
    #     self.fall_status = {}
    #
    #     log.info(f"Fall detection service initializing on device: {self.device}")
    #
    #     # Load YOLO pose model
    #     yolo_path = yolo_model_path or settings.FALL_YOLO_MODEL_PATH
    #     if Path(yolo_path).exists():
    #         self.yolo_model = YOLO(yolo_path)
    #         self.yolo_model.to(self.device)
    #         log.info(f"Loaded YOLOv11-pose model from {yolo_path}")
    #     else:
    #         log.error(f"YOLO model not found: {yolo_path}")
    #         raise FileNotFoundError(f"YOLO model not found: {yolo_path}")
    #
    #     # Load GRU model
    #     gru_path = gru_model_path or settings.FALL_GRU_MODEL_PATH
    #     if Path(gru_path).exists():
    #         self.gru_model = load_fall_detection_model(
    #             model_path=gru_path,
    #             device=self.device,
    #             input_size=34,
    #             hidden_size=64,
    #             num_layers=2,
    #             dropout_prob=0.6
    #         )
    #         log.info(f"Loaded GRU model from {gru_path}")
    #     else:
    #         log.error(f"GRU model not found: {gru_path}")
    #         raise FileNotFoundError(f"GRU model not found: {gru_path}")
    # ========================================================================

    def process_frame(
        self,
        frame: np.ndarray,
        person_id: int = 0
    ) -> Dict[str, Any]:
        """
        Process a single frame for fall detection using YOLO model (best_fall.pt - fine-tuned)

        Args:
            frame: Input frame (BGR)
            person_id: ID of person to track (for compatibility, not used)

        Returns:
            Detection results including fall status
        """
        # Run YOLO fall detection
        results = self.yolo_model(frame, conf=self.confidence_threshold, verbose=False)[0]

        detection_result = {
            'frame': frame.copy(),
            'persons_detected': 0,
            'falls_detected': [],
            'keypoints': [],
            'yolo_results': results  # Store YOLO results for drawing
        }

        # Check if any detections
        if results.boxes is None or len(results.boxes) == 0:
            log.debug("No fall detections in frame")
            return detection_result

        # Process each detection
        num_detections = len(results.boxes)
        log.debug(f"Detected {num_detections} objects")

        for idx, box in enumerate(results.boxes):
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = results.names[class_id] if class_id < len(results.names) else f"class_{class_id}"

            log.debug(f"Detection {idx}: class={class_name}, confidence={confidence:.4f}")

            # IMPORTANT: Only trigger alert for "fall" class (class_id == 0)
            # Model has 2 classes: 0='fall', 1='no-fall'
            # We should ONLY alert when class is exactly "fall", NOT "no-fall"
            if class_name == 'fall' or class_id == 0:
                detection_result['falls_detected'].append({
                    'person_idx': idx,
                    'probability': confidence,
                    'class_name': class_name,
                    'bbox': box.xyxy[0].cpu().numpy().tolist()
                })
                log.info(f"🚨 FALL DETECTED! Class: {class_name}, Confidence: {confidence:.4f}")
            else:
                # Person detected but NOT falling (no-fall class)
                log.debug(f"Person detected (no fall): class={class_name}, confidence={confidence:.4f}")

        detection_result['persons_detected'] = len(detection_result['falls_detected'])

        return detection_result

    # ========================================================================
    # GRU-BASED PROCESS_FRAME (COMMENTED OUT)
    # ========================================================================
    # def detect_poses(self, frame: np.ndarray) -> Tuple[np.ndarray, Any]:
    #     """Detect person poses in frame"""
    #     results = self.yolo_model(frame, conf=self.confidence_threshold, verbose=False)[0]
    #     return frame.copy(), results
    #
    # def process_frame(
    #     self,
    #     frame: np.ndarray,
    #     person_id: int = 0
    # ) -> Dict[str, Any]:
    #     """Process a single frame for fall detection with GRU"""
    #     annotated_frame, results = self.detect_poses(frame)
    #
    #     detection_result = {
    #         'frame': annotated_frame,
    #         'persons_detected': 0,
    #         'falls_detected': [],
    #         'keypoints': [],
    #         'yolo_results': results
    #     }
    #
    #     # Check if keypoints detected
    #     if results.keypoints is None or results.keypoints.data.shape[0] == 0:
    #         log.debug("No keypoints detected in frame")
    #         return detection_result
    #
    #     num_persons = results.keypoints.data.shape[0]
    #     detection_result['persons_detected'] = num_persons
    #
    #     log.debug(f"Detected {num_persons} persons in frame")
    #
    #     # Process each detected person
    #     for person_idx in range(num_persons):
    #         keypoints = results.keypoints.data[person_idx].cpu().numpy()
    #         keypoints_flat = keypoints[:, :2].flatten()
    #         person_key = f"{person_id}_{person_idx}"
    #
    #         # Add to buffer
    #         self.keypoints_buffers[person_key].append(keypoints_flat)
    #
    #         # Keep only last sequence_length frames
    #         if len(self.keypoints_buffers[person_key]) > self.sequence_length:
    #             self.keypoints_buffers[person_key].pop(0)
    #
    #         log.debug(f"Person {person_key} buffer size: {len(self.keypoints_buffers[person_key])}/{self.sequence_length}")
    #
    #         # If buffer is full, run fall detection
    #         if len(self.keypoints_buffers[person_key]) == self.sequence_length:
    #             fall_prob, is_fall = self._detect_fall(person_key)
    #
    #             log.info(f"Person {person_key} fall probability: {fall_prob:.4f}, is_fall: {is_fall}")
    #
    #             self.fall_status[person_key] = {
    #                 'is_fall': is_fall,
    #                 'probability': fall_prob,
    #                 'person_idx': person_idx
    #             }
    #
    #             if is_fall:
    #                 detection_result['falls_detected'].append({
    #                     'person_idx': person_idx,
    #                     'probability': fall_prob,
    #                     'keypoints': keypoints
    #                 })
    #
    #     return detection_result
    # ========================================================================


    # ========================================================================
    # GRU-BASED METHODS (COMMENTED OUT)
    # ========================================================================
    # def _detect_fall(self, person_key: str) -> Tuple[float, bool]:
    #     """Run GRU model on keypoint sequence"""
    #     keypoints_sequence = np.array(
    #         self.keypoints_buffers[person_key],
    #         dtype=np.float32
    #     )
    #     keypoints_tensor = torch.tensor(keypoints_sequence).unsqueeze(0)
    #     keypoints_tensor = keypoints_tensor.to(self.device)
    #
    #     with torch.no_grad():
    #         prediction = self.gru_model(keypoints_tensor)
    #         fall_probability = prediction.item()
    #         is_fall = fall_probability > self.fall_threshold
    #
    #     return fall_probability, is_fall
    #
    # def reset_tracking(self):
    #     """Reset all tracking buffers"""
    #     self.keypoints_buffers.clear()
    #     self.fall_status.clear()
    #     log.info("Reset fall detection tracking")
    # ========================================================================

    def draw_detections(
        self,
        frame: np.ndarray,
        detection_result: Dict[str, Any],
        show_pose: bool = True,
        show_fall_info: bool = True
    ) -> np.ndarray:
        """
        Draw detections on frame

        Args:
            frame: Input frame
            detection_result: Detection results from process_frame
            show_pose: Whether to draw bounding boxes (kept for compatibility)
            show_fall_info: Whether to show fall detection info

        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()

        # Draw bounding boxes for fall detections
        if 'yolo_results' in detection_result:
            results = detection_result['yolo_results']
            if results.boxes is not None and len(results.boxes) > 0:
                # Use YOLO's built-in plot method
                annotated_frame = results.plot(
                    img=annotated_frame,
                    boxes=True,
                    labels=True,
                    conf=True,
                    line_width=3
                )

        # Draw fall detections
        for fall in detection_result['falls_detected']:
            person_idx = fall['person_idx']
            probability = fall['probability']

            # Draw large red "FALL DETECTED!" text
            cv2.putText(
                annotated_frame,
                'FALL DETECTED!',
                (10, 100 + person_idx * 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3,
                cv2.LINE_AA
            )

            # Draw probability
            cv2.putText(
                annotated_frame,
                f'Confidence: {probability:.2%}',
                (10, 140 + person_idx * 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

        # Draw info panel
        if show_fall_info:
            # Background for info panel
            cv2.rectangle(annotated_frame, (5, 5), (300, 80), (0, 0, 0), -1)
            cv2.rectangle(annotated_frame, (5, 5), (300, 80), (255, 255, 255), 2)

            # Person count
            cv2.putText(
                annotated_frame,
                f'Persons Detected: {detection_result["persons_detected"]}',
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Fall count
            fall_color = (0, 0, 255) if detection_result['falls_detected'] else (0, 255, 0)
            cv2.putText(
                annotated_frame,
                f'Falls Detected: {len(detection_result["falls_detected"])}',
                (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                fall_color,
                2,
                cv2.LINE_AA
            )

        return annotated_frame


# Global fall detection service instance
fall_detection_service = None


def get_fall_detection_service() -> FallDetectionService:
    """Get or create fall detection service instance"""
    global fall_detection_service
    if fall_detection_service is None:
        fall_detection_service = FallDetectionService()
    return fall_detection_service

