from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import (
    JSONResponse,
)
from fastapi.staticfiles import StaticFiles

from routers import base_router
from routers import scrape_router

async def forbidden_error(request: Request, exc: Exception):
    return JSONResponse(status_code=403, content={"detail": "Forbidden"})

async def not_found_error(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

async def internal_error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

app = FastAPI(
    exception_handlers={
    403: forbidden_error,
    404: not_found_error,
    405: not_found_error,
    500: internal_error,
})

app.include_router(base_router)
app.include_router(scrape_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
