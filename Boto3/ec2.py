import boto3

# Replace with your desired VPC settings
region = 'ap-east-1'

# Create a Boto3 client for EC2
ec2 = boto3.client("ec2", region_name=region)

# ... (Previous code remains the same) ...

instance_params = {
    'ImageId': 'ami-0f234f3f104500fdd',
    'InstanceType': 't3.micro',
    'KeyName': 'sup-keypair-nithin',
    'MinCount': 1,
    'MaxCount': 1,
    'InstanceInitiatedShutdownBehavior': 'stop',  # Stop the instance when it's terminated
    'NetworkInterfaces': [{
        'DeviceIndex': 0,
        'Groups': ['sg-0eda58fb73eb77960'],
        'DeleteOnTermination': True,
        'SubnetId': 'subnet-0bc5ad9cc648d2d29',
        'AssociatePublicIpAddress': True,
    }]
}

# Create the instance
instance = ec2.run_instances(**instance_params)

# Print the response
print(instance['Instances'][0]['InstanceId'])
