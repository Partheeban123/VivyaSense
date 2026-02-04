#!/usr/bin/env python3
"""
Test script to verify fire and smoke detection models are loaded correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.fire_smoke_detection_service import get_fire_smoke_detection_service
from core.logger import log

def test_fire_smoke_service():
    """Test that fire and smoke detection service loads correctly"""
    try:
        log.info("Testing Fire and Smoke Detection Service...")
        
        # Get the service (this will load the models)
        service = get_fire_smoke_detection_service()
        
        log.info(f"✅ Fire detection model loaded: {service.fire_model is not None}")
        log.info(f"✅ Smoke detection model loaded: {service.smoke_model is not None}")
        
        # Check model details
        if service.fire_model:
            log.info(f"   Fire model classes: {list(service.fire_model.names.values())}")
        
        if service.smoke_model:
            log.info(f"   Smoke model classes: {list(service.smoke_model.names.values())}")
        
        log.info("\n🎉 Fire and Smoke Detection Service is ready!")
        return True
        
    except Exception as e:
        log.error(f"❌ Error loading fire/smoke detection service: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fire_smoke_service()
    sys.exit(0 if success else 1)

