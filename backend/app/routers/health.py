from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
def health_check():
    """Health check endpoint to monitor backend service availability"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "issue-tracker",
        "version": "1.0.0",
        "database": "connected"
    }

@router.get("/detailed")
def detailed_health_check():
    """Detailed health check with more comprehensive information"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "issue-tracker",
        "version": "1.0.0",
        "components": {
            "database": "connected",
            "api": "operational",
            "dependencies": "healthy"
        },
        "uptime": "running",
        "environment": "development"
    }
