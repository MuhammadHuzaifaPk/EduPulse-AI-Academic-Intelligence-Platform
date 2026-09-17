import time
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.config import settings
from app.core.logger import logger
from app.api.router import api_router
from app.core.exceptions import EduPulseException, get_http_exception_from_custom

# Instantiate FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description="Next-Generation Academic Intelligence Platform powered by Gemini 2.5 Flash & Hugging Face",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure Cross-Origin Resource Sharing (CORS) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Assets and Jinja2 Template Directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Register Primary API Router
app.include_router(api_router)

# Request Timing & Diagnostic Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Custom Application Exception Handler
@app.exception_handler(EduPulseException)
async def custom_edupulse_exception_handler(request: Request, exc: EduPulseException):
    http_exc = get_http_exception_from_custom(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )

# Primary SPA Web Route
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_dashboard(request: Request):
    """Renders the main single-page application (SPA) dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.APP_NAME}
    )

# Health Check & Diagnostic Endpoint
@app.get("/health", status_code=status.HTTP_200_OK, tags=["System Diagnostics"])
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "gemini_model": settings.GEMINI_MODEL_NAME,
        "hf_summarizer": settings.HF_SUMMARIZATION_MODEL
    }