from typing import List, Optional, Union
from fastapi import APIRouter, Query, UploadFile, File
from app.api.dao.dao import DAO
from app.api.dao.reappraisal_service_dao import ReappraisalServiceDAO
from app.api.dao.reimbursement_dao import ReappraisalServiceReimbursementDAO
from app.api.db_connection.db_connection import DBSessionDependency

from app.api.exceptions.reappraisal_service_exception import (
    ReappraisalServiceNotFoundAPIException,
)
from app.api.repository.s3_repository import S3ClientDependency
from app.api.services.S3_service.file_validation import validate_reappraisal_file
from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.pagination.pagination import PaginationResponse
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum

from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.pagination.pagination import PaginationResponse
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.model.reimbursement.reimbursement_table import (
    ReappraisalServiceReimbursementTable,
    ReappraisalServiceReimbursementIdPath,
)
from app.api.model.reimbursement.reimbursement_create import (
    ReappraisalServiceReimbursementCreateRequest,
    ReappraisalServiceReimbursementCreateResponse,
    ReimbursementFileUpdate,
)
from app.api.model.reimbursement.reimbursement_get import (
    ReappraisalServiceReimbursementGetResponse,
)
from app.api.exceptions.reimbursment_exception import (
    RsReimbursementNotFoundAPIException,
    RsReimbursementDetailsNotFoundAPIException,
    FileNotFoundAPIException,
)

router = APIRouter()


@router.post(
    "/v1/reimbursement",
    response_model=ReappraisalServiceReimbursementCreateResponse,
    summary="Create Reappraisal Service Reimbursement",
    description="This API Endpoint is used for creating reappraisal service reimbursement details with user requesting values in request body.",
    responses={201: {"description": "Reappraisal Service Reimbursement Created"}},
)
async def create_rs_reimbursement(
    payload: ReappraisalServiceReimbursementCreateRequest, session: DBSessionDependency
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    rs_reimbursement = ReappraisalServiceReimbursementTable.model_validate(payload)
    rs_reimbursement = await rs_reimbursementDao.create_rs_reimbursement(
        rs_reimbursement
    )
    return rs_reimbursement


@router.get(
    "/v1/reimbursements",
    response_model=Union[
        List[ReappraisalServiceReimbursementGetResponse],
        PaginationResponse[ReappraisalServiceReimbursementGetResponse],
    ],
    summary="Retrieve All Reappraisal Service Reimbursement Details",
    description="This API Endpoint is used for retrieving all Reappraisal service reimbursement details.",
    responses={200: {"description": "Reappraisal Service Reimbursements Retrieved"}},
)
async def get_rs_reimbursements(
    session: DBSessionDependency,
    rsr_transaction_epoch: Optional[int] = None,
    reimbursement_id: Optional[str] = None,
    reappraiser_service_id: Optional[str] = None,
    appraiser_id: Optional[str] = None,
    reimbursement_category: Optional[str] = None,
    reimbursement_document: Optional[str] = None,
    reimbursement_settlement_statuses: List[Optional[str]] = Query(None),
    page: Optional[str] = None,
    size: Optional[str] = None,
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    query = BaseQueryParams(
        search_values=(
            rsr_transaction_epoch,
            reimbursement_id,
            reappraiser_service_id,
            appraiser_id,
            reimbursement_category,
            reimbursement_document,
            reimbursement_settlement_statuses,
        ),
        fields=(
            ("rs_reimbursement_transaction_epoch", MatchTypeEnum.EXACT),
            ("rs_reimbursement_id", MatchTypeEnum.EXACT),
            ("rs_reappraisal_service_id", MatchTypeEnum.EXACT),
            ("rs_appraiser_id", MatchTypeEnum.EXACT),
            ("rs_reimbursement_category", MatchTypeEnum.EXACT),
            ("rs_reimbursement_file_path", MatchTypeEnum.FILE_PATH_STATUS),
            ("rs_reimbursement_settlement_status", MatchTypeEnum.EXACT),
        ),
        page=page,
        size=size,
    )
    rs_reimbursement = await rs_reimbursementDao.get_rs_reimbursements(query)
    if not rs_reimbursement:
        raise RsReimbursementDetailsNotFoundAPIException()
    return rs_reimbursement


@router.get(
    "/v1/reimbursement/{rs_reimbursement_id}",
    response_model=ReappraisalServiceReimbursementGetResponse,
    summary="Retrieve Reappraisal Service Reimbursement Details",
    description="This API Endpoint is used for retrieving Reappraisal service reimbursement details based on Reappraisal Service Reimbursement id.",
    responses={200: {"description": "Reappraisal Service Reimbursement Retrieved"}},
)
async def get_rs_reimbursement(
    rs_reimbursement_id: ReappraisalServiceReimbursementIdPath,
    session: DBSessionDependency,
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    rs_reimbursement = await rs_reimbursementDao.get_rs_reimbursement(
        rs_reimbursement_id
    )
    if not rs_reimbursement:
        raise RsReimbursementNotFoundAPIException(rs_reimbursement_id)
    return rs_reimbursement


@router.put(
    "/v1/reimbursement/{rs_reimbursement_id}",
    response_model=ReappraisalServiceReimbursementCreateResponse,
    summary="Update Reappraisal Service Reimbursement Details",
    description="This API Endpoint is used for updating the existing reappraisal service reimbursement details usingreappraisal service reimbursement id.",
    responses={200: {"description": "Reappraisal Service Reimbursement Updated"}},
)
async def update_rs_reimbursement(
    rs_reimbursement_id: ReappraisalServiceReimbursementIdPath,
    payload: ReappraisalServiceReimbursementCreateRequest,
    session: DBSessionDependency,
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    rs_reimbursement = await rs_reimbursementDao.update_rs_reimbursement(
        rs_reimbursement_id=rs_reimbursement_id, reimbursement_update=payload
    )
    if not rs_reimbursement:
        raise RsReimbursementNotFoundAPIException(rs_reimbursement_id)
    return rs_reimbursement


@router.delete(
    "/v1/reimbursement/{rs_reimbursement_id}",
    summary="Delete Reappraisal Service Reimbursement Details",
    description="This API Endpoint is used for deleting the existing reappraisal service reimbursement details using reappraisal service reimbursement id.",
    responses={204: {"description": "Reappraisal Service Reimbursement Deleted"}},
)
async def delete_rs_reimbursement(
    rs_reimbursement_id: ReappraisalServiceReimbursementIdPath,
    session: DBSessionDependency,
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    rs_reimbursement = await rs_reimbursementDao.delete_rs_reimbursement(
        rs_reimbursement_id
    )
    if not rs_reimbursement:
        raise RsReimbursementNotFoundAPIException(rs_reimbursement_id)
    return {"message": "Reappraisal Service Reimbursement Deleted Successfully"}


@router.post(
    "/v1/reimbursement/{rs_reimbursement_id}/reimbursement_proofs",
    summary="Upload Reimbursement Proof File",
    description="This API Endpoint is used for uploading reimbursement proof files to S3 and updating the reimbursement record with the file URL.",
    responses={201: {"description": "Reimbursement Proof File Uploaded"}},
)
async def upload_reimbursement_proof(
    rs_reimbursement_id: ReappraisalServiceReimbursementIdPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
    proof_file: UploadFile = File(...),
):
    validate_reappraisal_file(proof_file)  # for validating the file
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    # 1. Fetch reimbursement
    existing_reimbursement = await rs_reimbursementDao.get_rs_reimbursement(
        rs_reimbursement_id
    )
    if not existing_reimbursement:
        raise RsReimbursementNotFoundAPIException(rs_reimbursement_id)
    # 2. Get reappraisal_service_id from reimbursement
    reappraisal_service_id = existing_reimbursement.rs_reappraisal_service_id
    # 3. Fetch reappraisal service to get appraiser_id
    reappraisal_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not reappraisal_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)
    appraiser_id = reappraisal_service.rs_appraiser_id
    # 4. Build S3 prefix
    key_prefix = await DAO.build_s3_key_prefix(
        appraiser_id=appraiser_id,
        reappraisal_service_id=reappraisal_service_id,
        category="reimbursement_proofs",
        reimbursement_id=rs_reimbursement_id,
    )
    # 5. Upload new proof
    file_url = await s3.upload_file(
        file=proof_file,
        key_prefix=key_prefix,
        old_file_url=existing_reimbursement.rs_reimbursement_file_path,
    )
    # 6. Update DB
    update_data = ReimbursementFileUpdate(rs_reimbursement_file_path=file_url)
    await rs_reimbursementDao.update_rs_reimbursement(rs_reimbursement_id, update_data)
    return {
        "reimbursement_id": rs_reimbursement_id,
        "file_url": file_url,
    }


@router.get(
    "/v1/reimbursement/{reimbursement_id}/fetch_reimbursement_proofs",
    summary="Fetch Reimbursement Proof File",
    description="This API Endpoint is used for fetching reimbursement proof files from S3. Set `download=true` to force download in browser, or `download=false` to preview inline (PDF/image in browser).",
    responses={200: {"description": "Reimbursement Proof File Fetched"}},
)
async def get_reimbursement_file(
    reimbursement_id: ReappraisalServiceReimbursementIdPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
    download: bool = Query(False, description="Set to true to force download"),
):

    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)
    existing_reimbursement = await rs_reimbursementDao.get_rs_reimbursement(
        reimbursement_id
    )
    if not existing_reimbursement:
        raise RsReimbursementNotFoundAPIException(reimbursement_id)

    file_url = existing_reimbursement.rs_reimbursement_file_path
    if not file_url:
        raise FileNotFoundAPIException(file_url)

    return await s3.stream_file(file_url=file_url, download=download)


@router.delete(
    "/v1/reimbursement/{rs_reimbursement_id}/reimbursement_proofs",
    summary="Delete Reimbursement Proof File",
    description="Deletes the reimbursement proof file from S3 and updates the database record.",
    responses={204: {"description": "Reimbursement Proof File Deleted"}},
)
async def delete_reimbursement_proof(
    rs_reimbursement_id: ReappraisalServiceReimbursementIdPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
):
    rs_reimbursementDao = ReappraisalServiceReimbursementDAO(session)

    # Fetch the existing reimbursement record
    existing_reimbursement = await rs_reimbursementDao.get_rs_reimbursement(
        rs_reimbursement_id
    )
    if not existing_reimbursement:
        raise RsReimbursementNotFoundAPIException(rs_reimbursement_id)

    # Delete the file from S3
    await s3.delete_file(existing_reimbursement.rs_reimbursement_file_path)

    # Update the database (set file path to null)
    update_data = ReimbursementFileUpdate(rs_reimbursement_file_path=None)
    await rs_reimbursementDao.update_rs_reimbursement(
        rs_reimbursement_id=rs_reimbursement_id, reimbursement_update=update_data
    )

    return {"message": "Reimbursement Proof File Deleted Successfully"}
