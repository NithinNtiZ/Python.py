import boto3

def lambda_handler(event, context):
    # Extract relevant information from the event
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    aws_region = event['detail']['awsRegion']
    event_time = event['detail']['eventTime']
    aws_id = event['detail']['userIdentity']['userName']
    event_name = event['detail']['eventName']

    # Specify the tags you want to add
    tags = [
        {"Key": "Team", "Value": ""},
        {"Key": "CreateBy", "Value": ""},
        {"Key": "Email", "Value": ""},
        {"Key": "AwsID", "Value": aws_id},
        {"Key": "CreatedOn", "Value": event_time},
        {"Key": "LeaseDuration", "Value": ""},
        {"Key": "Environment", "Value": ""},
        {"Key": "Product", "Value": ""},
        {"Key": "Version", "Value": ""},
        {"Key": "Location", "Value": ""},
        {"Key": "Purpose", "Value": ""}
    ]
    if event_name == "RunInstances":
        ec2_client = boto3.client('ec2', region_name=aws_region)

        # Add tags to the specified instance
        ec2_client.create_tags(Resources=[instance_id], Tags=tags)

        return {
            'statusCode': 200,
            'body': f'Tags added successfully to instance {instance_id} in region {aws_region}!'
        }
    else:
        return {
            'statusCode': 200,
            'body': f'No action taken for event {event_name}.'
        }
