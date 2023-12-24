import subprocess
import datetime
import boto3
import argparse
import os

def update_security_group_rule(security_group_id):
    """
    Update the specified security group to allow SSH access from the current public IP address.

    This function performs the following steps:
    1. Fetches the current public IP address.
    2. Formats the IP address in CIDR notation.
    3. Checks the existing rules in the specified security group.
    4. Removes any existing rule that allows SSH access.
    5. Adds a new rule to allow SSH access from the current IP address.

    Args:
    security_group_id (str): The ID of the AWS security group to update.

    Returns:
    None
    """
    # Use 'dig' command to get the current public IP address
    try:
        my_ip = subprocess.check_output(
            ["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
            encoding='utf-8'
        ).strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to obtain public IP address: {e}")
        return

    cidr_ip = f"{my_ip}/32"

    # Create a Boto3 client for EC2
    ec2 = boto3.client('ec2')

    try:
        # Describe the security group
        sg = ec2.describe_security_groups(GroupIds=[security_group_id])['SecurityGroups'][0]

        # Find and remove the existing rule for SSH (port 22)
        for permission in sg['IpPermissions']:
            if permission['FromPort'] == 22 and permission['ToPort'] == 22 and permission['IpProtocol'] == 'tcp':
                ec2.revoke_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[permission]
                )

        # Add a new rule to the security group
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            CidrIp=cidr_ip
        )
        print(f"{datetime.datetime.now()} - Successfully updated rule in {security_group_id} allowing SSH access from {cidr_ip}")
    except Exception as e:
        print(f"{datetime.datetime.now()} - An error occurred: {e}")

def main():
    """
    Main function to process the command line arguments and update the security group.

    This function uses argparse to parse command line arguments for the AWS profile
    and the security group ID. It then sets the AWS profile and calls the
    update_security_group_rule function with the security group ID.

    Command Line Args:
    --aws_profile (str): The AWS profile to use for the session.
    --security_group_id (str): The ID of the AWS security group to update.

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description='Update Security Group to allow SSH from current IP.')
    parser.add_argument('--aws_profile', type=str, required=True, help='AWS profile to use')
    parser.add_argument('--security_group_id', type=str, required=True, help='Security Group ID to be updated')
    args = parser.parse_args()
    os.environ['AWS_PROFILE'] = args.aws_profile

    # Update the security group rule
    update_security_group_rule(args.security_group_id)

if __name__ == "__main__":
    main()
