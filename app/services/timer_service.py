import math
from typing import Dict, Any, List
from app.core.logger import logger

class TimerAnalyticsService:
    """
    In-memory analytics aggregator for user study sessions, focus scores,
    and Pomodoro metrics.
    """

    def __init__(self):
        # In-memory store for session logs (can be replaced with DB persistence)
        self._session_db: List[Dict[str, Any]] = []

    def record_session(
        self,
        session_type: str,
        duration_seconds: int,
        completed: bool,
        subject_tag: str = "General",
        distraction_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculates productivity score and logs a completed focus session.
        Score formula considers completion status, duration, and distraction penalties.
        """
        minutes = duration_seconds / 60.0
        
        # Base productivity score computation
        base_score = 100.0 if completed else (minutes / 25.0) * 70.0
        distraction_penalty = distraction_count * 8.0
        final_score = max(0.0, min(100.0, round(base_score - distraction_penalty, 1)))

        session_record = {
            "session_id": len(self._session_db) + 1,
            "session_type": session_type,  # 'pomodoro', 'short_break', 'long_break'
            "duration_seconds": duration_seconds,
            "duration_minutes": round(minutes, 1),
            "completed": completed,
            "subject_tag": subject_tag,
            "distraction_count": distraction_count,
            "productivity_score": final_score
        }

        self._session_db.append(session_record)
        logger.info(f"Recorded study session #{session_record['session_id']} for subject '{subject_tag}' with score {final_score}")
        return session_record

    def get_aggregate_stats() -> Dict[str, Any]:
        """Calculates global study statistics, focus time, and average productivity score."""
        total_sessions = len(self._session_db)
        if total_sessions == 0:
            return {
                "total_study_minutes": 0.0,
                "total_completed_pomodoros": 0,
                "average_productivity_score": 0.0,
                "subject_breakdown": {},
                "total_sessions_count": 0
            }

        total_study_seconds = sum(s["duration_seconds"] for s in self._session_db if s["session_type"] == "pomodoro")
        completed_pomodoros = sum(1 for s in self._session_db if s["session_type"] == "pomodoro" and s["completed"])
        scores = [s["productivity_score"] for s in self._session_db if s["session_type"] == "pomodoro"]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        # Group by subject tag
        subject_map: Dict[str, float] = {}
        for s in self._session_db:
            if s["session_type"] == "pomodoro":
                tag = s["subject_tag"]
                subject_map[tag] = subject_map.get(tag, 0.0) + s["duration_minutes"]

        return {
            "total_study_minutes": round(total_study_seconds / 60.0, 1),
            "total_completed_pomodoros": completed_pomodoros,
            "average_productivity_score": avg_score,
            "subject_breakdown": subject_map,
            "total_sessions_count": total_sessions
        }

# Global Singleton Instance
timer_service = TimerAnalyticsService()