from typing import Optional
from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class MultipleUnsettledPayoutStatementsApiException(ApiException):
    def __init__(self, pst_appraiser_id: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,  # 409 fits since it’s a business rule conflict
            error_code=ApiErrorCode.MULTIPLE_UNSETTLED_PAYOUT_STATEMENTS,
            error_message="Multiple unsettled payout statements found for appraiser",
            error_details={"pst_appraiser_id": pst_appraiser_id},
        )


class Reappraiser_Service_Details_Notfound_ApiException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_DETAILS_NOT_FOUND,
            error_message="No reappraisal services found",
            error_details={},
        )


class Reappraiser_Service_Notfound_ApiException(ApiException):
    def __init__(self, reappraisal_service_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_NOT_FOUND,
            error_message="Reappraisal service not found",
            error_details={"reappraisal_service_id": reappraisal_service_id},
        )


class Payout_Statement_Details_Notfound_ApiException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.PAYOUT_STATEMENT_DETAILS_NOT_FOUND,
            error_message="No payout statements found",
            error_details={},
        )


class Charge_Settlement_Notfound_ApiException(ApiException):
    def __init__(self, rs_id: Optional[str] = None, pst_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.REAPPRAISAL_SERVICE_CHARGE_SETTLEMENT_NOT_FOUND,
            error_message="Reappraisal service charge settlement not found",
            error_details={"rs_id": rs_id, "pst_id": pst_id},
        )
