from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RoadmapRequest(BaseModel):
    subject: str = Field(..., example="Organic Chemistry & Reaction Mechanisms")
    target_days: int = Field(default=7, ge=1, le=90, description="Total days target")
    daily_hours: float = Field(default=2.0, ge=0.5, le=12.0, description="Hours dedicated per day")
    current_level: str = Field(default="Beginner", description="Starting level: Beginner, Intermediate, Advanced")
    additional_notes: Optional[str] = Field(default="", description="Specific exam goals or sub-topics")

class DailyTask(BaseModel):
    day: int
    task_name: str
    duration_minutes: int
    resource_type: str
    details: str

class RoadmapPhase(BaseModel):
    phase_number: int
    phase_title: str
    day_range: str
    objectives: List[str]
    daily_tasks: List[DailyTask]

class RoadmapResponse(BaseModel):
    roadmap_title: str
    overview: str
    total_estimated_hours: float
    phases: List[RoadmapPhase]
    pro_tips: List[str]
    meta: Dict[str, Any]