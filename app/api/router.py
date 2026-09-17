from fastapi import APIRouter
from app.api.v1.youtube import router as youtube_router
from app.api.v1.pdf import router as pdf_router
from app.api.v1.roadmap import router as roadmap_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(youtube_router, prefix="/youtube", tags=["YouTube Intelligence"])
api_router.include_router(pdf_router, prefix="/pdf", tags=["PDF Synthesizer"])
api_router.include_router(roadmap_router, prefix="/roadmap", tags=["Study Roadmap"])