# Deployment Guide

## Development Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

### Manual Deployment
1. Setup backend:
   ```bash
   cd backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Setup frontend:
   ```bash
   cd frontend
   npm install
   ng serve
   ```

## Production Deployment

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Cloud Deployment
Instructions for AWS, Google Cloud, and Azure deployments will be added.
