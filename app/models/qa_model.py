from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ContextQARequest(BaseModel):
    context_text: str = Field(..., min_length=10, description="Document text or transcript excerpt")
    question: str = Field(..., min_length=3, description="Question regarding context")
    use_huggingface_extractive: bool = Field(default=False, description="Flag to toggle HF extractive model vs Gemini reasoning")

class ContextQAResponse(BaseModel):
    answer: str
    confidence_score: float
    relevant_quotes: List[str] = []
    engine_used: str

class FocusSessionLogRequest(BaseModel):
    session_type: str = Field(..., description="'pomodoro', 'short_break', or 'long_break'")
    duration_seconds: int = Field(..., ge=1, description="Duration in seconds")
    completed: bool = Field(default=True, description="Completed without cancellation")
    subject_tag: str = Field(default="General", description="Subject title or tag")
    distraction_count: int = Field(default=0, ge=0, description="Number of reported distractions")

class FocusSessionLogResponse(BaseModel):
    session_id: int
    session_type: str
    duration_minutes: float
    completed: bool
    subject_tag: str
    productivity_score: float