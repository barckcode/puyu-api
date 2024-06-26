from fastapi import HTTPException
from services.aws.clients import AwsClients
from schemas.aws.services.network import VpcCreateAwsSchema, VpcCreateDbSchema, SubnetCreateAwsSchema, SubnetCreateDbSchema


def create_vpc(vpc: VpcCreateAwsSchema):
    aws_clients = AwsClients(vpc.region_cloud_id)
    ec2_client = aws_clients.ec2_client()

    try:
        vpc_response = ec2_client.create_vpc(CidrBlock=vpc.cidr_block)
        vpc_id = vpc_response['Vpc']['VpcId']

        # Wait for the VPC to be available
        ec2_client.get_waiter('vpc_available').wait(VpcIds=[vpc_id])

        # Assign a name to the VPC using a tag
        ec2_client.create_tags(
            Resources=[vpc_id],
            Tags=[{'Key': 'Name', 'Value': vpc.name}]
        )

        # Internet Gateway
        igw_response = ec2_client.create_internet_gateway()
        igw_id = igw_response['InternetGateway']['InternetGatewayId']

        ec2_client.create_tags(
            Resources=[igw_id],
            Tags=[{'Key': 'Name', 'Value': vpc.name}]
        )
        ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

        # Route Table
        route_tables = ec2_client.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        route_table_id = route_tables['RouteTables'][0]['RouteTableId']

        ec2_client.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id
        )

        return VpcCreateDbSchema(
            name=vpc.name,
            aws_resource_id=vpc_id,
            cidr_block=vpc.cidr_block,
            region_cloud_id=vpc.region_cloud_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating VPC on AWS: {e}")


def create_subnet(subnet: SubnetCreateAwsSchema):
    aws_clients = AwsClients(subnet.region_cloud_id)
    ec2_client = aws_clients.ec2_client()

    try:
        subnet_response = ec2_client.create_subnet(
            VpcId=subnet.aws_vpc_id,
            CidrBlock=subnet.cidr_block,
            AvailabilityZone=subnet.availability_zone
        )
        subnet_id = subnet_response['Subnet']['SubnetId']

        ec2_client.get_waiter('subnet_available').wait(SubnetIds=[subnet_id])

        ec2_client.create_tags(
            Resources=[subnet_id],
            Tags=[{'Key': 'Name', 'Value': subnet.name}]
        )
        return SubnetCreateDbSchema(
            name=subnet.name,
            aws_resource_id=subnet_id,
            cidr_block=subnet.cidr_block,
            aws_vpc_id=subnet.aws_vpc_id,
            availability_zone=subnet.availability_zone,
            region_cloud_id=subnet.region_cloud_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating subnet on AWS: {e}")
