import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
if not BUCKET_NAME:
    logger.error("S3_BUCKET_NAME environment variable is not set")
    raise RuntimeError("S3_BUCKET_NAME environment variable is not set")

def upload_to_s3(file_path: str, object_name: str = None) -> None:
    """
    Upload a local file to an S3 bucket.

    :param file_path: Path to the local file to upload.
    :param object_name: S3 key under which to store the file (defaults to filename).
    :raises NoCredentialsError: If AWS credentials are missing.
    :raises ClientError: If the upload fails.
    """
    key = object_name or os.path.basename(file_path)
    s3 = boto3.client("s3")
    try:
        logger.info(f"Uploading '{file_path}' to 's3://{BUCKET_NAME}/{key}'")
        s3.upload_file(file_path, BUCKET_NAME, key)
        logger.info(f"Upload successful: s3://{BUCKET_NAME}/{key}")
    except NoCredentialsError:
        logger.exception("AWS credentials not found. Upload aborted.")
        raise
    except ClientError as e:
        logger.exception(f"Failed to upload '{file_path}' to 's3://{BUCKET_NAME}/{key}': {e}")
        raise

def download_from_s3(object_name: str, download_path: str = None) -> None:
    """
    Download an object from an S3 bucket to a local file.

    :param object_name: S3 key of the object to download.
    :param download_path: Local filesystem path to save the file (defaults to filename).
    :raises NoCredentialsError: If AWS credentials are missing.
    :raises ClientError: If the download fails.
    """
    local_path = download_path or os.path.basename(object_name)
    s3 = boto3.client("s3")
    try:
        logger.info(f"Downloading 's3://{BUCKET_NAME}/{object_name}' to '{local_path}'")
        s3.download_file(BUCKET_NAME, object_name, local_path)
        logger.info(f"Download successful: s3://{BUCKET_NAME}/{object_name} to {local_path}")
    except NoCredentialsError:
        logger.exception("AWS credentials not found. Download aborted.")
        raise
    except ClientError as e:
        logger.exception(f"Failed to download 's3://{BUCKET_NAME}/{object_name}': {e}")
        raise
