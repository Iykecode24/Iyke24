import boto3
from botocore.exceptions import ClientError
from app.config import settings
import uuid

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto',
        )
        self.bucket_name = settings.R2_BUCKET_NAME

    def upload_audio(self, audio_bytes: bytes, filename: str = None) -> str:
        if not filename:
            filename = f"audio/{uuid.uuid4()}.mp3"
            
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=audio_bytes,
                ContentType='audio/mpeg'
            )
            # Assuming public access or generating presigned url
            # For simplicity, returning the structured URL
            return f"{settings.R2_ENDPOINT_URL}/{self.bucket_name}/{filename}"
        except ClientError as e:
            print(f"Error uploading to R2: {e}")
            raise e
