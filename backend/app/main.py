from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import activities, auth, centers, children, insights, internal, measurements
from app.core.config import get_settings
from app.core.errors import AppError, app_error_handler, validation_error_handler
from app.db import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="아이쑥크림 API", version="0.1.0", lifespan=lifespan)
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(children.router)
app.include_router(measurements.router)
app.include_router(centers.router)
app.include_router(activities.router)
app.include_router(insights.router)
app.include_router(internal.router)
