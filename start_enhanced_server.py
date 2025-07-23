#!/usr/bin/env python3
"""
Simple startup script for the enhanced chatbot server
"""

import os
import sys
import subprocess

def start_server():
    """Start the FastAPI server"""
    
    # Change to backend directory
    backend_dir = "/Users/SAM/Downloads/smart-warehouse-system/backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting Enhanced Chatbot Server...")
    print(f"📁 Working directory: {os.getcwd()}")
    
    try:
        # Start uvicorn server
        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
        print(f"🔧 Command: {' '.join(cmd)}")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server()
