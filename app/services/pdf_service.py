import io
import re
from typing import Dict, Any, List, Optional
from pypdf import PdfReader
import pdfplumber
from app.core.logger import logger
from app.core.exceptions import PDFProcessingError

class PDFService:
    """
    Handles PDF ingestion, text extraction, page-level mapping,
    clean structural chunking, and metadata parsing.
    """

    @staticmethod
    def clean_extracted_text(text: str) -> str:
        """Removes hyphenated word breaks, excess whitespace, and unwanted control characters."""
        if not text:
            return ""
        # Fix line-break hyphenations (e.g., "commu-\nnication" -> "communication")
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        # Standardize multiple newlines and spaces
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    async def extract_text_from_bytes(self, file_bytes: bytes, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Parses raw PDF bytes using pypdf primary reader, falling back to pdfplumber
        for complex layouts or tabular text.
        """
        logger.info(f"Processing PDF document: {filename} ({len(file_bytes)} bytes)")
        
        if len(file_bytes) == 0:
            raise PDFProcessingError(f"Uploaded file '{filename}' is empty.")

        pages_data: List[Dict[str, Any]] = []
        full_text_list: List[str] = []

        try:
            # Primary Extraction using PyPDF
            stream = io.BytesIO(file_bytes)
            reader = PdfReader(stream)
            num_pages = len(reader.pages)

            if num_pages == 0:
                raise PDFProcessingError(f"PDF document '{filename}' contains 0 pages.")

            for index, page in enumerate(reader.pages):
                page_num = index + 1
                raw_page_text = page.extract_text() or ""
                cleaned_page_text = self.clean_extracted_text(raw_page_text)

                pages_data.append({
                    "page_number": page_num,
                    "text": cleaned_page_text,
                    "character_count": len(cleaned_page_text),
                    "word_count": len(cleaned_page_text.split())
                })
                if cleaned_page_text:
                    full_text_list.append(f"--- Page {page_num} ---\n{cleaned_page_text}")

            combined_text = "\n\n".join(full_text_list)

            # Fallback to pdfplumber if extracted text density is extremely low (scanned or unusual font encoding)
            if len(combined_text.strip()) < 50 and num_pages > 0:
                logger.warning(f"PyPDF returned low text count for '{filename}'. Retrying with pdfplumber.")
                stream.seek(0)
                full_text_list.clear()
                pages_data.clear()

                with pdfplumber.open(stream) as pdf:
                    for index, page in enumerate(pdf.pages):
                        page_num = index + 1
                        plumber_text = page.extract_text() or ""
                        cleaned_plumber_text = self.clean_extracted_text(plumber_text)

                        pages_data.append({
                            "page_number": page_num,
                            "text": cleaned_plumber_text,
                            "character_count": len(cleaned_plumber_text),
                            "word_count": len(cleaned_plumber_text.split())
                        })
                        if cleaned_plumber_text:
                            full_text_list.append(f"--- Page {page_num} ---\n{cleaned_plumber_text}")

                combined_text = "\n\n".join(full_text_list)

            if not combined_text.strip():
                raise PDFProcessingError(
                    f"Could not extract readable text from '{filename}'. The file may be image-only or scanned without OCR."
                )

            total_words = len(combined_text.split())
            estimated_reading_time_min = round(total_words / 200, 1)  # standard 200 wpm

            return {
                "filename": filename,
                "total_pages": num_pages,
                "total_words": total_words,
                "estimated_reading_minutes": estimated_reading_time_min,
                "combined_text": combined_text,
                "pages": pages_data
            }

        except PDFProcessingError:
            raise
        except Exception as err:
            logger.error(f"Unexpected error parsing PDF '{filename}': {str(err)}")
            raise PDFProcessingError(f"Failed to process PDF file: {str(err)}")

    def chunk_document_text(self, text: str, chunk_size: int = 1500, overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Splits long document text into overlapping token-friendly chunks for search & Q&A context.
        """
        if not text:
            return []

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_id = 1

        for para in paragraphs:
            para_len = len(para.split())
            if current_length + para_len > chunk_size and current_chunk:
                chunk_str = "\n\n".join(current_chunk)
                chunks.append({
                    "chunk_id": chunk_id,
                    "word_count": len(chunk_str.split()),
                    "text": chunk_str
                })
                chunk_id += 1
                # Preserve overlap from tail of current chunk
                current_chunk = current_chunk[-1:] if len(current_chunk) > 1 else []
                current_length = sum(len(p.split()) for p in current_chunk)

            current_chunk.append(para)
            current_length += para_len

        if current_chunk:
            final_str = "\n\n".join(current_chunk)
            chunks.append({
                "chunk_id": chunk_id,
                "word_count": len(final_str.split()),
                "text": final_str
            })

        return chunks

# Global Singleton Instance
pdf_service = PDFService()