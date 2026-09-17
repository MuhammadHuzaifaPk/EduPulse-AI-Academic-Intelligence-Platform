from fastapi import APIRouter, HTTPException, status
from app.services.youtube_service import youtube_service
from app.services.gemini_service import gemini_service
from app.models.youtube_model import YouTubeProcessRequest, YouTubeProcessResponse
from app.core.exceptions import TranscriptExtractionError, AIModelInferenceError, get_http_exception_from_custom
from app.core.logger import logger

router = APIRouter(prefix="/youtube", tags=["YouTube Intelligence"])

@router.post("/process", response_model=YouTubeProcessResponse, status_code=status.HTTP_200_OK)
async def process_youtube_video(payload: YouTubeProcessRequest):
    """
    Extracts transcripts from YouTube videos and executes Gemini 2.5 Flash to generate
    executive summaries, key takeaways, concept definitions, detailed notes, and a quiz.
    """
    try:
        logger.info(f"Received YouTube processing request for URL: {payload.video_url}")
        
        # Step 1: Retrieve video transcript
        transcript_data = await youtube_service.get_transcript(payload.video_url)
        
        # Step 2: Pass transcript to Gemini AI for structured notes & quiz synthesis
        ai_analysis = await gemini_service.generate_youtube_summary_and_quiz(
            transcript_text=transcript_data["transcript_text"],
            title=f"YouTube Video ID: {transcript_data['video_id']}"
        )

        # Step 3: Construct API response object
        response = YouTubeProcessResponse(
            video_id=transcript_data["video_id"],
            video_url=transcript_data["video_url"],
            word_count=transcript_data["word_count"],
            executive_summary=ai_analysis.get("executive_summary", "No summary available."),
            key_takeaways=ai_analysis.get("key_takeaways", []),
            core_concepts=ai_analysis.get("core_concepts", []),
            structured_notes=ai_analysis.get("structured_notes", ""),
            quiz=ai_analysis.get("quiz", []) if payload.generate_quiz else [],
            timestamps=transcript_data["timestamps"][:15]  # Limit initial timestamps payload for network speed
        )
        return response

    except TranscriptExtractionError as exc:
        raise get_http_exception_from_custom(exc)
    except AIModelInferenceError as exc:
        raise get_http_exception_from_custom(exc)
    except Exception as exc:
        logger.error(f"Unexpected error in YouTube endpoint: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the YouTube video: {str(exc)}"
        )