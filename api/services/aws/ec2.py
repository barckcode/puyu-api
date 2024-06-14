import time
from fastapi import HTTPException
from services.aws.clients import AwsClients
from schemas.aws.services.ec2 import KeyPairCreateSchema, SecurityGroupCreateAwsSchema, SecurityGroupCreateDbSchema, SecurityGroupRuleCreateAwsSchema, SecurityGroupRuleCreateDbSchema, InstanceCreateAwsSchema, InstanceCreateDbSchema


def create_key_pair(key_pair: KeyPairCreateSchema):
    aws_clients = AwsClients(key_pair.region_cloud_id)
    ec2_client = aws_clients.ec2_client()
    s3_client = aws_clients.s3_client()
    try:
        aws_key_pair = ec2_client.create_key_pair(KeyName=key_pair.name, KeyType="ed25519")
        private_key = aws_key_pair['KeyMaterial']

        s3_client.put_object(Bucket=aws_clients.aws_s3_bucket, Key=f'{key_pair.name}.pem', Body=private_key)
        return KeyPairCreateSchema(
            name=key_pair.name,
            region_cloud_id=key_pair.region_cloud_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating key pair on AWS: {e}")


def create_security_group(security_group: SecurityGroupCreateAwsSchema):
    aws_clients = AwsClients(security_group.region_cloud_id)
    ec2_client = aws_clients.ec2_client()
    try:
        aws_security_group = ec2_client.create_security_group(
            GroupName=security_group.name,
            Description=security_group.description,
            VpcId=security_group.aws_vpc_id
        )

        ec2_client.create_tags(
            Resources=[aws_security_group['GroupId']],
            Tags=[{'Key': 'Name', 'Value': security_group.name}]
        )
        return SecurityGroupCreateDbSchema(
            name=security_group.name,
            aws_resource_id=aws_security_group['GroupId'],
            aws_vpc_id=security_group.aws_vpc_id,
            region_cloud_id=security_group.region_cloud_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating security group on AWS: {e}")


def create_security_group_rule(security_group_rule: SecurityGroupRuleCreateAwsSchema):
    aws_clients = AwsClients(security_group_rule.region_cloud_id)
    ec2_client = aws_clients.ec2_client()
    rule = {
        "IpPermissions": [
            {
                "IpProtocol": security_group_rule.protocol,
                "FromPort": security_group_rule.port,
                "ToPort": security_group_rule.port,
                "IpRanges": [
                    {
                        "CidrIp": security_group_rule.cird_ip
                    }
                ]
            }
        ]
    }
    try:
        if security_group_rule.type == "ingress":
            rule = ec2_client.authorize_security_group_ingress(
                GroupId=security_group_rule.aws_security_group_id,
                IpPermissions=rule['IpPermissions']
            )
        elif security_group_rule.type == "egress":
            rule = ec2_client.authorize_security_group_egress(
                GroupId=security_group_rule.aws_security_group_id,
                IpPermissions=rule['IpPermissions']
            )
        else:
            raise HTTPException(status_code=400, detail="Type must be ingress or egress")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating security group rule on AWS: {e}")
    return SecurityGroupRuleCreateDbSchema(
        type=security_group_rule.type,
        aws_resource_id=rule['SecurityGroupRules'][0]['SecurityGroupRuleId'],
        aws_security_group_id=security_group_rule.aws_security_group_id,
        port=security_group_rule.port,
        protocol=security_group_rule.protocol,
        cird_ip=security_group_rule.cird_ip,
        region_cloud_id=security_group_rule.region_cloud_id
    )


def create_instance(instance: InstanceCreateAwsSchema):
    aws_clients = AwsClients(instance.region_cloud_id)
    ec2_client = aws_clients.ec2_client()
    try:
        aws_instance = ec2_client.run_instances(
            ImageId=instance.aws_ami_id,
            InstanceType=instance.instance_type_cloud_id,
            KeyName=instance.key_pair_name,
            MaxCount=1,
            MinCount=1,
            NetworkInterfaces=[
                {
                    'DeviceIndex': 0,
                    'SubnetId': instance.aws_subnet_id,
                    'AssociatePublicIpAddress': True,
                    'Groups': [instance.aws_security_group_id],
                }
            ],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'VolumeSize': instance.disk_size,
                        'VolumeType': 'gp3'
                    }
                }
            ],
            TagSpecifications=[
                {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': instance.name}]}
            ]
        )

        instance_id = aws_instance['Instances'][0]['InstanceId']
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

        # Wait for the public IP to be available
        while True:
            instance_description = ec2_client.describe_instances(InstanceIds=[instance_id])
            public_ip = instance_description['Reservations'][0]['Instances'][0].get('PublicIpAddress')
            private_ip = instance_description['Reservations'][0]['Instances'][0].get('PrivateIpAddress')
            if public_ip:
                break
            time.sleep(5)  # Wait 5 seconds before checking again

        return InstanceCreateDbSchema(
            name=instance.name,
            aws_resource_id=instance_id,
            disk_size=instance.disk_size,
            public_ip=public_ip,
            private_ip=private_ip,
            key_pair_name=instance.key_pair_name,
            instance_type_cloud_id=instance.instance_type_cloud_id,
            aws_ami_id=instance.aws_ami_id,
            aws_subnet_id=instance.aws_subnet_id,
            aws_security_group_id=instance.aws_security_group_id,
            region_cloud_id=instance.region_cloud_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating instance on AWS: {e}")


# Example usage:
# create_key_pair("eu-west-1", "puyu-key")
# create_instance("eu-west-1", "ami-03820227fb3e4ffad", "puyu", "puyu-key", "t4g.small", "subnet-00178a16532fb96bb", 50)
