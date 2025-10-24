from typing import Optional
from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class RsAdvanceNotFoundAPIException(ApiException):
    def __init__(self, rs_advance_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_ADVANCE_NOT_FOUND,
            error_message="Reappraisal service advance not found",
            error_details={"rs_advance_id": rs_advance_id},
        )


class RsAdvanceDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_ADVANCE_DETAILS_NOT_FOUND,
            error_message="No reappraisal service advances found",
            error_details={},
        )


class RsAdvanceSettlementStatusAPIException(ApiException):
    def __init__(
        self,
        rs_advance_id: Optional[str] = None,
        existing_status: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        super().__init__(
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_ADVANCE_SETTLEMENT_STATUS_ALREADY_EXISTS,
            error_message="Settlement status already set for this advance ",
            error_details={
                "rs_advance_id": rs_advance_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )
