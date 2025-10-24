from typing import Optional

from fastapi import status, HTTPException
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class ReappraisalServiceNotFoundAPIException(ApiException):
    def __init__(self, reappraisal_service_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_NOT_FOUND,
            error_message="Reappraisal service not found",
            error_details={"reappraisal_service_id": reappraisal_service_id},
        )


class ReappraisalServiceDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_DETAILS_NOT_FOUND,
            error_message="No reappraisal services found",
            error_details={},
        )


class ReappraisalServiceDateIncorrectAPIException(ApiException):
    def __init__(self, start_epoch: int, end_epoch: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_DATE_INCORRECT,
            error_message="Start date cannot be greater than end date",
            error_details={
                "rs_start_epoch": start_epoch,
                "rs_end_epoch": end_epoch,
            },
        )


class RsBranchIDNotFoundAPIException(ApiException):
    def __init__(self, branch_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_BRANCH_ID_NOT_FOUND,
            error_message="Reappraisal service BRANCH ID not found",
            error_details={"branch_id": branch_id},
        )


class ReappraiserServiceServiceStatusAPIException(ApiException):
    def __init__(self, reappraisal_service_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_INVALID_SETTLEMENT_STATUS,
            error_message=(
                "Invalid operation: Reappraisal service is not CONSOLIDATED, "
            ),
            error_details={
                "reappraisal_service_id": reappraisal_service_id,
            },
        )


class ReappraiserServiceSettlementStatusAlreadyExistsAPIException(ApiException):
    def __init__(
        self,
        reappraisal_service_id: Optional[str] = None,
        existing_status: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_SETTLEMENT_STATUS_ALREADY_EXISTS,
            error_message="Settlement status already set for this reappraisal_service_id ",
            error_details={
                "reappraisal_service_id": reappraisal_service_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )


class InvalidStatusException(ApiException):
    def __init__(
        self,
        message: str = "Only Active Reappraisal Services can be Ready for Payment",
        reappraisal_service_id: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_INVALID_STATUS,
            error_message=message,
            error_details={"reappraisal_service_id": reappraisal_service_id},
        )


class FilePendingException(ApiException):
    def __init__(
        self,
        message: str = "File is pending or not received",
        reappraisal_service_id: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_FILE_PENDING,
            error_message=message,
            error_details={"reappraisal_service_id": reappraisal_service_id},
        )


class ReappraisalServiceDeleteNotAllowedAPIException(ApiException):
    def __init__(
        self,
        reappraisal_service_id: str,
        current_status: str,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_DELETE_NOT_ALLOWED,
            error_message="Only Active reappraisal services can be deleted",
            error_details={
                "reappraisal_service_id": reappraisal_service_id,
                "current_status": current_status,
                "allowed_status": "ACTIVE",
            },
        )
