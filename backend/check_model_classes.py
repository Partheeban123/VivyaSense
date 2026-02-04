#!/usr/bin/env python3
"""Check classes in best.pt model"""
from ultralytics import YOLO

# Load the model
model = YOLO('./models/best.pt')

# Print model information
print("=" * 60)
print("Model Classes:")
print("=" * 60)
print(f"Number of classes: {len(model.names)}")
print(f"\nClass names: {model.names}")
print("\nClass mapping:")
for idx, name in model.names.items():
    print(f"  Class {idx}: {name}")
print("=" * 60)

