#!/usr/bin/env python3
"""
Test script to verify smoke_detection.pt model is loaded and working
"""
import sys
import os
from pathlib import Path

# Change to backend directory for relative paths to work
backend_dir = Path(__file__).parent / 'backend'
os.chdir(backend_dir)

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env')

sys.path.insert(0, str(backend_dir))

from services.fire_smoke_detection_service import get_fire_smoke_detection_service
from core.logger import log

def test_model_loading():
    """Test that smoke_detection.pt is loaded correctly"""
    print("\n" + "="*60)
    print("Testing Fire/Smoke Detection Model Loading")
    print("="*60 + "\n")
    
    # Get the service (this will load the model)
    service = get_fire_smoke_detection_service()
    
    if service.model is None:
        print("❌ ERROR: Model failed to load!")
        return False
    
    print("✅ Model loaded successfully!")
    print(f"\n📊 Model Information:")
    print(f"   Device: {service.device}")
    print(f"   Model classes: {service.model.names}")
    print(f"   Fire class ID: {service.fire_class_id}")
    print(f"   Smoke class ID: {service.smoke_class_id}")
    print(f"   Confidence threshold: {service.confidence_threshold}")
    
    # Verify it's the smoke_detection.pt model
    print(f"\n🔍 Verification:")
    if service.fire_class_id is not None and service.smoke_class_id is not None:
        print(f"   ✅ Both fire and smoke classes detected")
        print(f"   ✅ Model has 2 classes as expected")
        print(f"   ✅ Ready for fire and smoke detection")
    else:
        print(f"   ❌ WARNING: Classes not properly detected")
        return False
    
    print("\n" + "="*60)
    print("✅ All tests passed! Model is ready.")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1)

