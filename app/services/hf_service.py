import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AIModelInferenceError

class HuggingFaceService:
    """
    Integrates specialized Hugging Face models via HF Inference API / Pipelines.
    Provides rapid extractive text summarization and lightweight context Q&A.
    """

    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.summarization_model = settings.HF_SUMMARIZATION_MODEL
        self.qa_model = settings.HF_QA_MODEL
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        logger.info("HuggingFaceService initialized.")

    def summarize_text_fast(self, text: str, max_length: int = 150, min_length: int = 40) -> Dict[str, Any]:
        """
        Performs fast neural text summarization using HF Inference Endpoint (BART/PEGASUS).
        Falls back to rule-based extractive truncation if remote API is unconfigured.
        """
        if not self.api_key:
            logger.warning("Hugging Face API key not present. Utilizing fallback summarizer.")
            return self._fallback_summarizer(text)

        api_url = f"[https://api-inference.huggingface.co/models/](https://api-inference.huggingface.co/models/){self.summarization_model}"
        payload = {
            "inputs": text[:4000],  # Token safe range
            "parameters": {
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": False
            }
        }

        try:
            response = requests.post(api_url, headers=self.headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    summary_text = result[0].get("summary_text", "")
                    return {
                        "summary": summary_text,
                        "model_used": self.summarization_model,
                        "method": "huggingface_inference_api"
                    }
            logger.warning(f"HF API returned status {response.status_code}. Using fallback.")
            return self._fallback_summarizer(text)

        except Exception as err:
            logger.error(f"Hugging Face Inference call failed: {str(err)}")
            return self._fallback_summarizer(text)

    def answer_question_extractive(self, context: str, question: str) -> Dict[str, Any]:
        """
        Uses Hugging Face RoBERTa-SQuAD2 model to extract exact span answers from document context.
        """
        if not self.api_key:
            return {"answer": "Hugging Face API key missing for extractive Q&A.", "score": 0.0}

        api_url = f"[https://api-inference.huggingface.co/models/](https://api-inference.huggingface.co/models/){self.qa_model}"
        payload = {
            "inputs": {
                "question": question,
                "context": context[:3000]
            }
        }

        try:
            response = requests.post(api_url, headers=self.headers, json=payload, timeout=8)
            if response.status_code == 200:
                result = response.json()
                return {
                    "answer": result.get("answer", "No exact answer span found."),
                    "score": round(result.get("score", 0.0), 4),
                    "start": result.get("start", 0),
                    "end": result.get("end", 0),
                    "model_used": self.qa_model
                }
            return {"answer": "Could not extract answer from context.", "score": 0.0}
        except Exception as err:
            logger.error(f"HF Extractive QA error: {str(err)}")
            return {"answer": f"Extraction error: {str(err)}", "score": 0.0}

    def _fallback_summarizer(self, text: str) -> Dict[str, Any]:
        """Extractive fallback summarizer splitting key sentences."""
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        extracted = ". ".join(sentences[:3]) + ("." if sentences else "")
        return {
            "summary": extracted or "Text too short to extract summary.",
            "model_used": "local_fallback_extractor",
            "method": "rule_based"
        }

# Global Singleton Instance
hf_service = HuggingFaceService()