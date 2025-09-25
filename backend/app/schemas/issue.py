from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    open = "open"
    in_progress = "in-progress" 
    resolved = "resolved"
    closed = "closed"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: StatusEnum = StatusEnum.open
    priority: PriorityEnum = PriorityEnum.medium
    assignee: Optional[str] = Field(None, max_length=100)
    reporter: Optional[str] = Field(None, max_length=100)
    labels: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('assignee', 'reporter')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Must be a valid email address')
        return v

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    assignee: Optional[str] = Field(None, max_length=100)
    reporter: Optional[str] = Field(None, max_length=100)
    labels: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)

class IssueResponse(IssueBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginationResponse(BaseModel):
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool

class IssuesListResponse(BaseModel):
    issues: List[IssueResponse]
    pagination: PaginationResponse
    filters: dict
