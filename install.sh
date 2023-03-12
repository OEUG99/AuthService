#!/bin/bash

echo $AWS_REGION

# creating defaults for AWS
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY



# Install Python packages from requirements.txt
pip install -r requirements.txt


