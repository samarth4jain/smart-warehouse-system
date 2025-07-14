#!/usr/bin/env python3
"""
GitHub Pages Deployment Verification Script
Tests if the Smart Warehouse System is properly deployed on GitHub Pages
"""

import requests
import time
import sys
from urllib.parse import urljoin

# GitHub Pages URL (replace with your actual username/repo)
BASE_URL = "https://samarth4jain.github.io/smart-warehouse-system/"

# Test endpoints
ENDPOINTS_TO_TEST = [
    "",  # Landing page
    "chatbot.html",  # Chatbot interface
    "enterprise_dashboard.html",  # Enterprise dashboard
    "advanced_dashboard.html",  # Advanced dashboard
    "docs/index.html",  # Documentation
]

def test_endpoint(url):
    """Test if an endpoint is accessible"""
    try:
        print(f"🔍 Testing: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS: {url} (Status: {response.status_code})")
            return True
        else:
            print(f"❌ FAILED: {url} (Status: {response.status_code})")
            return False
            
    except requests.RequestException as e:
        print(f"❌ ERROR: {url} - {str(e)}")
        return False

def main():
    print("🚀 GitHub Pages Deployment Verification")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Wait a moment for GitHub Pages to process
    print("⏳ Waiting for GitHub Pages to process deployment...")
    time.sleep(5)
    
    success_count = 0
    total_tests = len(ENDPOINTS_TO_TEST)
    
    for endpoint in ENDPOINTS_TO_TEST:
        full_url = urljoin(BASE_URL, endpoint)
        if test_endpoint(full_url):
            success_count += 1
        time.sleep(1)  # Be nice to GitHub's servers
    
    print("=" * 60)
    print(f"📊 Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! GitHub Pages deployment successful!")
        print(f"🌐 Your Smart Warehouse System is live at: {BASE_URL}")
        return 0
    else:
        print("⚠️  Some tests failed. GitHub Pages might still be processing...")
        print("💡 Try again in a few minutes, GitHub Pages can take 5-10 minutes to deploy.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
