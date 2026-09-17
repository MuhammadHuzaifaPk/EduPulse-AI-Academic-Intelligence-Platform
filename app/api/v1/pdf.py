import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
import google.generativeai as genai
from app.core.config import settings

router = APIRouter()

@router.post("/synthesize")
async def synthesize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # 1. Extract text and metrics from PDF
    try:
        pdf_bytes = await file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        
        page_count = len(pdf_reader.pages)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        words = extracted_text.split()
        word_count = len(words)
        reading_time = max(1, round(word_count / 200))

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF (scanned or image PDFs require OCR).")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF document: {str(e)}")

    # 2. Synthesize notes using Gemini AI
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)

        prompt = f"""
        Analyze this educational document and generate detailed, structured study notes.
        
        Document Content:
        {extracted_text[:12000]}
        
        Structure your response with HTML:
        - <h4>Key Takeaways</h4> followed by bullet points
        - <h4>Detailed Explanation</h4> with structured paragraphs
        - <h4>Core Terminology</h4> defined simply
        """

        response = model.generate_content(prompt)
        synthesized_html = response.text.replace("```html", "").replace("```", "").strip()

        return {
            "status": "success",
            "filename": file.filename,
            "page_count": page_count,
            "word_count": word_count,
            "estimated_reading_time_min": reading_time,
            "synthesized_notes": synthesized_html
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini AI processing error: {str(e)}")