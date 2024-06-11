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

# Example usage:
# create_key_pair("eu-west-1", "test-puyu")
