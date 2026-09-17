from fastapi import APIRouter, status, HTTPException
from app.services.timer_service import timer_service
from app.models.qa_model import FocusSessionLogRequest, FocusSessionLogResponse
from app.core.logger import logger

router = APIRouter(prefix="/analytics", tags=["Focus Timer & Analytics"])

@router.post("/session", response_model=FocusSessionLogResponse, status_code=status.HTTP_201_CREATED)
async def log_focus_session(payload: FocusSessionLogRequest):
    """
    Logs a completed or interrupted Pomodoro study session and calculates
    productivity metric scores based on distractions and duration.
    """
    try:
        session = timer_service.record_session(
            session_type=payload.session_type,
            duration_seconds=payload.duration_seconds,
            completed=payload.completed,
            subject_tag=payload.subject_tag,
            distraction_count=payload.distraction_count
        )
        return FocusSessionLogResponse(
            session_id=session["session_id"],
            session_type=session["session_type"],
            duration_minutes=session["duration_minutes"],
            completed=session["completed"],
            subject_tag=session["subject_tag"],
            productivity_score=session["productivity_score"]
        )
    except Exception as exc:
        logger.error(f"Failed to log study session: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record study session."
        )

@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_study_statistics():
    """
    Returns aggregated productivity statistics, total focus time,
    and subject breakdown metrics.
    """
    try:
        stats = timer_service.get_aggregate_stats()
        return {"status": "success", "analytics": stats}
    except Exception as exc:
        logger.error(f"Failed to calculate study statistics: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analytics data."
        )