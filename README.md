# EduPulse AI: Academic Intelligence Platform

**Track:** Student Productivity, AI Study Co-Pilot & Learning Orchestration

---

## Problem
Students face severe cognitive overload due to fragmented study workflows. Learning materials are scattered across multi-hour YouTube lectures, lengthy PDF textbooks, disjointed schedule planning apps, and unintegrated timers. Traditional study approaches result in poor retention, wasted study hours, and inefficient preparation for exams.

---

<img width="1278" height="624" alt="edu1" src="https://github.com/user-attachments/assets/814caab6-604e-44dd-9901-815721dab52c" />

## The Solution: EduPulse AI
EduPulse AI is a unified, multi-model academic co-pilot engineered to transform raw educational resources into actionable knowledge. **Powered by an ensemble of Google Gemini API** (for complex reasoning, synthesis, and roadmap generation) and **Hugging Face Inference Models** (for specialized NLP, entity extraction, and fast local/cloud summarization), EduPulse AI provides:

1. **YouTube Video Intelligence Engine:** Extracts transcripts, generates timestamped structural notes, flashcards, and automated self-assessment quizzes.
2. **Multi-Modal PDF & Document Synthesizer:** Parses textbooks and lecture notes into structured summaries, key concept maps, and context-aware Q&A.
3. **Adaptive AI Roadmap & Schedule Generator:** Builds customized, goal-driven study roadmaps complete with task breakdowns, difficulty estimations, and milestone checkpoints.
4. **Interactive Focus Timer & Analytics Engine:** Integrates an animated Pomodoro/Focus timer with real-time study analytics and audio cues to optimize focus states.

---

## Target Users

* **University and Secondary Students:** Seeking structured review materials and efficient study workflows.
* **Self-Directed Learners:** Processing technical documentation and video courses.
* **Educators:** Extracting quick assessments and active recall decks from lecture material.

---

## ⚠️ Main Challenge

The principal technical challenge was enforcing strict structural output integrity from large language models across diverse user inputs. Handling video transcripts that exceed model context windows, managing YouTube videos with disabled captions, and preventing API failure during invalid client requests required strict Pydantic validation schemas, server-side payload truncation, and resilient error propagation to the client interface.

---

## Track Alignment

Education Technology and Generative AI Track.

---

<img width="1224" height="513" alt="edu2" src="https://github.com/user-attachments/assets/42d9c7c3-3e7b-4407-94bd-6644bd805f48" />

## Impact

EduPulse AI reduces preparation overhead for study sessions and improves active recall practice. Users can break down long video lectures and notes into verifiable takeaways, practice quizzes, and structured daily study schedules.

---

## Key Results

* **Transcript Extraction & Processing:** Automated transcript retrieval and generation of executive summaries, core concepts, and context-aware quizzes from YouTube URLs.
* **Active Recall Deck Generation:** Created a structured pipeline that converts raw text inputs into multi-card flashcard decks with dynamic front-and-back rendering.
* **Timeline Planning Algorithm:** Developed an endpoint that calculates daily hour allocations and subject roadmaps based on user-defined constraints.
* **Unified Interface:** Built a lightweight client interface that toggles workspace tools without page reloads.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python 3.11, FastAPI
* **Data Validation:** Pydantic v2
* **Language Models & APIs:** Google Gemini API (`google-generativeai`), Hugging Face Inference API
* **Integrations:** `youtube-transcript-api`
* **Frontend Architecture:** Async Vanilla JavaScript (ES6+), HTML5, Tailwind CSS
* **Server Execution:** Uvicorn ASGI

---

## Prerequisites

* Python 3.11 or higher
* Python `pip` package manager
* A valid Google Gemini API key
* A valid Hugging Face API key

---

## Local Setup Instructions

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/edupulse-ai.git](https://github.com/your-username/edupulse-ai.git)
cd edupulse-ai

```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install required dependencies:**
```bash
pip install fastapi uvicorn pydantic youtube-transcript-api google-generativeai

```


4. **Configure environment variables:**
Set your API keys in your terminal session:
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export HUGGINGFACE_API_KEY="your_huggingface_api_key_here"

```


*For Windows PowerShell:*
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
$env:HUGGINGFACE_API_KEY="your_huggingface_api_key_here"

```


5. **Start the FastAPI server:**
```bash
python run.py
# Or using uvicorn directly:
# uvicorn app.core.config:app --reload

```


6. **Open the web application:**
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## Project Directory Structure

```text
edupulse-ai/
│
├── .env.example                # Environment variable blueprint
├── requirements.txt            # Production Python dependency manifest
├── README.md                   # Documentation and setup instructions
├── run.py                      # Uvicorn server launcher entry point
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                   # System Core Configuration & Services
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic-driven settings management
│   │   ├── logger.py           # Structured logging system
│   │   ├── exceptions.py       # Custom error handling & HTTP exceptions
│   │   └── security.py         # API Key validation & CORS helpers
│   │
│   ├── services/               # Business Logic & External Integrations
│   │   ├── __init__.py
│   │   ├── gemini_service.py   # Google Gemini API orchestrator
│   │   ├── hf_service.py       # Hugging Face Inference & Model driver
│   │   ├── youtube_service.py  # Youtube transcript extractor & processor
│   │   ├── pdf_service.py      # PDF text extraction & structural parser
│   │   ├── roadmap_service.py  # AI Study schedule & path builder
│   │   └── timer_service.py    # Analytics tracker for focus sessions
│   │
│   ├── api/                    # REST API Endpoint Routers
│   │   ├── __init__.py
│   │   ├── router.py           # Main API Router registry
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── youtube.py      # YouTube processing API endpoints
│   │       ├── pdf.py          # PDF document processing API endpoints
│   │       └── roadmap.py      # Roadmap generation API endpoints
│   │
│   ├── models/                 # Pydantic Schemas & Data Contracts
│   │   ├── __init__.py
│   │   ├── youtube_model.py    # Request/Response schemas for YouTube
│   │   ├── pdf_model.py        # Request/Response schemas for PDF
│   │   └── roadmap_model.py    # Request/Response schemas for Roadmap
│   │
│   └── templates/              # Server-rendered HTML / SPA Loader
│       └── index.html          # Primary single-page interface entry
│
└── static/                     # Frontend Assets
    ├── css/
    │   ├── main.css            # Custom Tailwind/CSS architecture
    │   └── animations.css      # Keyframes, glow effects, transition styles
    └── js/
        ├── app.js              # Core JS orchestration engine
        ├── youtube.js          # UI handlers for YouTube tool
        ├── pdf.js              # UI handlers for PDF processor
        ├── roadmap.js          # UI handlers for AI Roadmap
        └── timer.js            # UI handlers for Focus Timer & analytics

```
