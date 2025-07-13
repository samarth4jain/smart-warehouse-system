#!/usr/bin/env python3
"""
Advanced Production Monitoring System for Smart Warehouse Management
Comprehensive real-time monitoring, performance analytics, and system health validation
"""

import requests
import time
import json
import sqlite3
import os
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import queue
from dataclasses import dataclass, asdict

@dataclass
class HealthMetric:
    timestamp: str
    endpoint: str
    response_time_ms: float
    status_code: int
    success: bool
    error_message: str = ""

@dataclass
class SystemStats:
    timestamp: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    response_avg: float

class ProductionMonitor:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.metrics_queue = queue.Queue()
        self.health_history = []
        self.alerts = []
        self.monitoring = False
        
        # Critical endpoints to monitor
        self.endpoints = {
            "System Health": "/health",
            "Commercial Dashboard": "/api/commercial/executive-dashboard",
            "Inventory API": "/api/inventory/products",
            "QR Code System": "/api/commercial/qr-codes",
            "ABC Analysis": "/api/commercial/abc-analysis",
            "Financial Metrics": "/api/commercial/financial-metrics",
            "Automation": "/api/commercial/automation-opportunities",
            "Commercial Intelligence": "/commercial-intelligence-dashboard",
            "Main Dashboard": "/",
            "API Documentation": "/docs"
        }
        
        # Performance thresholds
        self.thresholds = {
            "response_time_warning": 1000,  # ms
            "response_time_critical": 3000,  # ms
            "error_rate_warning": 5,  # %
            "error_rate_critical": 15,  # %
            "availability_critical": 95  # %
        }

    def check_endpoint_health(self, name: str, endpoint: str) -> HealthMetric:
        """Check health of a specific endpoint"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                endpoint=name,
                response_time_ms=response_time,
                status_code=response.status_code,
                success=response.status_code < 400
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                endpoint=name,
                response_time_ms=response_time,
                status_code=0,
                success=False,
                error_message=str(e)
            )

    def get_system_stats(self) -> SystemStats:
        """Get system resource statistics"""
        try:
            # Get CPU usage
            cpu_result = subprocess.run(['ps', '-A', '-o', '%cpu'], 
                                      capture_output=True, text=True)
            cpu_values = [float(line.strip()) for line in cpu_result.stdout.split('\n')[1:] 
                         if line.strip() and line.strip() != '%CPU']
            cpu_usage = sum(cpu_values)
            
            # Get memory info (simplified for demo)
            memory_usage = 0.0
            
            # Get disk usage
            disk_result = subprocess.run(['df', '-h', '.'], 
                                       capture_output=True, text=True)
            disk_lines = disk_result.stdout.split('\n')[1:]
            if disk_lines:
                disk_info = disk_lines[0].split()
                disk_usage = float(disk_info[4].replace('%', ''))
            else:
                disk_usage = 0.0
            
            # Get active connections (simplified)
            active_connections = len(self.health_history)
            
            # Calculate average response time
            recent_metrics = [m for m in self.health_history[-50:] if m.success]
            response_avg = sum(m.response_time_ms for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
            
            return SystemStats(
                timestamp=datetime.now().isoformat(),
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                active_connections=active_connections,
                response_avg=response_avg
            )
        except Exception as e:
            return SystemStats(
                timestamp=datetime.now().isoformat(),
                cpu_usage=0.0,
                memory_usage=0.0,
                disk_usage=0.0,
                active_connections=0,
                response_avg=0.0
            )

    def check_all_endpoints(self) -> List[HealthMetric]:
        """Check health of all endpoints"""
        metrics = []
        for name, endpoint in self.endpoints.items():
            metric = self.check_endpoint_health(name, endpoint)
            metrics.append(metric)
            self.health_history.append(metric)
        
        # Keep only last 1000 metrics
        if len(self.health_history) > 1000:
            self.health_history = self.health_history[-1000:]
        
        return metrics

    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze system performance and generate insights"""
        if not self.health_history:
            return {"status": "No data available"}
        
        recent_metrics = self.health_history[-100:]
        
        # Calculate availability
        total_requests = len(recent_metrics)
        successful_requests = len([m for m in recent_metrics if m.success])
        availability = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        
        # Calculate average response times by endpoint
        endpoint_performance = {}
        for endpoint_name in self.endpoints.keys():
            endpoint_metrics = [m for m in recent_metrics if m.endpoint == endpoint_name and m.success]
            if endpoint_metrics:
                avg_response = sum(m.response_time_ms for m in endpoint_metrics) / len(endpoint_metrics)
                endpoint_performance[endpoint_name] = {
                    "avg_response_ms": round(avg_response, 2),
                    "requests": len(endpoint_metrics),
                    "success_rate": (len(endpoint_metrics) / len([m for m in recent_metrics if m.endpoint == endpoint_name])) * 100
                }
        
        # Identify slow endpoints
        slow_endpoints = {k: v for k, v in endpoint_performance.items() 
                         if v["avg_response_ms"] > self.thresholds["response_time_warning"]}
        
        # Generate alerts
        alerts = []
        if availability < self.thresholds["availability_critical"]:
            alerts.append(f"🚨 CRITICAL: System availability is {availability:.1f}%")
        
        for endpoint, perf in slow_endpoints.items():
            if perf["avg_response_ms"] > self.thresholds["response_time_critical"]:
                alerts.append(f"🔴 CRITICAL: {endpoint} response time is {perf['avg_response_ms']:.1f}ms")
            elif perf["avg_response_ms"] > self.thresholds["response_time_warning"]:
                alerts.append(f"🟡 WARNING: {endpoint} response time is {perf['avg_response_ms']:.1f}ms")
        
        self.alerts.extend(alerts)
        
        return {
            "availability": round(availability, 2),
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "endpoint_performance": endpoint_performance,
            "slow_endpoints": slow_endpoints,
            "alerts": alerts,
            "system_health": "HEALTHY" if availability > 95 and not slow_endpoints else 
                           "DEGRADED" if availability > 85 else "CRITICAL"
        }

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive system test"""
        print("🔍 COMPREHENSIVE PRODUCTION MONITORING")
        print("=" * 60)
        print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test all endpoints
        print("\n🧪 ENDPOINT HEALTH CHECK")
        print("-" * 30)
        metrics = self.check_all_endpoints()
        
        success_count = 0
        for metric in metrics:
            status = "✅" if metric.success else "❌"
            response_time = f"{metric.response_time_ms:.1f}ms"
            print(f"{status} {metric.endpoint:<25} {response_time:>8} {metric.status_code}")
            if metric.success:
                success_count += 1
        
        success_rate = (success_count / len(metrics)) * 100
        print(f"\n📊 Success Rate: {success_rate:.1f}% ({success_count}/{len(metrics)})")
        
        # Performance analysis
        print("\n📈 PERFORMANCE ANALYSIS")
        print("-" * 30)
        analysis = self.analyze_performance()
        
        print(f"🎯 System Health: {analysis['system_health']}")
        print(f"📊 Availability: {analysis['availability']}%")
        print(f"📈 Total Requests: {analysis['total_requests']}")
        
        # System statistics
        print("\n💻 SYSTEM STATISTICS")
        print("-" * 30)
        sys_stats = self.get_system_stats()
        print(f"🖥️  CPU Usage: {sys_stats.cpu_usage:.1f}%")
        print(f"💾 Disk Usage: {sys_stats.disk_usage:.1f}%")
        print(f"⚡ Avg Response: {sys_stats.response_avg:.1f}ms")
        
        # Performance insights
        if analysis["endpoint_performance"]:
            print("\n⚡ ENDPOINT PERFORMANCE")
            print("-" * 30)
            for endpoint, perf in analysis["endpoint_performance"].items():
                status_icon = "🔥" if perf["avg_response_ms"] < 100 else "✅" if perf["avg_response_ms"] < 500 else "⚠️"
                print(f"{status_icon} {endpoint:<25} {perf['avg_response_ms']:>6.1f}ms ({perf['success_rate']:.0f}%)")
        
        # Alerts and recommendations
        if analysis["alerts"]:
            print("\n🚨 ALERTS & RECOMMENDATIONS")
            print("-" * 30)
            for alert in analysis["alerts"]:
                print(alert)
        else:
            print("\n✅ NO ALERTS - SYSTEM PERFORMING OPTIMALLY")
        
        # Commercial feature validation
        print("\n🏢 COMMERCIAL FEATURES VALIDATION")
        print("-" * 30)
        commercial_features = [
            ("Executive Dashboard", "/api/commercial/executive-dashboard"),
            ("Financial Metrics", "/api/commercial/financial-metrics"),
            ("ABC Analysis", "/api/commercial/abc-analysis"),
            ("QR Management", "/api/commercial/qr-codes"),
            ("Commercial UI", "/commercial-intelligence-dashboard")
        ]
        
        commercial_success = 0
        for name, endpoint in commercial_features:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code < 400:
                    print(f"✅ {name:<20} OPERATIONAL")
                    commercial_success += 1
                else:
                    print(f"❌ {name:<20} ERROR ({response.status_code})")
            except Exception as e:
                print(f"❌ {name:<20} FAILED ({str(e)[:30]})")
        
        commercial_rate = (commercial_success / len(commercial_features)) * 100
        print(f"\n🏢 Commercial Features: {commercial_rate:.0f}% operational")
        
        # Overall status
        overall_health = "EXCELLENT" if success_rate >= 95 and commercial_rate >= 90 else \
                        "GOOD" if success_rate >= 85 and commercial_rate >= 80 else \
                        "NEEDS_ATTENTION"
        
        print(f"\n🎯 OVERALL SYSTEM HEALTH: {overall_health}")
        print("=" * 60)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "success_rate": success_rate,
            "commercial_success_rate": commercial_rate,
            "overall_health": overall_health,
            "metrics": [asdict(m) for m in metrics],
            "analysis": analysis,
            "system_stats": asdict(sys_stats)
        }

    def start_continuous_monitoring(self, interval: int = 60):
        """Start continuous monitoring"""
        self.monitoring = True
        print(f"🔄 Starting continuous monitoring (interval: {interval}s)")
        
        while self.monitoring:
            try:
                self.check_all_endpoints()
                analysis = self.analyze_performance()
                
                # Print status update
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Health: {analysis['system_health']} | "
                      f"Availability: {analysis['availability']:.1f}%")
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(interval)

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False

def main():
    monitor = ProductionMonitor()
    
    print("🚀 SMART WAREHOUSE PRODUCTION MONITORING SYSTEM")
    print("=" * 60)
    print("Available commands:")
    print("1. 'test' - Run comprehensive test")
    print("2. 'monitor' - Start continuous monitoring")
    print("3. 'status' - Quick status check")
    print("4. 'quit' - Exit")
    print("=" * 60)
    
    while True:
        try:
            command = input("\n💻 Enter command: ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command in ['test', 't']:
                monitor.run_comprehensive_test()
            elif command in ['monitor', 'm']:
                try:
                    monitor.start_continuous_monitoring()
                except KeyboardInterrupt:
                    print("\n🛑 Monitoring stopped")
            elif command in ['status', 's']:
                metrics = monitor.check_all_endpoints()
                success_count = len([m for m in metrics if m.success])
                print(f"📊 Quick Status: {success_count}/{len(metrics)} endpoints healthy")
            else:
                print("❓ Unknown command. Try 'test', 'monitor', 'status', or 'quit'")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
