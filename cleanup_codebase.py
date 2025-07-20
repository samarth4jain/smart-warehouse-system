#!/usr/bin/env python3
"""
Smart Warehouse Codebase Cleanup Script
Removes unnecessary files and keeps only relevant, useful files
"""

import os
import shutil
import glob
from pathlib import Path

def clean_codebase():
    """Clean up the codebase by removing unnecessary files"""
    base_dir = Path(".")
    
    print("🧹 Starting Codebase Cleanup...")
    print("=" * 50)
    
    # Files to keep (essential core files)
    essential_files = {
        # Core application files
        "README.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        ".env.example",
        "docker-compose.yml",
        "Dockerfile",
        
        # Main documentation
        "LOCAL_SETUP.md",
        "DEPLOYMENT.md",
        
        # Essential test files
        "test_chatbot_comprehensive.py",
        "simple_chatbot_test.ps1",
        
        # Core setup/utility files
        "setup_enhanced_demo_data.py",
        
        # Latest test results (for reference)
        "chatbot_test_results.json",
        "chatbot_test_results.md",
        "chatbot_test_summary.md"
    }
    
    # Directories to keep (essential)
    essential_dirs = {
        "backend",
        "frontend", 
        "docs",
        ".git",
        ".github"
    }
    
    # Files/patterns to remove
    files_to_remove = []
    
    # Find all markdown reports and status files (too many duplicates)
    report_patterns = [
        "*_REPORT.md",
        "*_SUCCESS*.md", 
        "*_STATUS*.md",
        "*_COMPLETION*.md",
        "*_SUMMARY.md",
        "*_GUIDE.md",
        "PHASE*.md",
        "FINAL_*.md",
        "ULTRA_*.md",
        "COMMERCIAL_*.md",
        "MISSION_*.md",
        "PROJECT_*.md",
        "ENHANCED_*.md",
        "ERROR_*.md",
        "LLM_*.md",
        "PROFESSIONAL_*.md",
        "WEBSITE_*.md",
        "GITHUB_PAGES_*.md"
    ]
    
    # Find deployment scripts (keep only essential ones)
    deploy_patterns = [
        "deploy_*.sh",
        "start_*.sh",
        "final_*.sh",
        "validate_*.sh"
    ]
    
    # Find test scripts (keep only essential ones)
    test_patterns = [
        "test_*.py",
        "test_*.sh",
        "*_test.sh",
        "phase*_test.sh"
    ]
    
    # Find old README variants
    readme_patterns = [
        "README_*.md"
    ]
    
    # Find demo/example files
    demo_patterns = [
        "demo_*.py",
        "final_*.py",
        "*_demo.py",
        "debug_*.py",
        "implement_*.py",
        "optimize_*.py",
        "monitor_*.py",
        "comprehensive_*.py",
        "advanced_*.py",
        "create_*.py"
    ]
    
    # Find old data files
    data_patterns = [
        "setup_phase*.py",
        "setup_sample*.py",
        "health_check_*.json",
        "*_test_results.json",
        "github_pages_*.json"
    ]
    
    # Find various other unnecessary files
    misc_patterns = [
        "quick_test.sh",
        "quick_chatbot_test.ps1",  # Keep simple_chatbot_test.ps1 instead
        "*GUIDE.md",
        "TESTING_*.md",
        "CONTRIBUTING.md",
        "CLEANUP_*.md"
    ]
    
    # Collect all patterns
    all_patterns = (report_patterns + deploy_patterns + test_patterns + 
                   readme_patterns + demo_patterns + data_patterns + misc_patterns)
    
    # Find files to remove
    for pattern in all_patterns:
        matches = glob.glob(pattern)
        files_to_remove.extend(matches)
    
    # Remove duplicates and filter out essential files
    files_to_remove = list(set(files_to_remove))
    files_to_remove = [f for f in files_to_remove if f not in essential_files]
    
    # Count and categorize files
    removed_count = 0
    categories = {
        "Reports & Documentation": [],
        "Test Scripts": [],
        "Deploy Scripts": [],
        "Demo Files": [],
        "Data Files": [],
        "Other": []
    }
    
    for file in files_to_remove:
        if any(pattern.replace("*", "") in file for pattern in report_patterns):
            categories["Reports & Documentation"].append(file)
        elif any(pattern.replace("*", "") in file for pattern in (test_patterns + ["test"])):
            categories["Test Scripts"].append(file)
        elif any(pattern.replace("*", "") in file for pattern in deploy_patterns):
            categories["Deploy Scripts"].append(file)
        elif any(pattern.replace("*", "") in file for pattern in demo_patterns):
            categories["Demo Files"].append(file)
        elif any(pattern.replace("*", "") in file for pattern in data_patterns):
            categories["Data Files"].append(file)
        else:
            categories["Other"].append(file)
    
    # Display what will be removed
    print("📋 Files to be removed:")
    print("-" * 30)
    for category, files in categories.items():
        if files:
            print(f"\n{category} ({len(files)} files):")
            for file in sorted(files)[:5]:  # Show first 5
                print(f"  - {file}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
    
    total_to_remove = sum(len(files) for files in categories.values())
    print(f"\n📊 Summary:")
    print(f"  Total files to remove: {total_to_remove}")
    
    # Ask for confirmation
    response = input(f"\n❓ Remove {total_to_remove} files? [y/N]: ").strip().lower()
    
    if response in ['y', 'yes']:
        print("\n🗑️  Removing files...")
        
        for file in files_to_remove:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    removed_count += 1
                    print(f"  ✅ Removed: {file}")
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    removed_count += 1
                    print(f"  ✅ Removed directory: {file}")
            except Exception as e:
                print(f"  ❌ Error removing {file}: {e}")
        
        print(f"\n✅ Cleanup complete! Removed {removed_count} files/directories.")
        
        # Show what's left
        print(f"\n📁 Essential files kept:")
        remaining_files = [f for f in os.listdir(".") if os.path.isfile(f)]
        for file in sorted(remaining_files):
            print(f"  - {file}")
        
        remaining_dirs = [d for d in os.listdir(".") if os.path.isdir(d) and not d.startswith('.')]
        print(f"\n📂 Essential directories kept:")
        for dir_name in sorted(remaining_dirs):
            print(f"  - {dir_name}/")
        
    else:
        print("❌ Cleanup cancelled.")

def clean_frontend_duplicates():
    """Remove duplicate HTML files in frontend"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        return
    
    print(f"\n🧹 Cleaning frontend duplicates...")
    
    # Keep only essential frontend files
    essential_frontend = {
        "index.html",      # Landing page
        "dashboard.html",  # Main dashboard
        "chatbot.html",    # Chatbot interface
        "static"           # Static assets directory
    }
    
    frontend_files = [f for f in os.listdir(frontend_dir) if f not in essential_frontend]
    
    print(f"📋 Frontend files to remove ({len(frontend_files)}):")
    for file in sorted(frontend_files):
        print(f"  - frontend/{file}")
    
    if frontend_files:
        response = input(f"\n❓ Remove {len(frontend_files)} frontend files? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            for file in frontend_files:
                try:
                    file_path = frontend_dir / file
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  ✅ Removed: frontend/{file}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"  ✅ Removed directory: frontend/{file}")
                except Exception as e:
                    print(f"  ❌ Error removing frontend/{file}: {e}")

def clean_docs_duplicates():
    """Remove duplicate files in docs directory"""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return
    
    print(f"\n🧹 Cleaning docs duplicates...")
    
    # Keep only essential docs files
    essential_docs = {
        "index.html",
        "dashboard.html",
        "chatbot.html", 
        "static",
        "style.css",
        "script.js"
    }
    
    docs_files = []
    for item in os.listdir(docs_dir):
        if item not in essential_docs:
            docs_files.append(item)
    
    if docs_files:
        print(f"📋 Docs files to remove ({len(docs_files)}):")
        for file in sorted(docs_files):
            print(f"  - docs/{file}")
        
        response = input(f"\n❓ Remove {len(docs_files)} docs files? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            for file in docs_files:
                try:
                    file_path = docs_dir / file
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  ✅ Removed: docs/{file}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"  ✅ Removed directory: docs/{file}")
                except Exception as e:
                    print(f"  ❌ Error removing docs/{file}: {e}")

def main():
    """Main cleanup function"""
    print("🏭 Smart Warehouse Codebase Cleanup")
    print("=" * 40)
    print("This will remove duplicate, outdated, and unnecessary files")
    print("while keeping the core functionality intact.\n")
    
    # Main cleanup
    clean_codebase()
    
    # Frontend cleanup
    clean_frontend_duplicates()
    
    # Docs cleanup
    clean_docs_duplicates()
    
    print(f"\n🎉 Codebase cleanup completed!")
    print("✅ Core functionality preserved")
    print("✅ Duplicate files removed")
    print("✅ Repository is now cleaner and more maintainable")

if __name__ == "__main__":
    main()
