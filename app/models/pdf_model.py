from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PDFSummaryRequest(BaseModel):
    summary_depth: str = Field(default="standard", description="Depth level: 'concise', 'standard', 'deep'")

class PDFProcessResponse(BaseModel):
    filename: str
    total_pages: int
    total_words: int
    estimated_reading_minutes: float
    executive_summary: str
    key_takeaways: List[str]
    core_concepts: List[Dict[str, str]]
    structured_notes: str
    quiz: List[Dict[str, Any]]