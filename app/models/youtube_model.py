from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any

class YouTubeProcessRequest(BaseModel):
    video_url: str = Field(
        ...,
        description="Full YouTube URL or 11-character video ID",
        example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    generate_quiz: bool = Field(default=True, description="Whether to include self-assessment quiz")

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class ConceptDefinition(BaseModel):
    concept: str
    definition: str

class YouTubeProcessResponse(BaseModel):
    video_id: str
    video_url: str
    word_count: int
    executive_summary: str
    key_takeaways: List[str]
    core_concepts: List[ConceptDefinition]
    structured_notes: str
    quiz: List[QuizQuestion]
    timestamps: List[Dict[str, Any]]