import boto3
import botocore
import argparse
import logging
import sys

# ==== Logging Setup ====
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ==== AWS Clients ====
def get_clients(region):
    return boto3.client("s3", region_name=region), boto3.client("dynamodb", region_name=region)

# ==== S3 Bucket Functions ====
import logging
import botocore.exceptions

def create_s3_bucket(bucket_name, region, s3):
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        logging.info(f"S3 bucket '{bucket_name}' created.")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            logging.warning(f"S3 bucket '{bucket_name}' already exists and is owned by you.")
        else:
            logging.error(f"Failed to create S3 bucket: {e}")
            raise

    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    logging.info("Versioning enabled on S3 bucket.")

def delete_s3_bucket(bucket_name, s3):
    try:
        # Delete all objects first (versioned)
        versioned = s3.list_object_versions(Bucket=bucket_name)
        delete_markers = versioned.get('DeleteMarkers', [])
        versions = versioned.get('Versions', [])
        objects = delete_markers + versions

        if objects:
            s3.delete_objects(
                Bucket=bucket_name,
                Delete={
                    'Objects': [{'Key': obj['Key'], 'VersionId': obj['VersionId']} for obj in objects]
                }
            )
            logging.info("All objects in bucket deleted.")

        s3.delete_bucket(Bucket=bucket_name)
        logging.info(f"S3 bucket '{bucket_name}' deleted.")
    except Exception as e:
        logging.error(f"Failed to delete S3 bucket: {e}")

# ==== DynamoDB Table Functions ====
def create_dynamodb_table(table_name, dynamodb):
    existing_tables = dynamodb.list_tables()["TableNames"]
    if table_name in existing_tables:
        logging.warning(f"DynamoDB table '{table_name}' already exists.")
        return

    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[{
            'AttributeName': 'LockID',
            'AttributeType': 'S'
        }],
        KeySchema=[{
            'AttributeName': 'LockID',
            'KeyType': 'HASH'
        }],
        BillingMode='PAY_PER_REQUEST'
    )
    logging.info(f"DynamoDB table '{table_name}' created.")

    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    logging.info("DynamoDB table is now active.")

def delete_dynamodb_table(table_name, dynamodb):
    try:
        dynamodb.delete_table(TableName=table_name)
        logging.info(f"DynamoDB table '{table_name}' deleted.")
    except Exception as e:
        logging.error(f"Failed to delete DynamoDB table: {e}")

# ==== Main CLI Logic ====
def main():
    parser = argparse.ArgumentParser(description="Terraform S3 + DynamoDB backend setup script")
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--bucket', required=True, help='Name of the S3 bucket to create')
    parser.add_argument('--table', required=True, help='Name of the DynamoDB table to create')
    parser.add_argument('--delete', action='store_true', help='Delete existing resources instead of creating')

    args = parser.parse_args()
    s3, dynamodb = get_clients(args.region)

    if args.delete:
        logging.info(" Deletion mode enabled.")
        delete_dynamodb_table(args.table, dynamodb)
        delete_s3_bucket(args.bucket, s3)
    else:
        logging.info(" Creating Terraform backend infrastructure...")
        create_s3_bucket(args.bucket, args.region, s3)
        create_dynamodb_table(args.table, dynamodb)

    logging.info(" Operation complete.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)