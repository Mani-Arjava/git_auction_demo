from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from app.api.db_connection.db_connection import create_db_and_tables
# from app.api.controller.bank.bank_controller import router as bank_router
# from app.api.controller.branch.branch_controller import router as branch_router
# Routers
from app.api.controller.appraiser.appraiser_controller import router as appraiser_router
# from app.api.controller.reappraisal_service.reappraisal_service_controller import (
#     router as reappraisal_service_router,
# )
# from app.api.controller.reimbursement.reimbursment_controller import (
#     router as reimbursement_router,
# )
# from app.api.controller.advance.advance_controller import router as advance_router

# from app.api.router import router as test_router
from app.api.exceptions.appraiser_exception import DuplicatePanException, ValidationException
from app.api.exceptions.api_error_codes import ApiErrorCode

@asynccontextmanager
async def lifespan(app: FastAPI):
    # """Application lifespan manager - initializes database and handles cleanup"""
    # logger.info("Starting Phobos Backend application...")
    # await create_db_and_tables()  # Temporarily disabled for local testing
    # logger.info("Database tables created successfully")
    yield
    # logger.info("Shutting down Phobos Backend application...")


app = FastAPI(
    lifespan=lifespan,
    title="Phobos Backend API",
    description="Production-ready FastAPI Lambda backend with comprehensive business logic and database integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers - Only appraiser router enabled for testing
# app.include_router(bank_router, tags=["Bank_Api"])
# app.include_router(branch_router, tags=["Branch_Api"])
app.include_router(appraiser_router, tags=["Appraiser_Api"])
# app.include_router(reappraisal_service_router, tags=["Reappraisal_Service_Api"])
# app.include_router(reimbursement_router, tags=["Reimbursement_Api"])
# app.include_router(advance_router, tags=["Advance_Api"])
# app.include_router(test_router, tags=["Test_Api"])

@app.get("/")
async def root():
    """Root endpoint with comprehensive application status"""
    # logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Phobos Backend API",
        "version": "1.0.0",
        "status": "healthy",
        "features": [
            "Database integration",
            "Comprehensive business logic",
            "Multiple API modules",
            "Lambda deployment ready",
        ],
    }
