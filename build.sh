#!/bin/bash
# Render.com build script

echo "🏗️ Building Smart Warehouse System on Render..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!"
