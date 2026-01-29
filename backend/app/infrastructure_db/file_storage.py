import boto3
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

# Load environment variables
load_dotenv()

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name='ap-south-1' # Mumbai Region
)

bucket_name = os.getenv("S3_BUCKET_NAME")

def save_photo_to_s3(file):
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file.filename)
        return f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{file.filename}"
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None

def delete_photo_from_s3(photo_url: str):
    # Deletes a file from S3 given its full URL
    try:
        # 1. Extract the filename (key) from the URL
        parsed_url = urlparse(photo_url)
        file_key = parsed_url.path.lstrip('/')

        # 2. Initialize the S3 client and delete
        s3 = boto3.client('s3')
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        print(f"Failed to delete S3 object: {e}")
        return False