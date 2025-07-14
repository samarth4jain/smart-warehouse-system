#!/bin/bash

# GitHub Pages Deployment Script for Smart Warehouse Management System
# This script prepares and deploys the frontend-only version for GitHub Pages

echo "🚀 Preparing Smart Warehouse System for GitHub Pages deployment..."

# Remove any potential sensitive files
echo "🧹 Cleaning up sensitive files..."
rm -rf .venv venv node_modules __pycache__ *.log

# Create a deployment info file
echo "📋 Creating deployment info..."
cat > DEPLOYMENT_INFO.md << 'EOF'
# GitHub Pages Deployment

This is the static frontend deployment of the Smart Warehouse Management System.

## Live Demo
- **Main Landing Page**: [index.html](./index.html)
- **Dashboard**: [frontend/index.html](./frontend/index.html)
- **Enterprise Dashboard**: [frontend/enterprise_dashboard.html](./frontend/enterprise_dashboard.html)
- **Advanced Analytics**: [frontend/advanced_dashboard.html](./frontend/advanced_dashboard.html)
- **AI Chatbot**: [frontend/chatbot.html](./frontend/chatbot.html)
- **Documentation**: [docs/index.html](./docs/index.html)

## Features
- 📊 Real-time Dashboard
- 🤖 AI-Powered Chatbot Interface
- 📦 Inventory Management UI
- 📈 Advanced Analytics
- 🚛 Logistics Tracking
- 💼 Enterprise Features

## Technology Stack
- HTML5, CSS3, JavaScript
- Chart.js for analytics
- Font Awesome icons
- Responsive design

## Note
This is a frontend-only deployment. For the full-stack version with backend APIs, 
please visit: [GitHub Repository](https://github.com/samarth4jain/smart-warehouse-system)

Deployed on: $(date)
EOF

echo "✅ Deployment preparation complete!"
echo "📁 Ready to push to GitHub Pages"
