import uvicorn as uvicorn
from api.v1 import (
    users,
)
from fastapi import (
    FastAPI,
)


app = FastAPI(
    title="FastAPI Project",
    description="FastAPI Project",
    docs_url="/",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    docs_url_prefix="/docs",
)

app.include_router(users.router, tags=["users"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        workers=1,
    )