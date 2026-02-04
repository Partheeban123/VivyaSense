"""
PPE (Personal Protective Equipment) Detection Service
Uses trained YOLO model to detect various PPE items
Model: ppe_detection.pt (130.5 MB)
Classes: 17 PPE items including helmet, vest, gloves, mask, etc.
"""
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from core.config import settings
from core.logger import log


class PPEDetectionService:
    """
    PPE detection using trained YOLO model
    
    Features:
    - Detects 17 different PPE items
    - Supports filtering by specific PPE types
    - Real-time video processing
    - Compliance checking (person with/without PPE)
    """
    
    # PPE class mapping
    PPE_CLASSES = {
        0: 'person',
        1: 'ear',
        2: 'ear-muffs',
        3: 'face',
        4: 'face-guard',
        5: 'face-mask',
        6: 'foot',
        7: 'tool',
        8: 'glasses',
        9: 'gloves',
        10: 'helmet',
        11: 'hands',
        12: 'head',
        13: 'medical-suit',
        14: 'shoes',
        15: 'safety-suit',
        16: 'safety-vest'
    }
    
    # Critical PPE items for safety compliance
    CRITICAL_PPE = ['helmet', 'safety-vest', 'gloves', 'glasses', 'face-mask']
    
    def __init__(
        self,
        model_path: str = None,
        confidence_threshold: float = 0.5
    ):
        """
        Initialize PPE detection service
        
        Args:
            model_path: Path to the PPE model (defaults to PPE_MODEL_PATH from config)
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

        log.info(f"PPE detection service initializing on device: {self.device}")
        
        # Load PPE detection model
        model_path = model_path or settings.PPE_MODEL_PATH
        if Path(model_path).exists():
            self.model = YOLO(model_path)
            self.model.to(self.device)

            # Performance optimizations
            if self.device == 'cuda':
                # Enable half precision for faster inference on GPU
                self.model.model.half()
                log.info("✅ Enabled FP16 (half precision) for faster GPU inference")

            log.info(f"✅ Loaded PPE detection model from {model_path}")
            log.info(f"   Device: {self.device}")
            log.info(f"   Model classes: {len(self.model.names)} PPE items")
            log.info(f"   Classes: {list(self.model.names.values())}")
        else:
            log.error(f"❌ Model not found: {model_path}. PPE detection will be unavailable.")
            self.model = None
    
    def detect_ppe(
        self,
        image: np.ndarray,
        confidence: float = None,
        ppe_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Detect PPE items in image
        
        Args:
            image: Input image (BGR format)
            confidence: Confidence threshold (uses default if None)
            ppe_types: List of specific PPE types to detect (None = all)
        
        Returns:
            Dictionary with detection results
        """
        if self.model is None:
            return {
                'detections': [],
                'total_detections': 0,
                'ppe_counts': {},
                'persons_detected': 0,
                'compliance_status': 'unknown'
            }
        
        conf = confidence if confidence is not None else self.confidence_threshold

        # Run detection with performance optimizations
        # - half=True: Use FP16 for faster inference (GPU only)
        # - verbose=False: Suppress output
        # - stream=False: Process single image (not batch)
        results = self.model(
            image,
            conf=conf,
            verbose=False,
            half=(self.device == 'cuda')  # Use half precision on GPU
        )
        
        detections = []
        ppe_counts = {}
        persons_detected = 0
        
        # Pre-check if filtering is needed (performance optimization)
        filter_enabled = ppe_types is not None and len(ppe_types) > 0

        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                conf_score = float(box.conf[0])
                bbox = box.xyxy[0].cpu().numpy()

                # Filter by PPE types if specified (optimized check)
                if filter_enabled and class_name not in ppe_types:
                    continue

                detection = {
                    'class_id': class_id,
                    'class_name': class_name,
                    'confidence': conf_score,
                    'bbox': {
                        'x1': float(bbox[0]),
                        'y1': float(bbox[1]),
                        'x2': float(bbox[2]),
                        'y2': float(bbox[3])
                    },
                    'detection_type': 'ppe'
                }

                detections.append(detection)

                # Count PPE items
                if class_name in ppe_counts:
                    ppe_counts[class_name] += 1
                else:
                    ppe_counts[class_name] = 1

                # Count persons
                if class_name == 'person':
                    persons_detected += 1
        
        # Check compliance
        compliance_status = self._check_compliance(ppe_counts, persons_detected)
        
        return {
            'detections': detections,
            'total_detections': len(detections),
            'ppe_counts': ppe_counts,
            'persons_detected': persons_detected,
            'compliance_status': compliance_status
        }

    def _check_compliance(self, ppe_counts: Dict[str, int], persons_detected: int) -> str:
        """
        Check PPE compliance status

        Args:
            ppe_counts: Dictionary of detected PPE items and counts
            persons_detected: Number of persons detected

        Returns:
            Compliance status: 'compliant', 'partial', 'non-compliant', 'no-person'
        """
        if persons_detected == 0:
            return 'no-person'

        # Check if critical PPE items are present
        critical_ppe_found = []
        for ppe_item in self.CRITICAL_PPE:
            if ppe_item in ppe_counts and ppe_counts[ppe_item] > 0:
                critical_ppe_found.append(ppe_item)

        # Determine compliance level
        if len(critical_ppe_found) >= 3:  # At least 3 critical PPE items
            return 'compliant'
        elif len(critical_ppe_found) >= 1:  # Some PPE items
            return 'partial'
        else:
            return 'non-compliant'

    def draw_detections(
        self,
        image: np.ndarray,
        results: Dict[str, Any]
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image

        Args:
            image: Input image
            results: Detection results from detect_ppe()

        Returns:
            Annotated image
        """
        annotated = image.copy()

        # Color mapping for different PPE types
        colors = {
            'person': (255, 255, 0),      # Cyan
            'helmet': (0, 255, 0),        # Green
            'safety-vest': (0, 255, 255), # Yellow
            'gloves': (255, 0, 255),      # Magenta
            'glasses': (255, 128, 0),     # Orange
            'face-mask': (128, 255, 0),   # Light green
            'default': (0, 165, 255)      # Orange (default)
        }

        for det in results['detections']:
            bbox = det['bbox']
            x1, y1 = int(bbox['x1']), int(bbox['y1'])
            x2, y2 = int(bbox['x2']), int(bbox['y2'])

            class_name = det['class_name']
            confidence = det['confidence']

            # Get color for this PPE type
            color = colors.get(class_name, colors['default'])

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            # Draw label background
            label = f"{class_name}: {confidence:.2f}"
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated, (x1, y1 - label_h - 10), (x1 + label_w, y1), color, -1)

            # Draw label text
            cv2.putText(annotated, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # Draw compliance status
        compliance = results['compliance_status']
        status_colors = {
            'compliant': (0, 255, 0),      # Green
            'partial': (0, 255, 255),      # Yellow
            'non-compliant': (0, 0, 255),  # Red
            'no-person': (128, 128, 128)   # Gray
        }

        status_color = status_colors.get(compliance, (255, 255, 255))
        status_text = f"Compliance: {compliance.upper()}"

        cv2.rectangle(annotated, (10, 10), (300, 50), status_color, -1)
        cv2.putText(annotated, status_text, (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        return annotated

    def get_ppe_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of PPE detection results

        Args:
            results: Detection results from detect_ppe()

        Returns:
            Summary dictionary
        """
        ppe_counts = results['ppe_counts']

        # Categorize PPE items
        head_protection = sum([
            ppe_counts.get('helmet', 0),
            ppe_counts.get('face-guard', 0),
            ppe_counts.get('face-mask', 0)
        ])

        body_protection = sum([
            ppe_counts.get('safety-vest', 0),
            ppe_counts.get('safety-suit', 0),
            ppe_counts.get('medical-suit', 0)
        ])

        hand_protection = ppe_counts.get('gloves', 0)
        eye_protection = ppe_counts.get('glasses', 0)
        foot_protection = ppe_counts.get('shoes', 0)

        return {
            'total_ppe_items': results['total_detections'] - results['persons_detected'],
            'persons_detected': results['persons_detected'],
            'compliance_status': results['compliance_status'],
            'categories': {
                'head_protection': head_protection,
                'body_protection': body_protection,
                'hand_protection': hand_protection,
                'eye_protection': eye_protection,
                'foot_protection': foot_protection
            },
            'detailed_counts': ppe_counts
        }


# Singleton instance
_ppe_detection_service = None


def get_ppe_detection_service() -> PPEDetectionService:
    """Get or create PPE detection service singleton"""
    global _ppe_detection_service
    if _ppe_detection_service is None:
        _ppe_detection_service = PPEDetectionService()
    return _ppe_detection_service


