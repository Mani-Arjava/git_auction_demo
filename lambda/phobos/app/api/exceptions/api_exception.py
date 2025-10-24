from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from datetime import datetime
from app.api.exceptions.api_error_codes import ApiErrorCode


class ApiException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: ApiErrorCode,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
    ):
        self.error_body = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": {
                "status": status_code,
                "code": error_code,
                "message": error_message,
                "details": error_details,
            },
        }
        super().__init__(status_code=status_code, detail=self.error_body)


class RecordAlreadyExistsException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,  # conflict instead of 400
            error_code=ApiErrorCode.DUPLICATE_ENTRY,
            error_message=f"Record already exists.",
            error_details={},
        )
