from typing import Optional
from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class AdvanceSettlementNotFoundAPIException(ApiException):
    def __init__(
        self,
        rs_advance_id: Optional[str] = None,
        payout_statement_id: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.ADVANCE_SETTLEMENT_NOT_FOUND,
            error_message="Reappraisal service advance settlement not found",
            error_details={
                "rs_advance_id": rs_advance_id,
                "payout_statement_id": payout_statement_id,
            },
        )


class AdvanceSettlementDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.ADVANCE_SETTLEMENT_DETAILS_NOT_FOUND,
            error_message="No reappraisal service advance settlements found",
            error_details={},
        )


class AdvanceSettlementStatusAPIException(ApiException):
    def __init__(
        self,
        rs_advance_id: Optional[str] = None,
        payout_statement_id: Optional[str] = None,
        existing_status: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        super().__init__(
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_ADVANCE_SETTLEMENT_STATUS_ALREADY_EXISTS,
            error_message="Settlement status already set for this advance settlement",
            error_details={
                "reapprairs_advance_idsal_service_id": rs_advance_id,
                "payout_statement_id": payout_statement_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )
