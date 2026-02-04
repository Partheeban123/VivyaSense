#!/usr/bin/env python3
"""
Test CORS configuration for contact form
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
    "message": "Testing CORS from frontend"
}

print("=" * 80)
print("🧪 TESTING CORS CONFIGURATION")
print("=" * 80)

# Test 1: OPTIONS request (preflight)
print("\n1️⃣ Testing OPTIONS request (CORS preflight)...")
try:
    response = requests.options(
        "http://localhost:8000/api/contact",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers:")
    for header, value in response.headers.items():
        if 'access-control' in header.lower():
            print(f"     {header}: {value}")
    
    if response.status_code == 200:
        print("   ✅ CORS preflight passed!")
    else:
        print(f"   ❌ CORS preflight failed! Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: POST request with Origin header
print("\n2️⃣ Testing POST request with Origin header...")
try:
    response = requests.post(
        "http://localhost:8000/api/contact",
        json=test_data,
        headers={
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers:")
    for header, value in response.headers.items():
        if 'access-control' in header.lower():
            print(f"     {header}: {value}")
    
    if response.status_code == 200:
        print("   ✅ POST request successful!")
        print(f"   Response: {json.dumps(response.json(), indent=6)}")
    else:
        print(f"   ❌ POST request failed! Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check if endpoint exists
print("\n3️⃣ Testing if endpoint exists...")
try:
    response = requests.get("http://localhost:8000/api/contact/test")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Endpoint exists!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Endpoint not found! Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("\n💡 TROUBLESHOOTING TIPS:")
print("   1. Make sure backend server is restarted after code changes")
print("   2. Check browser console (F12) for CORS errors")
print("   3. Verify frontend is running on http://localhost:3000")
print("   4. Check Network tab in browser DevTools for failed requests")
print("\n" + "=" * 80)

