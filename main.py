from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import (
    JSONResponse,
)
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from database import init_db
from routers import (
    base_router,
    pandas_router,
    pokemon_router
)

async def forbidden_error(request: Request, exc: Exception):
    return JSONResponse(status_code=403, content={"detail": "Forbidden"})

async def not_found_error(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

async def internal_error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield

    # --- Shutdown ---
    print("Shutting down...")

    
app = FastAPI(
    exception_handlers={
    403: forbidden_error,
    404: not_found_error,
    500: internal_error,
},
    lifespan=lifespan
)

app.include_router(base_router)
app.include_router(pandas_router)
app.include_router(pokemon_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
