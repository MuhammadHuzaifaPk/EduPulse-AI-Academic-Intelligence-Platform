import uvicorn
from app.core.config import settings
from app.core.logger import logger

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} server on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
        access_log=True
    )