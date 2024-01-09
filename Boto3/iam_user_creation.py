import boto3

#  User creation with custom made policies 

# Replace with your desired VPC settings
region = 'ap-east-1'

# Create a Boto3 client for IAM
iam = boto3.client('iam', region_name=region)

def user_creation_with_policy(user_name):
    CreateBy = input('Enter value for CreateBy: ')
    CreatedOn = input('Enter value for CreatedOn: ')
    Team = input('Enter value for Team: ')
    ApprovedBy = input('Enter value for ApprovedBy: ')

    policy_arn = "arn:aws:iam::123456789:policy/test-policy"
    tags = [
        {'Key': 'CreatedBy', 'Value': CreateBy},
        {'Key': 'CreatedOn', 'Value': CreatedOn},
        {'Key': 'Team', 'Value': Team},
        {'Key': 'ApprovedBy', 'Value': ApprovedBy}
    ]

    # Create a user
    iam.create_user(UserName=user_name, Tags=tags)
    print(f"User {user_name} created successfully with the tags.")

    # Attach a policy to the user
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    print(f"Policy {policy_arn} attached to the user {user_name} successfully.")


    # Set password for the user
    password = "Admin@123"  # Replace with your desired password
    try:
        iam.create_login_profile(UserName=user_name, Password=password, PasswordResetRequired=True)
        print(f"Password set for user {user_name}.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Login profile already exists for user {user_name}.")

if __name__ == "__main__":
    xnumerofuser = int(input("Enter how many users to create: "))
    for i in range(xnumerofuser):
        user_name = input("Enter user name: ")
        user_creation_with_policy(user_name)
