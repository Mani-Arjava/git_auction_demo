from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class PayoutStatementNotFoundAPIException(ApiException):
    def __init__(self, pst_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.PAYOUT_STATEMENT_NOT_FOUND,
            error_message="Payout statement not found",
            error_details={"pst_id": pst_id},
        )


class PayoutStatementDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.PAYOUT_STATEMENT_DETAILS_NOT_FOUND,
            error_message="No payout statements found",
            error_details={},
        )


class PayoutStatementSettlementStatusAPIException(ApiException):
    def __init__(self, payout_statement_id: str, existing_status: str, new_status: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ApiErrorCode.DATA_ALREADY_EXITS,
            error_message="Settlement status has already been updated and cannot be changed again",
            error_details={
                "payout_statement_id": payout_statement_id,
                "existing_status": existing_status,
                "new_status": new_status,
            },
        )
