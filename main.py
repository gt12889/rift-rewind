"""
Main entry point for Rift Rewind application.
"""
from config.settings import settings
import uvicorn

if __name__ == "__main__":
    if settings.app_debug:
        # Use import string for reload to work
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=settings.api_port,
            reload=True
        )
    else:
        # Direct import for production
        from src.api.main import app
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=settings.api_port,
            reload=False
        )

