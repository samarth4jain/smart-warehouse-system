#!/usr/bin/env python3
"""
Test GitHub Pages Deployment of Smart Warehouse Management System
"""

import requests
from urllib.parse import urljoin
import time

BASE_URL = "https://samarth4jain.github.io/smart-warehouse-system/"

def test_github_pages_deployment():
    """Test the GitHub Pages deployment comprehensively"""
    print("🌐 TESTING GITHUB PAGES DEPLOYMENT")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Test main pages
    pages_to_test = [
        ("", "Main Landing Page"),
        ("dashboard.html", "Dashboard Interface"),
        ("chatbot.html", "Chatbot Interface"),
        ("analytics.html", "Analytics Dashboard"),
        ("api-docs.html", "API Documentation"),
        ("index.html", "Index Page"),
    ]
    
    results = {}
    
    for path, name in pages_to_test:
        url = urljoin(BASE_URL, path)
        print(f"\n🧪 Testing: {name}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code} - Working")
                
                # Check for specific content
                content = response.text.lower()
                
                # Check for warehouse-related content
                warehouse_keywords = [
                    "warehouse", "inventory", "chatbot", "assistant", 
                    "smart", "management", "dashboard"
                ]
                
                found_keywords = [kw for kw in warehouse_keywords if kw in content]
                print(f"📝 Content Keywords Found: {', '.join(found_keywords[:5])}")
                
                # Check for interactive elements
                interactive_elements = [
                    "onclick", "onsubmit", "addEventListener", "function",
                    "chat", "input", "button"
                ]
                
                found_interactive = [el for el in interactive_elements if el in content]
                print(f"🎮 Interactive Elements: {', '.join(found_interactive[:3])}")
                
                # Check content length as quality indicator
                content_length = len(response.text)
                print(f"📊 Content Size: {content_length:,} characters")
                
                results[name] = {
                    "status": "✅ Working",
                    "status_code": response.status_code,
                    "content_length": content_length,
                    "keywords": found_keywords,
                    "interactive": found_interactive
                }
                
            else:
                print(f"❌ Status: {response.status_code} - Error")
                results[name] = {
                    "status": "❌ Error",
                    "status_code": response.status_code,
                    "content_length": 0,
                    "keywords": [],
                    "interactive": []
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Failed: {e}")
            results[name] = {
                "status": "❌ Failed",
                "error": str(e),
                "content_length": 0,
                "keywords": [],
                "interactive": []
            }
        
        time.sleep(0.5)  # Be respectful to GitHub Pages
    
    return results

def analyze_chatbot_capability(url):
    """Analyze the chatbot interface specifically"""
    print(f"\n🤖 ANALYZING CHATBOT INTERFACE")
    print("=" * 60)
    
    try:
        response = requests.get(urljoin(BASE_URL, "chatbot.html"), timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Check for enhanced features
            enhanced_features = [
                "enhanced natural language",
                "fuzzy search", 
                "context-aware",
                "advanced nlp",
                "smart understanding"
            ]
            
            found_enhanced = [f for f in enhanced_features if f.lower() in content.lower()]
            
            # Check for chatbot functionality
            chatbot_features = [
                "message", "chat", "input", "send", "response",
                "assistant", "help", "query", "api"
            ]
            
            found_chatbot = [f for f in chatbot_features if f.lower() in content.lower()]
            
            # Check for API integration
            api_patterns = [
                "fetch(", "axios", "XMLHttpRequest", "api/chat", "/api/",
                "json", "post", "get"
            ]
            
            found_api = [p for p in api_patterns if p.lower() in content.lower()]
            
            print(f"🧠 Enhanced NLP Features: {found_enhanced or 'None detected'}")
            print(f"💬 Chatbot Features: {', '.join(found_chatbot[:5])}")
            print(f"🔗 API Integration: {', '.join(found_api[:3]) if found_api else 'Static chatbot (no backend)'}")
            
            # Determine chatbot type
            if found_api:
                chatbot_type = "🚀 Dynamic (API-connected)"
            else:
                chatbot_type = "📄 Static (Demo/Mock responses)"
            
            print(f"🤖 Chatbot Type: {chatbot_type}")
            
            return {
                "enhanced_features": found_enhanced,
                "chatbot_features": found_chatbot,
                "api_integration": found_api,
                "type": chatbot_type
            }
        else:
            print(f"❌ Could not access chatbot page: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error analyzing chatbot: {e}")
        return None

def test_responsive_design():
    """Test if the site is mobile-responsive"""
    print(f"\n📱 TESTING RESPONSIVE DESIGN")
    print("=" * 60)
    
    try:
        # Test with mobile user agent
        mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        }
        
        response = requests.get(BASE_URL, headers=mobile_headers, timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            
            responsive_indicators = [
                "viewport", "responsive", "mobile", "@media",
                "flex", "grid", "meta name=\"viewport\""
            ]
            
            found_responsive = [r for r in responsive_indicators if r in content]
            
            print(f"📱 Responsive Features: {', '.join(found_responsive)}")
            
            if found_responsive:
                print("✅ Site appears to be mobile-responsive")
                return True
            else:
                print("⚠️ Limited responsive design detected")
                return False
        else:
            print(f"❌ Could not test mobile responsiveness: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing responsiveness: {e}")
        return False

def generate_deployment_report(results, chatbot_analysis, responsive):
    """Generate a comprehensive deployment report"""
    print(f"\n📊 GITHUB PAGES DEPLOYMENT REPORT")
    print("=" * 80)
    
    # Overall status
    working_pages = sum(1 for r in results.values() if "✅" in r["status"])
    total_pages = len(results)
    success_rate = (working_pages / total_pages) * 100
    
    print(f"🎯 Overall Status: {working_pages}/{total_pages} pages working ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("✅ Deployment Status: HEALTHY")
    elif success_rate >= 60:
        print("⚠️ Deployment Status: PARTIAL")
    else:
        print("❌ Deployment Status: ISSUES DETECTED")
    
    print(f"\n📄 Page Status Summary:")
    for name, result in results.items():
        status = result["status"]
        size = result.get("content_length", 0)
        print(f"  {status} {name} ({size:,} chars)")
    
    print(f"\n🤖 Chatbot Analysis:")
    if chatbot_analysis:
        print(f"  Type: {chatbot_analysis['type']}")
        if chatbot_analysis['enhanced_features']:
            print(f"  Enhanced Features: {', '.join(chatbot_analysis['enhanced_features'])}")
        else:
            print(f"  Enhanced Features: None (Standard chatbot)")
        
        if chatbot_analysis['api_integration']:
            print(f"  Backend Integration: Detected")
        else:
            print(f"  Backend Integration: Static/Demo only")
    else:
        print(f"  Status: Could not analyze")
    
    print(f"\n📱 Mobile Support:")
    if responsive:
        print(f"  ✅ Responsive design detected")
    else:
        print(f"  ⚠️ Limited mobile optimization")
    
    print(f"\n🌐 Access Information:")
    print(f"  Primary URL: {BASE_URL}")
    print(f"  Chatbot: {urljoin(BASE_URL, 'chatbot.html')}")
    print(f"  Dashboard: {urljoin(BASE_URL, 'dashboard.html')}")
    print(f"  Analytics: {urljoin(BASE_URL, 'analytics.html')}")
    
    print(f"\n💡 Recommendations:")
    if success_rate == 100:
        print(f"  🎉 Perfect deployment! All pages accessible.")
    else:
        print(f"  🔧 Check failed pages and fix any broken links.")
    
    if not chatbot_analysis or not chatbot_analysis.get('api_integration'):
        print(f"  📝 Note: GitHub Pages hosts static files only.")
        print(f"  🚀 For full backend functionality, use local server or cloud deployment.")
    
    print(f"\n🎯 Deployment Type:")
    print(f"  📄 Static Website (GitHub Pages)")
    print(f"  🎮 Interactive Frontend with Demo Data")
    print(f"  💡 Perfect for showcasing and user testing")

def main():
    """Main test function"""
    print("🚀 GITHUB PAGES DEPLOYMENT TEST")
    print("Smart Warehouse Management System")
    print("=" * 80)
    
    # Test all pages
    results = test_github_pages_deployment()
    
    # Analyze chatbot specifically
    chatbot_analysis = analyze_chatbot_capability(BASE_URL)
    
    # Test responsive design
    responsive = test_responsive_design()
    
    # Generate comprehensive report
    generate_deployment_report(results, chatbot_analysis, responsive)
    
    print(f"\n✨ Test Complete! Visit {BASE_URL} to explore the deployed system.")

if __name__ == "__main__":
    main()
