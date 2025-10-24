from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.api.db_connection.db_config import engine

# Create session factory only if engine is available
if engine:
    SessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )
else:
    SessionLocal = None


async def get_db_session():
    if not SessionLocal:
        # Return a mock session for testing without database
        raise HTTPException(
            status_code=503,
            detail="Database connection not configured. Please set up database environment variables."
        )
    async with SessionLocal() as session:
        yield session


async def create_db_and_tables():
    if engine:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    else:
        print("Warning: Database engine not available. Skipping table creation.")


DBSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
