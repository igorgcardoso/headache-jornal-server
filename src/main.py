from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError

from config import settings
from routers import drink, food, headache, remedy, sessions, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['db.models', 'aerich.models']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

if settings.IS_DOCS_ENABLED:
    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

@app.exception_handler(DoesNotExist)
async def doesnotexist_exception_handler(request: Request, exc: DoesNotExist):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(IntegrityError)
async def integrityerror_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=422,
        content={"detail": [{"loc": [], "msg": str(exc), "type": "IntegrityError"}]},
    )

@app.exception_handler(ValidationError)
async def integrityerror_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

app.include_router(headache.router)
app.include_router(food.router)
app.include_router(remedy.router)
app.include_router(drink.router)
app.include_router(stats.router)
app.include_router(sessions.router)
