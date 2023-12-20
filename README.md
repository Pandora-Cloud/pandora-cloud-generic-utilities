# Pandora Cloud Generic Utilities

Welcome to the Pandora Cloud Generic Utilities repository. This repository contains a collection of miscellaneous tools and scripts designed to enhance and simplify various cloud-related operations. Each utility in this repository serves a specific purpose, making it easier to manage and automate tasks in cloud environments.

## Utilities

### AWS Security Group SSH Access Updater (`aws_security_group_ssh_access_updater.py`)

The `aws_security_group_ssh_access_updater.py` script is a Python utility designed to update an AWS Security Group to allow SSH access from the user's current public IP address. This is particularly useful for dynamically updating security groups to ensure secure and temporary SSH access to AWS resources.

#### Features

- Automatically fetches the user's current public IP address.
- Updates the specified AWS Security Group to allow SSH access from this IP address.
- Removes any existing SSH (port 22) access rules from the security group before adding the new rule.

#### Prerequisites

- Python 3.x
- AWS CLI configured with the necessary AWS credentials and permissions.
- `boto3` (AWS SDK for Python).

#### Usage

Run the script with the security group ID as an argument. Optionally, set the `AWS_PROFILE` environment variable to use a specific AWS profile:

```bash
export AWS_PROFILE=myawsprofile  # Optional: Set this if using a specific AWS profile
python aws_security_group_ssh_access_updater.py --security_group_id [security-group-id] --aws_profile [aws-profile-name]
```

Replace [security-group-id] with the actual ID of the AWS security group you wish to update.
Replace [aws-profile-name] with the name of the AWS Profile with permission to perform the update.


#### Scheduling with Cron

To ensure your SSH access is always up-to-date with your current IP address, you can schedule the `aws_security_group_ssh_access_updater.py` script to run automatically at regular intervals using `cron`. This is especially useful if your public IP changes frequently.

##### Steps to Schedule the Script:

1. **Add a cron job:**

    You can edit the crontab for the current user using the following command:

    ```bash
    crontab -e
    0 7 * * * /usr/bin/python3 /path/to/aws_security_group_ssh_access_updater.py --security_group_id [security-group-id] --aws_profile [aws-profile-name] >> /path/to/logfile.log 2>&1
    ```
