from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate, IssuesListResponse, PaginationResponse
from datetime import datetime
import math

class IssueService:
    def __init__(self, db: Session):
        self.db = db

    def list_issues(
        self, 
        search: Optional[str] = None,
        status: Optional[List[str]] = None,
        priority: Optional[List[str]] = None,
        assignee: Optional[List[str]] = None,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> IssuesListResponse:

        query = self.db.query(Issue)

        # Apply filters
        if search:
            search_filter = or_(
                Issue.title.ilike(f"%{search}%"),
                Issue.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)

        if status:
            query = query.filter(Issue.status.in_(status))

        if priority:
            query = query.filter(Issue.priority.in_(priority))

        if assignee:
            query = query.filter(Issue.assignee.in_(assignee))

        # Apply sorting
        sort_column = getattr(Issue, sort_by, Issue.updated_at)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Get total count before pagination
        total_items = query.count()
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        # Apply pagination
        offset = (page - 1) * page_size
        issues = query.offset(offset).limit(page_size).all()

        # Get available filter options
        all_issues = self.db.query(Issue).all()
        available_statuses = list(set(issue.status for issue in all_issues))
        available_priorities = list(set(issue.priority for issue in all_issues))
        available_assignees = list(set(issue.assignee for issue in all_issues if issue.assignee))

        pagination = PaginationResponse(
            current_page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )

        filters = {
            "availableStatuses": available_statuses,
            "availablePriorities": available_priorities,
            "availableAssignees": available_assignees
        }

        return IssuesListResponse(
            issues=[self._issue_to_response(issue) for issue in issues],
            pagination=pagination,
            filters=filters
        )

    def get_issue(self, issue_id: str) -> Optional[Issue]:
        return self.db.query(Issue).filter(Issue.id == issue_id).first()

    def create_issue(self, issue_data: IssueCreate) -> Issue:
        issue = Issue(
            title=issue_data.title,
            description=issue_data.description,
            status=issue_data.status,
            priority=issue_data.priority,
            assignee=issue_data.assignee,
            reporter=issue_data.reporter,
            labels=issue_data.labels,
            due_date=issue_data.due_date,
            estimated_hours=issue_data.estimated_hours
        )

        self.db.add(issue)
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def update_issue(self, issue_id: str, issue_data: IssueUpdate) -> Optional[Issue]:
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return None

        update_data = issue_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "due_date":
                setattr(issue, "due_date", value)
            elif field == "estimated_hours":
                setattr(issue, "estimated_hours", value)
            else:
                setattr(issue, field, value)

        issue.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def delete_issue(self, issue_id: str) -> bool:
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return False

        self.db.delete(issue)
        self.db.commit()
        return True

    def bulk_create_issues(self, issues_data: List[IssueCreate]) -> List[Issue]:
        issues = []
        for issue_data in issues_data:
            issue = Issue(
                title=issue_data.title,
                description=issue_data.description,
                status=issue_data.status,
                priority=issue_data.priority,
                assignee=issue_data.assignee,
                reporter=issue_data.reporter,
                labels=issue_data.labels,
                due_date=issue_data.due_date,
                estimated_hours=issue_data.estimated_hours
            )
            issues.append(issue)

        self.db.add_all(issues)
        self.db.commit()
        return issues

    def _issue_to_response(self, issue: Issue):
        return {
            "id": issue.id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status,
            "priority": issue.priority,
            "assignee": issue.assignee,
            "reporter": issue.reporter,
            "labels": issue.labels or [],
            "dueDate": issue.due_date.isoformat() if issue.due_date else None,
            "estimatedHours": issue.estimated_hours,
            "createdAt": issue.created_at.isoformat(),
            "updatedAt": issue.updated_at.isoformat()
        }
