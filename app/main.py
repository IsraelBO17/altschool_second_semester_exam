from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user, event, speaker, registration


def create_application():
    application = FastAPI()
    application.include_router(user.router)
    application.include_router(event.router)
    application.include_router(speaker.router)
    application.include_router(registration.router)

    return application

app = create_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler for better error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "detail": exc.detail,
                "type": "http_error"
            }
        }
    )

