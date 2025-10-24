from io import BytesIO
from typing import Annotated
import uuid
from fastapi import UploadFile, Depends
from urllib.parse import urlparse
from app.api.db_connection.db_config import (
    s3_client,
    AWS_S3_BUCKET,
    AWS_S3_BASE_URL,
    AWS_REGION,
)
import mimetypes
from fastapi.responses import StreamingResponse


class S3Client:
    def __init__(self):
        self.s3 = s3_client
        self.bucket = AWS_S3_BUCKET
        self.base_url_template = AWS_S3_BASE_URL
        self.region = AWS_REGION

    async def upload_file(
        self,
        file: UploadFile,
        key_prefix: str,  # generic "folder path" (built outside)
        old_file_url: str | None = None,
    ) -> str:
        """
        Deletes old file (if any) and uploads new file to S3 using the given key_prefix.
        Returns the new file URL.
        """
        # Delete old file if exists
        if old_file_url:
            parsed = urlparse(old_file_url)
            key = parsed.path.lstrip("/")
            if key:
                self.s3.delete_object(Bucket=self.bucket, Key=key)

        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Combine prefix + filename
        key = f"{key_prefix}/{unique_filename}"

        # Upload to S3
        self.s3.upload_fileobj(file.file, self.bucket, key)

        # Build final file URL
        base_url = self.base_url_template.format(bucket=self.bucket, region=self.region)
        file_url = f"{base_url}/{key}"

        return file_url

    async def stream_file(
        self,
        file_url: str,
        download: bool = False,
    ) -> StreamingResponse:
        parsed = urlparse(file_url)
        key = parsed.path.lstrip("/").replace("//", "/")

        content_type, _ = mimetypes.guess_type(key)
        if not content_type:
            content_type = "application/octet-stream"

        disposition = "attachment" if download else "inline"

        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        file_stream = obj["Body"]

        return StreamingResponse(
            file_stream,
            media_type=content_type,
            headers={
                "Content-Disposition": f"{disposition}; filename={key.split('/')[-1]}"
            },
        )

    async def upload_bytesio(
        self,
        buffer: BytesIO,
        key_prefix: str,
        filename: str,
    ) -> str:

        key = f"{key_prefix}/{filename}"
        # Upload the buffer
        self.s3.upload_fileobj(buffer, self.bucket, key)

        # Build final URL
        base_url = self.base_url_template.format(bucket=self.bucket, region=self.region)
        file_url = f"{base_url}/{key}"

        return file_url

    async def delete_file(self, file_url: str | None):
        """
        Deletes the given file from S3 if the file URL is provided.
        """
        if file_url:
            parsed = urlparse(file_url)
            key = parsed.path.lstrip("/")
            if key:
                self.s3.delete_object(Bucket=self.bucket, Key=key)


async def get_s3_client():
    yield S3Client()


S3ClientDependency = Annotated[S3Client, Depends(get_s3_client)]
