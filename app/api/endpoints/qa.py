from fastapi import APIRouter, HTTPException, status
from app.services.gemini_service import gemini_service
from app.services.hf_service import hf_service
from app.models.qa_model import ContextQARequest, ContextQAResponse
from app.core.exceptions import AIModelInferenceError, get_http_exception_from_custom
from app.core.logger import logger

router = APIRouter(prefix="/qa", tags=["Contextual Q&A Engine"])

@router.post("/ask", response_model=ContextQAResponse, status_code=status.HTTP_200_OK)
async def ask_context_question(payload: ContextQARequest):
    """
    Executes precise question answering against provided text materials.
    Supports either Gemini deep reasoning or Hugging Face lightweight extractive models.
    """
    try:
        logger.info(f"Processing context Q&A query: '{payload.question[:50]}...'")

        if payload.use_huggingface_extractive:
            # Use Hugging Face RoBERTa extractive Q&A pipeline
            hf_res = hf_service.answer_question_extractive(
                context=payload.context_text,
                question=payload.question
            )
            return ContextQAResponse(
                answer=hf_res.get("answer", "No span answer identified."),
                confidence_score=hf_res.get("score", 0.0),
                relevant_quotes=[hf_res.get("answer")] if hf_res.get("score", 0) > 0.3 else [],
                engine_used=f"HuggingFace ({hf_res.get('model_used', 'RoBERTa')})"
            )

        # Default: Gemini 2.5 Flash Reasoning Q&A
        gemini_res = await gemini_service.answer_context_question(
            context_text=payload.context_text,
            question=payload.question
        )

        return ContextQAResponse(
            answer=gemini_res.get("answer", "No answer could be determined from context."),
            confidence_score=float(gemini_res.get("confidence_score", 0.9)),
            relevant_quotes=gemini_res.get("relevant_quotes", []),
            engine_used="Google Gemini 2.5 Flash"
        )

    except AIModelInferenceError as exc:
        raise get_http_exception_from_custom(exc)
    except Exception as exc:
        logger.error(f"Unexpected error in Q&A endpoint: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context Q&A error: {str(exc)}"
        )