from typing import List, Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from app.api.dao.appraiser_dao import AppraiserDAO
from app.api.db_connection.db_connection import DBSessionDependency
from app.api.exceptions.appraiser_exception import (
    AppraiserNotFoundAPIException,
    AppraiserDetailsNotFoundAPIException,
    AppraiserHasServicesAPIException,
    AppraiserNoActiveServicesAPIException,
    DuplicatePanException,
)
from app.api.model.appraiser.appraiser_table import AppraiserTable, AppraiserIdPath
from app.api.model.appraiser.appraiser_create import (
    AppraiserCreateRequest,
    AppraiserCreateResponse,
    AppraiserUpdateResponse,
    BankAccountResponse,
    PANResponse,
    AppraiserUpdateResponse,
)
from app.api.model.appraiser.appraiser_create import AppraiserPatchRequest
from app.api.model.appraiser.appraiser_get import AppraiserGetResponse

from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.pagination.pagination import PaginationResponse
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.model.reappraisal_service.reappraisal_service_get import ReappraisalServiceAPIResponse, ReappraisalServiceGetResponse

router = APIRouter()


# Simple response model for direct appraiser query (no relationships)
class AppraiserDirectResponse(BaseModel):
    appraiser_id: str
    appraiser_full_name: str
    appraiser_email: str
    appraiser_phone: str
    appraiser_pan: str
    appraiser_address: str
    appraiser_account_number: str
    appraiser_account_ifsc_code: str
    appraiser_bank_name: str
    appraiser_branch_name: str


# DIRECT QUERY ENDPOINT - No relationships, no joins
@router.get(
    "/v1/appraisers-direct",
    response_model=List[AppraiserDirectResponse],
    summary="Get All Appraisers (Direct Query)",
    description="Direct database query to get all appraisers without any joins or relationships",
    responses={200: {"description": "Appraisers Retrieved"}},
)
async def get_all_appraisers_direct(
    session: DBSessionDependency,
):
    """Direct query to appraiser table - no joins, no complex relationships"""
    try:
        from sqlalchemy.orm import noload
        # Use noload to prevent SQLAlchemy from loading relationships
        query = select(AppraiserTable).options(noload(AppraiserTable.services))
        result = await session.exec(query)
        appraisers = result.scalars().all()

        if not appraisers:
            return []

        response_list = []
        for appraiser in appraisers:
            response_list.append(
                AppraiserDirectResponse(
                    appraiser_id=f"APR-{appraiser.appraiser_id:04d}",
                    appraiser_full_name=appraiser.appraiser_full_name,
                    appraiser_email=appraiser.appraiser_email,
                    appraiser_phone=appraiser.appraiser_phone,
                    appraiser_pan=appraiser.appraiser_pan,
                    appraiser_address=appraiser.appraiser_address,
                    appraiser_account_number=appraiser.appraiser_account_number,
                    appraiser_account_ifsc_code=appraiser.appraiser_account_ifsc_code,
                    appraiser_bank_name=appraiser.appraiser_bank_name,
                    appraiser_branch_name=appraiser.appraiser_branch_name,
                )
            )
        return response_list
    except Exception as e:
        raise Exception(f"Error fetching appraisers: {str(e)}")


# ============================================================================
# COMMENTED OUT - OLD ENDPOINTS WITH ISSUES
# ============================================================================

# @router.post(
#     "/v1/appraiser",
#     response_model=AppraiserCreateResponse,
#     summary="Create Appraiser Details",
#     description="This API Endpoint is used for creating appraiser details with user requesting values in request body.",
#     responses={201: {"description": "Appraiser Created"}},
# )
# async def create_appraiser(
#     payload: AppraiserCreateRequest, session: DBSessionDependency
# ):
#     appraiserDao = AppraiserDAO(session)
#     appraiser = AppraiserTable.model_validate(payload)
#     appraiser = await appraiserDao.create_appraiser(appraiser)
#     return AppraiserGetResponse.from_db_record(appraiser)


# @router.get(
#     "/v1/appraiser/{appraiser_id}",
#     response_model=AppraiserGetResponse,
#     summary="Retrieve Appraiser Details",
#     description="This API Endpoint is used for retrieving appraiser details based on appraiser id.",
#     responses={200: {"description": "Appraiser Retrieved"}},
# )
# async def get_appraiser(
#     appraiser_id: AppraiserIdPath,
#     session: DBSessionDependency,
# ):
#     appraiserDao = AppraiserDAO(session)
#     appraiser = await appraiserDao.get_appraiser(appraiser_id)
#     if not appraiser:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#
#     # Get active services count
#     active_services = await appraiserDao.get_active_services(appraiser_id)
#     active_services_count = len(active_services)
#
#     # Create response with active services count
#     response = AppraiserGetResponse(
#         appraiser_id=f"APR-{appraiser.appraiser_id:04d}",
#         appraiser_full_name=appraiser.appraiser_full_name,
#         appraiser_email=appraiser.appraiser_email,
#         appraiser_phone=appraiser.appraiser_phone,
#         appraiser_pan=appraiser.appraiser_pan,
#         appraiser_address=appraiser.appraiser_address,
#         appraiser_account_number=appraiser.appraiser_account_number,
#         appraiser_account_ifsc_code=appraiser.appraiser_account_ifsc_code,
#         appraiser_bank_name=appraiser.appraiser_bank_name,
#         appraiser_branch_name=appraiser.appraiser_branch_name,
#         active_services_count=active_services_count,
#         services=appraiser.services if appraiser.services else []
#     )
#
#     return response


# @router.get(
#     "/v1/appraiser/{appraiser_id}/active-services",
#     response_model=List[ReappraisalServiceGetResponse],
#     summary="Get Active Reappraisal Services for Appraiser",
#     description="This API Endpoint retrieves only ACTIVE reappraisal services for a specific appraiser.",
#     responses={200: {"description": "Active Services Retrieved"}},
# )
# async def get_appraiser_active_services(
#     appraiser_id: AppraiserIdPath,
#     session: DBSessionDependency,
# ):
#     appraiserDao = AppraiserDAO(session)
#
#     # Check if appraiser exists
#     appraiser = await appraiserDao.get_appraiser(appraiser_id)
#     if not appraiser:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#
#     # Get only active services
#     active_services = await appraiserDao.get_active_services(appraiser_id)
#
#     # Convert to response format
#     return [
#         ReappraisalServiceGetResponse.from_db_record(
#             service,
#             appraiser_name=appraiser.appraiser_full_name,
#             bank_name=service.bank.bank_name if service.bank else "",
#             branch_name=service.branch.branch_name if service.branch else ""
#         )
#         for service in active_services
#     ]


# @router.get(
#     "/v1/appraisers",
#     response_model=List[AppraiserGetResponse],
#     summary="Retrieve All Appraiser Details",
#     description="This API Endpoint is used for retrieving all appraiser details.",
#     responses={200: {"description": "Appraisers Retrieved"}},
# )
# async def get_appraisers(
#     session: DBSessionDependency,
# ):
#     appraiserDao = AppraiserDAO(session)
#
#     appraisers_with_count = await appraiserDao.get_appraisers_with_active_count()
#     if not appraisers_with_count:
#         raise AppraiserDetailsNotFoundAPIException()
#
#     response_list = []
#     for appraiser, active_services_count in appraisers_with_count:
#         response_list.append(
#             AppraiserGetResponse(
#                 appraiser_id=f"APR-{appraiser.appraiser_id:04d}",
#                 appraiser_full_name=appraiser.appraiser_full_name,
#                 appraiser_email=appraiser.appraiser_email,
#                 appraiser_phone=appraiser.appraiser_phone,
#                 appraiser_pan=appraiser.appraiser_pan,
#                 appraiser_address=appraiser.appraiser_address,
#                 appraiser_account_number=appraiser.appraiser_account_number,
#                 appraiser_account_ifsc_code=appraiser.appraiser_account_ifsc_code,
#                 appraiser_bank_name=appraiser.appraiser_bank_name,
#                 appraiser_branch_name=appraiser.appraiser_branch_name,
#                 active_services_count=active_services_count,
#                 services=appraiser.services if appraiser.services else []
#             )
#         )
#     return response_list


# @router.put(
#     "/v1/appraiser/{appraiser_id}",
#     response_model=AppraiserUpdateResponse,
#     summary="Update Appraiser Details",
#     description="This API Endpoint is used for updating the existing appraiser details using appraiser id. Only appraisers with no services can be updated.",
#     responses={200: {"description": "Appraiser Updated"}, 400: {"description": "Appraiser has services - cannot update"}},
# )
# async def update_appraiser(
#     appraiser_id: AppraiserIdPath,
#     payload: AppraiserCreateRequest,
#     session: DBSessionDependency,
# ):
#     appraiserDao = AppraiserDAO(session)
#
#     # Check if appraiser exists
#     appraiser = await appraiserDao.get_appraiser(appraiser_id)
#     if not appraiser:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#
#     # Check if appraiser has any services (active or inactive)
#     service_count = await appraiserDao.count_services(appraiser_id)
#     if service_count > 0:
#         raise AppraiserHasServicesAPIException(appraiser_id, service_count)
#
#     # Update the appraiser
#     appraiser = await appraiserDao.update_appraiser(
#         appraiser_id=appraiser_id, appraiser_update=payload
#     )
#     return AppraiserGetResponse.from_db_record(appraiser)


# @router.patch(
#     "/v1/appraiser/{appraiser_id}",
#     response_model=AppraiserUpdateResponse,
#     summary="Partially Update Appraiser Details",
#     description="This API Endpoint updates only the provided fields of the appraiser. Only works when appraiser has any services. Name and PAN cannot be edited.",
#     responses={200: {"description": "Appraiser Updated"}, 400: {"description": "No services found"}},
# )
# async def partial_update_appraiser(
#     appraiser_id: AppraiserIdPath,
#     payload: AppraiserPatchRequest,
#     session: DBSessionDependency,
# ):
#     appraiserDao = AppraiserDAO(session)
#
#     # Check if appraiser exists
#     appraiser = await appraiserDao.get_appraiser(appraiser_id)
#     if not appraiser:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#
#     # Check if appraiser has at least one service (any status)
#     service_count = await appraiserDao.count_services(appraiser_id)
#     if service_count == 0:
#         raise AppraiserNoActiveServicesAPIException(appraiser_id)
#
#     # Update only provided fields (excluding name and PAN)
#     appraiser = await appraiserDao.update_appraiser(
#         appraiser_id=appraiser_id, appraiser_update=payload
#     )
#     return AppraiserGetResponse.from_db_record(appraiser)


# @router.delete(
#     "/v1/appraiser/{appraiser_id}",
#     summary="Delete Appraiser Details",
#     description="This API Endpoint is used for deleting an appraiser details based on appraiser id.",
#     responses={204: {"description": "Appraiser Deleted"}},
# )
# async def delete_appraiser(
#     session: DBSessionDependency,
#     appraiser_id: AppraiserIdPath,
# ):
#     appraiserDao = AppraiserDAO(session)
#
#     # Check for associated services using back-population
#     service_count = await appraiserDao.count_services(appraiser_id)
#     if service_count > 0:
#         raise AppraiserHasServicesAPIException(appraiser_id, service_count)
#
#     # Delete the appraiser
#     isAppraiserDeleted = await appraiserDao.delete_appraiser(appraiser_id)
#     if not isAppraiserDeleted:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#
#     return {"message": "Appraiser deleted successfully"}


# @router.get(
#     "/v1/appraiser/{appraiser_id}/pan",
#     response_model=PANResponse,
#     summary="Retrieve Appraiser PAN",
#     description="This API Endpoint is used for retrieving appraiser PAN number based on appraiser id.",
#     responses={200: {"description": "PAN Retrieved"}},
# )
# async def get_appraiser_pan(
#     appraiser_id: AppraiserIdPath, session: DBSessionDependency
# ):
#     appraiserDao = AppraiserDAO(session)
#     pan = await appraiserDao.get_pan(appraiser_id)
#     if not pan:
#         raise AppraiserNotFoundAPIException(appraiser_id)
#     return PANResponse(appraiser_id=appraiser_id, appraiser_pan=pan)


