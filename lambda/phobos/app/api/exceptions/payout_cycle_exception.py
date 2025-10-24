from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class PayoutCycleNotFoundAPIException(ApiException):
    def __init__(self, payout_Cycle_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.PAYOUT_CYCLE_NOT_FOUND,
            error_message="Payout cycle not found",
            error_details={"payout_cycle_id": payout_Cycle_id},
        )


class PayoutCycleDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.PAYOUT_CYCLE_DETAILS_NOT_FOUND,
            error_message="No payout cycle details found",
            error_details={},
        )
