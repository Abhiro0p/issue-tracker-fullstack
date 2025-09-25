from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate, IssueResponse, IssuesListResponse, PaginationResponse
from app.services.issue_service import IssueService

router = APIRouter()

@router.get("/", response_model=IssuesListResponse)
def list_issues(
    search: Optional[str] = Query(None, description="Full-text search in title and description"),
    status: Optional[List[str]] = Query(None, description="Filter by one or more status values"),
    priority: Optional[List[str]] = Query(None, description="Filter by one or more priority levels"),
    assignee: Optional[List[str]] = Query(None, description="Filter by assignee names"),
    sort_by: str = Query("updated_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort direction (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(20, ge=10, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List issues with advanced filtering and pagination.

    Supports filtering by search term, status, priority, assignee, and sorting options.
    Returns paginated results with metadata about available filter options.
    """
    service = IssueService(db)
    return service.list_issues(
        search=search, status=status, priority=priority, assignee=assignee,
        sort_by=sort_by, sort_order=sort_order, page=page, page_size=page_size
    )

@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: str, db: Session = Depends(get_db)):
    """
    Get a single issue by ID.

    Returns complete issue information including all fields.
    """
    service = IssueService(db)
    issue = service.get_issue(issue_id)
    if not issue:
        raise HTTPException(
            status_code=404, 
            detail={
                "error": {
                    "code": "ISSUE_NOT_FOUND",
                    "message": f"Issue with ID '{issue_id}' not found",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            }
        )
    return issue

@router.post("/", response_model=IssueResponse, status_code=201)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    """
    Create a new issue.

    Auto-generates ID, createdAt, and updatedAt fields.
    """
    service = IssueService(db)
    return service.create_issue(issue)

@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue(issue_id: str, issue: IssueUpdate, db: Session = Depends(get_db)):
    """
    Update an existing issue.

    Only provided fields will be updated. Auto-updates updatedAt field.
    """
    service = IssueService(db)
    updated_issue = service.update_issue(issue_id, issue)
    if not updated_issue:
        raise HTTPException(
            status_code=404, 
            detail={
                "error": {
                    "code": "ISSUE_NOT_FOUND",
                    "message": f"Issue with ID '{issue_id}' not found",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            }
        )
    return updated_issue

@router.delete("/{issue_id}")
def delete_issue(issue_id: str, db: Session = Depends(get_db)):
    """
    Delete an issue by ID.
    """
    service = IssueService(db)
    if not service.delete_issue(issue_id):
        raise HTTPException(
            status_code=404, 
            detail={
                "error": {
                    "code": "ISSUE_NOT_FOUND",
                    "message": f"Issue with ID '{issue_id}' not found",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            }
        )
    return {"message": "Issue deleted successfully"}

@router.post("/bulk", response_model=List[IssueResponse])
def bulk_create_issues(issues: List[IssueCreate], db: Session = Depends(get_db)):
    """
    Create multiple issues in bulk.
    """
    service = IssueService(db)
    return service.bulk_create_issues(issues)
