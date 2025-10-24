from fastapi import status
from exceptions.api_exception import ApiException
from exceptions.api_error_codes import ApiErrorCode


class ResourceNotFoundException(ApiException):
    def __init__(self, resource_name: str, identifier: str | int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.DETAILS_NOT_FOUND,
            error_message=f"{resource_name} not found",
            error_details={"id": identifier},
        )


class UnprocessableEntityException(ApiException):
    def __init__(self, error_details: dict):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ApiErrorCode.VALIDATION_ERROR,
            error_message="Request validation failed",
            error_details=error_details or {},
        )


class InternalServerErrorException(ApiException):
    def __init__(self, error_details: dict = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ApiErrorCode.INTERNAL_SERVER_ERROR,
            error_message="Internal Server Error",
            error_details=error_details or {},
        )


class BadRequestException(ApiException):
    def __init__(self, error_details: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.BAD_REQUEST,
            error_message="Invalid request parameters",
            error_details=error_details or {},
        )
