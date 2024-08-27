import boto3
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def upload_to_processed_bucket(pq_bytes, filename:str):
    
    try:
        if isinstance(pq_bytes, bytes):
            s3 = boto3.client("s3")
            response = s3.put_object(
                    Body=pq_bytes,
                    Bucket="team-hyper-accelerated-dragon-bucket-processed",
                    Key = filename
                )
            logger.info("Successfully uploaded PQ bytes to the processed bucket!")
        else:
            logger.error("Failed to upload PQ Bytes to processed bucket!")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return e


