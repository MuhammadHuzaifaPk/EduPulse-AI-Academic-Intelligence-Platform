import json
import re
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AIModelInferenceError

class GeminiService:
    """
    Wrapper for Google GenAI SDK (Gemini 2.5 Flash).
    Handles structured reasoning, long-context summarization, flashcard synthesis,
    and adaptive roadmap generation.
    """

    def __init__(self):
        try:
            # Initialize official GenAI client with configured API key
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model_name = settings.GEMINI_MODEL_NAME
            logger.info(f"GeminiService initialized using model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {str(e)}")
            raise AIModelInferenceError(f"Gemini client initialization failed: {str(e)}")

    def _clean_json_response(self, text: str) -> str:
        """Removes Markdown code block ticks if LLM wraps JSON response in ```json ... ```."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return text.strip()

    async def generate_youtube_summary_and_quiz(
        self, transcript_text: str, title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes YouTube transcript into structured notes, key takeaways, and a self-assessment quiz.
        """
        system_instruction = (
            "You are EduPulse AI, an expert academic co-pilot. Your task is to analyze lecture transcripts "
            "and produce clear, highly structured academic notes, core takeaway bullet points, key terminology definitions, "
            "and a 5-question multiple choice quiz for study assessment. "
            "You MUST respond ONLY with a valid JSON object matching the requested schema."
        )

        prompt = f"""
        Video Title: {title or 'Academic Lecture / Video'}
        
        Transcript Context:
        {transcript_text[:30000]}  # Truncated to safe token limit for processing speed

        Generate a JSON object with the exact following schema:
        {{
            "executive_summary": "A concise 2-3 sentence overview of the video content.",
            "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3", "Takeaway 4"],
            "core_concepts": [
                {{"concept": "Term Name", "definition": "Clear concise explanation"}}
            ],
            "structured_notes": "Detailed Markdown formatted structured notes with headings and bullet points.",
            "quiz": [
                {{
                    "id": 1,
                    "question": "Question text?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "explanation": "Why this answer is correct."
                }}
            ]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                    response_mime_type="application/json",
                ),
            )
            
            raw_text = self._clean_json_response(response.text)
            parsed_data = json.loads(raw_text)
            return parsed_data

        except json.JSONDecodeError as err:
            logger.error(f"Gemini output parsing error: {err}. Raw response: {response.text}")
            raise AIModelInferenceError("Failed to parse AI structured output into valid JSON.")
        except Exception as err:
            logger.error(f"Gemini YouTube Summary generation error: {str(err)}")
            raise AIModelInferenceError(f"Gemini API execution error: {str(err)}")

    async def generate_study_roadmap(
        self, subject: str, target_days: int, daily_hours: float, current_level: str
    ) -> Dict[str, Any]:
        """
        Generates a structured, day-by-day learning roadmap tailored to user input constraints.
        """
        system_instruction = (
            "You are an elite academic curriculum designer. Create a realistic, highly effective, "
            "phase-by-phase learning schedule and study roadmap based on the student's constraints."
        )

        prompt = f"""
        Subject / Topic: {subject}
        Target Completion Horizon: {target_days} Days
        Daily Study Commitment: {daily_hours} Hours/day
        Student Starting Level: {current_level}

        Generate a JSON object with this exact structure:
        {{
            "roadmap_title": "Mastering {subject} in {target_days} Days",
            "overview": "High-level strategy and learning methodology.",
            "total_estimated_hours": {target_days * daily_hours},
            "phases": [
                {{
                    "phase_number": 1,
                    "phase_title": "Phase Title",
                    "day_range": "Days 1-3",
                    "objectives": ["Objective 1", "Objective 2"],
                    "daily_tasks": [
                        {{
                            "day": 1,
                            "task_name": "Task Name",
                            "duration_minutes": 60,
                            "resource_type": "Reading / Practice / Project",
                            "details": "Specific actionable steps."
                        }}
                    ]
                }}
            ],
            "pro_tips": ["Tip 1", "Tip 2", "Tip 3"]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.4,
                    response_mime_type="application/json",
                ),
            )

            raw_text = self._clean_json_response(response.text)
            return json.loads(raw_text)

        except Exception as err:
            logger.error(f"Gemini Roadmap generation error: {str(err)}")
            raise AIModelInferenceError(f"Roadmap generation failed: {str(err)}")

    async def answer_context_question(
        self, context_text: str, question: str
    ) -> Dict[str, Any]:
        """
        Answers specific questions grounded strictly in provided context (PDF or Transcript).
        """
        prompt = f"""
        Context Material:
        ---
        {context_text[:25000]}
        ---

        User Question: {question}

        Answer the question accurately using ONLY the provided context. If the answer cannot be determined directly from the context, state that clearly. Include relevant quotes or section references where applicable.

        Respond with JSON format:
        {{
            "answer": "Detailed answer based on context.",
            "confidence_score": 0.95,
            "relevant_quotes": ["Quote 1", "Quote 2"]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json"
                ),
            )
            return json.loads(self._clean_json_response(response.text))
        except Exception as err:
            logger.error(f"Gemini Context Q&A error: {str(err)}")
            raise AIModelInferenceError(f"Context Q&A failed: {str(err)}")

# Global Singleton Instance
gemini_service = GeminiService()