#!/usr/bin/env python3
"""
Comprehensive Production Monitoring System
Real-time monitoring of Smart Warehouse Management System
"""

import requests
import json
import time
import psutil
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import signal
import sys

class ProductionMonitor:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.monitoring = True
        self.metrics_history = []
        self.alert_thresholds = {
            "response_time_ms": 2000,
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "error_rate": 5.0
        }
        
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        try:
            # System resource metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network metrics
            network = psutil.net_io_counters()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory.percent,
                    "memory_available_mb": memory.available / (1024 * 1024),
                    "disk_usage": disk.percent,
                    "disk_free_gb": disk.free / (1024 * 1024 * 1024),
                    "network_bytes_sent": network.bytes_sent,
                    "network_bytes_recv": network.bytes_recv
                }
            }
        except Exception as e:
            return {"timestamp": datetime.now().isoformat(), "system_error": str(e)}
    
    def test_api_endpoints(self) -> Dict[str, Any]:
        """Test critical API endpoints and measure performance"""
        endpoints = [
            "/health",
            "/api/inventory/products",
            "/api/dashboard/overview",
            "/api/chat/message",
            "/api/commercial/health",
            "/api/commercial/analytics/abc-analysis",
            "/api/commercial/qr-codes",
            "/api/phase3/health",
            "/docs"
        ]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": {},
            "summary": {
                "total_tested": len(endpoints),
                "successful": 0,
                "failed": 0,
                "avg_response_time": 0
            }
        }
        
        total_response_time = 0
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                
                if endpoint == "/api/chat/message":
                    # POST request for chatbot
                    response = requests.post(
                        f"{self.base_url}{endpoint}",
                        json={"message": "health check"},
                        timeout=10
                    )
                else:
                    # GET request
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # ms
                total_response_time += response_time
                
                results["endpoints"][endpoint] = {
                    "status_code": response.status_code,
                    "response_time_ms": round(response_time, 2),
                    "success": response.status_code == 200,
                    "response_size": len(response.text) if response.text else 0
                }
                
                if response.status_code == 200:
                    results["summary"]["successful"] += 1
                else:
                    results["summary"]["failed"] += 1
                    
            except Exception as e:
                results["endpoints"][endpoint] = {
                    "error": str(e),
                    "success": False,
                    "response_time_ms": 0
                }
                results["summary"]["failed"] += 1
        
        if results["summary"]["total_tested"] > 0:
            results["summary"]["avg_response_time"] = round(
                total_response_time / results["summary"]["total_tested"], 2
            )
            results["summary"]["success_rate"] = round(
                (results["summary"]["successful"] / results["summary"]["total_tested"]) * 100, 1
            )
        
        return results
    
    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and health"""
        try:
            db_path = "backend/smart_warehouse.db"
            if not os.path.exists(db_path):
                db_path = "smart_warehouse.db"
            
            if not os.path.exists(db_path):
                return {
                    "timestamp": datetime.now().isoformat(),
                    "database": {
                        "status": "error",
                        "error": "Database file not found"
                    }
                }
            
            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            
            # Basic connectivity test
            cursor.execute("SELECT 1")
            
            # Get table info
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Get record counts for key tables
            table_counts = {}
            for table in ["products", "inventory", "stock_movements", "chat_messages"]:
                if table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        table_counts[table] = cursor.fetchone()[0]
                    except:
                        table_counts[table] = "error"
            
            conn.close()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "database": {
                    "status": "healthy",
                    "tables_count": len(tables),
                    "tables": tables,
                    "record_counts": table_counts,
                    "file_size_mb": round(os.path.getsize(db_path) / (1024 * 1024), 2)
                }
            }
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "database": {
                    "status": "error",
                    "error": str(e)
                }
            }
    
    def analyze_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze metrics and generate alerts"""
        alerts = []
        timestamp = datetime.now().isoformat()
        
        # System resource alerts
        if "system" in metrics:
            system = metrics["system"]
            
            if system.get("cpu_usage", 0) > self.alert_thresholds["cpu_usage"]:
                alerts.append({
                    "timestamp": timestamp,
                    "level": "warning",
                    "type": "system",
                    "message": f"High CPU usage: {system['cpu_usage']:.1f}%",
                    "value": system["cpu_usage"],
                    "threshold": self.alert_thresholds["cpu_usage"]
                })
            
            if system.get("memory_usage", 0) > self.alert_thresholds["memory_usage"]:
                alerts.append({
                    "timestamp": timestamp,
                    "level": "warning",
                    "type": "system",
                    "message": f"High memory usage: {system['memory_usage']:.1f}%",
                    "value": system["memory_usage"],
                    "threshold": self.alert_thresholds["memory_usage"]
                })
            
            if system.get("disk_usage", 0) > self.alert_thresholds["disk_usage"]:
                alerts.append({
                    "timestamp": timestamp,
                    "level": "critical",
                    "type": "system",
                    "message": f"High disk usage: {system['disk_usage']:.1f}%",
                    "value": system["disk_usage"],
                    "threshold": self.alert_thresholds["disk_usage"]
                })
        
        # API performance alerts
        if "api_test" in metrics and "summary" in metrics["api_test"]:
            api_summary = metrics["api_test"]["summary"]
            
            if api_summary.get("avg_response_time", 0) > self.alert_thresholds["response_time_ms"]:
                alerts.append({
                    "timestamp": timestamp,
                    "level": "warning",
                    "type": "performance",
                    "message": f"Slow API response: {api_summary['avg_response_time']:.1f}ms",
                    "value": api_summary["avg_response_time"],
                    "threshold": self.alert_thresholds["response_time_ms"]
                })
            
            if api_summary.get("success_rate", 100) < (100 - self.alert_thresholds["error_rate"]):
                alerts.append({
                    "timestamp": timestamp,
                    "level": "critical",
                    "type": "api",
                    "message": f"High API error rate: {100 - api_summary['success_rate']:.1f}%",
                    "value": 100 - api_summary["success_rate"],
                    "threshold": self.alert_thresholds["error_rate"]
                })
        
        return alerts
    
    def generate_health_report(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        alerts = self.analyze_alerts(metrics)
        
        # Calculate overall health score
        health_score = 100
        
        # Deduct points for system issues
        if "system" in metrics:
            system = metrics["system"]
            if system.get("cpu_usage", 0) > 70:
                health_score -= 10
            if system.get("memory_usage", 0) > 80:
                health_score -= 15
            if system.get("disk_usage", 0) > 85:
                health_score -= 20
        
        # Deduct points for API issues
        if "api_test" in metrics and "summary" in metrics["api_test"]:
            api_summary = metrics["api_test"]["summary"]
            success_rate = api_summary.get("success_rate", 100)
            if success_rate < 95:
                health_score -= (100 - success_rate) * 2
        
        # Deduct points for database issues
        if "database" in metrics and metrics["database"].get("status") != "healthy":
            health_score -= 30
        
        health_score = max(0, health_score)
        
        # Determine health status
        if health_score >= 90:
            health_status = "excellent"
        elif health_score >= 75:
            health_status = "good"
        elif health_score >= 50:
            health_status = "warning"
        else:
            health_status = "critical"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": health_status,
            "alerts_count": len(alerts),
            "alerts": alerts,
            "recommendations": self.generate_recommendations(metrics, alerts)
        }
    
    def generate_recommendations(self, metrics: Dict[str, Any], alerts: List[Dict[str, Any]]) -> List[str]:
        """Generate system recommendations based on metrics and alerts"""
        recommendations = []
        
        # System recommendations
        if "system" in metrics:
            system = metrics["system"]
            if system.get("cpu_usage", 0) > 70:
                recommendations.append("Consider scaling up CPU resources or optimizing application performance")
            if system.get("memory_usage", 0) > 80:
                recommendations.append("Monitor memory usage and consider increasing available RAM")
            if system.get("disk_usage", 0) > 85:
                recommendations.append("Clean up disk space or expand storage capacity")
        
        # API recommendations
        if "api_test" in metrics and "summary" in metrics["api_test"]:
            api_summary = metrics["api_test"]["summary"]
            if api_summary.get("avg_response_time", 0) > 1000:
                recommendations.append("Optimize API performance or implement caching")
            if api_summary.get("success_rate", 100) < 98:
                recommendations.append("Investigate and fix API endpoint failures")
        
        # Database recommendations
        if "database" in metrics:
            db = metrics["database"]
            if db.get("status") != "healthy":
                recommendations.append("Check database connectivity and integrity")
            if db.get("file_size_mb", 0) > 1000:
                recommendations.append("Consider database optimization or archival of old data")
        
        if not recommendations:
            recommendations.append("System is performing well - continue monitoring")
        
        return recommendations
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run a complete monitoring cycle"""
        print(f"🔍 Running monitoring cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Collect all metrics
        system_metrics = self.collect_system_metrics()
        api_test_results = self.test_api_endpoints()
        database_health = self.check_database_health()
        
        # Combine all metrics
        combined_metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": system_metrics.get("system", {}),
            "api_test": api_test_results,
            "database": database_health.get("database", {})
        }
        
        # Generate health report
        health_report = self.generate_health_report(combined_metrics)
        
        # Combine everything into final report
        full_report = {
            **combined_metrics,
            "health_report": health_report
        }
        
        # Store in history
        self.metrics_history.append(full_report)
        
        # Keep only last 100 records
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
        
        return full_report
    
    def print_status_report(self, report: Dict[str, Any]):
        """Print formatted status report"""
        health = report.get("health_report", {})
        system = report.get("system", {})
        api = report.get("api_test", {}).get("summary", {})
        database = report.get("database", {})
        
        print("\n" + "="*80)
        print("🏭 SMART WAREHOUSE PRODUCTION MONITORING REPORT")
        print("="*80)
        
        # Health Summary
        health_score = health.get("health_score", 0)
        health_status = health.get("health_status", "unknown")
        status_emoji = {"excellent": "🟢", "good": "🟡", "warning": "🟠", "critical": "🔴"}.get(health_status, "⚪")
        
        print(f"\n🎯 OVERALL HEALTH: {status_emoji} {health_status.upper()} ({health_score}/100)")
        
        # System Metrics
        print(f"\n💻 SYSTEM RESOURCES:")
        print(f"   CPU Usage: {system.get('cpu_usage', 0):.1f}%")
        print(f"   Memory Usage: {system.get('memory_usage', 0):.1f}%")
        print(f"   Disk Usage: {system.get('disk_usage', 0):.1f}%")
        print(f"   Available Memory: {system.get('memory_available_mb', 0):.0f} MB")
        print(f"   Free Disk Space: {system.get('disk_free_gb', 0):.1f} GB")
        
        # API Performance
        print(f"\n🌐 API PERFORMANCE:")
        print(f"   Success Rate: {api.get('success_rate', 0):.1f}%")
        print(f"   Average Response Time: {api.get('avg_response_time', 0):.1f}ms")
        print(f"   Successful Endpoints: {api.get('successful', 0)}/{api.get('total_tested', 0)}")
        
        # Database Status
        print(f"\n💾 DATABASE:")
        print(f"   Status: {database.get('status', 'unknown').upper()}")
        if database.get("status") == "healthy":
            print(f"   Tables: {database.get('tables_count', 0)}")
            print(f"   Size: {database.get('file_size_mb', 0):.1f} MB")
        
        # Alerts
        alerts = health.get("alerts", [])
        if alerts:
            print(f"\n⚠️  ALERTS ({len(alerts)}):")
            for alert in alerts:
                level_emoji = {"warning": "🟡", "critical": "🔴"}.get(alert.get("level"), "⚪")
                print(f"   {level_emoji} {alert.get('message', 'Unknown alert')}")
        else:
            print(f"\n✅ NO ALERTS - System operating normally")
        
        # Recommendations
        recommendations = health.get("recommendations", [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        print(f"\n⏰ Last Updated: {report.get('timestamp', 'unknown')}")
        print("="*80)
    
    def continuous_monitoring(self, interval_seconds=60):
        """Run continuous monitoring"""
        print("🚀 Starting Smart Warehouse Production Monitoring...")
        print(f"📊 Monitoring interval: {interval_seconds} seconds")
        print("💡 Press Ctrl+C to stop monitoring\n")
        
        try:
            while self.monitoring:
                report = self.run_monitoring_cycle()
                self.print_status_report(report)
                
                # Save report to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = f"monitoring_report_{timestamp}.json"
                
                try:
                    with open(report_file, 'w') as f:
                        json.dump(report, f, indent=2)
                    print(f"📝 Report saved to: {report_file}")
                except Exception as e:
                    print(f"⚠️  Could not save report: {e}")
                
                # Wait for next cycle
                print(f"\n⏳ Next check in {interval_seconds} seconds... (Ctrl+C to stop)")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            self.monitoring = False
    
    def single_check(self):
        """Run a single monitoring check"""
        print("🔍 Running single production health check...")
        report = self.run_monitoring_cycle()
        self.print_status_report(report)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"health_check_{timestamp}.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📝 Detailed report saved to: {report_file}")
        except Exception as e:
            print(f"⚠️  Could not save report: {e}")
        
        return report

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n\n🛑 Monitoring stopped by user signal')
    sys.exit(0)

def main():
    """Main monitoring function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    import argparse
    parser = argparse.ArgumentParser(description="Smart Warehouse Production Monitor")
    parser.add_argument("--url", default="http://localhost:8001", help="Base URL for the system")
    parser.add_argument("--interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--single", action="store_true", help="Run single check instead of continuous monitoring")
    
    args = parser.parse_args()
    
    monitor = ProductionMonitor(args.url)
    
    if args.single:
        monitor.single_check()
    else:
        monitor.continuous_monitoring(args.interval)

if __name__ == "__main__":
    main()
