#!/bin/bash

# Assigning Variables

LOCAL_FILE="$1"
BUCKET="$2"
EXP_TIME="$3"

# Uploading a local file image to a private s3 bucket 
aws s3 cp "$LOCAL_FILE" s3://"$BUCKET"/

# Presigning a URL to that file with an expiration of 604800 (7 days)
aws s3 presign --expires-in "$EXP_TIME" s3://"$BUCKET"/"$LOCAL_FILE"


