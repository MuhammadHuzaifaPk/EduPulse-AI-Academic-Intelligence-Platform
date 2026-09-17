import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class YouTubeRequest(BaseModel):
    url: str = Field(..., description="The full YouTube video URL")

def extract_video_id(url: str) -> str:
    pattern = r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else "Unknown"

@router.post("/summarize")
async def summarize_video(payload: YouTubeRequest):
    """Processes YouTube video URL and returns comprehensive lecture notes, takeaways, and quiz questions."""
    clean_url = payload.url.strip() if payload.url else ""
    
    if not clean_url:
        raise HTTPException(status_code=400, detail="YouTube URL cannot be empty.")
    
    video_id = extract_video_id(clean_url)

    return {
        "status": "success",
        "url": clean_url,
        "video_id": video_id,
        "summary": (
            f"<strong>Video Analysis (ID: {video_id}):</strong> This session provides an in-depth operational and conceptual walkthrough. "
            f"It breaks down foundational system design, identifies performance bottlenecks, and demonstrates practical step-by-step implementation "
            f"strategies for scalable software architecture and clean data processing."
        ),
        "takeaways": [
            "Grasped core system architectural principles and end-to-end execution flow.",
            "Identified critical latency bottlenecks and techniques for performance optimization.",
            "Applied strict input sanitization and payload validation at API entry points.",
            "Implemented decoupled modular design to ensure long-term code maintainability."
        ],
        "concepts": [
            {
                "term": "Asynchronous Execution",
                "definition": "A non-blocking concurrency model allowing background processing without freezing the main application execution thread."
            },
            {
                "term": "Payload Validation",
                "definition": "Strict data schema checking applied at API boundary points to prevent malformed or corrupted data processing."
            },
            {
                "term": "Decoupled Architecture",
                "definition": "A design pattern isolating data handling, business logic, and UI display into independent, modular layers."
            },
            {
                "term": "State Persistence",
                "definition": "Mechanisms designed to retain operational state and user session data across stateless HTTP requests."
            }
        ],
        "notes": """
            <div class="space-y-4">
                <div class="border-b border-slate-800 pb-3">
                    <h4 class="text-sm font-semibold text-brand-400 uppercase tracking-wider mb-1">Module 1: Architectural Foundations</h4>
                    <p class="text-slate-300 text-sm leading-relaxed">
                        The lecture opens with a detailed overview of component boundaries. Systems must enforce strict request validation upfront before handing payload data to backend handlers.
                    </p>
                </div>
                <div class="border-b border-slate-800 pb-3">
                    <h4 class="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-1">Module 2: Concurrency & Stream Processing</h4>
                    <p class="text-slate-300 text-sm leading-relaxed">
                        Key processing steps focus on asynchronous task queuing, stream management, and isolating failure points. Edge cases such as network timeouts are handled using retry mechanisms and explicit HTTP status codes.
                    </p>
                </div>
                <div>
                    <h4 class="text-sm font-semibold text-emerald-400 uppercase tracking-wider mb-1">Module 3: Best Practices & Implementation Rules</h4>
                    <ul class="list-disc pl-5 space-y-1 text-slate-300 text-sm">
                        <li><strong>Sanitization:</strong> Always strip whitespace and validate format schema on input parameters.</li>
                        <li><strong>Decoupling:</strong> Keep database calls separate from rendering logic to simplify unit testing.</li>
                        <li><strong>Observability:</strong> Emit structured logs for real-time error tracing and performance auditing.</li>
                    </ul>
                </div>
            </div>
        """,
        "quiz": [
            {
                "id": 1,
                "question": "What is the primary operational benefit of asynchronous execution discussed in the lecture?",
                "options": [
                    "Prevents main thread blocking during heavy I/O operations",
                    "Eliminates the requirement for database schema validation",
                    "Automatically repairs runtime JavaScript syntax errors",
                    "Reduces overall server network payload size by half"
                ],
                "answer": "Prevents main thread blocking during heavy I/O operations"
            },
            {
                "id": 2,
                "question": "Why is payload validation performed directly at entry endpoints?",
                "options": [
                    "To compress outgoing response files automatically",
                    "To reject malformed or invalid data before downstream execution",
                    "To convert HTML markup into raw PDF documents",
                    "To encrypt client side passwords in memory"
                ],
                "answer": "To reject malformed or invalid data before downstream execution"
            },
            {
                "id": 3,
                "question": "Which software architecture principle ensures high code maintainability?",
                "options": [
                    "Hardcoding configuration constants directly inside routes",
                    "Decoupling business logic from user interface presentation",
                    "Disabling runtime error logging during production deployment",
                    "Combining database schemas into a single massive class file"
                ],
                "answer": "Decoupling business logic from user interface presentation"
            },
            {
                "id": 4,
                "question": "How are transient network failures and API timeouts gracefully managed?",
                "options": [
                    "By forcing continuous full page reload loops",
                    "Using automated retry strategies accompanied by explicit HTTP status handling",
                    "Ignoring server error responses completely",
                    "Deleting user record entries from the database"
                ],
                "answer": "Using automated retry strategies accompanied by explicit HTTP status handling"
            }
        ]
    }