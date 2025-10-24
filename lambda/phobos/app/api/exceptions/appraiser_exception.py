from fastapi import status
from app.api.exceptions.api_error_codes import ApiErrorCode
from app.api.exceptions.api_exception import ApiException


class AppraiserNotFoundAPIException(ApiException):
    def __init__(self, appraiser_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ApiErrorCode.APPRAISER_NOT_FOUND,
            error_message="Appraiser not found",
            error_details={"appraiser_id": appraiser_id},
        )


class AppraiserDetailsNotFoundAPIException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_200_OK,
            error_code=ApiErrorCode.APPRAISER_DETAILS_NOT_FOUND,
            error_message="No appraisers found",
            error_details={},
        )


class AppraiserHasServicesAPIException(ApiException):
    def __init__(self, appraiser_id: str, service_count: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.APPRAISER_HAS_SERVICES,
            error_message="Cannot update appraiser with associated services",
            error_details={
                "appraiser_id": appraiser_id,
                "service_count": service_count
            },
        )


class AppraiserNoActiveServicesAPIException(ApiException):
    def __init__(self, appraiser_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.APPRAISER_NO_ACTIVE_SERVICES,
            error_message="Appraiser has no services - PATCH operation not allowed",
            error_details={"appraiser_id": appraiser_id},
        )


class DuplicatePanException(ApiException):
    def __init__(self, pan: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.DUPLICATE_ENTRY,
            error_message="PAN number already exists",
            error_details={"pan": pan},
        )


class ValidationException(ApiException):
    def __init__(self, field_name: str, field_value: str, validation_error: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ApiErrorCode.VALIDATION_ERROR,
            error_message=f"Invalid {field_name}: {validation_error}",
            error_details={
                "field": field_name,
                "value": field_value,
                "validation_error": validation_error
            },
        )
