# Issue Tracker System - Full Stack

A comprehensive full-stack web application for tracking software development issues.

## Architecture
- **Frontend**: Angular 16+ with TypeScript
- **Backend**: Python FastAPI with SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)

## Quick Setup

### Prerequisites
- Node.js 16+
- Python 3.10+
- Git (optional)
# Setup angular in frontend directory
### Development Setup
```bash
# 1. Clone/extract the project
cd issue-tracker-system

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# 3. Setup frontend (new terminal)
cd ../frontend
npm install
ng serve --port 4200
```

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Access URLs
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features
- Complete CRUD operations for issues
- Advanced filtering and search
- Real-time updates
- Responsive design
- Professional UI with Material Design
- Comprehensive API documentation
- Docker containerization
- Production-ready configuration

For detailed setup instructions, see `docs/setup-guide.md`.
