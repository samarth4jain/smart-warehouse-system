#!/usr/bin/env python3
"""
Smart Warehouse File Consolidation Script
Merges redundant files and creates a clean, readable codebase
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class FileConsolidator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.changes_made = []
    
    def consolidate_chatbot_services(self):
        """Merge multiple chatbot services into one unified service"""
        print("🤖 Consolidating chatbot services...")
        
        # The conversational_chatbot_service.py appears to be the most comprehensive
        # We'll keep it as the main chatbot service and remove duplicates
        services_path = self.project_root / "backend" / "app" / "services"
        
        files_to_remove = [
            "chatbot_service.py",  # Basic version, superseded by conversational
            "enhanced_chatbot_service.py"  # LLM version, can be integrated later if needed
        ]
        
        main_chatbot = services_path / "conversational_chatbot_service.py"
        new_chatbot = services_path / "chatbot_service.py"
        
        if main_chatbot.exists():
            # Rename conversational_chatbot_service.py to chatbot_service.py
            if new_chatbot.exists():
                os.remove(new_chatbot)
            shutil.move(main_chatbot, new_chatbot)
            self.changes_made.append("Renamed conversational_chatbot_service.py to chatbot_service.py")
        
        # Remove duplicate files
        for file_name in files_to_remove:
            file_path = services_path / file_name
            if file_path.exists() and file_path != new_chatbot:
                os.remove(file_path)
                self.changes_made.append(f"Removed duplicate: {file_name}")
    
    def consolidate_llm_services(self):
        """Merge LLM services into one unified service"""
        print("🧠 Consolidating LLM services...")
        
        services_path = self.project_root / "backend" / "app" / "services"
        
        # Keep enhanced_smart_llm_service.py as the main LLM service
        # Remove duplicates
        files_to_remove = [
            "llm_service.py",
            "smart_llm_service.py",
            "hf_inference_service.py",
            "ollama_service.py", 
            "openai_compatible_service.py"
        ]
        
        for file_name in files_to_remove:
            file_path = services_path / file_name
            if file_path.exists():
                os.remove(file_path)
                self.changes_made.append(f"Removed duplicate LLM service: {file_name}")
    
    def consolidate_analytics_services(self):
        """Merge analytics services"""
        print("📊 Consolidating analytics services...")
        
        services_path = self.project_root / "backend" / "app" / "services"
        
        # Keep enhanced_analytics_service.py as primary
        # Remove ultra_enhanced_analytics_service.py (duplicate)
        ultra_analytics = services_path / "ultra_enhanced_analytics_service.py"
        if ultra_analytics.exists():
            os.remove(ultra_analytics)
            self.changes_made.append("Removed duplicate: ultra_enhanced_analytics_service.py")
    
    def consolidate_forecasting_services(self):
        """Merge forecasting services"""
        print("🔮 Consolidating forecasting services...")
        
        services_path = self.project_root / "backend" / "app" / "services"
        
        # Keep forecasting_service.py as primary
        # Remove simple_forecasting_service.py
        simple_forecasting = services_path / "simple_forecasting_service.py"
        if simple_forecasting.exists():
            os.remove(simple_forecasting)
            self.changes_made.append("Removed duplicate: simple_forecasting_service.py")
    
    def consolidate_space_optimization_services(self):
        """Merge space optimization services"""
        print("📦 Consolidating space optimization services...")
        
        services_path = self.project_root / "backend" / "app" / "services"
        
        # Keep space_optimization_service.py as primary
        # Remove simple_space_optimization_service.py
        simple_space = services_path / "simple_space_optimization_service.py"
        if simple_space.exists():
            os.remove(simple_space)
            self.changes_made.append("Removed duplicate: simple_space_optimization_service.py")
    
    def consolidate_nlp_services(self):
        """Merge NLP services"""
        print("🔤 Consolidating NLP services...")
        
        services_path = self.project_root / "backend" / "app" / "services"
        
        # Keep enhanced_nlp_processor.py as primary
        # Remove natural_language_processor.py if it's a duplicate
        basic_nlp = services_path / "natural_language_processor.py"
        enhanced_nlp = services_path / "enhanced_nlp_processor.py"
        
        if basic_nlp.exists() and enhanced_nlp.exists():
            os.remove(basic_nlp)
            self.changes_made.append("Removed duplicate: natural_language_processor.py")
    
    def consolidate_router_files(self):
        """Merge duplicate router files"""
        print("🛣️ Consolidating router files...")
        
        routers_path = self.project_root / "backend" / "app" / "routers"
        
        # Remove backup and fixed versions of commercial features
        files_to_remove = [
            "commercial_features_backup.py",
            "commercial_features_fixed.py"
        ]
        
        for file_name in files_to_remove:
            file_path = routers_path / file_name
            if file_path.exists():
                os.remove(file_path)
                self.changes_made.append(f"Removed duplicate router: {file_name}")
        
        # Remove enhanced_dashboard.py if dashboard.py exists
        enhanced_dashboard = routers_path / "enhanced_dashboard.py"
        dashboard = routers_path / "dashboard.py"
        
        if enhanced_dashboard.exists() and dashboard.exists():
            os.remove(enhanced_dashboard)
            self.changes_made.append("Removed duplicate: enhanced_dashboard.py")
    
    def update_imports_in_main(self):
        """Update imports in main.py to reflect consolidated services"""
        print("🔧 Updating imports in main.py...")
        
        main_file = self.project_root / "backend" / "app" / "main.py"
        
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove references to consolidated files
            old_imports = [
                "enhanced_dashboard",
                "ultra_analytics"
            ]
            
            updated = False
            for old_import in old_imports:
                if old_import in content:
                    # Remove the import line
                    lines = content.split('\n')
                    new_lines = []
                    for line in lines:
                        if f"from .routers import" in line and old_import in line:
                            # Remove the old import from the line
                            imports = line.split('import')[1].strip().split(',')
                            imports = [imp.strip() for imp in imports if old_import not in imp]
                            if imports:
                                new_lines.append(f"from .routers import {', '.join(imports)}")
                        elif f"app.include_router({old_import}" in line:
                            # Skip the include_router line for removed modules
                            continue
                        else:
                            new_lines.append(line)
                    content = '\n'.join(new_lines)
                    updated = True
            
            if updated:
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.changes_made.append("Updated imports in main.py")
    
    def run_consolidation(self):
        """Run the complete file consolidation"""
        print("🏭 Starting Smart Warehouse File Consolidation")
        print("=" * 60)
        
        self.consolidate_chatbot_services()
        self.consolidate_llm_services()
        self.consolidate_analytics_services()
        self.consolidate_forecasting_services()
        self.consolidate_space_optimization_services()
        self.consolidate_nlp_services()
        self.consolidate_router_files()
        self.update_imports_in_main()
        
        print("\n" + "=" * 60)
        print("✅ File consolidation completed!")
        print(f"📁 Changes made: {len(self.changes_made)}")
        
        for change in self.changes_made:
            print(f"  ✓ {change}")
        
        return self.changes_made

def main():
    """Main consolidation function"""
    consolidator = FileConsolidator()
    changes = consolidator.run_consolidation()
    
    # Create a summary report
    report_file = Path("file_consolidation_report.txt")
    with open(report_file, 'w') as f:
        f.write(f"File Consolidation Report - {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total changes made: {len(changes)}\n\n")
        for change in changes:
            f.write(f"- {change}\n")
    
    print(f"\n📊 Consolidation report saved to: {report_file}")

if __name__ == "__main__":
    main()
