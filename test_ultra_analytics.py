#!/usr/bin/env python3
"""
Ultra Enhanced Analytics Testing Suite
Tests all new ultra analytics endpoints and validates responses
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List

class UltraAnalyticsTestSuite:
    def __init__(self, base_url: str = "http://localhost:8002/api"):
        self.base_url = base_url
        self.test_results = []
        
    def run_all_tests(self):
        """Run complete test suite for ultra analytics"""
        print("🚀 Starting Ultra Enhanced Analytics Test Suite")
        print("=" * 60)
        
        # Test each endpoint
        tests = [
            self.test_health_check,
            self.test_multi_dimensional_analytics,
            self.test_predictive_analytics,
            self.test_cognitive_insights,
            self.test_optimization_engine,
            self.test_strategic_dashboard,
            self.test_innovation_opportunities
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                self.log_error(test.__name__, str(e))
        
        self.print_summary()
    
    def test_health_check(self):
        """Test ultra analytics health check"""
        print("🔍 Testing Health Check Endpoint...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/health-check")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Health Check", {
                "status": data.get("status"),
                "service": data.get("service"),
                "version": data.get("version"),
                "capabilities_count": len(data.get("capabilities", []))
            })
        else:
            self.log_error("Health Check", f"Status: {response.status_code}")
    
    def test_multi_dimensional_analytics(self):
        """Test multi-dimensional business intelligence"""
        print("🧠 Testing Multi-Dimensional Analytics...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/multi-dimensional")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Multi-Dimensional Analytics", {
                "success": data.get("success"),
                "analysis_type": data.get("analysis_type"),
                "confidence_score": data.get("confidence_score"),
                "recommendations_count": len(data.get("recommendations", []))
            })
        else:
            self.log_error("Multi-Dimensional Analytics", f"Status: {response.status_code}")
    
    def test_predictive_analytics(self):
        """Test predictive business intelligence"""
        print("🔮 Testing Predictive Analytics...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/predictive?horizon=6")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Predictive Analytics", {
                "success": data.get("success"),
                "trends_count": len(data.get("trends", [])),
                "growth_rate": data.get("predictions", {}).get("growth_rate"),
                "business_impact": data.get("business_impact", {})
            })
        else:
            self.log_error("Predictive Analytics", f"Status: {response.status_code}")
    
    def test_cognitive_insights(self):
        """Test cognitive business insights"""
        print("🧩 Testing Cognitive Insights...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/cognitive?focus_area=strategic")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Cognitive Insights", {
                "success": data.get("success"),
                "strategic_insights_count": len(data.get("strategic_insights", [])),
                "innovation_opportunities_count": len(data.get("innovation_opportunities", [])),
                "overall_risk": data.get("risk_assessment", {}).get("overall_risk")
            })
        else:
            self.log_error("Cognitive Insights", f"Status: {response.status_code}")
    
    def test_optimization_engine(self):
        """Test AI optimization engine"""
        print("⚙️ Testing Optimization Engine...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/optimization-engine?scope=full_warehouse")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Optimization Engine", {
                "success": data.get("success"),
                "recommendations_count": len(data.get("recommendations", [])),
                "efficiency_gain": data.get("impact_analysis", {}).get("efficiency_gain"),
                "roi_year_1": data.get("roi_projections", {}).get("year_1")
            })
        else:
            self.log_error("Optimization Engine", f"Status: {response.status_code}")
    
    def test_strategic_dashboard(self):
        """Test strategic intelligence dashboard"""
        print("📊 Testing Strategic Dashboard...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/strategic-dashboard")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Strategic Dashboard", {
                "success": data.get("success"),
                "dashboard_type": data.get("dashboard_type"),
                "business_health_score": data.get("executive_summary", {}).get("business_health_score"),
                "growth_trajectory": data.get("executive_summary", {}).get("growth_trajectory"),
                "optimization_potential": data.get("executive_summary", {}).get("optimization_potential")
            })
        else:
            self.log_error("Strategic Dashboard", f"Status: {response.status_code}")
    
    def test_innovation_opportunities(self):
        """Test innovation opportunities analysis"""
        print("💡 Testing Innovation Opportunities...")
        
        response = requests.get(f"{self.base_url}/analytics/ultra/innovation-opportunities?sector=all")
        
        if response.status_code == 200:
            data = response.json()
            self.log_success("Innovation Opportunities", {
                "success": data.get("success"),
                "analysis_scope": data.get("analysis_scope"),
                "innovation_opportunities_count": len(data.get("innovation_opportunities", [])),
                "emerging_technologies_count": len(data.get("emerging_technologies", [])),
                "market_disruption_alerts_count": len(data.get("market_disruption_alerts", []))
            })
        else:
            self.log_error("Innovation Opportunities", f"Status: {response.status_code}")
    
    def log_success(self, test_name: str, details: Dict):
        """Log successful test result"""
        self.test_results.append({
            "test": test_name,
            "status": "✅ PASS",
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"   ✅ {test_name}: PASSED")
        for key, value in details.items():
            print(f"      • {key}: {value}")
    
    def log_error(self, test_name: str, error: str):
        """Log failed test result"""
        self.test_results.append({
            "test": test_name,
            "status": "❌ FAIL",
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        print(f"   ❌ {test_name}: FAILED - {error}")
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.test_results if "PASS" in r["status"]])
        failed = len([r for r in self.test_results if "FAIL" in r["status"]])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "FAIL" in result["status"]:
                    print(f"   • {result['test']}: {result.get('error', 'Unknown error')}")
        
        # Save detailed results
        with open('ultra_analytics_test_results.json', 'w') as f:
            json.dump({
                "summary": {
                    "total_tests": total,
                    "passed": passed,
                    "failed": failed,
                    "success_rate": f"{(passed/total*100):.1f}%",
                    "test_date": datetime.now().isoformat()
                },
                "detailed_results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: ultra_analytics_test_results.json")


def test_frontend_integration():
    """Test frontend integration with ultra analytics"""
    print("\n🌐 Testing Frontend Integration...")
    print("=" * 60)
    
    # Test that the ultra intelligence dashboard can be opened
    dashboard_path = "/Users/sammyboy/Downloads/code proj del/frontend/ultra_intelligence_dashboard.html"
    
    try:
        with open(dashboard_path, 'r') as f:
            content = f.read()
            
        # Check for key components
        checks = [
            ("Ultra Intelligence Dashboard title", "Ultra Intelligence Dashboard" in content),
            ("Strategic Intelligence tab", "Strategic Intelligence" in content),
            ("Predictive Analytics tab", "Predictive Analytics" in content),
            ("Cognitive Insights tab", "Cognitive Insights" in content),
            ("Innovation Lab tab", "Innovation Lab" in content),
            ("AI Optimization tab", "AI Optimization" in content),
            ("Chart.js integration", "chart.js" in content),
            ("Plotly integration", "plotly" in content),
            ("API integration", "analytics/ultra" in content)
        ]
        
        print("Frontend Component Checks:")
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
        
        passed_checks = sum(1 for _, result in checks if result)
        print(f"\nFrontend Integration: {passed_checks}/{len(checks)} checks passed")
        
    except FileNotFoundError:
        print("❌ Ultra Intelligence Dashboard file not found")


if __name__ == "__main__":
    print("🧪 Ultra Enhanced Analytics - Complete Test Suite")
    print("🕒 Test started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Test backend API
    test_suite = UltraAnalyticsTestSuite()
    test_suite.run_all_tests()
    
    # Test frontend integration
    test_frontend_integration()
    
    print("\n🎉 Testing completed!")
    print("📋 Check the generated test results file for detailed analysis.")
