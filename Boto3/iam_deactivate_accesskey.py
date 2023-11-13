import boto3
from datetime import datetime, timezone

# Replace with your desired AWS region
region = 'ap-east-1'

# Create a Boto3 client for IAM
iam = boto3.client("iam", region_name=region)

# List all IAM users
response = iam.list_users()

for user in response['Users']:
    username = user['UserName']
    
    # List access keys for the user
    access_keys = iam.list_access_keys(UserName=username)
    
    for access_key_metadata in access_keys['AccessKeyMetadata']:
        name_key = access_key_metadata['UserName']
        access = access_key_metadata['AccessKeyId']
        create_date = access_key_metadata['CreateDate'].replace(tzinfo=timezone.utc)

        # Calculate the difference in days
        days_difference = (datetime.now(timezone.utc) - create_date).days

        print(f"{name_key}:{access} : {days_difference}")

        # # Deactivate keys older than 31 days
        # if days_difference > 31:
        #     iam.update_access_key(AccessKeyId=access, Status='Inactive')
