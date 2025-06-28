# GitHub Deployment Guide

This guide will help you deploy the Smart Warehouse Management System to GitHub and set up various deployment options.

## 🚀 Quick Deployment to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon and select "New repository"
3. Name your repository: `smart-warehouse-system`
4. Add description: "AI-powered warehouse management system with real-time inventory tracking, demand forecasting, and intelligent chatbot assistant"
5. Choose "Public" or "Private" based on your needs
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### Step 2: Push to GitHub

```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/smart-warehouse-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Set Up GitHub Pages (Optional)

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll down to "Pages" section
4. Under "Source", select "Deploy from a branch"
5. Choose "main" branch and "/ (root)" folder
6. Click "Save"
7. Your site will be available at `https://YOUR_USERNAME.github.io/smart-warehouse-system`

## 🔧 Environment Setup for Deployment

### GitHub Secrets Configuration

For CI/CD and deployment, set up these secrets in your GitHub repository:

1. Go to repository Settings → Secrets and variables → Actions
2. Add the following secrets:

```
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password
DATABASE_URL=your_production_database_url
API_HOST=0.0.0.0
API_PORT=8000
```

### Environment Variables

Create production environment files:

**.env.production**
```env
DATABASE_URL=postgresql://user:password@host:port/database
API_HOST=0.0.0.0
API_PORT=8000
ENABLE_AI_FEATURES=true
LOG_LEVEL=INFO
```

## 🐳 Docker Deployment Options

### Option 1: GitHub Container Registry

The CI/CD pipeline automatically builds and pushes to GitHub Container Registry:

```bash
# Pull and run from GitHub Container Registry
docker pull ghcr.io/YOUR_USERNAME/smart-warehouse-system:latest
docker run -p 8000:8000 ghcr.io/YOUR_USERNAME/smart-warehouse-system:latest
```

### Option 2: Docker Hub

```bash
# Build and push to Docker Hub
docker build -t YOUR_USERNAME/smart-warehouse-system .
docker push YOUR_USERNAME/smart-warehouse-system

# Run from Docker Hub
docker run -p 8000:8000 YOUR_USERNAME/smart-warehouse-system
```

### Option 3: Local Docker Compose

```bash
# Clone and run with Docker Compose
git clone https://github.com/YOUR_USERNAME/smart-warehouse-system.git
cd smart-warehouse-system
docker-compose up --build
```

## ☁️ Cloud Deployment Options

### Heroku Deployment

1. Install Heroku CLI
2. Create Heroku app:
```bash
heroku create your-app-name
heroku config:set DATABASE_URL=your_database_url
git push heroku main
```

3. Add Procfile:
```
web: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### AWS ECS Deployment

1. Build and push to ECR
2. Create ECS task definition
3. Set up ECS service
4. Configure load balancer

### Google Cloud Run

```bash
# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/smart-warehouse
gcloud run deploy --image gcr.io/PROJECT_ID/smart-warehouse --platform managed
```

### Azure Container Instances

```bash
# Deploy to Azure
az container create --resource-group myResourceGroup \
  --name smart-warehouse --image YOUR_USERNAME/smart-warehouse-system \
  --ports 8000 --ip-address public
```

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions workflows:

### **`.github/workflows/ci-cd.yml`**
- Runs tests on multiple Python versions
- Security scanning with safety and bandit
- Docker image building and testing
- Automatic deployment on main branch

### **`.github/workflows/deploy.yml`**
- Production deployment workflow
- Triggered by releases or manual dispatch
- Builds and pushes to container registry
- Supports staging and production environments

## 📊 Monitoring and Observability

### GitHub Insights
- Use GitHub's built-in analytics
- Monitor CI/CD pipeline performance
- Track issues and pull requests

### Application Monitoring
```python
# Add to your FastAPI app for health checks
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Logging Setup
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🛡️ Security Best Practices

1. **Never commit sensitive data**
   - Use .env files (already in .gitignore)
   - Use GitHub Secrets for CI/CD
   - Rotate API keys regularly

2. **Dependency Management**
   - Regular dependency updates
   - Security scanning in CI/CD
   - Pin dependency versions

3. **Container Security**
   - Use official base images
   - Regular security updates
   - Scan images for vulnerabilities

## 🔧 Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Find and kill processes using port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection issues:**
```bash
# Check database connectivity
python -c "from backend.app.database import engine; print(engine.url)"
```

**Docker build failures:**
```bash
# Clean Docker cache
docker system prune -a
```

### Getting Help

1. Check the [Issues](https://github.com/YOUR_USERNAME/smart-warehouse-system/issues) page
2. Review the [Contributing Guidelines](CONTRIBUTING.md)
3. Check the [Wiki](https://github.com/YOUR_USERNAME/smart-warehouse-system/wiki) for detailed documentation

## 📈 Scaling Considerations

### Database Scaling
- Use PostgreSQL for production
- Implement connection pooling
- Consider read replicas for analytics

### Application Scaling
- Use load balancers
- Implement horizontal scaling
- Consider microservices architecture

### Monitoring Scaling
- Set up application metrics
- Use container orchestration (Kubernetes)
- Implement auto-scaling policies

---

## 🎉 Next Steps

1. **Customize for your needs**
   - Update repository name and URLs
   - Modify deployment configurations
   - Add your specific requirements

2. **Set up monitoring**
   - Configure health checks
   - Set up alerting
   - Monitor application performance

3. **Community engagement**
   - Star the repository
   - Report issues and contribute
   - Share your deployment success story

Happy deploying! 🚀
