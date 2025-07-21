#!/usr/bin/env python3
"""
Smart Warehouse Codebase Cleanup Script
Removes duplicate, old, and unnecessary files while preserving all functionality
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# Get the current directory (project root)
PROJECT_ROOT = Path(__file__).parent

class CodebaseCleanup:
    def __init__(self):
        self.cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "files_removed": [],
            "files_kept": [],
            "directories_removed": [],
            "total_space_freed": 0,
            "summary": {}
        }
    
    def get_file_size(self, file_path):
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def should_remove_file(self, file_path):
        """Determine if a file should be removed"""
        file_name = os.path.basename(file_path)
        file_str = str(file_path).replace("\\", "/")
        
        # Files to definitely remove (duplicates, old versions, temporary)
        remove_patterns = [
            # Duplicate/old README files
            "README_OLD.md",
            "README_NEW.md", 
            "README_COMMERCIAL.md",
            "README_GITHUB.md",
            "README_ULTRA_INTELLIGENCE.md",
            
            # Old deployment scripts (keep main ones)
            "deploy_phase2.sh",
            "deploy_phase3.sh", 
            "deploy_llm_system.sh",
            "deploy_ultra_intelligence.sh",
            "deploy_commercial_integrated.sh",
            
            # Old test files (keep recent chatbot tests)
            "test_basic_system.py",
            "test_complete_system.py",
            "test_enhanced_chatbot.py",
            "test_nlp_only.py",
            "test_optimization_verification.py",
            "test_performance_optimizations.py",
            "test_quick_performance.py",
            "test_ultra_analytics.py",
            "test_github_deployment.py",
            "test_github_pages_deployment.py",
            "test_website_deployment.py",
            "test_website_integration.py",
            
            # Old shell test scripts
            "test_all_features.sh",
            "test_chatbot.sh",
            "test_commercial_features.sh",
            "test_complete_system.sh",
            "test_dynamic_responses.sh",
            "test_error_fixes_and_enhancements.sh",
            "test_llm_integration.sh",
            "test_phase3.sh",
            "quick_test.sh",
            "phase2_completion_test.sh",
            "final_system_demonstration.sh",
            
            # Duplicate Python scripts
            "advanced_production_validator.py",
            "comprehensive_production_monitor.py",
            "create_advanced_dashboard.py",
            "debug_nlp.py",
            "demo_enhanced_chatbot.py",
            "final_chatbot_demo.py",
            "implement_complete_system.py",
            "monitor_production_system.py",
            "optimize_warehouse_system.py",
            "setup_enhanced_demo_data.py",
            "setup_phase3_data.py",
            "setup_sample_data.py",
            "start_phase4.sh",
            "validate_production_readiness.sh",
            
            # Excessive report files (keep essential ones)
            "COMMERCIAL_API_DOCS.md",
            "COMMERCIAL_ENHANCEMENT_SUMMARY.md",
            "COMMERCIAL_PRODUCTION_COMPLETION_REPORT.md",
            "COMMERCIAL_SUCCESS_REPORT.md",
            "COMPLETE_IMPLEMENTATION_SUMMARY.md",
            "COMPREHENSIVE_TESTING_COMPLETE_REPORT.md", 
            "COMPREHENSIVE_TESTING_VALIDATION_REPORT.md",
            "DEPLOYMENT_SUCCESS_REPORT.md",
            "ENHANCED_CHATBOT_SUMMARY.md",
            "ERROR_FIXES_AND_AI_ENHANCEMENT_REPORT.md",
            "FINAL_COMMERCIAL_PRODUCTION_GUIDE.md",
            "FINAL_DELIVERY_SUMMARY.md",
            "FINAL_DEPLOYMENT_STATUS_REPORT.md",
            "FINAL_DEPLOYMENT_SUCCESS_REPORT.md",
            "FINAL_LLM_IMPLEMENTATION_SUMMARY.md",
            "FINAL_NATURAL_LANGUAGE_CHATBOT_SUMMARY.md",
            "FINAL_PHASE2_COMPLETION.md",
            "FINAL_SYSTEM_STATUS_REPORT.md",
            "FINAL_TEST_RESULTS.md",
            "GITHUB_PAGES_DEPLOYMENT_SUCCESS.md",
            "GITHUB_PAGES_TEST_RESULTS.md",
            "INVENTORY_SERVICE_OPTIMIZATION_REPORT.md",
            "LLM_DYNAMIC_RESPONSE_FIX_REPORT.md",
            "LLM_INTEGRATION_STATUS_REPORT.md",
            "MISSION_COMPLETE_FINAL_REPORT.md",
            "PHASE1_COMPLETION_REPORT.md",
            "PHASE2_COMPLETION_REPORT.md",
            "PHASE3_IMPLEMENTATION_REPORT.md",
            "PHASE4_ENHANCEMENT_PLAN.md",
            "PHASE4_SUCCESS_REPORT.md",
            "PROFESSIONAL_INTERFACE_DEPLOYMENT_REPORT.md",
            "PROFESSIONAL_INTERFACE_UPDATE.md",
            "PROJECT_COMPLETION_SUMMARY.md",
            "ULTRA_INTELLIGENCE_COMPLETION_REPORT.md",
            "ULTRA_INTELLIGENCE_DEPLOYMENT_SUCCESS.md",
            "ULTRA_PERFORMANCE_FINAL_REPORT.md",
            "WEBSITE_DEPLOYMENT_SUCCESS.md",
            "WEBSITE_TESTING_REPORT.md",
            
            # Old JSON test results
            "github_pages_test_results.json",
            "ultra_analytics_test_results.json",
            "health_check_20250713_152935.json",
            "health_check_20250713_153055.json",
        ]
        
        # Check if file matches any removal pattern
        return any(pattern in file_str for pattern in remove_patterns)
    
    def cleanup_duplicate_frontend_files(self, dry_run=False):
        """Remove duplicate frontend dashboard files"""
        frontend_path = PROJECT_ROOT / "frontend"
        if not frontend_path.exists():
            return 0, 0
        
        # Keep only essential frontend files
        essential_frontend = [
            "index.html",  # Main landing page
            "dashboard.html",  # Core dashboard
            "chatbot.html",  # AI assistant
            "enterprise_dashboard.html",  # Enterprise analytics
            "commercial_intelligence_dashboard.html",  # Business intelligence
        ]
        
        files_removed = 0
        space_freed = 0
        
        # Remove duplicate dashboard files
        duplicate_dashboards = [
            "advanced_dashboard.html",
            "commercial_dashboard.html", 
            "enhanced_chatbot.html",
            "enterprise_analytics_dashboard.html",
            "ultra_intelligence_dashboard.html"
        ]
        
        for dashboard in duplicate_dashboards:
            file_path = frontend_path / dashboard
            if file_path.exists():
                file_size = self.get_file_size(file_path)
                print(f"🗑️  Removing duplicate frontend: {dashboard}")
                
                if not dry_run:
                    try:
                        os.remove(file_path)
                        self.cleanup_report["files_removed"].append(f"frontend/{dashboard}")
                        space_freed += file_size
                        files_removed += 1
                    except Exception as e:
                        print(f"❌ Error removing {dashboard}: {e}")
                else:
                    self.cleanup_report["files_removed"].append(f"[DRY RUN] frontend/{dashboard}")
                    space_freed += file_size
                    files_removed += 1
        
        return files_removed, space_freed
    
    def cleanup_duplicate_backend_files(self, dry_run=False):
        """Remove duplicate backend main files"""
        backend_app = PROJECT_ROOT / "backend" / "app"
        if not backend_app.exists():
            return 0, 0
        
        files_removed = 0
        space_freed = 0
        
        # Remove main_commercial.py if main.py exists (keep main.py as primary)
        main_commercial = backend_app / "main_commercial.py"
        main_py = backend_app / "main.py"
        
        if main_commercial.exists() and main_py.exists():
            file_size = self.get_file_size(main_commercial)
            print(f"🗑️  Removing duplicate backend: main_commercial.py")
            
            if not dry_run:
                try:
                    os.remove(main_commercial)
                    self.cleanup_report["files_removed"].append("backend/app/main_commercial.py")
                    space_freed += file_size
                    files_removed += 1
                except Exception as e:
                    print(f"❌ Error removing main_commercial.py: {e}")
            else:
                self.cleanup_report["files_removed"].append("[DRY RUN] backend/app/main_commercial.py")
                space_freed += file_size
                files_removed += 1
        
        return files_removed, space_freed
    
    def cleanup_files(self, dry_run=False):
        """Perform the cleanup operation"""
        print(f"🧹 Starting Smart Warehouse Codebase Cleanup {'(DRY RUN)' if dry_run else ''}")
        print("=" * 70)
        
        total_files_removed = 0
        total_space_freed = 0
        
        # Cleanup root directory files
        for item in PROJECT_ROOT.iterdir():
            if item.is_file() and self.should_remove_file(item):
                file_size = self.get_file_size(item)
                print(f"🗑️  Removing file: {item.name}")
                
                if not dry_run:
                    try:
                        os.remove(item)
                        self.cleanup_report["files_removed"].append(str(item.name))
                        total_space_freed += file_size
                        total_files_removed += 1
                    except Exception as e:
                        print(f"❌ Error removing {item.name}: {e}")
                else:
                    self.cleanup_report["files_removed"].append(f"[DRY RUN] {item.name}")
                    total_space_freed += file_size
                    total_files_removed += 1
        
        # Cleanup duplicate frontend files
        frontend_removed, frontend_space = self.cleanup_duplicate_frontend_files(dry_run)
        total_files_removed += frontend_removed
        total_space_freed += frontend_space
        
        # Cleanup duplicate backend files  
        backend_removed, backend_space = self.cleanup_duplicate_backend_files(dry_run)
        total_files_removed += backend_removed
        total_space_freed += backend_space
        
        # Update summary
        self.cleanup_report["summary"] = {
            "total_files_removed": total_files_removed,
            "total_space_freed_bytes": total_space_freed,
            "total_space_freed_mb": round(total_space_freed / (1024 * 1024), 2),
            "dry_run": dry_run
        }
        
        print("\n" + "=" * 70)
        print(f"✅ Cleanup {'simulation' if dry_run else 'completed'}!")
        print(f"📁 Files removed: {total_files_removed}")
        print(f"💾 Space freed: {round(total_space_freed / (1024 * 1024), 2)} MB")
        
        return self.cleanup_report
    
    def list_files_to_keep(self):
        """List all core files that will be preserved"""
        print("📋 CORE FILES TO PRESERVE:")
        print("=" * 50)
        
        core_files = [
            # Backend Core
            "✅ backend/app/main.py",
            "✅ backend/app/database.py",
            "✅ backend/app/__init__.py", 
            "✅ backend/app/models/ (all database models)",
            "✅ backend/app/routers/ (all API routes)",
            "✅ backend/app/services/ (all business logic)",
            "✅ backend/requirements.txt",
            "✅ backend/smart_warehouse.db",
            
            # Frontend Core
            "✅ frontend/index.html (main landing)",
            "✅ frontend/dashboard.html (core dashboard)",
            "✅ frontend/chatbot.html (AI assistant)", 
            "✅ frontend/enterprise_dashboard.html (analytics)",
            "✅ frontend/commercial_intelligence_dashboard.html (BI)",
            "✅ frontend/static/ (all CSS, JS, assets)",
            
            # Essential Config & Docs
            "✅ README.md",
            "✅ LICENSE",
            "✅ requirements.txt", 
            "✅ docker-compose.yml",
            "✅ Dockerfile",
            "✅ .gitignore",
            "✅ .env.example",
            "✅ QUICK_START_GUIDE.md",
            "✅ LOCAL_SETUP.md",
            "✅ DEPLOYMENT.md",
            "✅ TESTING_GUIDE.md",
            "✅ CONTRIBUTING.md",
            "✅ CLEANUP_SUMMARY.md",
            "✅ PRODUCTION_DEPLOYMENT_GUIDE.md",
            
            # Recent Test Results (Valuable Reference)
            "✅ chatbot_test_results.json",
            "✅ chatbot_test_results.md", 
            "✅ chatbot_test_summary.md",
            "✅ simple_chatbot_test.ps1",
            "✅ test_chatbot_comprehensive.py",
            
            # Essential Deployment Scripts
            "✅ deploy_commercial.sh",
            "✅ deploy_production.sh",
            "✅ deploy_production_commercial.sh",
            "✅ github_deploy.sh",
            
            # Project Structure
            "✅ .git/ (version control)",
            "✅ .github/ (GitHub workflows)",
            "✅ docs/ (documentation site)"
        ]
        
        for file_desc in core_files:
            print(f"  {file_desc}")
        
        print(f"\n✅ All core functionality will be preserved!")
        print(f"🔥 Only duplicate, old, and unnecessary files will be removed!")
    
    def save_cleanup_report(self, report):
        """Save cleanup report to file"""
        report_file = PROJECT_ROOT / "cleanup_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📊 Cleanup report saved to: cleanup_report.json")

def main():
    """Main cleanup function"""
    cleanup = CodebaseCleanup()
    
    print("🏭 Smart Warehouse Codebase Cleanup Tool")
    print("=" * 70)
    print("This tool removes duplicate, old, and unnecessary files while")
    print("preserving ALL core functionality and recent test results.\n")
    
    # Show what will be preserved
    cleanup.list_files_to_keep()
    
    print("\n" + "⚠️  WARNING: This will permanently delete files!")
    print("Review the list above and run with --dry-run first to preview changes.")
    
    import sys
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    force = "--force" in sys.argv or "-f" in sys.argv
    
    if not dry_run and not force:
        response = input("\nContinue with cleanup? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cleanup cancelled.")
            return
    
    # Perform cleanup
    report = cleanup.cleanup_files(dry_run=dry_run)
    
    # Save report
    cleanup.save_cleanup_report(report)
    
    if dry_run:
        print("\n💡 To perform actual cleanup, run: python cleanup_codebase.py")
        print("💡 To force cleanup without prompts: python cleanup_codebase.py --force")

if __name__ == "__main__":
    main()
