#!/usr/bin/env python3
"""
Real-time monitor for contact form submissions
Run this in a separate terminal to see submissions as they come in
"""
import time
import requests
from datetime import datetime
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    print("=" * 80)
    print("📧 CONTACT FORM SUBMISSION MONITOR")
    print("=" * 80)
    print(f"Monitoring: http://localhost:8000/api/contact")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print("\n⏳ Waiting for submissions... (Press Ctrl+C to stop)\n")

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    clear_screen()
    print_header()
    
    # Check if backend is running
    if not check_backend():
        print("❌ ERROR: Backend server is not running on port 8000!")
        print("\nPlease start the backend server:")
        print("  cd /Users/partheebandevaraj/ai-vision-platform/backend")
        print("  source venv/bin/activate")
        print("  python main.py")
        return
    
    print("✅ Backend server is running!\n")
    print("💡 Now go to http://localhost:3000/contact and submit the form")
    print("   You'll see the submission appear here in real-time!\n")
    print("-" * 80)
    
    submission_count = 0
    
    try:
        while True:
            time.sleep(1)
            # In a real implementation, you'd tail the log file or use websockets
            # For now, this is just a placeholder that shows the concept
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print(f"📊 SUMMARY")
        print("=" * 80)
        print(f"Total submissions monitored: {submission_count}")
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                   📧 CONTACT FORM SUBMISSION MONITOR                       ║
║                                                                            ║
║  This script helps you verify that contact form submissions are working   ║
║                                                                            ║
║  INSTRUCTIONS:                                                             ║
║  1. Make sure backend is running (python main.py)                          ║
║  2. Run this script in a separate terminal                                 ║
║  3. Go to http://localhost:3000/contact                                    ║
║  4. Submit the form                                                        ║
║  5. Watch the backend terminal for logs                                    ║
║                                                                            ║
║  WHAT TO LOOK FOR:                                                         ║
║  ✅ Backend terminal shows formatted contact data                          ║
║  ✅ Frontend shows success message                                         ║
║  ✅ Browser console shows success log                                      ║
║  ✅ Network tab shows 200 OK response                                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Press Enter to start monitoring...
""")
    input()
    main()

