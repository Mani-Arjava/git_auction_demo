from typing import Optional
from typing import Optional
from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class ChargeSettlementNotFoundAPIException(ApiException):
    def __init__(self, reappraisal_service_id: str, payout_statement_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_CHARGE_SETTLEMENT_NOT_FOUND,
            error_message="Reappraisal service charge settlement not found",
            error_details={
                "rs_id": reappraisal_service_id,
                "pst_id": payout_statement_id,
            },
        )


class ChargeSettlementDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_CHARGE_SETTLEMENT_DETAILS_NOT_FOUND,
            error_message="No reappraisal service charge settlements found",
            error_details={},
        )


class ChargeSettlementStatusAPIException(ApiException):
    def __init__(
        self,
        reappraisal_service_id: Optional[str] = None,
        payout_statement_id: Optional[str] = None,
        existing_status: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        super().__init__(
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_CHARGE_SETTLEMENT_STATUS_ALREADY_EXISTS,
            error_message="Settlement status already set for this charge settlement",
            error_details={
                "reappraisal_service_id": reappraisal_service_id,
                "payout_statement_id": payout_statement_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )
