#!/usr/bin/env python3
"""
Advanced Production Validation Suite
Comprehensive testing and validation for commercial deployment
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

class ProductionValidator:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        self.performance_metrics = []
        
    def test_endpoint(self, endpoint: str, method: str = "GET", data: dict = None, 
                     expected_status: int = 200, test_name: str = "") -> Dict[str, Any]:
        """Test an API endpoint with comprehensive validation"""
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # ms
            
            result = {
                "endpoint": endpoint,
                "method": method,
                "test_name": test_name or f"{method} {endpoint}",
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_time_ms": round(response_time, 2),
                "success": response.status_code == expected_status,
                "response_size": len(response.text) if response.text else 0,
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to parse JSON response
            try:
                result["response_data"] = response.json()
            except:
                result["response_text"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
            self.test_results.append(result)
            self.performance_metrics.append(response_time)
            
            return result
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "test_name": test_name or f"{method} {endpoint}",
                "error": str(e),
                "success": False,
                "response_time_ms": 0,
                "timestamp": datetime.now().isoformat()
            }
            self.test_results.append(result)
            return result
    
    def validate_core_system(self):
        """Validate core system functionality"""
        print("🔍 VALIDATING CORE SYSTEM...")
        
        # Health check
        result = self.test_endpoint("/health", test_name="System Health Check")
        if result["success"]:
            print("✅ Health Check: PASSED")
        else:
            print("❌ Health Check: FAILED")
        
        # API documentation
        result = self.test_endpoint("/docs", test_name="API Documentation")
        if result["success"]:
            print("✅ API Documentation: ACCESSIBLE")
        else:
            print("❌ API Documentation: INACCESSIBLE")
        
        # Database connectivity (through inventory)
        result = self.test_endpoint("/api/inventory/products", test_name="Database Connectivity")
        if result["success"]:
            print("✅ Database Connectivity: HEALTHY")
        else:
            print("❌ Database Connectivity: FAILED")
    
    def validate_inventory_management(self):
        """Validate inventory management features"""
        print("\n📦 VALIDATING INVENTORY MANAGEMENT...")
        
        endpoints = [
            ("/api/inventory/products", "Product Listing"),
            ("/api/inventory/low-stock", "Low Stock Detection"),
            ("/api/inventory/stock-levels", "Stock Level Tracking"),
            ("/api/inventory/search?query=PROD", "Product Search")
        ]
        
        for endpoint, name in endpoints:
            result = self.test_endpoint(endpoint, test_name=name)
            if result["success"]:
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
    
    def validate_commercial_features(self):
        """Validate commercial enterprise features"""
        print("\n🏢 VALIDATING COMMERCIAL FEATURES...")
        
        endpoints = [
            ("/api/commercial/health", "Commercial Health Check"),
            ("/api/commercial/executive-dashboard", "Executive Dashboard"),
            ("/api/commercial/financial-metrics", "Financial Metrics"),
            ("/api/commercial/analytics/abc-analysis", "ABC Analysis"),
            ("/api/commercial/analytics/velocity-analysis", "Velocity Analysis"),
            ("/api/commercial/qr-codes", "QR Code Management"),
            ("/api/commercial/kpi/real-time", "Real-time KPIs"),
            ("/api/commercial/compliance/report", "Compliance Reporting")
        ]
        
        for endpoint, name in endpoints:
            result = self.test_endpoint(endpoint, test_name=name)
            if result["success"]:
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
    
    def validate_ai_chatbot(self):
        """Validate AI chatbot functionality"""
        print("\n🤖 VALIDATING AI CHATBOT...")
        
        test_messages = [
            "Hello, what can you help me with?",
            "Show me current inventory levels",
            "What items are running low?",
            "Help me understand the system",
            "What's the status of product PROD001?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            result = self.test_endpoint(
                "/api/chat/message",
                method="POST",
                data={"message": message},
                test_name=f"Chatbot Query {i}"
            )
            if result["success"]:
                print(f"✅ Chatbot Query {i}: PASSED")
            else:
                print(f"❌ Chatbot Query {i}: FAILED")
    
    def validate_advanced_analytics(self):
        """Validate advanced analytics features"""
        print("\n📊 VALIDATING ADVANCED ANALYTICS...")
        
        endpoints = [
            ("/api/dashboard/overview", "Dashboard Overview"),
            ("/api/phase3/health", "Phase 3 Health"),
            ("/api/phase3/forecast/all-products", "Demand Forecasting"),
            ("/api/phase3/space/analyze-velocity", "Space Analysis"),
            ("/api/analytics/ultra/health-check", "Ultra Analytics Health")
        ]
        
        for endpoint, name in endpoints:
            result = self.test_endpoint(endpoint, test_name=name)
            if result["success"]:
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
    
    def validate_frontend_interfaces(self):
        """Validate frontend interface accessibility"""
        print("\n🌐 VALIDATING FRONTEND INTERFACES...")
        
        interfaces = [
            ("/", "Main Dashboard"),
            ("/chatbot", "Chatbot Interface"),
            ("/advanced-dashboard", "Advanced Dashboard"),
            ("/enterprise-dashboard", "Enterprise Dashboard"),
            ("/commercial-intelligence-dashboard", "Commercial Intelligence")
        ]
        
        for endpoint, name in interfaces:
            result = self.test_endpoint(endpoint, test_name=name)
            if result["success"]:
                print(f"✅ {name}: ACCESSIBLE")
            else:
                print(f"❌ {name}: INACCESSIBLE")
    
    def performance_analysis(self):
        """Analyze system performance"""
        print("\n⚡ PERFORMANCE ANALYSIS...")
        
        if not self.performance_metrics:
            print("❌ No performance data available")
            return
        
        avg_response = sum(self.performance_metrics) / len(self.performance_metrics)
        min_response = min(self.performance_metrics)
        max_response = max(self.performance_metrics)
        
        print(f"📊 Average Response Time: {avg_response:.2f}ms")
        print(f"⚡ Fastest Response: {min_response:.2f}ms")
        print(f"🐌 Slowest Response: {max_response:.2f}ms")
        
        # Performance rating
        if avg_response < 100:
            print("🏆 Performance Rating: EXCELLENT")
        elif avg_response < 500:
            print("👍 Performance Rating: GOOD")
        elif avg_response < 1000:
            print("⚠️  Performance Rating: ACCEPTABLE")
        else:
            print("🐌 Performance Rating: NEEDS IMPROVEMENT")
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        successful_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Categorize results
        categories = {
            "Core System": 0,
            "Inventory Management": 0,
            "Commercial Features": 0,
            "AI Chatbot": 0,
            "Advanced Analytics": 0,
            "Frontend Interfaces": 0
        }
        
        category_totals = categories.copy()
        
        for result in self.test_results:
            test_name = result.get("test_name", "")
            if "Health" in test_name or "Documentation" in test_name or "Database" in test_name:
                category_totals["Core System"] += 1
                if result["success"]:
                    categories["Core System"] += 1
            elif "inventory" in result.get("endpoint", "").lower():
                category_totals["Inventory Management"] += 1
                if result["success"]:
                    categories["Inventory Management"] += 1
            elif "commercial" in result.get("endpoint", "").lower():
                category_totals["Commercial Features"] += 1
                if result["success"]:
                    categories["Commercial Features"] += 1
            elif "chat" in result.get("endpoint", "").lower():
                category_totals["AI Chatbot"] += 1
                if result["success"]:
                    categories["AI Chatbot"] += 1
            elif "phase3" in result.get("endpoint", "").lower() or "analytics" in result.get("endpoint", "").lower():
                category_totals["Advanced Analytics"] += 1
                if result["success"]:
                    categories["Advanced Analytics"] += 1
            else:
                category_totals["Frontend Interfaces"] += 1
                if result["success"]:
                    categories["Frontend Interfaces"] += 1
        
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "overall_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate": round(success_rate, 1)
            },
            "category_results": {},
            "performance_metrics": {
                "avg_response_time_ms": round(sum(self.performance_metrics) / len(self.performance_metrics), 2) if self.performance_metrics else 0,
                "min_response_time_ms": round(min(self.performance_metrics), 2) if self.performance_metrics else 0,
                "max_response_time_ms": round(max(self.performance_metrics), 2) if self.performance_metrics else 0
            },
            "detailed_results": self.test_results
        }
        
        # Add category success rates
        for category, passed in categories.items():
            total = category_totals[category]
            rate = (passed / total * 100) if total > 0 else 0
            report["category_results"][category] = {
                "passed": passed,
                "total": total,
                "success_rate": round(rate, 1)
            }
        
        return report
    
    def print_summary_report(self, report: Dict[str, Any]):
        """Print formatted summary report"""
        print("\n" + "="*80)
        print("🎯 PRODUCTION VALIDATION SUMMARY REPORT")
        print("="*80)
        
        overall = report["overall_summary"]
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Tests: {overall['total_tests']}")
        print(f"   Successful: {overall['successful_tests']}")
        print(f"   Failed: {overall['failed_tests']}")
        print(f"   Success Rate: {overall['success_rate']}%")
        
        # Overall status
        if overall["success_rate"] >= 95:
            status = "🟢 PRODUCTION READY"
        elif overall["success_rate"] >= 85:
            status = "🟡 MOSTLY READY (minor issues)"
        elif overall["success_rate"] >= 70:
            status = "🟠 NEEDS ATTENTION"
        else:
            status = "🔴 NOT READY"
        
        print(f"\n🎯 PRODUCTION STATUS: {status}")
        
        print(f"\n📂 CATEGORY BREAKDOWN:")
        for category, results in report["category_results"].items():
            rate = results["success_rate"]
            if rate == 100:
                emoji = "✅"
            elif rate >= 80:
                emoji = "⚠️"
            else:
                emoji = "❌"
            print(f"   {emoji} {category}: {results['passed']}/{results['total']} ({rate}%)")
        
        perf = report["performance_metrics"]
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   Average Response: {perf['avg_response_time_ms']}ms")
        print(f"   Fastest: {perf['min_response_time_ms']}ms")
        print(f"   Slowest: {perf['max_response_time_ms']}ms")
        
        print(f"\n⏰ Validation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def run_full_validation(self):
        """Run complete production validation suite"""
        print("🚀 STARTING COMPREHENSIVE PRODUCTION VALIDATION")
        print("="*60)
        
        start_time = time.time()
        
        # Run all validation categories
        self.validate_core_system()
        self.validate_inventory_management()
        self.validate_commercial_features()
        self.validate_ai_chatbot()
        self.validate_advanced_analytics()
        self.validate_frontend_interfaces()
        
        # Performance analysis
        self.performance_analysis()
        
        # Generate and display report
        report = self.generate_validation_report()
        self.print_summary_report(report)
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"production_validation_report_{timestamp}.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📝 Detailed report saved to: {report_file}")
        except Exception as e:
            print(f"⚠️  Could not save report: {e}")
        
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print(f"⏱️  Total validation time: {total_time} seconds")
        
        return report

def main():
    """Main validation function"""
    import argparse
    parser = argparse.ArgumentParser(description="Smart Warehouse Production Validator")
    parser.add_argument("--url", default="http://localhost:8001", help="Base URL for the system")
    parser.add_argument("--quick", action="store_true", help="Run quick validation (core features only)")
    
    args = parser.parse_args()
    
    validator = ProductionValidator(args.url)
    
    if args.quick:
        print("🔍 RUNNING QUICK VALIDATION...")
        validator.validate_core_system()
        validator.validate_inventory_management()
        validator.performance_analysis()
        
        report = validator.generate_validation_report()
        validator.print_summary_report(report)
    else:
        validator.run_full_validation()

if __name__ == "__main__":
    main()
