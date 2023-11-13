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
    user_id = user['UserId']
    

    # Calculate the difference in days
    try: 
        createOn = user['CreateDate'].replace(tzinfo=timezone.utc)
        passwordLastUsed = user['PasswordLastUsed'].replace(tzinfo=timezone.utc)
        days_difference = (datetime.now(timezone.utc) - createOn).days
        days_difference_pass = (datetime.now(timezone.utc) - passwordLastUsed).days
        print(f"{username} >>>> last reset password on  {days_difference_pass} days back")
    except KeyError:
        print(f"{username} >>>> Login details not available")

    # print(f"{username} created on  {days_difference} day back")
    
