import boto3
from django.conf import settings
import logging
import mimetypes

logger = logging.getLogger(__name__)

def upload_to_s3(file_obj, file_path):
    """
    Unified S3 upload helper with region fallback for Supabase/S3 compatibility.
    Tries multiple regions to prevent 'SignatureDoesNotMatch' errors.
    """
    key_id = settings.AWS_ACCESS_KEY_ID
    secret = settings.AWS_SECRET_ACCESS_KEY
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    
    if not key_id or not secret:
        logger.error("AWS credentials missing in settings.")
        return None

    # Detect Content-Type
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'

    # Regions to attempt
    regions_to_try = [settings.AWS_S3_REGION_NAME, 'ap-southeast-1', 'us-east-1']
    # Remove duplicates while preserving order
    regions_to_try = list(dict.fromkeys(regions_to_try))

    last_error = None
    
    # Ensure we are at the start of the file
    if hasattr(file_obj, 'seek'):
        file_obj.seek(0)
    file_data = file_obj.read()

    for region in regions_to_try:
        try:
            logger.info(f"Attempting S3 upload to {region}...")
            s3_client = boto3.client(
                's3',
                region_name=region,
                endpoint_url=endpoint_url,
                aws_access_key_id=key_id,
                aws_secret_access_key=secret,
            )
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_path,
                Body=file_data,
                ContentType=content_type
            )
            
            # Construct the absolute URL
            # Using AWS_S3_CUSTOM_DOMAIN if available, otherwise fallback to endpoint
            if settings.AWS_S3_CUSTOM_DOMAIN:
                url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
            else:
                url = f"{endpoint_url}/{bucket_name}/{file_path}"
            
            logger.info(f"Successfully uploaded to S3 via {region}: {url}")
            return url
            
        except Exception as e:
            logger.warning(f"S3 upload failed for region {region}: {str(e)}")
            last_error = e
            continue

    logger.error(f"All S3 regions failed. Last error: {str(last_error)}")
    return None

def delete_from_s3(file_path):
    """
    Delete a file from S3 bucket.
    """
    key_id = settings.AWS_ACCESS_KEY_ID
    secret = settings.AWS_SECRET_ACCESS_KEY
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    
    if not key_id or not secret:
        return False

    try:
        s3_client = boto3.client(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=endpoint_url,
            aws_access_key_id=key_id,
            aws_secret_access_key=secret,
        )
        s3_client.delete_object(Bucket=bucket_name, Key=file_path)
        logger.info(f"Successfully deleted from S3: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete from S3: {str(e)}")
        return False
