# 🐳 Smart Warehouse Management System - Production Docker Setup
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    gunicorn==21.2.0 \
    uvicorn[standard]==0.24.0 \
    redis==5.0.1 \
    celery==5.3.4 \
    psycopg2-binary==2.9.9 \
    prometheus-client==0.19.0

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 warehouse && chown -R warehouse:warehouse /app
USER warehouse

# Expose ports
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Production startup command
CMD ["gunicorn", "backend.app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001", "--access-logfile", "-", "--error-logfile", "-"]
