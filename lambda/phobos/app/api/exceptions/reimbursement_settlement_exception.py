from typing import Optional
from typing import Optional
from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class ReimbursementSettlementNotFoundAPIException(ApiException):
    def __init__(self, rs_reimbursement_id: str, payout_statement_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_REIMBURSEMENT_SETTLEMENT_NOT_FOUND,
            error_message="Reimbursement settlement not found",
            error_details={
                "reimbursement_settlement_id": rs_reimbursement_id,
                "payout_statement_id": payout_statement_id,
            },
        )


class ReimbursementSettlementDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_REIMBURSEMENT_SETTLEMENT_DETAILS_NOT_FOUND,
            error_message="No reimbursement settlements found",
            error_details={},
        )


class ReimbursementSettlementStatusAlreadyExistsAPIException(ApiException):
    def __init__(
        self,
        rs_reimbursement_id: Optional[str] = None,
        payout_statement_id: Optional[str] = None,
        existing_status: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_REIMBURSEMENT_SETTLEMENT_STATUS_ALREADY_EXISTS,
            error_message="Settlement status already set for this reimbursement settement ",
            error_details={
                "rs_reimbursement_id": rs_reimbursement_id,
                "payout_statement_id": payout_statement_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )
