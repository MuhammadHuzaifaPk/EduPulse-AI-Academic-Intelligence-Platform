from fastapi import APIRouter, HTTPException, status
from app.services.roadmap_service import roadmap_service
from app.models.roadmap_model import RoadmapRequest, RoadmapResponse
from app.core.exceptions import AIModelInferenceError, get_http_exception_from_custom
from app.core.logger import logger

router = APIRouter(prefix="/roadmap", tags=["Study Schedule & Roadmap Generator"])

@router.post("/generate", response_model=RoadmapResponse, status_code=status.HTTP_200_OK)
async def generate_study_roadmap(payload: RoadmapRequest):
    """
    Generates a phase-by-phase daily study roadmap and workload estimate
    tailored to student timeline, commitment hours, and starting skill level.
    """
    try:
        logger.info(f"Generating study roadmap for topic: '{payload.subject}' over {payload.target_days} days")
        
        roadmap = await roadmap_service.generate_custom_roadmap(
            subject=payload.subject,
            target_days=payload.target_days,
            daily_hours=payload.daily_hours,
            current_level=payload.current_level,
            additional_notes=payload.additional_notes or ""
        )
        return roadmap

    except AIModelInferenceError as exc:
        raise get_http_exception_from_custom(exc)
    except Exception as exc:
        logger.error(f"Unexpected error generating roadmap: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate study roadmap: {str(exc)}"
        )