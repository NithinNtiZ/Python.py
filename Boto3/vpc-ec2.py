# More Organized and Optimized code of vpc.py

import boto3

# Replace with your desired VPC settings
vpc_cidr_block = '10.0.0.0/16'
vpc_name = 'sup-vpc-nithin-01112023-01'
region = 'ap-east-1'

ec2 = boto3.client('ec2', region_name=region)

def create_vpc(ec2, vpc_cidr_block, vpc_name):
    vpc = ec2.create_vpc(CidrBlock=vpc_cidr_block)
    vpc_id = vpc['Vpc']['VpcId']
    print(f'VPC {vpc_name} created with ID {vpc_id}')
    return vpc_id

def add_name_tag(ec2, resource_id, resource_name):
    ec2.create_tags(Resources=[resource_id], Tags=[{'Key': 'Name', 'Value': resource_name}, {'Key': 'CreatedOn', 'Value': "1-11-2023"}])

vpc_id = create_vpc(ec2, vpc_cidr_block, vpc_name)
add_name_tag(ec2, vpc_id, vpc_name)

# Define subnet settings for the public subnet
subnet_cidr_block_public = '10.0.1.0/24'
subnet_availability_zone_public = 'ap-east-1a'

def create_subnet(ec2, vpc_id, subnet_cidr_block, subnet_availability_zone, subnet_name):
    subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock=subnet_cidr_block, AvailabilityZone=subnet_availability_zone)
    subnet_id = subnet['Subnet']['SubnetId']
    print(f'{subnet_name} created with ID {subnet_id}')
    return subnet_id

subnet_pub_id = create_subnet(ec2, vpc_id, subnet_cidr_block_public, subnet_availability_zone_public, 'Public Subnet')
add_name_tag(ec2, subnet_pub_id, 'sup-public-subnet-nithin')

# Internet gateway configuration
internet_gateway = ec2.create_internet_gateway()
IG_id = internet_gateway['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=IG_id, VpcId=vpc_id)
print(f'Internet gateway created with ID {IG_id} and attached to the VPC')
add_name_tag(ec2, IG_id, 'sup-IG-nithin')

# Route table configuration
route_table = ec2.create_route_table(VpcId=vpc_id)
RT_id = route_table['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=RT_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=IG_id)
print(f'Route table created with ID {RT_id}')
add_name_tag(ec2, RT_id, 'sup-RT-nithin')

# Associate Route Table
ec2.associate_route_table(RouteTableId=RT_id,SubnetId=subnet_pub_id)

# Security group configuration
security_group = ec2.create_security_group(Description='sup-sg-nithin', GroupName='sup-sg-nithin', VpcId=vpc_id)
security_group_id = security_group['GroupId']
ec2.authorize_security_group_ingress(GroupId=security_group_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
add_name_tag(ec2, security_group_id, 'sup-SG-nithin')
print(f'Security group created with ID: {security_group_id}')

# Key-pair configuration
key_pair = ec2.create_key_pair(KeyName='sup-keypair-nithin', KeyType='rsa')
kp_id = key_pair['KeyPairId']
print(f'KeyPair created with ID: {kp_id}')

# Network interface configuration
network_interface = ec2.create_network_interface(SubnetId=subnet_pub_id, Description='sup-NI-nithin-01112023', Groups=[security_group_id])
network_interface_id = network_interface['NetworkInterface']['NetworkInterfaceId']
print(f'Network interface created with ID {network_interface_id}')

# EC2 instance configuration
instance_params = {
    'ImageId': 'ami-0f234f3f104500fdd',
    'InstanceType': 't3.micro',
    'KeyName': 'sup-keypair-nithin',
    'MinCount': 1,
    'MaxCount': 1,
    'InstanceInitiatedShutdownBehavior': 'stop',
    'NetworkInterfaces': [{
        'DeviceIndex': 0,
        'Groups': [security_group_id],
        'DeleteOnTermination': True,
        'SubnetId': subnet_pub_id,
        'AssociatePublicIpAddress': True,
    }]
}

instance = ec2.run_instances(**instance_params)
instance_id = instance['Instances'][0]['InstanceId']
add_name_tag(ec2, instance_id, 'sup-Ec2-nithin-01112023-01')
print(f'Ec2 instance ID:{instance_id}')
