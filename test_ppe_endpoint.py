#!/usr/bin/env python3
"""
Test script for PPE detection endpoint
"""
import sys
import os
sys.path.append('./backend')

# Set minimal environment variables
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['SECRET_KEY'] = 'test-secret-key'

from services.ppe_detection_service import get_ppe_detection_service
import cv2
import numpy as np

def test_ppe_service():
    print("\n" + "="*60)
    print("Testing PPE Detection Service")
    print("="*60 + "\n")

    # Change to backend directory for model loading
    os.chdir('backend')

    # Get service
    ppe_service = get_ppe_detection_service()
    
    if ppe_service.model is None:
        print("❌ PPE model not loaded")
        return
    
    print("✅ PPE Detection Service initialized")
    print(f"   Device: {ppe_service.device}")
    print(f"   Confidence threshold: {ppe_service.confidence_threshold}")
    print(f"   Model classes: {len(ppe_service.model.names)}")
    print(f"   Critical PPE items: {ppe_service.CRITICAL_PPE}")
    
    # Create a dummy image for testing
    print("\n📊 Testing with dummy image...")
    dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
    
    # Run detection
    results = ppe_service.detect_ppe(dummy_image, confidence=0.5)
    
    print(f"\n✅ Detection completed:")
    print(f"   Total detections: {results['total_detections']}")
    print(f"   Persons detected: {results['persons_detected']}")
    print(f"   Compliance status: {results['compliance_status']}")
    print(f"   PPE counts: {results['ppe_counts']}")
    
    # Test summary
    summary = ppe_service.get_ppe_summary(results)
    print(f"\n📋 Summary:")
    print(f"   Total PPE items: {summary['total_ppe_items']}")
    print(f"   Categories: {summary['categories']}")
    
    print("\n" + "="*60)
    print("✅ PPE Detection Service is working!")
    print("="*60 + "\n")
    
    print("🎯 Available PPE Classes:")
    for class_id, class_name in ppe_service.PPE_CLASSES.items():
        print(f"   {class_id}: {class_name}")
    
    print("\n🔧 API Endpoint: POST /api/detection/ppe")
    print("   Parameters:")
    print("   - file: Image or video file")
    print("   - ppe_types: Comma-separated list (optional)")
    print("   - confidence: Float (default: 0.5)")
    print("   - draw_boxes: Boolean (default: true)")
    
    print("\n📝 Example cURL:")
    print('   curl -X POST "http://localhost:8000/api/detection/ppe" \\')
    print('     -F "file=@image.jpg" \\')
    print('     -F "ppe_types=helmet,safety-vest,gloves" \\')
    print('     -F "confidence=0.5" \\')
    print('     -F "draw_boxes=true"')

if __name__ == "__main__":
    test_ppe_service()

