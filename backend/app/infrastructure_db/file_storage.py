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

def save_photo_to_s3(file):
    # Get the bucket name inside the function to ensure it's fresh
    bucket = os.getenv("S3_BUCKET_NAME")
    
    if not bucket:
        print("S3 Error: S3_BUCKET_NAME environment variable is missing!")
        return None

    try:
        # Seek to the start of the file to ensure we read from the beginning
        file.file.seek(0)
        
        s3_client.upload_fileobj(
            file.file, 
            bucket, 
            file.filename,
            ExtraArgs={"ContentType": file.content_type} # Helps browser view image
        )
        return f"https://{bucket}.s3.ap-south-1.amazonaws.com/{file.filename}"
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None

def delete_photo_from_s3(photo_url: str):
    # Deletes a file from S3 given its full URL
    try:
        bucket_name = os.getenv("S3_BUCKET_NAME")
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