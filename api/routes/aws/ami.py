from fastapi import APIRouter, HTTPException
import boto3
import os


aws_ami = APIRouter()
aws_region = os.getenv('AWS_DEFAULT_REGION')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


@aws_ami.get(
    "/aws/ami/search",
    tags=["AWS"],
    summary="Search for an AMI",
    description="Search for an AMI by name and architecture"
)
def search_ami(name: str, architecture: str):
    ec2 = boto3.client(
        'ec2',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    filters = [
        # ubuntu, debian, rhel, amazon_linux
        {'Name': 'name', 'Values': [f'*{name}*']},
        # arm64 & x86_64
        {'Name': 'architecture', 'Values': [f'{architecture}']}
    ]

    try:
        response = ec2.describe_images(Filters=filters)
        return response['Images']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
