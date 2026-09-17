from typing import Dict, Any, List
from app.services.gemini_service import gemini_service
from app.core.logger import logger

class RoadmapService:
    """
    Service layer for constructing, formatting, and refining study schedules
    and milestone checkpoints using Gemini AI.
    """

    async def generate_custom_roadmap(
        self,
        subject: str,
        target_days: int,
        daily_hours: float,
        current_level: str,
        additional_notes: str = ""
    ) -> Dict[str, Any]:
        """
        Synthesizes student targets into an actionable, daily learning program.
        Calculates time allocations and milestone tracking metrics.
        """
        logger.info(f"Building roadmap for '{subject}' ({target_days} days, {daily_hours} hrs/day)")

        # Invoke Gemini AI model service
        raw_roadmap = await gemini_service.generate_study_roadmap(
            subject=subject,
            target_days=target_days,
            daily_hours=daily_hours,
            current_level=current_level
        )

        # Enrich roadmap with metadata and summary metrics
        total_days = target_days
        total_hours = round(target_days * daily_hours, 1)
        total_sessions = int((total_hours * 60) // 25)  # 25-minute Pomodoro block count

        raw_roadmap["meta"] = {
            "subject": subject,
            "target_days": total_days,
            "daily_hours": daily_hours,
            "total_hours": total_hours,
            "recommended_pomodoros": total_sessions,
            "starting_level": current_level,
            "notes": additional_notes
        }

        return raw_roadmap

# Global Singleton Instance
roadmap_service = RoadmapService()