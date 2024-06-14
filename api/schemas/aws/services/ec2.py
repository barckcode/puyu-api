from pydantic import BaseModel


class KeyPairCreateSchema(BaseModel):
    name: str
    region_cloud_id: str


class SecurityGroupCreateAwsSchema(BaseModel):
    name: str
    description: str
    aws_vpc_id: str
    region_cloud_id: str

class SecurityGroupCreateDbSchema(BaseModel):
    name: str
    aws_resource_id: str
    aws_vpc_id: str
    region_cloud_id: str


class SecurityGroupRuleCreateAwsSchema(BaseModel):
    type: str
    aws_security_group_id: str
    port: int
    protocol: str
    cird_ip: str
    region_cloud_id: str


class SecurityGroupRuleCreateDbSchema(BaseModel):
    type: str
    aws_resource_id: str
    aws_security_group_id: str
    port: int
    protocol: str
    cird_ip: str
    region_cloud_id: str


class InstanceCreateSchema(BaseModel):
    name: str
    disk_size: int
    instance_type_cloud_id: str
    aws_ami_id: str
    region_cloud_id: str
    project_id: int


class CreatedInstanceSchema(BaseModel):
    name: str
    public_ip: str
    private_ip: str
    aws_security_group_id: str
    aws_instance_id: str


class InstanceCreateAwsSchema(BaseModel):
    name: str
    disk_size: int
    key_pair_name: str
    instance_type_cloud_id: str
    aws_ami_id: str
    aws_subnet_id: str
    aws_security_group_id: str
    region_cloud_id: str


class InstanceCreateDbSchema(BaseModel):
    name: str
    aws_resource_id: str
    disk_size: int
    public_ip: str
    private_ip: str
    key_pair_name: str
    instance_type_cloud_id: str
    aws_ami_id: str
    aws_subnet_id: str
    aws_security_group_id: str
    region_cloud_id: str
