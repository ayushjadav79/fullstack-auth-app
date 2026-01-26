import boto3
import uuid
from botocore.exceptions import NoCredentialsError

# Use S3 Bucket name
BUCKET_NAME = 'user-images-ayush'

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='ap-south-1' # Mumbai Region
)

def save_photo_to_s3(file):
    # Uploads the profile photo to S3 instead of saving it locally.
    try:
        # Generate a unique filename using UUID
        extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"

        # Upload to S3
        s3_client.upload_fileobj(
            file.file, 
            BUCKET_NAME, 
            unique_filename,
            ExtraArgs={'ContentType': file.content_type}
        )

        # Construct the public URL
        # Once uploaded, the URL will be: https://bucket-name.s3.region.amazonaws.com/filename
        return f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{unique_filename}"

    except NoCredentialsError:
        print("AWS Credentials not found")
        return None