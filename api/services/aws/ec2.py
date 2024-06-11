import time
from fastapi import HTTPException
from clients import AwsClients


def create_key_pair(region: str, key_name: str):
    aws_clients = AwsClients(region)
    ec2_client = aws_clients.ec2_client()
    s3_client = aws_clients.s3_client()
    try:
        key_pair = ec2_client.create_key_pair(KeyName=key_name, KeyType="ed25519")
        private_key = key_pair['KeyMaterial']

        s3_client.put_object(Bucket=aws_clients.aws_s3_bucket, Key=f'{key_name}.pem', Body=private_key)
        return f"Key pair {key_name} created successfully. Private key saved to S3 bucket: {aws_clients.aws_s3_bucket}."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating key pair: {e}")


def create_instance(region: str, ami_id:str, name: str, key_name: str, instance_type: str, subnet_id: str, disk_size: int):
    aws_clients = AwsClients(region)
    ec2_client = aws_clients.ec2_client()
    try:
        instance = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MaxCount=1,
            MinCount=1,
            NetworkInterfaces=[
                {
                    'DeviceIndex': 0,
                    'SubnetId': subnet_id,
                    'AssociatePublicIpAddress': True,
                    'Groups': [], # TODO: Add security group
                }
            ],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'VolumeSize': disk_size,
                        'VolumeType': 'gp3'
                    }
                }
            ],
            TagSpecifications=[
                {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': name}]}
            ]
        )

        instance_id = instance['Instances'][0]['InstanceId']
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

        # Wait for the public IP to be available
        while True:
            instance_description = ec2_client.describe_instances(InstanceIds=[instance_id])
            public_ip = instance_description['Reservations'][0]['Instances'][0].get('PublicIpAddress')
            if public_ip:
                break
            time.sleep(5)  # Wait 5 seconds before checking again

        return f"Instance created successfully with ID: {instance_id} and IP: {public_ip}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating instance: {e}")


# Example usage:
# create_key_pair("eu-west-1", "puyu-key")
# create_instance("eu-west-1", "ami-03820227fb3e4ffad", "puyu", "puyu-key", "t4g.small", "subnet-00178a16532fb96bb", 50)
