# 🚨 Deployment Troubleshooting Guide

## Common Railway Deployment Issues & Fixes

### Issue 1: Build Timeout
**Problem**: Dependencies taking too long to install
**Fix**: Use minimal requirements
```bash
# Use requirements.minimal.txt instead
cp requirements.minimal.txt requirements.txt
git commit -am "Use minimal requirements for deployment"
git push
```

### Issue 2: Memory Issues
**Problem**: App crashes due to memory limits
**Fix**: Reduce memory usage in Dockerfile
```dockerfile
# Use smaller Python base image
FROM python:3.11-slim
# Install only essential packages
```

### Issue 3: Port Issues
**Problem**: App not accessible
**Fix**: Ensure correct port binding
```bash
# In start.sh, use Railway's PORT variable
uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Issue 4: Database Issues
**Problem**: SQLite permissions or path issues
**Fix**: Use relative database path
```python
DATABASE_URL = "sqlite:///./smart_warehouse.db"
```

---

## 🔧 Quick Fixes

### Option 1: Minimal Deployment
```bash
# 1. Switch to minimal requirements
cp requirements.minimal.txt requirements.txt

# 2. Use optimized Dockerfile
cp Dockerfile.railway Dockerfile

# 3. Commit and redeploy
git add .
git commit -m "Optimize for deployment"
git push
```

### Option 2: Alternative Platforms

#### Render.com (if Railway fails)
1. Go to render.com
2. Connect GitHub repo
3. Use these settings:
   - **Build Command**: `pip install -r requirements.minimal.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

#### Fly.io (Docker-based)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Create fly.toml
fly launch --no-deploy

# Deploy
fly deploy
```

---

## 🏥 Health Check URLs
- Main app: `https://your-app.railway.app/`
- Health check: `https://your-app.railway.app/health`
- Dashboard: `https://your-app.railway.app/dashboard`
- API docs: `https://your-app.railway.app/docs`

---

## 💬 Tell me the specific error you're seeing and I'll help fix it!
