from sqlalchemy import Column, String, Text, DateTime, Float, JSON
from app.core.database import Base
from datetime import datetime
import uuid

class Issue(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, default=lambda: f"iss-{str(uuid.uuid4())[:8]}")
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="open")
    priority = Column(String(20), nullable=False, default="medium")
    assignee = Column(String(100), nullable=True)
    reporter = Column(String(100), nullable=True)
    labels = Column(JSON, nullable=True, default=list)
    due_date = Column(DateTime, nullable=True)
    estimated_hours = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assignee": self.assignee,
            "reporter": self.reporter,
            "labels": self.labels or [],
            "dueDate": self.due_date.isoformat() if self.due_date else None,
            "estimatedHours": self.estimated_hours,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
