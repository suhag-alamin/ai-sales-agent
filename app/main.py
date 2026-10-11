from app.core.exceptions.handlers import register_exception_handlers
from sqlalchemy import text
from fastapi import Depends, FastAPI
from app.core.config import Settings, get_settings
from app.db.session import SessionDep, StreamingSessionDep

app = FastAPI(title=get_settings().APP_NAME)

register_exception_handlers(app)


@app.get("/health")
async def health(
        settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME
    }


@app.get("/health/db")
async def health_db(session: SessionDep) -> dict[str, str]:
    result = await session.execute(text(text="SELECT version();"))
    version = result.scalar_one()

    ext = await session.execute(
        text(text="SELECT extname from pg_extension WHERE extname = 'vector';")
    )
    has_vector = ext.scalar_one_or_none() is not None

    return {
        "status": "ok",
        "database": "connected",
        "db_version": version,
        "has_vector": str(has_vector)
    }
