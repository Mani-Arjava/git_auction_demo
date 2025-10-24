from fastapi import status
from ..exceptions.api_error_codes import ApiErrorCode
from ..exceptions.api_exception import ApiException


class BankNotFoundAPIException(ApiException):
    def __init__(self, bank_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.BANK_NOT_FOUND,
            error_message="Bank not found",
            error_details={"bank_id": bank_id},
        )


class BankDetailsNotFoundAPIException(ApiException):
    def __init__(
        self,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.BANK_DETAILS_NOT_FOUND,
            error_message="Bank details not found",
            error_details={},
        )
