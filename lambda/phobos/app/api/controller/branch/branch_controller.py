from typing import List, Optional, Union
from fastapi import APIRouter, Query
from ...dao.branch_dao import BranchDao
from ...db_connection.db_connection import DBSessionDependency
from ...exceptions.branch_exception import (
    BranchNotFoundAPIException,
    BranchDetailsNotFoundAPIException,
)
from ...services.search_filter.basequery import BaseQueryParams
from ...model.branch.branch_create import BranchCreateRequest, BranchCreateResponse, BranchUpdateRequest
from ...model.branch.branch_get import BranchGetResponse
from ...model.branch.branch_table import BranchIdPath, BranchTable
from ...model.bank.bank_table import BankIdQuery
from ...services.pagination.pagination import PaginationResponse
from ...services.search_filter.matchtype_enum import MatchTypeEnum

router = APIRouter()


@router.post(
    "/v1/branch",
    response_model=BranchCreateResponse,
    summary="Create Branch",
    description="Create a new branch",
    responses={201: {"description": "Branch Created Successfully"}},
)
async def create_branch(payload: BranchCreateRequest, session: DBSessionDependency):
    branchDao = BranchDao(session)
    branch = BranchTable.model_validate(payload)
    branch = await branchDao.create_branch(branch)
    return BranchGetResponse.from_db_record(branch)

@router.patch(
    "/v1/branch/{branch_id}",
    response_model=BranchGetResponse,
    summary="Update Branch by ID",
    description="Update a branch by its ID",
    responses={200: {"description": "Branch Updated Successfully"}},
)
async def update_branch(
    branch_id: BranchIdPath, payload: BranchUpdateRequest, session: DBSessionDependency
):
    branchDao = BranchDao(session)
    branch = await branchDao.update_branch(branch_id, payload)
    if not branch:
        raise BranchNotFoundAPIException(branch_id)
    return BranchGetResponse.from_db_record(branch)


@router.delete(
    "/v1/branch/{branch_id}",
    summary="Delete Branch by ID",
    description="Delete a branch by its ID",
    responses={204: {"description": "Branch Deleted Successfully"}},
)
async def delete_branch_by_id(branch_id: BranchIdPath, session: DBSessionDependency):
    branchDao = BranchDao(session)
    deleted = await branchDao.delete_branch(branch_id)
    if not deleted:
        raise BranchNotFoundAPIException(branch_id)
    return {"message": "Branch Deleted Successfully"}


@router.get(
    "/v1/branches",
    response_model=Union[
        List[BranchGetResponse], PaginationResponse[BranchGetResponse]
    ],
    summary="Get Branches",
    description="Retrieve a list of branches",
    responses={200: {"description": "List of Branches Retrieved Successfully"}},
)
async def get_branches(
    session: DBSessionDependency,
    branch_id: Optional[str] = None,
    bank_id: Optional[str] = None,
    branch_name: Optional[str] = None,
    bank_name: Optional[str] = None,
    branch_sol_id: Optional[str] = None,
    IFSC_code: Optional[str] = None,
    city: Optional[str] = None,
    region: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    page: Optional[int] = None,
    size: Optional[int] = None,
):
    branchDao = BranchDao(session)
    query = BaseQueryParams(
        search_values=(
            branch_id,
            bank_id,
            branch_name,
            bank_name,
            branch_sol_id,
            IFSC_code,
            city,
            region,
            state,
            postal_code,
        ),
        fields=(
            ("branch_id", MatchTypeEnum.EXACT),
            ("bank_id", MatchTypeEnum.EXACT),
            ("branch_name", MatchTypeEnum.PARTIAL),
            ("bank_name", MatchTypeEnum.PARTIAL),
            ("branch_sol_id", MatchTypeEnum.PARTIAL),
            ("branch_ifsc_code", MatchTypeEnum.PARTIAL),
            ("branch_city", MatchTypeEnum.PARTIAL),
            ("branch_region", MatchTypeEnum.PARTIAL),
            ("branch_state", MatchTypeEnum.PARTIAL),
            ("branch_postal_code", MatchTypeEnum.EXACT),
        ),
        page=page,
        size=size,
    )
    branches = await branchDao.get_branches(query)
    if not branches:
        raise BranchDetailsNotFoundAPIException()
    return [BranchGetResponse.from_db_record(branch) for branch in branches]


# @router.get(
#     "/v1/branch/{branch_id}",
#     response_model=BranchGetResponse,
#     summary="Get Branch by ID",
#     description="Retrieve a branch by it's ID",
#     responses={200: {"description": "Branch Retrieved Successfully"}},
# )
# async def get_branch(
#     branch_id: BranchIdPath,
#     session: DBSessionDependency,
#     reappraisal_client: ReappraisalServiceClientDependency,
# ):
#     branchDao = BranchDao(session)
#     branch = await branchDao.get_branch_by_id_or_ids(branch_id)
#     if not branch:
#         raise BranchNotFoundAPIException(branch_id)

#     await session.refresh(branch, ["bank", "bank_employees"])
#     branch_response = BranchGetResponse.model_validate(branch, from_attributes=True)
#     if branch_response:
#         reappraisals = await reappraisal_client.get_reappraisal_details_by_branch(
#             branch_id=branch_id
#         )
#         if reappraisals:
#             branch_response.reappraisal_services = [
#                 ReappraisalServiceAPIResponse(**r) for r in reappraisals
#             ]
#         return branch_response
#     return branch


# @router.put(
#     "/v1/branch/{branch_id}",
#     response_model=BranchGetResponse,
#     summary="Update Branch by ID",
#     description="Update a branch by its ID",
#     responses={200: {"description": "Branch Updated Successfully"}},
# )
# async def update_branch(
#     branch_id: BranchIdPath, payload: BranchCreateRequest, session: DBSessionDependency
# ):
#     branchDao = BranchDao(session)
#     branch = await branchDao.update_branch(branch_id, payload)
#     if not branch:
#         raise BranchNotFoundAPIException(branch_id)
#     return branch


# @router.put(
#     "/v1/branch/{branch_id}",
#     response_model=BranchGetResponse,
#     summary="Update Branch by ID",
#     description="Update a branch by its ID",
#     responses={200: {"description": "Branch Updated Successfully"}},
# )
# async def update_branch(
#     branch_id: BranchIdPath, payload: BranchCreateRequest, session: DBSessionDependency
# ):
#     branchDao = BranchDao(session)
#     updated_branch = await branchDao.update_branch(branch_id, payload)
#     if not updated_branch:
#         raise BranchNotFoundAPIException(branch_id)
#     return updated_branch


# @router.delete(
#     "/v1/branch/{branch_id}",
#     summary="Delete Branch by ID",
#     description="Delete a branch by its ID",
#     responses={204: {"description": "Branch Deleted Successfully"}},
# )
# async def delete_branch_by_id(branch_id: BranchIdPath, session: DBSessionDependency):
#     branchDao = BranchDao(session)
#     deleted = await branchDao.delete_branch(branch_id)
#     if not deleted:
#         raise BranchNotFoundAPIException(branch_id)
#     return {"message": "Branch Deleted Successfully"}


# @router.get(
#     "/v1/branches/by_ids",
#     response_model=List[BranchGetResponse],
#     summary="Get Branches by IDs",
#     description="Retrieve multiple branches by providing a list of branch IDs.",
#     responses={200: {"description": "Branches Retrieved Successfully"}},
# )
# async def get_branches_by_ids(
#     session: DBSessionDependency,
#     branch_ids: List[str] = Query(..., description="List of branch IDs"),
# ):
#     branchDao = BranchDao(session)
#     branches = await branchDao.get_branch_by_id_or_ids(branch_ids)

#     return [BranchGetResponse.model_validate(b, from_attributes=True) for b in branches]
