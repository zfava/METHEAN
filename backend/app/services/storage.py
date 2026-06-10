"""S3-compatible storage service for artifact uploads.

Uses boto3 with the S3 settings from config. Handles bucket creation
on first use and presigned URL generation.
"""

import uuid

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

from app.core.config import settings

# Module-level singleton client
_s3_client = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=BotoConfig(signature_version="s3v4"),
            region_name="us-east-1",
        )
    return _s3_client


def _ensure_bucket() -> None:
    """Create the bucket if it does not exist."""
    client = _get_s3_client()
    try:
        client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
    except ClientError:
        client.create_bucket(Bucket=settings.S3_BUCKET_NAME)


def upload_artifact(
    file_bytes: bytes,
    filename: str,
    content_type: str,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
) -> str:
    """Upload bytes to S3 and return the object key.

    Key format: {household_id}/{child_id}/{random_uuid}/{filename}
    This ensures household-level key isolation.
    """
    _ensure_bucket()
    client = _get_s3_client()

    key = f"{household_id}/{child_id}/{uuid.uuid4()}/{filename}"
    client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return key


def list_artifact_keys(prefix: str) -> list[str]:
    """List every object key under a prefix.

    Object keys are namespaced {household_id}/..., so passing the
    household id as the prefix enumerates everything the household
    owns regardless of which table tracked the upload.
    """
    client = _get_s3_client()
    keys: list[str] = []
    paginator = client.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=settings.S3_BUCKET_NAME, Prefix=prefix):
            keys.extend(obj["Key"] for obj in page.get("Contents", []))
    except ClientError:
        # Bucket missing means nothing was ever uploaded.
        return []
    return keys


def delete_artifact(s3_key: str) -> None:
    """Delete a single object. Raises on transport errors so callers
    can decide whether partial erasure is acceptable (the purge task
    treats any failure as a reason to retry the whole household)."""
    client = _get_s3_client()
    client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=s3_key)


def get_presigned_url(s3_key: str, expires_in: int = 3600) -> str:
    """Generate a presigned download URL for an S3 object."""
    client = _get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=expires_in,
    )
