import boto3

regions_list = [
    "af-south-1",
    "ap-south-1",
    "eu-north-1",
    "eu-west-3",
    "eu-south-1",
    "eu-west-2",
    "eu-west-1",
    "ap-northeast-3",
    "ap-northeast-2",
    "me-south-1",
    "ap-northeast-1",
    "ca-central-1",
    "sa-east-1",
    "ap-east-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "eu-central-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

# Print the list of regions
print("List of AWS Regions:")
print("\n")
for i, region in enumerate(regions_list, 1):
    print(f"#>>> {region}")

# Prompt the user to input a region
while True:
    user_input = input("Enter a region from the list: ")
    if user_input in regions_list:
        region = user_input
        print(f"you selected {region}")
        break
    else:
        print("Invalid input. Please enter a region from the list.")

# Replace with your desired VPC settings
vpc_cidr_block = '10.0.0.0/16'
vpc_name = 'sup-vpc-nithin-01112023-01'
# regions = 'ap-east-1'

# Create a Boto3 client for EC2
ec2 = boto3.client('ec2', region_name=region)

# Create a VPC

vpc = ec2.create_vpc(
    CidrBlock=vpc_cidr_block
)
vpc_id = vpc['Vpc']['VpcId']
print(f'VPC {vpc_name} created with ID {vpc_id}')

# Add a Name tag to the VPC
ec2.create_tags(
    Resources=[vpc_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': vpc_name
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)

# Define subnet settings for the public subnet
subnet_cidr_block_public = '10.0.1.0/24'
subnet_availability_zone_public = 'ap-east-1a'

# Create the public subnet
subnet_public = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock=subnet_cidr_block_public,
    AvailabilityZone=subnet_availability_zone_public
)
subnet_pub_id = subnet_public['Subnet']['SubnetId']
ec2.create_tags(
    Resources=[subnet_pub_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': "sup-public-subnet-nithin-01112023-01"
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)
print(f'Public Subnet created with ID {subnet_pub_id}')

# # Define subnet settings for the private subnet
# subnet_cidr_block_private = '10.0.2.0/24'

# # Create the private subnet
# subnet_private = ec2.create_subnet(
#     VpcId=vpc_id,
#     CidrBlock=subnet_cidr_block_private,
#     AvailabilityZone=subnet_availability_zone_public
# )

# print(f'Private Subnet created with ID {subnet_private["Subnet"]["SubnetId"]}')

# Create an internet gateway
internet_gateway = ec2.create_internet_gateway()

IG_id = internet_gateway['InternetGateway']['InternetGatewayId']
ec2.create_tags(
    Resources=[IG_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': "sup-IG-nithin-01112023-01"
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)

# Attach the internet gateway to the VPC
ec2.attach_internet_gateway(
    InternetGatewayId=IG_id,
    VpcId=vpc_id
)

print(f'Internet gateway created with ID {IG_id} and attached to the VPC')

# Create a route table
route_table = ec2.create_route_table(
    VpcId=vpc_id
)

RT_id = route_table['RouteTable']['RouteTableId']

print(f'Route table created with ID {RT_id}')

# Create a route for the public subnet
ec2.create_route(
    RouteTableId=RT_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=IG_id
)
ec2.create_tags(
    Resources=[RT_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': "sup-RT-nithin-01112023-01"
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)


print('Route added to the route table for the internet gateway')

# Associate the public subnet with the route table
ec2.associate_route_table(
    RouteTableId=RT_id,
    SubnetId=subnet_pub_id
)

print('Public subnet associated with the route table')

# Associate the private subnet with the route table
# Here, we don't associate the private subnet with the internet gateway, keeping it private
# ec2.associate_route_table(
#     RouteTableId=RT_id,
#     SubnetId=subnet_private['Subnet']['SubnetId']
# )

# print('Private subnet associated with the route table')

# Add tags to the subnets


# ec2.create_tags(
#     Resources=[subnet_private['Subnet']['SubnetId']],
#     Tags=[
#         {
#             'Key': 'Name',
#             'Value': "sup-subnet-nithin-private"
#         },
#         {
#             'Key': 'CreatedOn',
#             'Value': "1-11-2023"
#         }
#     ]
# )

# Security group configuration
sg = ec2.create_security_group(
    Description='sup-sg-nithin-01112023-01',
    GroupName='sup-sg-nithin-01112023-01',
    VpcId = vpc_id
)

security_group_id = sg['GroupId']

# Add a rule to the security group to allow inbound SSH traffic
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {'IpProtocol': 'tcp',
         'FromPort': 22,
         'ToPort': 22,
         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ]
)

ec2.create_tags(
    Resources=[sg['GroupId']],
    Tags=[
        {
            'Key': 'Name',
            'Value': "sup-SG-nithin-01112023-01"
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)
print(f"Security group created with ID: {security_group_id}")

# Create Key-pair 
kp = ec2.create_key_pair(
    KeyName='sup-keypair-nithin-01112023-01',
    KeyType='rsa'
)

kp_id = kp['KeyPairId'] 

print(f"KeyPair created with ID: {kp_id}")


# # Create a network interface
# network_interface = ec2.create_network_interface(
#     SubnetId=subnet_pub_id,
#     Description='sup-NI-nithin-01112023',
#     Groups=[security_group_id],  # Replace with your security group ID
#     # PrivateIpAddress='10.0.1.5'  # Replace with your desired private IP address
# )

# network_interface_id = network_interface['NetworkInterface']['NetworkInterfaceId']
# ec2.create_tags(
#     Resources=[network_interface_id],
#     Tags=[
#         {
#             'Key': 'Name',
#             'Value': "sup-NI-nithin-01112023-01"
#         },
#         {
#             'Key': 'CreatedOn',
#             'Value': "1-11-2023"
#         }
#     ]
# )
# print(f'Network interface created with ID {network_interface_id}')

# Create Ec2 instance
instance_params = {
    'ImageId': 'ami-0f234f3f104500fdd',
    'InstanceType': 't3.micro',
    'KeyName': 'sup-keypair-nithin-01112023-01',
    'MinCount': 1,
    'MaxCount': 1,
    'InstanceInitiatedShutdownBehavior': 'stop',  # Stop the instance when it's terminated
    'NetworkInterfaces': [{
        'DeviceIndex': 0,
        'Description': 'sup-NI-nithin-01112023-01',
        'Groups': [security_group_id],
        'DeleteOnTermination': True,
        'SubnetId': subnet_pub_id,
        'AssociatePublicIpAddress': True,
    }]
}


instance = ec2.run_instances(**instance_params)
instance_id = instance['Instances'][0]['InstanceId']
ec2.create_tags(
    Resources=[instance_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': "sup-Ec2-nithin-01112023-01"
        },
        {
            'Key': 'CreatedOn',
            'Value': "1-11-2023"
        }
    ]
)

print(f'Ec2 instance ID:{instance_id}')
