import boto3
from dotenv import load_dotenv
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

def save_photo_to_s3(file):
    bucket_name = os.getenv("S3_BUCKET_NAME")
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file.filename)
        return f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{file.filename}"
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None