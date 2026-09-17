from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RoadmapRequest(BaseModel):
    subject_title: str
    horizon_days: int
    daily_hours: float

@router.post("/generate")
async def generate_roadmap(payload: RoadmapRequest):
    schedule_items = []
    for day in range(1, min(payload.horizon_days + 1, 8)):
        schedule_items.append({
            "day": day,
            "topic": f"Module {day}: Key concepts for {payload.subject_title}",
            "hours": payload.daily_hours
        })

    return {
        "status": "success",
        "subject": payload.subject_title,
        "duration_days": payload.horizon_days,
        "daily_allocation_hours": payload.daily_hours,
        "schedule": schedule_items
    }