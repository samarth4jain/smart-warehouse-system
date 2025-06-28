#!/bin/bash

# GitHub Deployment Script for Smart Warehouse Management System
# This script helps automate the GitHub deployment process

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_status "Smart Warehouse Management System - GitHub Deployment"
print_status "============================================================"

# Check prerequisites
print_status "Checking prerequisites..."

if ! command_exists git; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

if ! command_exists docker; then
    print_warning "Docker is not installed. Some deployment options will not be available."
fi

print_success "Prerequisites check completed"

# Get user input
echo ""
print_status "Setting up GitHub deployment..."

read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: smart-warehouse-system): " REPO_NAME
REPO_NAME=${REPO_NAME:-smart-warehouse-system}

read -p "Enter your email for git config: " USER_EMAIL
read -p "Enter your name for git config: " USER_NAME

# Configure git
print_status "Configuring Git..."
git config user.email "$USER_EMAIL"
git config user.name "$USER_NAME"

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    print_warning "Remote origin already exists. Removing..."
    git remote remove origin
fi

# Add GitHub remote
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
print_status "Adding GitHub remote: $REPO_URL"
git remote add origin "$REPO_URL"

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your configuration before deploying"
fi

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_status "Switching to main branch..."
    git checkout -b main 2>/dev/null || git checkout main
fi

# Offer to push to GitHub
echo ""
print_status "Ready to deploy to GitHub!"
print_status "Repository URL: $REPO_URL"
print_status "Current branch: $(git branch --show-current)"
print_status "Files to be pushed: $(git ls-files | wc -l) files"

echo ""
read -p "Do you want to push to GitHub now? (y/N): " PUSH_CONFIRM

if [[ $PUSH_CONFIRM =~ ^[Yy]$ ]]; then
    print_status "Pushing to GitHub..."
    
    # Try to push
    if git push -u origin main; then
        print_success "Successfully pushed to GitHub!"
        print_success "Repository URL: $REPO_URL"
        
        echo ""
        print_status "Next steps:"
        echo "1. Visit your repository: $REPO_URL"
        echo "2. Set up GitHub Pages (optional): Settings → Pages"
        echo "3. Configure GitHub Secrets for CI/CD (see DEPLOYMENT.md)"
        echo "4. Review and customize the GitHub Actions workflows"
        echo "5. Edit .env file with your production configuration"
        
    else
        print_error "Failed to push to GitHub. Make sure:"
        echo "1. The repository exists on GitHub"
        echo "2. You have push access to the repository"
        echo "3. You're authenticated with GitHub"
        echo ""
        print_status "You can try pushing manually:"
        echo "git push -u origin main"
    fi
else
    print_status "Skipping GitHub push. You can push manually later:"
    echo "git push -u origin main"
fi

# Offer to create GitHub repository
echo ""
read -p "Do you want to open GitHub to create the repository? (y/N): " OPEN_GITHUB

if [[ $OPEN_GITHUB =~ ^[Yy]$ ]]; then
    if command_exists open; then
        open "https://github.com/new"
    elif command_exists xdg-open; then
        xdg-open "https://github.com/new"
    else
        print_status "Please visit: https://github.com/new"
    fi
fi

# Docker setup option
echo ""
read -p "Do you want to test the Docker setup? (y/N): " TEST_DOCKER

if [[ $TEST_DOCKER =~ ^[Yy]$ ]] && command_exists docker; then
    print_status "Testing Docker setup..."
    
    if docker build -t smart-warehouse-test .; then
        print_success "Docker build successful!"
        
        print_status "Starting container for testing..."
        if docker run -d -p 8000:8000 --name smart-warehouse-test smart-warehouse-test; then
            print_success "Container started successfully!"
            print_status "Application should be available at: http://localhost:8000"
            print_status "API docs available at: http://localhost:8000/docs"
            
            # Wait a moment then clean up
            sleep 5
            print_status "Cleaning up test container..."
            docker stop smart-warehouse-test >/dev/null 2>&1 || true
            docker rm smart-warehouse-test >/dev/null 2>&1 || true
            docker rmi smart-warehouse-test >/dev/null 2>&1 || true
            print_success "Cleanup completed"
        fi
    else
        print_error "Docker build failed. Please check the Dockerfile and try again."
    fi
fi

echo ""
print_success "GitHub deployment setup completed!"
print_status "Documentation available:"
echo "• README.md - Project overview and installation"
echo "• DEPLOYMENT.md - Detailed deployment guide"
echo "• CONTRIBUTING.md - How to contribute"
echo "• .github/ - GitHub Actions workflows and templates"

print_status "Happy deploying! 🚀"
