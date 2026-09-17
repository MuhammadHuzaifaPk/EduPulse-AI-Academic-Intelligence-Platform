from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class EduPulseException(Exception):
    """Base exception class for all custom EduPulse application errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class TranscriptExtractionError(EduPulseException):
    """Raised when YouTube transcript retrieval fails."""
    pass

class PDFProcessingError(EduPulseException):
    """Raised when parsing or extracting text from a PDF document fails."""
    pass

class AIModelInferenceError(EduPulseException):
    """Raised when calls to Gemini or Hugging Face API models encounter failures."""
    pass

class InvalidFileFormatException(EduPulseException):
    """Raised when an unsupported file type is uploaded."""
    pass

# FastAPI Exception Handlers mapping
def get_http_exception_from_custom(exc: EduPulseException) -> HTTPException:
    if isinstance(exc, TranscriptExtractionError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Transcript Error", "message": exc.message, "details": exc.details}
        )
    elif isinstance(exc, PDFProcessingError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "PDF Processing Error", "message": exc.message, "details": exc.details}
        )
    elif isinstance(exc, AIModelInferenceError):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": "AI Inference Failure", "message": exc.message, "details": exc.details}
        )
    elif isinstance(exc, InvalidFileFormatException):
        return HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"error": "Invalid File Format", "message": exc.message, "details": exc.details}
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={"error": "Internal Server Error", "message": str(exc)}
    )