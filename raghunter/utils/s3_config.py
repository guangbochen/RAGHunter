import os
from sys import prefix
import boto3

from dotenv import load_dotenv
from typing import Optional, Tuple, List
from botocore.exceptions import BotoCoreError, ClientError
from botocore.config import Config
from boto3.s3.transfer import TransferConfig, S3Transfer

class S3Config:
    """S3 configuration handler for managing S3 credentials and validation."""

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        region: str = 'us-east-1',
        bucket: Optional[str] = None
    ):
        load_dotenv()
        self.endpoint_url = endpoint_url or os.getenv('S3_ENDPOINT_URL')
        self.access_key_id = access_key_id or os.getenv('S3_ACCESS_KEY_ID')
        self.secret_access_key = secret_access_key or os.getenv('S3_SECRET_ACCESS_KEY')
        self.region = region or os.getenv('S3_REGION', 'us-east-1')
        self.bucket = bucket or os.getenv('S3_BUCKET_NAME')

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate that all required configuration values are set."""
        if not self.endpoint_url:
            return False, 'Missing S3_ENDPOINT_URL'
        if not self.access_key_id:
            return False, 'Missing S3_ACCESS_KEY_ID'
        if not self.secret_access_key:
            return False, 'Missing S3_SECRET_ACCESS_KEY'
        if not self.bucket:
            return False, 'Missing S3_BUCKET_NAME'
        return True, None

    def get_client(self):
        """Create and return a boto3 S3 client instance."""
        return boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=Config(
                retries={'max_attempts': 3, 'mode': 'standard'}, 
                s3={'addressing_style': 'virtual'}
                )
        )

    def get_file(self, file_key: str, download_path: str) -> None:
        """Download a file from the S3 bucket with progress tracking."""
        client = self.get_client()
        config = TransferConfig(use_threads=False)
        transfer = S3Transfer(client, config)
        try:
            transfer.download_file(self.bucket, file_key, download_path, callback=ProgressPercentage(download_path))
        except (ClientError, BotoCoreError) as e:
            raise RuntimeError(f"Failed to download {file_key} from bucket {self.bucket}: {e}")

    def upload_file(self, file_path: str, file_key: str) -> None:
        """Upload a file to the S3 bucket."""
        client = self.get_client()
        try:
            client.upload_file(file_path, self.bucket, file_key)
        except (ClientError, BotoCoreError) as e:
            raise RuntimeError(f"Failed to upload {file_path} to bucket {self.bucket} as {file_key}: {e}")

    def list_files(self, path: str) -> List[str]:
        """List all files in the S3 bucket."""
        client = self.get_client()
        try:
            response = client.list_objects_v2(Bucket=self.bucket, Prefix=path)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except (ClientError, BotoCoreError) as e:
            raise RuntimeError(f"Failed to list files in bucket {self.bucket}: {e}")

    def sync_to_local(self, prefix: str, local_dir: str):
        """
        Mirror all objects under s3://{bucket_name}/{prefix} to local_dir.
        Only downloads new or changed objects (by size & ETag).
        """
        client = self.get_client()
        paginator = client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix=prefix)

        for page in page_iterator:
            for obj in page.get('Contents', []):
                key = obj['Key']
                print(f"Found key: {key}")
                # Compute relative path and local path
                rel_path = os.path.relpath(key, prefix)
                local_path = os.path.join(local_dir, rel_path)

                # Skip “directory” keys
                if key.endswith('/'):
                    continue

                # Ensure local directory exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # Determine whether to download
                download = True
                if os.path.exists(local_path):
                    local_size = os.path.getsize(local_path)
                    s3_size = obj['Size']
                    # Compare sizes (or fetch ETag via head_object for checksum)
                    if local_size == s3_size:
                        download = False

                if download:
                    print(f"Downloading s3://{self.bucket}/{key} → {local_path}")
                    client.download_file(self.bucket, key, local_path)