# Local Development Setup

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/samarth4jain/smart-warehouse-system.git
cd smart-warehouse-system
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
cd backend
python -c "from app.database import init_db; init_db()"
```

### 4. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open Frontend
- **Option 1**: Open `frontend/index.html` in your browser
- **Option 2**: Use a local server:
```bash
# From project root
python -m http.server 3000
# Then visit: http://localhost:3000/frontend/
```

## API Endpoints

Once running locally, the API will be available at:
- Base URL: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Environment Variables

Create a `.env` file in the backend directory:
```env
DATABASE_URL=sqlite:///./smart_warehouse.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Production Deployment

For production deployment, see `DEPLOYMENT.md` for detailed instructions including:
- Docker containerization
- Cloud deployment options
- Environment configuration
- Security considerations
