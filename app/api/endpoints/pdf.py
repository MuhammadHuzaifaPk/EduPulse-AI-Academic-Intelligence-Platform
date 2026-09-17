from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
from app.services.pdf_service import pdf_service
from app.services.gemini_service import gemini_service
from app.models.pdf_model import PDFProcessResponse
from app.core.exceptions import PDFProcessingError, AIModelInferenceError, InvalidFileFormatException, get_http_exception_from_custom
from app.core.config import settings
from app.core.logger import logger

router = APIRouter(prefix="/pdf", tags=["PDF & Document Intelligence"])

@router.post("/process", response_model=PDFProcessResponse, status_code=status.HTTP_200_OK)
async def process_pdf_document(
    file: UploadFile = File(...),
    summary_depth: Optional[str] = Form("standard")
):
    """
    Accepts PDF upload, validates size/format, extracts multi-page text,
    and runs Gemini LLM synthesis to create notes, summaries, and self-assessment quizzes.
    """
    logger.info(f"Received PDF processing request for file: {file.filename}")

    # Validate file type extension
    if not file.filename.lower().endswith('.pdf'):
        raise get_http_exception_from_custom(
            InvalidFileFormatException(f"File '{file.filename}' is not a valid PDF document.")
        )

    try:
        # Read file byte stream
        file_bytes = await file.read()
        
        # Validate upload size against setting limits
        if len(file_bytes) > settings.max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        # Step 1: Extract document text and metadata
        pdf_data = await pdf_service.extract_text_from_bytes(file_bytes, filename=file.filename)

        # Step 2: Synthesize structured notes and quiz with Gemini
        ai_analysis = await gemini_service.generate_youtube_summary_and_quiz(
            transcript_text=pdf_data["combined_text"],
            title=f"Document: {pdf_data['filename']}"
        )

        return PDFProcessResponse(
            filename=pdf_data["filename"],
            total_pages=pdf_data["total_pages"],
            total_words=pdf_data["total_words"],
            estimated_reading_minutes=pdf_data["estimated_reading_minutes"],
            executive_summary=ai_analysis.get("executive_summary", "No summary generated."),
            key_takeaways=ai_analysis.get("key_takeaways", []),
            core_concepts=ai_analysis.get("core_concepts", []),
            structured_notes=ai_analysis.get("structured_notes", ""),
            quiz=ai_analysis.get("quiz", [])
        )

    except PDFProcessingError as exc:
        raise get_http_exception_from_custom(exc)
    except AIModelInferenceError as exc:
        raise get_http_exception_from_custom(exc)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Unexpected error in PDF endpoint: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the PDF document: {str(exc)}"
        )