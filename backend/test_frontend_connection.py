#!/usr/bin/env python3
"""
Complete test to verify frontend-backend connection for contact form
"""
import requests
import json
from datetime import datetime

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_backend_health():
    """Test if backend is running"""
    print_section("1️⃣  TESTING BACKEND SERVER")
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running!")
            print(f"   App: {data.get('app')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend on http://localhost:8000")
        print("\n💡 Start the backend server:")
        print("   cd /Users/partheebandevaraj/ai-vision-platform/backend")
        print("   source venv/bin/activate")
        print("   python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_contact_endpoint():
    """Test if contact endpoint exists"""
    print_section("2️⃣  TESTING CONTACT ENDPOINT")
    try:
        response = requests.get("http://localhost:8000/api/contact/test", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Contact endpoint exists!")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cors():
    """Test CORS configuration"""
    print_section("3️⃣  TESTING CORS CONFIGURATION")
    try:
        # Test OPTIONS request (preflight)
        response = requests.options(
            "http://localhost:8000/api/contact",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            },
            timeout=3
        )
        
        if response.status_code == 200:
            allow_origin = response.headers.get('access-control-allow-origin')
            allow_methods = response.headers.get('access-control-allow-methods')
            
            print(f"✅ CORS is configured!")
            print(f"   Allow-Origin: {allow_origin}")
            print(f"   Allow-Methods: {allow_methods}")
            
            if 'localhost:3000' in str(allow_origin):
                print(f"   ✅ Frontend origin (localhost:3000) is allowed!")
                return True
            else:
                print(f"   ⚠️  Warning: localhost:3000 might not be explicitly allowed")
                return True
        else:
            print(f"❌ CORS preflight failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_form_submission():
    """Test actual form submission"""
    print_section("4️⃣  TESTING FORM SUBMISSION")
    
    test_data = {
        "name": "Test User (Automated Test)",
        "email": "test@example.com",
        "company": "Test Company",
        "phone": "+1 (555) 123-4567",
        "subject": "demo",
        "message": f"This is an automated test submission at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    
    print("📤 Sending test submission...")
    print(f"   Data: {json.dumps(test_data, indent=6)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/contact",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:3000"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Form submission successful!")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Submission ID: {data.get('submission_id')}")
            print(f"\n💡 Check your backend terminal - you should see the formatted log!")
            return True
        else:
            print(f"\n❌ Submission failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              🧪 FRONTEND-BACKEND CONNECTION TEST                           ║
║                                                                            ║
║  This script tests the complete connection between frontend and backend   ║
║  for the contact form functionality.                                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    
    results = []
    
    # Run all tests
    results.append(("Backend Server", test_backend_health()))
    if results[-1][1]:  # Only continue if backend is running
        results.append(("Contact Endpoint", test_contact_endpoint()))
        results.append(("CORS Configuration", test_cors()))
        results.append(("Form Submission", test_form_submission()))
    
    # Print summary
    print_section("📊 TEST SUMMARY")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}  {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 80)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour contact form is fully connected and working!")
        print("\n📋 Next Steps:")
        print("   1. Go to http://localhost:3000/contact")
        print("   2. Fill out and submit the form")
        print("   3. Watch your backend terminal for the formatted log")
        print("   4. Check browser console (F12) for success message")
        print("   5. Check Network tab for 200 OK response")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure backend is running: python main.py")
        print("   2. Make sure frontend is running: npm run dev")
        print("   3. Check for errors in backend terminal")
        print("   4. Try restarting both servers")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()

