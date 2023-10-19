import json
import boto3
import logging

# Specify the AWS region where your S3 buckets are located
region_name = 'ap-south-1'

# Initialize a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Create an S3 client in the specified region
    s3_client = boto3.client('s3', region_name=region_name)

    # List all S3 buckets in the region
    s3_buckets = s3_client.list_buckets()

    unencrypted_buckets = []

    # Detect buckets without server-side encryption
    for bucket in s3_buckets['Buckets']:
        bucket_name = bucket['Name']

        # Check the bucket's server-side encryption configuration
        try:
            bucket_encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
        except Exception as e:
            # If the bucket doesn't have server-side encryption configured, it raises an exception
            logger.info(f"Bucket {bucket_name} doesn't have server-side encryption.")
            unencrypted_buckets.append(bucket_name)

    if unencrypted_buckets:
        logger.info(f"Unencrypted S3 buckets: {', '.join(unencrypted_buckets)}")
    else:
        logger.info("No unencrypted S3 buckets found.")
