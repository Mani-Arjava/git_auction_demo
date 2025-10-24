from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class RsReimbursementNotFoundAPIException(ApiException):
    def __init__(self, rs_reimbursement_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_REIMBURSEMENT_NOT_FOUND,
            error_message="Reappraisal service not found",
            error_details={"rs_reimbursement_id": rs_reimbursement_id},
        )


class RsReimbursementDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_REIMBURSEMENT_DETAILS_NOT_FOUND,
            error_message="No reappraisal services found",
            error_details={},
        )


class FileNotFoundAPIException(ApiException):
    def __init__(self, file_url: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.FILE_NOT_FOUND,
            error_message="File not found",
            error_details={"file_url": file_url},
        )
