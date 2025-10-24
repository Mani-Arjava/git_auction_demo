from typing import List, Optional, Union
from fastapi import APIRouter
from ...dao.bank_dao import BankDao
from ...dao.branch_dao import BranchDao
from ...db_connection.db_connection import DBSessionDependency
from ...exceptions.bank_exception import (
    BankNotFoundAPIException,
    BankDetailsNotFoundAPIException,
)
from ...model.bank.bank_create import BankCreateRequest, BankCreateResponse
from ...model.bank.bank_get import BankGetResponse, BankWithBranchServicesResponse, BranchWithServicesCountResponse
from ...model.bank.bank_table import BankIdPath, BankTable
from ...services.search_filter.basequery import BaseQueryParams
from ...services.search_filter.matchtype_enum import MatchTypeEnum
from ...services.pagination.pagination import PaginationResponse

router = APIRouter()


@router.post(
    "/v1/bank",
    response_model=BankCreateResponse,
    summary="Create Bank",
    description="Create a new bank",
    responses={201: {"description": "Bank Created Successfully"}},
)
async def create_bank(payload: BankCreateRequest, session: DBSessionDependency):
    bankDao = BankDao(session)
    bank = BankTable(
        bank_name=payload.bank_name,
        bank_code=payload.bank_code,
        bank_head_office_address=payload.bank_head_office_address,
        bank_contact_email=payload.bank_contact_email,
        bank_contact_number=payload.bank_contact_number
    )
    bank_response = await bankDao.create_bank(bank)
    return BankCreateResponse.from_db_record(bank_response)


@router.get(
    "/v1/banks",
    response_model=Union[List[BankGetResponse], PaginationResponse[BankGetResponse]],
    summary="Get Banks",
    description="Retrieve a list of banks",
    responses={200: {"description": "List of Banks Retrieved Successfully"}},
)
async def get_banks(
    session: DBSessionDependency,
    bank_id: Optional[int] = None,
    bank_code: Optional[str] = None,
    bank_name: Optional[str] = None,
    total_branches_count: Optional[str] = None,
    page: Optional[int] = None,
    size: Optional[int] = None,
):
    bankDao = BankDao(session)
    branchDao = BranchDao(session)

    query = BaseQueryParams(
        search_values=(
            bank_id,
            bank_code,
            bank_name,
            total_branches_count,
        ),
        fields=(
            ("bank_id", MatchTypeEnum.EXACT),
            ("bank_code", MatchTypeEnum.PARTIAL),
            ("bank_name", MatchTypeEnum.PARTIAL),
            ("total_branches_count", MatchTypeEnum.EXACT),
        ),
        page=page,
        size=size,
    )
    banks = await bankDao.get_banks(query)
    if not banks:
        raise BankDetailsNotFoundAPIException()

    # For now, return basic bank info without branch details
    # TODO: Implement branch details with formatted responses
    return [BankGetResponse.from_db_record(bank) for bank in banks]


@router.get(
    "/v1/bank/{bank_id}",
    response_model=BankWithBranchServicesResponse,
    summary="Get Bank by ID with Branch Services",
    description="Retrieve a bank by its ID with all branches and active reappraisal service counts",
    responses={200: {"description": "Bank Retrieved Successfully"}},
)
async def get_bank_by_id(bank_id: int, session: DBSessionDependency):
    bankDao = BankDao(session)

    # Get bank details
    bank_response = await bankDao.get_bank(bank_id)
    if not bank_response:
        raise BankNotFoundAPIException(str(bank_id))

    # For now, return basic bank info without branch details
    # TODO: Implement branch details with formatted responses
    return BankWithBranchServicesResponse.from_response_type(bank_response)


@router.put(
    "/v1/bank/{bank_id}",
    response_model=BankGetResponse,
    summary="Update Bank by ID",
    description="Update a bank by its ID",
    responses={200: {"description": "Bank Updated Successfully"}},
)
async def update_bank_by_id(
    bank_id: int, payload: BankCreateRequest, session: DBSessionDependency
):
    bankDao = BankDao(session)
    bank_response = await bankDao.update_bank(bank_id, payload)
    if not bank_response:
        raise BankNotFoundAPIException(str(bank_id))
    return BankGetResponse.from_db_record(bank_response)


@router.delete(
    "/v1/bank/{bank_id}",
    summary="Delete Bank by ID",
    description="Delete a bank by its ID",
    responses={204: {"description": "Bank Deleted Successfully"}},
)
async def delete_bank_by_id(bank_id: int, session: DBSessionDependency):
    bankDao = BankDao(session)
    deleted = await bankDao.delete_bank(bank_id)
    if not deleted:
        raise BankNotFoundAPIException(str(bank_id))
    return {"message": "Bank Deleted Successfully"}
