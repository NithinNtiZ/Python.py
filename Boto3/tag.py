import boto3
import json

# Replace with your desired VPC settings
region = 'ap-east-1'

# Create a Boto3 client for EC2
ec2 = boto3.client('ec2', region_name=region)

# Get a list of all AWS regions
ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Loop through each region
for region in ec2_regions:
    ec2 = boto3.client('ec2', region_name=region)
    describe = ec2.describe_instances()
    instance_ids = []
    for reservation in describe['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # Print the list of instance IDs
    print(f"Instance IDs in {region}:")
    print("\n")
    for instance_id in instance_ids:
        print(instance_id)
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': 'test',
                    'Value': "test"
                },
            ]
        )
