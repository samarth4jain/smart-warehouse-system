# GitHub Pages Deployment

This document describes the GitHub Pages deployment of the Smart Warehouse System demo.

## Live Demo

🌐 **Live Demo**: https://samarth4jain.github.io/smart-warehouse-system/

The GitHub Pages deployment provides:

### 📱 Demo Interface
- **Static Demo**: Interactive demo with sample data
- **Feature Showcase**: Overview of all system capabilities
- **Setup Instructions**: Complete guide for local development
- **Repository Access**: Direct links to source code

### 🚀 What's Deployed

1. **Landing Page** (`/`) - Main project overview and features
2. **Demo Dashboard** (`/demo.html`) - Interactive demo with sample data
3. **Original Documentation** - All existing docs and resources

### ⚠️ Important Notes

**GitHub Pages Limitations:**
- Only serves static files (HTML, CSS, JavaScript)
- Cannot run the FastAPI backend server
- Demo uses mock/sample data instead of live database

**For Full Functionality:**
- Clone the repository locally
- Follow the setup instructions
- Run the backend server for live data and API connectivity

### 🔧 Local Development Setup

To run the complete application with backend functionality:

```bash
# Clone repository
git clone https://github.com/samarth4jain/smart-warehouse-system.git
cd smart-warehouse-system

# Install dependencies
pip3 install fastapi uvicorn sqlalchemy python-multipart python-dotenv jinja2 aiofiles

# Initialize database
python3 create_minimal_db.py

# Start backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8001

# Access full dashboard
# http://localhost:8001/dashboard
```

### 📊 Dashboard Features (Local Only)

When running locally, you get:
- **Live Data**: Real database connectivity
- **API Endpoints**: Full REST API functionality
- **Interactive Features**: Add/edit inventory, real-time updates
- **AI Assistant**: Working chatbot functionality
- **Analytics**: Real-time charts and metrics

### 🔄 Deployment Process

The GitHub Pages deployment automatically triggers on:
- Push to `main` branch
- Manual workflow dispatch

**Workflow Steps:**
1. Checkout repository
2. Setup GitHub Pages
3. Copy docs to build directory
4. Use `landing.html` as main index
5. Deploy to GitHub Pages

### 📋 File Structure

```
docs/
├── index.html          # Main landing page (copied from landing.html)
├── landing.html        # Source landing page
├── demo.html          # Interactive demo
├── style.css          # Styling
├── script.js          # JavaScript functionality
└── [other docs]       # Additional documentation
```

### 🌟 Benefits

**For Users:**
- Quick preview without setup
- Feature overview
- Easy access to source code
- Mobile-responsive demo

**For Developers:**
- Automatic deployment
- Version control integration
- Professional project showcase
- Easy sharing and collaboration

---

**Note**: The GitHub Pages demo showcases the interface and features but requires local setup for full backend functionality including database operations, API calls, and real-time data.
