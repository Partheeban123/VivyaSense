#!/usr/bin/env python3
"""
Test script to verify contact form endpoint works
"""
import requests
import json

# Test data
test_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "company": "Test Company Inc.",
    "phone": "+1 (555) 123-4567",
    "subject": "demo",
    "message": "I'm interested in learning more about Vivya Sense AI Vision Platform. Please contact me for a demo."
}

print("=" * 80)
print("🧪 TESTING CONTACT FORM API")
print("=" * 80)
print(f"\n📤 Sending POST request to: http://localhost:8000/api/contact")
print(f"\n📋 Test Data:")
print(json.dumps(test_data, indent=2))
print("\n" + "=" * 80)

try:
    response = requests.post(
        "http://localhost:8000/api/contact",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n✅ Response Status: {response.status_code}")
    print(f"\n📥 Response Body:")
    print(json.dumps(response.json(), indent=2))
    print("\n" + "=" * 80)
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Contact form is working correctly!")
        print("\n💡 Now check the backend logs to see the contact form data.")
    else:
        print(f"\n❌ FAILED! Status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Could not connect to backend server!")
    print("   Make sure the backend is running on http://localhost:8000")
    print("\n   To start the backend:")
    print("   cd /Users/partheebandevaraj/ai-vision-platform/backend")
    print("   source venv/bin/activate")
    print("   python main.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")

print("\n" + "=" * 80)

