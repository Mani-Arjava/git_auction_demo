from http.client import HTTPException
from fastapi import UploadFile


def validate_reappraisal_file(file: UploadFile, max_size_mb: int = 5):
    """
    Validate file type and size for reappraisal completion certificates.
    Allowed: PNG, JPG, PDF
    Max Size: 5 MB
    """
    allowed_types = ["image/png", "image/jpeg", "application/pdf", "image/jpg"]

    # Check content type
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: PNG, JPG, PDF.",
        )

    # check size
    file.file.seek(0, 2)  # move to end of file
    size = file.file.tell()
    file.file.seek(0)  # reset pointer

    if size > max_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size / (1024*1024):.2f} MB. Max allowed: {max_size_mb} MB.",
        )
