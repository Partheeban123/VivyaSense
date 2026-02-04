#!/usr/bin/env python3
"""
Check what classes are in the fire and smoke detection models
"""
import sys
from pathlib import Path
from ultralytics import YOLO

def check_model_classes(model_path: str, model_name: str):
    """Check and print model classes"""
    if not Path(model_path).exists():
        print(f"❌ {model_name} not found at: {model_path}")
        return False
    
    try:
        print(f"\n{'='*60}")
        print(f"Loading {model_name}...")
        print(f"Path: {model_path}")
        print(f"{'='*60}")
        
        model = YOLO(model_path)
        
        print(f"\n✅ Model loaded successfully!")
        print(f"Number of classes: {len(model.names)}")
        print(f"\nClass mapping:")
        for class_id, class_name in model.names.items():
            print(f"  {class_id}: {class_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading {model_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔥 Checking Fire and Smoke Detection Models\n")
    
    fire_model_path = "backend/models/fire_detection.pt"
    smoke_model_path = "backend/models/smoke_detection.pt"
    
    fire_ok = check_model_classes(fire_model_path, "Fire Detection Model")
    smoke_ok = check_model_classes(smoke_model_path, "Smoke Detection Model")
    
    print(f"\n{'='*60}")
    if fire_ok and smoke_ok:
        print("✅ Both models loaded successfully!")
    else:
        print("⚠️  Some models failed to load")
    print(f"{'='*60}\n")

