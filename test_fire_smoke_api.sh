#!/bin/bash

# Test Fire and Smoke Detection API
# This script tests the fire/smoke detection endpoints

API_URL="http://localhost:8000"

echo "🔥 Testing Fire and Smoke Detection API"
echo "========================================"
echo ""

# Check if test image is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_test_image>"
    echo ""
    echo "Example:"
    echo "  $0 ~/Downloads/smoke_test.jpg"
    echo ""
    exit 1
fi

TEST_IMAGE="$1"

if [ ! -f "$TEST_IMAGE" ]; then
    echo "❌ Error: Image file not found: $TEST_IMAGE"
    exit 1
fi

echo "📸 Test Image: $TEST_IMAGE"
echo ""

# Test 1: Detect both fire and smoke
echo "Test 1: Detect BOTH fire and smoke"
echo "-----------------------------------"
curl -X POST "$API_URL/api/detection/fire-smoke" \
  -F "file=@$TEST_IMAGE" \
  -F "detection_mode=both" \
  -F "confidence=0.5" \
  -F "draw_boxes=true" \
  -s | python3 -m json.tool

echo ""
echo ""

# Test 2: Detect only fire
echo "Test 2: Detect ONLY fire"
echo "------------------------"
curl -X POST "$API_URL/api/detection/fire-smoke" \
  -F "file=@$TEST_IMAGE" \
  -F "detection_mode=fire" \
  -F "confidence=0.5" \
  -F "draw_boxes=true" \
  -s | python3 -m json.tool

echo ""
echo ""

# Test 3: Detect only smoke
echo "Test 3: Detect ONLY smoke"
echo "-------------------------"
curl -X POST "$API_URL/api/detection/fire-smoke" \
  -F "file=@$TEST_IMAGE" \
  -F "detection_mode=smoke" \
  -F "confidence=0.5" \
  -F "draw_boxes=true" \
  -s | python3 -m json.tool

echo ""
echo ""

# Test 4: General detection endpoint with fire and smoke
echo "Test 4: General detection endpoint (fire,smoke)"
echo "-----------------------------------------------"
curl -X POST "$API_URL/api/detection/image" \
  -F "file=@$TEST_IMAGE" \
  -F "detection_types=fire,smoke" \
  -F "confidence=0.5" \
  -F "draw_boxes=true" \
  -s | python3 -m json.tool

echo ""
echo ""
echo "✅ All tests completed!"
echo ""
echo "Check the results above to verify:"
echo "  - Fire detections are labeled as 'fire'"
echo "  - Smoke detections are labeled as 'smoke'"
echo "  - Alert levels are correct"
echo ""

