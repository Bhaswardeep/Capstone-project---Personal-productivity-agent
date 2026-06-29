"""Dashboard API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database.database import get_db
from backend.models.models import User
from backend.services.dashboard import get_dashboard_statistics

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def read_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Return dashboard statistics for the authenticated user."""
    return get_dashboard_statistics(db=db, user_id=current_user.id)
