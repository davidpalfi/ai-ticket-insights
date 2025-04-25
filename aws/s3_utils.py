import boto3
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

s3 = boto3.client("s3")
bucket_name = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path.split("/")[-1]
    try:
        logger.info(f"Uploading '{file_path}' to 's3://{bucket_name}/{object_name}'")
        s3.upload_file(file_path, bucket_name, object_name)
        logger.info(f"Upload successful: 's3://{bucket_name}/{object_name}'")
    except Exception as e:
        logger.error(f"Upload failed: {e}")

def download_file_from_s3(bucket_name, object_name, download_path=None):
    if download_path is None:
        download_path = object_name.split("/")[-1]
    try:
        logger.info(f"Downloading 's3://{bucket_name}/{object_name}' to '{download_path}'")
        s3.download_file(bucket_name, object_name, download_path)
        logger.info(f"Download successful: 's3://{bucket_name}/{object_name}' to '{download_path}'")
    except Exception as e:
        logger.error(f"Download failed: {e}")
