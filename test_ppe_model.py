#!/usr/bin/env python3
"""
Test script to check PPE detection model classes
"""
import sys
sys.path.append('./backend')

from ultralytics import YOLO
from pathlib import Path

def test_ppe_model():
    print("\n" + "="*60)
    print("Testing PPE Detection Model")
    print("="*60 + "\n")
    
    model_path = Path("./backend/models/ppe_detection.pt")
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return
    
    print(f"✅ Found model: {model_path}")
    print(f"   Size: {model_path.stat().st_size / (1024*1024):.1f} MB\n")
    
    # Load model
    print("Loading model...")
    model = YOLO(str(model_path))
    
    # Get model info
    print("\n📊 Model Information:")
    print(f"   Task: {model.task}")
    print(f"   Model type: {type(model.model).__name__}")
    
    # Get class names
    if hasattr(model, 'names'):
        class_names = model.names
        print(f"\n🏷️  PPE Classes ({len(class_names)} total):")
        for class_id, class_name in class_names.items():
            print(f"   Class {class_id}: {class_name}")
    else:
        print("\n⚠️  Could not retrieve class names")
    
    print("\n" + "="*60)
    print("✅ Model loaded successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_ppe_model()

