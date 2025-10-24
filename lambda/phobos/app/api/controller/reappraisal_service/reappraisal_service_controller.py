import asyncio
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
from fastapi import UploadFile, File, Form
from pydantic import ValidationError
from app.api.dao.bank_dao import BankDao
from app.api.dao.branch_dao import BranchDao    
from app.api.dao.advance_dao import ReappraisalServiceAdvanceDAO
from app.api.dao.reappraisal_service_dao import ReappraisalServiceDAO
from app.api.dao.reimbursement_dao import ReappraisalServiceReimbursementDAO
from app.api.db_connection.db_connection import DBSessionDependency
from app.api.services.pagination.pagination import PaginationResponse
from app.api.services.pagination.pagination import PaginationResponse
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceIDPath,
    ReappraisalServiceTable,
)
from app.api.model.reappraisal_service.reappraisal_service_create import (
    ReappraisalServiceCreateRequest,
    ReappraisalServiceCreateResponse,
    ReappraisalServiceUpdateRequest,
)
from app.api.model.reappraisal_service.reappraisal_service_get import (
    ReappraisalServiceGetByIdResponse,
    ReappraisalServiceGetResponse,
)
from app.api.exceptions.reappraisal_service_exception import (
    ReappraisalServiceNotFoundAPIException,
    ReappraisalServiceDetailsNotFoundAPIException,
    RsBranchIDNotFoundAPIException,
    ReappraisalServiceDateIncorrectAPIException,
    ReappraisalServiceDeleteNotAllowedAPIException,
)

from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.repository.branch_API_repository import BranchServiceClientDependency
from app.api.exceptions.reimbursment_exception import FileNotFoundAPIException
from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.repository.branch_API_repository import (
    BranchServiceClientDependency,
)
from app.api.repository.s3_repository import S3Client, S3ClientDependency
from app.api.model.reappraisal_service.reappraisal_service_create import (
    ReappraisalFileUpdate,
)
from app.api.dao.dao import DAO
from app.api.services.S3_service.file_validation import validate_reappraisal_file
from app.api.dao.appraiser_dao import AppraiserDAO
from app.api.exceptions.appraiser_exception import AppraiserNotFoundAPIException
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
from app.api.services.S3_service.pdf_generator import generate_authorisation_pdf
from app.api.services.service_settlement.queue_reappraisal_service import (
    QueuedReappraisalService,
)
from app.api.model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum

router = APIRouter()


@router.post(
    "/v1/reappraisal_service",
    response_model=ReappraisalServiceCreateResponse,
    summary="Create Appraiser Details",
    description="This API Endpoint is used for creating appraiser details with user requesting values in request body.",
    responses={201: {"description": "Appraiser Created"}},
)
async def create_reappraisal_service(
    payload: ReappraisalServiceCreateRequest,
    session: DBSessionDependency,
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    reappraisal_service = ReappraisalServiceTable.model_validate(payload)
    if reappraisal_service.rs_start_epoch > reappraisal_service.rs_end_epoch:
        raise ReappraisalServiceDateIncorrectAPIException(
            start_epoch=reappraisal_service.rs_start_epoch,
            end_epoch=reappraisal_service.rs_end_epoch,
        )
    reappraisal_service = await reappraisal_serviceDao.create_reappraisal_service(
        reappraisal_service
    )
    return reappraisal_service


@router.get(
    "/v1/reappraisal_service/{reappraisal_service_id}",
    response_model=ReappraisalServiceGetByIdResponse,
    summary="Retrieve Reappraisal Details",
    description="This API Endpoint is used for retrieving reappraisal details based on Reappraisal Service id.",
    responses={200: {"description": "Reappraisal Service Retrieved"}},
)
async def get_reappraisal_service(
    reappraisal_service_id: ReappraisalServiceIDPath, session: DBSessionDependency
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    reappraisal_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not reappraisal_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

    # Get reimbursement and advance amounts from database
    reimbursement_serviceDao = ReappraisalServiceReimbursementDAO(session)
    reimbursement_amount = (
        await reimbursement_serviceDao.get_total_reimbursement_amount(
            reappraisal_service_id
        )
    )

    advanceDao = ReappraisalServiceAdvanceDAO(session)
    advance_amount = await advanceDao.get_total_advance_amount(reappraisal_service_id)

    # Calculate total amount: rs_charge + reimbursement - advance
    total_amount = reappraisal_service.rs_charge + reimbursement_amount - advance_amount

    # Get bank and branch details from database
    bankDao = BankDao(session)
    branchDao = BranchDao(session)

    bank = await bankDao.get_bank(reappraisal_service.rs_bank_id)
    branch = await branchDao.get_branch_by_id_or_ids(reappraisal_service.rs_branch_id)

    # Calculate number of days from start and end epoch
    start_date = reappraisal_service.rs_start_epoch
    end_date = reappraisal_service.rs_end_epoch
    no_of_days = (end_date - start_date) // (24 * 60 * 60) + 1  # Convert epoch difference to days

    # Prepare response data with all mandatory fields from database
    response_data = {
        "reappraisal_service_id": reappraisal_service.reappraisal_service_id,
        "rs_appraiser_id": reappraisal_service.rs_appraiser_id,
        "rs_bank_id": reappraisal_service.rs_bank_id,
        "rs_branch_id": reappraisal_service.rs_branch_id,
        "rs_start_epoch": reappraisal_service.rs_start_epoch,
        "rs_end_epoch": reappraisal_service.rs_end_epoch,
        "rs_packet_count": reappraisal_service.rs_packet_count,
        "rs_charge": reappraisal_service.rs_charge,
        "rs_status": reappraisal_service.rs_status,
        "rs_completion_file_path": reappraisal_service.rs_completion_file_path,
        "rs_description": reappraisal_service.rs_description,
        "appraiser": reappraisal_service.appraiser,
        "reimbursements": reappraisal_service.reimbursements,
        "advances": reappraisal_service.advances,

        # Set financial fields
        "reimbursement_amount": reimbursement_amount,
        "advance_amount": advance_amount,
        "total_amount": total_amount,

        # Set appraiser fields from database
        "appraiser_name": reappraisal_service.appraiser.appraiser_full_name if reappraisal_service.appraiser else "",

        # Set bank and branch fields from database
        "bank_name": bank.bank_name if bank else "",
        "bank_code": bank.bank_code if bank else "",
        "branch_name": branch.branch_name if branch else "",
        "branch_sol_id": branch.branch_sol_id if branch else "",

        # Set calculated fields
        "no_of_days": no_of_days,

        # Set timestamp fields
        "created_at_epoch": str(reappraisal_service.created_at_epoch),
        "updated_at_epoch": str(reappraisal_service.updated_at_epoch),
    }

    return ReappraisalServiceGetByIdResponse(**response_data)


@router.get(
    "/v1/reappraisal_services",
    response_model=Union[
        List[ReappraisalServiceGetResponse],
        PaginationResponse[ReappraisalServiceGetResponse],
    ],
    summary="Retrieve All Reappraisal Service Details",
    description="This API Endpoint is used for retrieving all Reappraisal details.",
    responses={200: {"description": "Reappraisals Retrieved"}},
)
async def get_reappraisal_services(
    session: DBSessionDependency,
    reappraisal_id: Optional[str] = None,
    appraiser_id: Optional[str] = None,
    branch_id: Optional[str] = None,
    service_date: Optional[int] = None,
    bank_name: Optional[str] = None,
    appraiser_name: Optional[str] = None,
    service_statuses: List[Optional[str]] = Query(None),
    file_path_status: Optional[str] = None,
    settlement_statuses: List[Optional[str]] = Query(None),
    page: Optional[int] = None,
    size: Optional[int] = None,
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)


    # Build query params
    query = BaseQueryParams(
        search_values=(
            reappraisal_id,
            appraiser_id,
            service_date,
            appraiser_name,
            service_statuses,
            file_path_status,
            settlement_statuses,
        ),
        fields=(
            ("reappraisal_service_id", MatchTypeEnum.EXACT),
            ("rs_appraiser_id", MatchTypeEnum.EXACT),
            ("rs_branch_id", MatchTypeEnum.EXACT),  # will handle list of branch_ids too
            (("rs_start_epoch", "rs_end_epoch"), MatchTypeEnum.EPOCH_RANGE),
            (("full_name"), MatchTypeEnum.PARTIAL),
            ("rs_status", MatchTypeEnum.EXACT),
            ("rs_completion_file_path", MatchTypeEnum.FILE_PATH_STATUS),
            ("rs_settlement_status", MatchTypeEnum.EXACT),
        ),
        page=page,
        size=size,
    )

    # Fetch from app.api.dao
    reappraisal_service = await reappraisal_serviceDao.get_reappraisal_services(query)

    if not reappraisal_service:
        raise ReappraisalServiceDetailsNotFoundAPIException()

    # Transform data to match the new response structure
    response_list = []
    for service in reappraisal_service:
        # Get bank and branch details
        bankDao = BankDao(session)
        branchDao = BranchDao(session)

        bank = await bankDao.get_bank(service.rs_bank_id)
        branch = await branchDao.get_branch_by_id_or_ids(service.rs_branch_id)

        # Get reimbursement and advance amounts for total calculation
        reimbursement_serviceDao = ReappraisalServiceReimbursementDAO(session)
        reimbursement_amount = await reimbursement_serviceDao.get_total_reimbursement_amount(
            service.reappraisal_service_id
        )

        advanceDao = ReappraisalServiceAdvanceDAO(session)
        advance_amount = await advanceDao.get_total_advance_amount(service.reappraisal_service_id)

        # Calculate total amount: rs_charge + reimbursement - advance
        total_amount = service.rs_charge + reimbursement_amount - advance_amount

        response_item = {
            "reappraisal_service_id": service.reappraisal_service_id,
            "appraiser_name": service.appraiser.appraiser_full_name if service.appraiser else "",
            "bank_name": bank.bank_name if bank else "",
            "branch_name": branch.branch_name if branch else "",
            "start_epoch": service.rs_start_epoch,
            "end_epoch": service.rs_end_epoch,
            "no_of_packets": service.rs_packet_count,
            "status": service.rs_status,
            "total_amount": total_amount,
        }
        response_list.append(ReappraisalServiceGetResponse(**response_item))

    return response_list


@router.put(
    "/v1/reappraisal_service/{reappraisal_service_id}",
    response_model=ReappraisalServiceCreateResponse,
    summary="Update Reappraisal Service Details",
    description="This API Endpoint is used for updating the existing reappraisal service details using appraiser id.",
    responses={200: {"description": "Reappraisal Updated"}},
)
async def update_reappraisal_service(
    reappraisal_service_id: ReappraisalServiceIDPath,
    payload: ReappraisalServiceCreateRequest,
    session: DBSessionDependency,
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    reappraisal_service = await reappraisal_serviceDao.update_reappraisal_service(
        reappraisal_service_id=reappraisal_service_id,
        reappraisal_service_update=payload,
    )

    if not reappraisal_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)
    return reappraisal_service


@router.delete(
    "/v1/reappraisal_service/{reappraisal_service_id}",
    summary="Delete Reappraisal Service Details",
    description="This API Endpoint is used for deleting the existing reappraisal service details using appraiser id. Only services with ACTIVE status can be deleted.",
    responses={204: {"description": "Reappraisal Deleted"}},
)
async def delete_reappraisal_service(
    reappraisal_service_id: ReappraisalServiceIDPath, session: DBSessionDependency
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)

    # First, get the reappraisal service to check its status
    reappraisal_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not reappraisal_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

    # Check if the service status is ACTIVE before allowing deletion
    if reappraisal_service.rs_status != ReappraisalServiceStatusEnum.ACTIVE:
        raise ReappraisalServiceDeleteNotAllowedAPIException(
            reappraisal_service_id=reappraisal_service_id,
            current_status=reappraisal_service.rs_status.value
        )

    # Proceed with deletion if status is ACTIVE
    is_reappraisal_service = await reappraisal_serviceDao.delete_reappraisal_service(
        reappraisal_service_id
    )
    return {"message": "Reappraisal Service Deleted Successfully"}


@router.post(
    "/v1/reappraisal_service/{reappraisal_service_id}/completion_certificates",
    summary="Upload Completion Certificate",
    description="Uploads a completion certificate file for the specified reappraisal service.",
    responses={201: {"description": "File Uploaded Successfully"}},
)
async def create_reappraisal_file(
    reappraisal_service_id: ReappraisalServiceIDPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
    completion_file: UploadFile = File(...),
):
    validate_reappraisal_file(completion_file)  # for validating the file
    reappraisal_serviceDao = ReappraisalServiceDAO(session)

    # Fetch reappraisal service
    existing_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not existing_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

    appraiser_id = existing_service.rs_appraiser_id

    # Key prefix for completion certificate
    key_prefix = await DAO.build_s3_key_prefix(
        appraiser_id=appraiser_id,
        reappraisal_service_id=reappraisal_service_id,
        category="completion_certificates",
    )

    file_url = await s3.upload_file(
        file=completion_file,
        key_prefix=key_prefix,
        old_file_url=existing_service.rs_completion_file_path,
    )

    update_data = ReappraisalFileUpdate(rs_completion_file_path=file_url)
    await reappraisal_serviceDao.update_reappraisal_service(
        reappraisal_service_id, update_data
    )

    return {"reappraisal_id": reappraisal_service_id, "file_url": file_url}


@router.get(
    "/v1/reappraisal_service/{reappraisal_service_id}/fetch_completion_certificates",
    summary="Fetch Completion Certificate",
    description="Streams the completion certificate file for the specified reappraisal service directly from S3.",
    responses={200: {"description": "File Streamed Successfully"}},
)
async def get_reappraisal_file(
    reappraisal_service_id: ReappraisalServiceIDPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
    download: bool = Query(False, description="Set to true to force download"),
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    existing_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not existing_service:
        raise ReappraisalServiceNotFoundAPIException(
            reappraisal_service_id=reappraisal_service_id
        )

    file_url = existing_service.rs_completion_file_path
    if not file_url:
        raise FileNotFoundAPIException(file_url=file_url)

    return await s3.stream_file(file_url=file_url, download=download)


@router.get(
    "/v1/reappraisal_service/{reappraisal_service_id}/generate_authorisation",
    summary="Generate Authorization Letter",
    description="Generates an authorization letter PDF for the specified reappraisal service and streams it directly. Also uploads a copy to S3.",
    responses={200: {"description": "Authorization Letter Generated"}},
)
async def generate_authorisation_letter(
    reappraisal_service_id: ReappraisalServiceIDPath,
    session: DBSessionDependency,
    branch_service_client: BranchServiceClientDependency,
    s3: S3ClientDependency,
):
    # fetch from app.api.dao + microservices
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

    appraiser = {
        "full_name": f"{service.appraiser.appraiser_first_name} {service.appraiser.appraiser_last_name}",
        "aadhaar": service.appraiser.appraiser_aadhaar,
        "pan": service.appraiser.appraiser_pan,
        "phone": service.appraiser.appraiser_phone,
    }

    branch = await branch_service_client.get_branches(service.rs_branch_id)
    if branch is None:
        raise RsBranchIDNotFoundAPIException(service.rs_branch_id)
    bank_name = branch.get("bank", {}).get("bank_name", "")

    key_prefix = await DAO.build_s3_key_prefix(
        appraiser_id=service.rs_appraiser_id,
        reappraisal_service_id=reappraisal_service_id,
        category="authorization_letters",
    )

    buffer, document_id = generate_authorisation_pdf(
        reappraisal_service_id=reappraisal_service_id,
        appraiser=appraiser,
        branch=branch,
        bank_name=bank_name,
    )
    filename = f"{document_id}.pdf"
    upload_buffer = BytesIO(buffer.getvalue())

    # Upload copy to S3
    filename = f"{document_id}.pdf"
    file_url = await s3.upload_bytesio(
        buffer=upload_buffer, key_prefix=key_prefix, filename=filename
    )

    # Reset main buffer for StreamingResponse
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=authorisation_{reappraisal_service_id}.pdf",
            "X-Document-ID": document_id,
            "X-File-URL": file_url,
        },
    )  # this will download the file


@router.patch(
    "/v1/reappraisal_service/{reappraisal_service_id}/queue",
    response_model=ReappraisalServiceCreateResponse,
    summary="Queue a reappraisal service",
)
async def queue_reappraisal_service(
    reappraisal_service_id: ReappraisalServiceIDPath,
    session: DBSessionDependency,
):
    service = QueuedReappraisalService(session)
    updated_reappraisal = await service.queue_reappraisal_service(
        reappraisal_service_id
    )
    return updated_reappraisal


@router.delete(
    "/v1/reappraisal_service/{reappraisal_service_id}/completion_certificates",
    summary="Delete Completion Certificate",
    description="Deletes the completion certificate file for the specified reappraisal service from both S3 and the database record.",
    responses={204: {"description": "File Deleted Successfully"}},
)
async def delete_reappraisal_file(
    reappraisal_service_id: ReappraisalServiceIDPath,
    session: DBSessionDependency,
    s3: S3ClientDependency,
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)

    # Fetch reappraisal service
    existing_service = await reappraisal_serviceDao.get_reappraisal_service(
        reappraisal_service_id
    )
    if not existing_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

    file_url = existing_service.rs_completion_file_path
    if not file_url:
        raise FileNotFoundAPIException(file_url=file_url)

    # Delete from S3
    await s3.delete_file(file_url=file_url)

    # Update DB record to remove file URL
    update_data = ReappraisalFileUpdate(rs_completion_file_path=None)
    await reappraisal_serviceDao.update_reappraisal_service(
        reappraisal_service_id, update_data
    )

    return {"message": "Completion Certificate Deleted Successfully"}


@router.patch(
    "/v1/reappraisal_service/{reappraisal_service_id}",
    response_model=ReappraisalServiceCreateResponse,
    summary="Partially Update Reappraisal Service Details",
    description="This API Endpoint is used for partially updating the existing reappraisal service details using appraiser id.",
    responses={200: {"description": "Reappraisal Partially Updated"}},
)
async def partial_update_reappraisal_service(
    reappraisal_service_id: ReappraisalServiceIDPath,
    payload: ReappraisalServiceUpdateRequest,
    session: DBSessionDependency,
):
    reappraisal_serviceDao = ReappraisalServiceDAO(session)
    # Validate payload against the model
    valid_data = ReappraisalServiceUpdateRequest.model_validate(payload)

    reappraisal_service = await reappraisal_serviceDao.update_reappraisal_service(
        reappraisal_service_id=reappraisal_service_id,
        reappraisal_service_update=valid_data,
    )

    if not reappraisal_service:
        raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)
    return reappraisal_service
