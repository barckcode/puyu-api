import boto3
import os
import pytz
import re
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta


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
        {'Name': 'architecture', 'Values': [f'{architecture}']},
        {'Name': 'state', 'Values': ['available']}
    ]

    try:
        response = ec2.describe_images(Filters=filters)
        images = response['Images']
        one_year_later = datetime.now(pytz.utc) + timedelta(days=1*365)
        filtered_images = [
            {
                "Architecture": image["Architecture"],
                "CreationDate": image["CreationDate"],
                "ImageId": image["ImageId"],
                "UsageOperation": image["UsageOperation"],
                "State": image["State"],
                "Description": image.get("Description", "No description available"),
                "DeprecationTime": image.get("DeprecationTime", "Not deprecated")
            } for image in images
            if datetime.fromisoformat(image.get("DeprecationTime", "9999-12-31T23:59:59.000Z").replace('Z', '+00:00')) > one_year_later
            and re.search(r'Debian (10|11|12)(?!.*backports)', image.get("Description", ""))
        ]

        latest_images = {}
        for image in filtered_images:
            version_match = re.search(r'Debian (10|11|12)', image["Description"])
            if version_match:
                version = version_match.group(0)
                if version not in latest_images or datetime.fromisoformat(latest_images[version]["CreationDate"]) < datetime.fromisoformat(image["CreationDate"]):
                    latest_images[version] = image

        return list(latest_images.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
