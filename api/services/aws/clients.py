import boto3
#from routes.aws.config import aws_access_key_id, aws_secret_access_key, aws_s3_bucket


class AwsClients:
    def __init__(self, region: str):
        self.region = region
        # self.aws_access_key_id = aws_access_key_id
        # self.aws_secret_access_key = aws_secret_access_key
        # self.aws_s3_bucket = aws_s3_bucket
        # Test
        import os
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_s3_bucket = os.getenv("AWS_S3_BUCKET")

    def ec2_client(self):
        return boto3.client(
            "ec2",
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def s3_client(self):
        return boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
