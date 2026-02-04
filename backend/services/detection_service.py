"""
AI Detection Service - Integrates YOLOv8/v11 models
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Any, Optional
from pathlib import Path
import torch
from core.config import settings
from core.logger import log


class DetectionService:
    """Service for running AI detection models"""
    
    def __init__(self):
        self.models = {}
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        log.info(f"Detection service initialized on device: {self.device}")
        self._load_models()
    
    def _load_models(self):
        """Load all YOLO models"""
        model_configs = {
            'ppe': settings.PPE_MODEL_PATH,
            'fall': settings.FALL_MODEL_PATH,
            'fire': settings.FIRE_MODEL_PATH
        }

        for model_name, model_path in model_configs.items():
            try:
                if Path(model_path).exists():
                    self.models[model_name] = YOLO(model_path)
                    self.models[model_name].to(self.device)
                    log.info(f"Loaded {model_name} detection model from {model_path}")
                else:
                    log.warning(f"Model file not found: {model_path}. Using default YOLOv8n model.")
                    # Use default YOLOv8n model as fallback
                    self.models[model_name] = YOLO('yolov8n.pt')
                    self.models[model_name].to(self.device)
                    log.info(f"Loaded default YOLOv8n model for {model_name} detection")
            except Exception as e:
                log.error(f"Error loading {model_name} model: {e}")
    
    def detect(
        self,
        image: np.ndarray,
        detection_type: str,
        confidence_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Run detection on an image
        
        Args:
            image: Input image as numpy array (BGR format)
            detection_type: Type of detection ('ppe', 'fall', 'fire')
            confidence_threshold: Confidence threshold (default from settings)
        
        Returns:
            List of detection results
        """
        if detection_type not in self.models:
            log.error(f"Model not loaded for detection type: {detection_type}")
            return []
        
        confidence = confidence_threshold or settings.CONFIDENCE_THRESHOLD
        
        try:
            # Run inference
            results = self.models[detection_type].predict(
                image,
                conf=confidence,
                iou=settings.IOU_THRESHOLD,
                device=self.device,
                verbose=False
            )
            
            # Parse results
            detections = []
            for result in results:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    detection = {
                        'class_id': int(box.cls[0]),
                        'class_name': result.names[int(box.cls[0])],
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
        
        except Exception as e:
            log.error(f"Error during detection: {e}")
            return []
    
    def detect_multiple_types(
        self,
        image: np.ndarray,
        detection_types: List[str],
        confidence_threshold: Optional[float] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run multiple detection types on the same image
        
        Args:
            image: Input image
            detection_types: List of detection types to run
            confidence_threshold: Confidence threshold
        
        Returns:
            Dictionary with detection results for each type
        """
        results = {}
        for detection_type in detection_types:
            results[detection_type] = self.detect(
                image, detection_type, confidence_threshold
            )
        return results
    
    def draw_detections(
        self,
        image: np.ndarray,
        detections: List[Dict[str, Any]],
        colors: Optional[Dict[str, tuple]] = None
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Input image
            detections: List of detections
            colors: Color mapping for different detection types
        
        Returns:
            Image with drawn detections
        """
        if colors is None:
            colors = {
                'ppe': (0, 255, 0),      # Green
                'fall': (0, 0, 255),     # Red
                'fire': (255, 0, 0)      # Blue (BGR format)
            }
        
        output_image = image.copy()
        
        for detection in detections:
            bbox = detection['bounding_box']
            x1, y1 = int(bbox['x1']), int(bbox['y1'])
            x2, y2 = int(bbox['x2']), int(bbox['y2'])
            
            # Get color for detection type
            color = colors.get(detection['detection_type'], (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(output_image, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{detection['class_name']}: {detection['confidence']:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(
                output_image,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color,
                -1
            )
            cv2.putText(
                output_image,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )
        
        return output_image


# Global detection service instance
detection_service = DetectionService()

