import requests
import os
import boto3
import logging
from botocore.exceptions import ClientError

# create client
s3 = boto3.client('s3', region_name="us-east-1")

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

def upload_file(bucket_name, file_name, make_public=False):
    """Upload a file to an S3 bucket with private or public access."""
    try:
        with open(file_name, "rb") as data:
            s3.put_object(
		Body=data,
                Bucket=bucket_name,
                Key=file_name,
                ACL='public-read' if make_public else 'private'  # Make public if specified
            )
        print(f"File uploaded to S3: s3://{bucket_name}/{file_name}")
        if make_public:
            print(f"Public URL: https://s3.amazonaws.com/{bucket_name}/{file_name}/")
        else:
            print("File is private. Access is restricted.")
    except Exception as e:
        print(f"Upload failed: {e}")
        exit(1)

def create_presigned_url(bucket_name, object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


# Take user input for URL and file name
image_url = input("Enter the image URL: ")
file_name = input("Enter the file name to save as: ")
make_public = input("Make file public? (yes/no): ").strip().lower() == "yes"

# Save file to the current directory
file_path = os.path.join(os.getcwd(), file_name)
print(file_path)

# Bucket name
bucket_name = input("Enter the s3 bucket name: ")
 

# Download file
download_file(image_url, file_path)

# Upload file
upload_file(bucket_name, file_name, make_public)
 
# Presigned URLs
if upload_file:
    expiration = int(input("Enter expiration time for the presigned URL in seconds (default 3600): ") or 3600)
    presigned_url = create_presigned_url(bucket_name, file_name, expiration)
    
    if presigned_url:
        print(f"Presigned URL (valid for {expiration} seconds):\n{presigned_url}")
    else:
        print("Failed to generate presigned URL.") 
