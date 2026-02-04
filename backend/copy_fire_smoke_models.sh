#!/bin/bash

# Script to copy fire and smoke detection models from Downloads to models directory

echo "🔥 Copying Fire and Smoke Detection Models..."
echo ""

# Check if Downloads directory exists
if [ ! -d ~/Downloads ]; then
    echo "❌ Downloads directory not found"
    exit 1
fi

# Create models directory if it doesn't exist
mkdir -p ./models

# Copy fire detection model
if [ -f ~/Downloads/best_model1.pt ]; then
    echo "✅ Found best_model1.pt (Fire Detection)"
    cp ~/Downloads/best_model1.pt ./models/fire_detection.pt
    echo "   Copied to ./models/fire_detection.pt"
else
    echo "❌ best_model1.pt not found in Downloads"
    echo "   Please ensure the file is in ~/Downloads/"
fi

echo ""

# Copy smoke detection model
if [ -f ~/Downloads/best_model_kfold5.pt ]; then
    echo "✅ Found best_model_kfold5.pt (Smoke Detection)"
    cp ~/Downloads/best_model_kfold5.pt ./models/smoke_detection.pt
    echo "   Copied to ./models/smoke_detection.pt"
else
    echo "❌ best_model_kfold5.pt not found in Downloads"
    echo "   Please ensure the file is in ~/Downloads/"
fi

echo ""
echo "📁 Current models directory:"
ls -lh ./models/*.pt 2>/dev/null || echo "No .pt files found"

echo ""
echo "✨ Done! If models were copied successfully, restart the backend server."

