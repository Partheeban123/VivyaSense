"""
Fire and Smoke Detection Service
Uses a single trained YOLO model that detects both fire and smoke
Currently using: smoke_detection.pt (can be changed to fire_detection.pt if needed)
Model classes: 0=smoke, 1=fire
"""
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from core.config import settings
from core.logger import log


class FireSmokeDetectionService:
    """
    Fire and Smoke detection using a single trained YOLO model

    Features:
    - Single model detects both fire and smoke (currently using smoke_detection.pt)
    - Both models (fire_detection.pt and smoke_detection.pt) have 2 classes: 0=smoke, 1=fire
    - Can switch between models easily by changing config
    - Separate detection methods for fire-only, smoke-only, or both
    - Real-time video processing
    - Better performance using only one model
    """
    
    def __init__(
        self,
        model_path: str = None,
        confidence_threshold: float = 0.5
    ):
        """
        Initialize fire and smoke detection service

        Uses a single model that detects both fire and smoke.
        Currently configured to use smoke_detection.pt, but can easily switch to fire_detection.pt.
        Both models have the same 2 classes: 0=smoke, 1=fire

        Args:
            model_path: Path to the model (defaults to FIRE_SMOKE_MODEL_PATH from config)
            confidence_threshold: Detection confidence threshold
        """
        # Device selection: CUDA > MPS (Apple Silicon) > CPU
        if torch.cuda.is_available():
            self.device = 'cuda'
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            self.device = 'mps'  # Apple Silicon GPU
        else:
            self.device = 'cpu'

        self.confidence_threshold = confidence_threshold

        log.info(f"Fire/Smoke detection service initializing on device: {self.device}")

        # Load single model that detects both fire and smoke
        # Model classes: 0=smoke, 1=fire (same for both fire_detection.pt and smoke_detection.pt)
        model_path = model_path or settings.FIRE_SMOKE_MODEL_PATH
        if Path(model_path).exists():
            self.model = YOLO(model_path)
            self.model.to(self.device)
            log.info(f"✅ Loaded fire/smoke detection model from {model_path}")
            log.info(f"   Model classes: {self.model.names}")

            # Store class IDs for filtering
            self.fire_class_id = None
            self.smoke_class_id = None
            for class_id, class_name in self.model.names.items():
                if 'fire' in class_name.lower():
                    self.fire_class_id = class_id
                if 'smoke' in class_name.lower():
                    self.smoke_class_id = class_id

            log.info(f"   Fire class ID: {self.fire_class_id}, Smoke class ID: {self.smoke_class_id}")

            # For backward compatibility
            self.fire_model = self.model
            self.smoke_model = self.model
        else:
            log.error(f"❌ Model not found: {model_path}. Fire/smoke detection will be unavailable.")
            self.model = None
            self.fire_model = None
            self.smoke_model = None
            self.fire_class_id = None
            self.smoke_class_id = None
    
    def detect_fire(
        self,
        frame: np.ndarray,
        confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect ONLY fire in frame (filters out smoke detections)

        Args:
            frame: Input frame (BGR)
            confidence: Confidence threshold

        Returns:
            List of fire detections only
        """
        if self.model is None:
            log.error("Model not loaded")
            return []

        conf = confidence or self.confidence_threshold

        try:
            results = self.model(frame, conf=conf, verbose=False)[0]
            detections = self._parse_detections(results, 'fire')
            return detections
        except Exception as e:
            log.error(f"Error during fire detection: {e}")
            return []
    
    def detect_smoke(
        self,
        frame: np.ndarray,
        confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect ONLY smoke in frame (filters out fire detections)

        Args:
            frame: Input frame (BGR)
            confidence: Confidence threshold

        Returns:
            List of smoke detections only
        """
        if self.model is None:
            log.error("Model not loaded")
            return []

        conf = confidence or self.confidence_threshold

        try:
            results = self.model(frame, conf=conf, verbose=False)[0]
            detections = self._parse_detections(results, 'smoke')
            return detections
        except Exception as e:
            log.error(f"Error during smoke detection: {e}")
            return []
    
    def detect_fire_and_smoke(
        self,
        frame: np.ndarray,
        confidence: Optional[float] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect both fire and smoke in frame using a single model inference

        This is more efficient than calling detect_fire() and detect_smoke() separately
        because it runs the model only once.

        Args:
            frame: Input frame (BGR)
            confidence: Confidence threshold

        Returns:
            Dictionary with fire and smoke detections separately
        """
        if self.model is None:
            log.error("Model not loaded")
            return {
                'fire': [],
                'smoke': [],
                'total_detections': 0,
                'has_fire': False,
                'has_smoke': False,
                'alert_level': 'none'
            }

        conf = confidence or self.confidence_threshold

        try:
            # Run model once and separate detections by class
            results = self.model(frame, conf=conf, verbose=False)[0]

            fire_detections = []
            smoke_detections = []

            if results.boxes is not None and len(results.boxes) > 0:
                boxes = results.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    cls_id = int(box.cls[0])

                    detection = {
                        'class_id': cls_id,
                        'class_name': results.names[cls_id],
                        'confidence': float(box.conf[0]),
                        'bounding_box': {
                            'x1': float(box.xyxy[0][0]),
                            'y1': float(box.xyxy[0][1]),
                            'x2': float(box.xyxy[0][2]),
                            'y2': float(box.xyxy[0][3])
                        }
                    }

                    # Separate by class
                    if cls_id == self.fire_class_id:
                        detection['detection_type'] = 'fire'
                        fire_detections.append(detection)
                    elif cls_id == self.smoke_class_id:
                        detection['detection_type'] = 'smoke'
                        smoke_detections.append(detection)

            return {
                'fire': fire_detections,
                'smoke': smoke_detections,
                'total_detections': len(fire_detections) + len(smoke_detections),
                'has_fire': len(fire_detections) > 0,
                'has_smoke': len(smoke_detections) > 0,
                'alert_level': self._calculate_alert_level(fire_detections, smoke_detections)
            }

        except Exception as e:
            log.error(f"Error during fire/smoke detection: {e}")
            return {
                'fire': [],
                'smoke': [],
                'total_detections': 0,
                'has_fire': False,
                'has_smoke': False,
                'alert_level': 'none'
            }

    def _parse_detections(
        self,
        results: Any,
        detection_type: str
    ) -> List[Dict[str, Any]]:
        """
        Parse YOLO detection results and filter by detection type

        Args:
            results: YOLO results object
            detection_type: Type of detection ('fire' or 'smoke') - filters to only this class

        Returns:
            List of parsed detections (filtered by detection_type)
        """
        detections = []

        if results.boxes is None or len(results.boxes) == 0:
            return detections

        boxes = results.boxes
        for i in range(len(boxes)):
            box = boxes[i]
            cls_id = int(box.cls[0])
            class_name = results.names[cls_id]

            # Filter: only include detections matching the requested type
            # Check if the class name matches the detection type
            if detection_type == 'fire' and cls_id != self.fire_class_id:
                continue  # Skip non-fire detections
            elif detection_type == 'smoke' and cls_id != self.smoke_class_id:
                continue  # Skip non-smoke detections

            detection = {
                'class_id': cls_id,
                'class_name': class_name,
                'confidence': float(box.conf[0]),
                'bounding_box': {
                    'x1': float(box.xyxy[0][0]),
                    'y1': float(box.xyxy[0][1]),
                    'x2': float(box.xyxy[0][2]),
                    'y2': float(box.xyxy[0][3])
                },
                'detection_type': detection_type
            }
            detections.append(detection)

        return detections

    def _calculate_alert_level(
        self,
        fire_detections: List[Dict[str, Any]],
        smoke_detections: List[Dict[str, Any]]
    ) -> str:
        """
        Calculate alert level based on detections

        Args:
            fire_detections: List of fire detections
            smoke_detections: List of smoke detections

        Returns:
            Alert level: 'critical', 'high', 'medium', 'low', or 'none'
        """
        has_fire = len(fire_detections) > 0
        has_smoke = len(smoke_detections) > 0

        if has_fire and has_smoke:
            return 'critical'
        elif has_fire:
            return 'high'
        elif has_smoke:
            return 'medium'
        else:
            return 'none'

    def draw_detections(
        self,
        frame: np.ndarray,
        detections: Dict[str, List[Dict[str, Any]]],
        show_labels: bool = True
    ) -> np.ndarray:
        """
        Draw fire and smoke detections on frame

        Args:
            frame: Input frame
            detections: Detection results from detect_fire_and_smoke
            show_labels: Whether to show labels

        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()

        # Colors (BGR format)
        fire_color = (0, 69, 255)    # Orange-red for fire
        smoke_color = (128, 128, 128)  # Gray for smoke

        # Draw fire detections
        for detection in detections.get('fire', []):
            annotated_frame = self._draw_single_detection(
                annotated_frame,
                detection,
                fire_color,
                show_labels
            )

        # Draw smoke detections
        for detection in detections.get('smoke', []):
            annotated_frame = self._draw_single_detection(
                annotated_frame,
                detection,
                smoke_color,
                show_labels
            )

        # Draw alert banner if detections found
        if detections.get('has_fire') or detections.get('has_smoke'):
            annotated_frame = self._draw_alert_banner(
                annotated_frame,
                detections
            )

        return annotated_frame

    def _draw_single_detection(
        self,
        frame: np.ndarray,
        detection: Dict[str, Any],
        color: Tuple[int, int, int],
        show_labels: bool
    ) -> np.ndarray:
        """Draw a single detection box"""
        bbox = detection['bounding_box']
        x1, y1 = int(bbox['x1']), int(bbox['y1'])
        x2, y2 = int(bbox['x2']), int(bbox['y2'])

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        if show_labels:
            # Draw label
            label = f"{detection['class_name']}: {detection['confidence']:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

            # Background for label
            cv2.rectangle(
                frame,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color,
                -1
            )

            # Label text
            cv2.putText(
                frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        return frame

    def _draw_alert_banner(
        self,
        frame: np.ndarray,
        detections: Dict[str, Any]
    ) -> np.ndarray:
        """Draw alert banner at top of frame"""
        alert_level = detections.get('alert_level', 'none')

        if alert_level == 'none':
            return frame

        # Alert colors
        alert_colors = {
            'critical': (0, 0, 255),    # Red
            'high': (0, 69, 255),       # Orange
            'medium': (0, 165, 255),    # Orange-yellow
            'low': (0, 255, 255)        # Yellow
        }

        color = alert_colors.get(alert_level, (0, 255, 255))

        # Draw banner background
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), color, 3)

        # Alert text
        alert_text = f"⚠️ {alert_level.upper()} ALERT"
        cv2.putText(
            frame,
            alert_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color,
            3,
            cv2.LINE_AA
        )

        # Detection counts
        fire_count = len(detections.get('fire', []))
        smoke_count = len(detections.get('smoke', []))
        details = f"Fire: {fire_count} | Smoke: {smoke_count}"

        cv2.putText(
            frame,
            details,
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        return frame


# Global fire/smoke detection service instance
fire_smoke_detection_service = None


def get_fire_smoke_detection_service() -> FireSmokeDetectionService:
    """Get or create fire/smoke detection service instance"""
    global fire_smoke_detection_service
    if fire_smoke_detection_service is None:
        fire_smoke_detection_service = FireSmokeDetectionService()
    return fire_smoke_detection_service


