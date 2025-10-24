from fastapi import status
from ..exceptions.api_error_codes import ApiErrorCode
from ..exceptions.api_exception import ApiException


class BranchNotFoundAPIException(ApiException):
    def __init__(self, branch_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.BRANCH_NOT_FOUND,
            error_message="Branch not found",
            error_details={"branch_id": branch_id},
        )


class BranchDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.BRANCH_DETAILS_NOT_FOUND,
            error_message="Branch details not found",
            error_details={},
        )
