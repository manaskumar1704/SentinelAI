"""
Supabase PostgreSQL Database Connection

Provides async database session management for SQLModel operations.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from config import get_settings


def get_database_url() -> str:
    """Get the async PostgreSQL connection URL for Supabase."""
    settings = get_settings()
    
    # Supabase connection string format for async
    # postgresql+asyncpg://user:password@host:port/database
    return (
        f"postgresql+asyncpg://{settings.supabase_db_user}:{settings.supabase_db_password}"
        f"@{settings.supabase_db_host}:{settings.supabase_db_port}/{settings.supabase_db_name}"
    )


# Async engine for database operations
_engine = None


def get_engine():
    """Get or create the async database engine."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            get_database_url(),
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _engine


# Session factory
_async_session_factory = None


def get_session_factory():
    """Get or create the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.
    
    Usage:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    async_session = get_session_factory()
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with get_db_session() as session:
        yield session


async def init_db() -> None:
    """
    Initialize database tables.
    
    Creates all tables defined in SQLModel metadata.
    Call this on application startup.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.
    
    Call this on application shutdown.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
