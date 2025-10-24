from dataclasses import fields
from typing import List, Optional, Union
from fastapi import APIRouter
from fastapi import APIRouter, Query

from app.api.dao.advance_dao import ReappraisalServiceAdvanceDAO
from app.api.db_connection.db_connection import DBSessionDependency
from app.api.model.advance.advance_table import (
    ReappraisalServiceAdvanceIdPath,
    ReappraisalServiceAdvanceTable,
)
from app.api.model.advance.advance_create import (
    ReappraisalServiceAdvanceCreateRequest,
    ReappraisalServiceAdvanceCreateResponse,
)
from app.api.model.advance.advance_get import (
    ReappraisalServiceAdvanceGetResponse,
)
from app.api.exceptions.advance_exception import (
    RsAdvanceNotFoundAPIException,
    RsAdvanceDetailsNotFoundAPIException,
)
from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.pagination.pagination import PaginationResponse
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum

router = APIRouter()


@router.post(
    "/v1/advance",
    response_model=ReappraisalServiceAdvanceCreateResponse,
    summary="Create a New Reappraisal Service Advance",
    description="Creates a new reappraisal service advance record in the system.",
    responses={201: {"description": "Reappraisal Service Advance Created"}},
)
async def create_rs_advance(
    payload: ReappraisalServiceAdvanceCreateRequest, session: DBSessionDependency
):
    rs_advanceDao = ReappraisalServiceAdvanceDAO(session)
    rs_advance = ReappraisalServiceAdvanceTable.model_validate(payload)
    rs_advance = await rs_advanceDao.create_rs_advance(rs_advance)
    return rs_advance


@router.get(
    "/v1/advances",
    response_model=Union[
        List[ReappraisalServiceAdvanceGetResponse],
        PaginationResponse[ReappraisalServiceAdvanceGetResponse],
    ],
    summary="Retrieve all Reappraisal Service Advances",
    description="Retrieves all Reappraisal Service Advance records.",
    responses={200: {"description": "Reappraisal Service Advances Retrieved"}},
)
async def get_rs_advances(
    session: DBSessionDependency,
    rsa_transaction_epoch: Optional[int] = None,
    rs_advance_id: Optional[str] = None,
    reappraisal_service_id: Optional[str] = None,
    appraiser_id: Optional[str] = None,
    rs_advance_category: Optional[str] = None,
    rs_advance_settlement_statuses: List[Optional[str]] = Query(None),
    page: Optional[int] = None,
    size: Optional[int] = None,
):
    rs_advanceDao = ReappraisalServiceAdvanceDAO(session)
    query = BaseQueryParams(
        search_values=(
            rsa_transaction_epoch,
            rs_advance_id,
            reappraisal_service_id,
            appraiser_id,
            rs_advance_category,
            rs_advance_settlement_statuses,
        ),
        fields=(
            ("rs_advance_transaction_epoch", MatchTypeEnum.EXACT),
            ("rs_advance_id", MatchTypeEnum.EXACT),
            ("reappraisal_service_id", MatchTypeEnum.EXACT),
            ("rs_appraiser_id", MatchTypeEnum.EXACT),
            ("rs_advance_category", MatchTypeEnum.EXACT),
            ("rs_advance_settlement_status", MatchTypeEnum.EXACT),
        ),
        page=page,
        size=size,
    )
    rs_advance = await rs_advanceDao.get_rs_advances(query=query)
    if not rs_advance:
        raise RsAdvanceDetailsNotFoundAPIException()
    return rs_advance


@router.get(
    "/v1/advance/{rs_advance_id}",
    response_model=ReappraisalServiceAdvanceGetResponse,
    summary="Retrieve a Reappraisal Service Advance by ID",
    description="Retrieves a Reappraisal Service Advance record based on the provided ID.",
    responses={200: {"description": "Reappraisal Service Advance Retrieved"}},
)
async def get_rs_advance(
    rs_advance_id: ReappraisalServiceAdvanceIdPath,
    session: DBSessionDependency,
):
    rs_advanceDao = ReappraisalServiceAdvanceDAO(session)
    rs_advance = await rs_advanceDao.get_rs_advance(rs_advance_id)
    if not rs_advance:
        raise RsAdvanceNotFoundAPIException(rs_advance_id)
    return rs_advance


@router.put(
    "/v1/advance/{rs_advance_id}",
    response_model=ReappraisalServiceAdvanceGetResponse,
    summary="Update a Reappraisal Service Advance",
    description="Updates an existing Reappraisal Service Advance record based on the provided ID.",
    responses={200: {"description": "Reappraisal Service Advance Updated"}},
)
async def update_rs_advance(
    rs_advance_id: ReappraisalServiceAdvanceIdPath,
    payload: ReappraisalServiceAdvanceCreateRequest,
    session: DBSessionDependency,
):
    rs_advanceDao = ReappraisalServiceAdvanceDAO(session)
    rs_advance = await rs_advanceDao.update_rs_advance(
        rs_advance_id=rs_advance_id, rs_advance_update=payload
    )
    if not rs_advance:
        raise RsAdvanceNotFoundAPIException(rs_advance_id)
    return rs_advance


@router.delete(
    "/v1/advance/{rs_advance_id}",
    summary="Delete a reappraisal service advance",
    description="Deletes a reappraisal service advance record based on the provided ID.",
    responses={204: {"description": "Reappraisal Service Advance Deleted"}},
)
async def delete_rs_advance(
    rs_advance_id: ReappraisalServiceAdvanceIdPath,
    session: DBSessionDependency,
):
    rs_advanceDao = ReappraisalServiceAdvanceDAO(session)
    is_advance = await rs_advanceDao.delete_rs_advance(rs_advance_id)
    if not is_advance:
        raise RsAdvanceNotFoundAPIException(rs_advance_id)
    return {"message": "Reappraisal Service Advance deleted successfully"}
