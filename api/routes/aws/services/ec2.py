from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
#from routes.aws.config import aws_access_key_id, aws_secret_access_key
from models.core.project import ProjectModel
from models.aws.services.network import VpcModel, SubnetModel
from models.aws.services.ec2 import KeyPairModel, SecurityGroupModel, SecurityGroupRuleModel, InstanceModel
from schemas.aws.services.network import VpcCreateAwsSchema, SubnetCreateAwsSchema
from schemas.aws.services.ec2 import KeyPairCreateSchema, SecurityGroupCreateAwsSchema, SecurityGroupRuleCreateAwsSchema, InstanceCreateAwsSchema, InstanceCreateSchema, CreatedInstanceSchema
from services.aws.network import create_vpc, create_subnet
from services.aws.ec2 import create_key_pair, create_security_group, create_security_group_rule, create_instance


aws_instance = APIRouter()

# Frontend data
# serverName
# selectedRegion.region_cloud_id
# selectedDistribution.ami_aws_id
# selectedInstanceType.instance_type_cloud_id
# selectedStorage.size
# project_id

# Backend
# ¿key_pair? -> It will be obtained from the indicated project_id
# ¿subnet? -> It will be obtained from the indicated project_id
# ¿security_group? -> Create it before the server.

@aws_instance.post(
    "/aws/instance",
    tags=["AWS Service"],
    summary="Create Instance",
    description="Create One Instance",
    response_model=CreatedInstanceSchema
)
def create_instance_route(instance: InstanceCreateSchema, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == instance.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")

    # Validate Initial Setup
    # VPC
    vpc = db.query(VpcModel).filter(VpcModel.project_id == instance.project_id).first()
    if not vpc:
        vpc_created = create_vpc(VpcCreateAwsSchema(
            name=project.name,
            cidr_block="10.255.0.0/16", # TODO: Make CIDR user selectable
            region_cloud_id=instance.region_cloud_id
        ))
        new_vpc = VpcModel(
            name=vpc_created.name,
            aws_resource_id=vpc_created.aws_resource_id,
            cidr_block=vpc_created.cidr_block,
            region_cloud_id=vpc_created.region_cloud_id,
            project_id=instance.project_id
        )
        try:
            db.add(new_vpc)
            db.commit()
            db.refresh(new_vpc)
            aws_vpc_id = new_vpc.aws_resource_id

            # Subnet:
            subnet_created = create_subnet(SubnetCreateAwsSchema(
                name=f"{new_vpc.name}-00",
                cidr_block="10.255.0.0/20", # TODO: Make CIDR user selectable
                region_cloud_id=new_vpc.region_cloud_id,
                aws_vpc_id=aws_vpc_id,
                availability_zone=f"{new_vpc.region_cloud_id}a"
            ))
            new_subnet = SubnetModel(
                name=subnet_created.name,
                aws_resource_id=subnet_created.aws_resource_id,
                cidr_block=subnet_created.cidr_block,
                aws_vpc_id=subnet_created.aws_vpc_id,
                availability_zone=subnet_created.availability_zone,
                region_cloud_id=subnet_created.region_cloud_id,
                project_id=instance.project_id
            )
            db.add(new_subnet)
            db.commit()
            db.refresh(new_subnet)
            aws_subnet_id = new_subnet.aws_resource_id

            # Key Pair
            key_pair_created = create_key_pair(KeyPairCreateSchema(
                name=f"{project.name}",
                region_cloud_id=instance.region_cloud_id
            ))
            new_key_pair = KeyPairModel(
                name=key_pair_created.name,
                region_cloud_id=key_pair_created.region_cloud_id,
                project_id=instance.project_id
            )
            db.add(new_key_pair)
            db.commit()
            db.refresh(new_key_pair)
            key_pair_name = new_key_pair.name

            # Security Group
            security_group_created = create_security_group(SecurityGroupCreateAwsSchema(
                name=f"{instance.name}-sg",
                description=f"Security Group for {instance.name}",
                aws_vpc_id=aws_vpc_id,
                region_cloud_id=instance.region_cloud_id
            ))
            new_security_group = SecurityGroupModel(
                name=security_group_created.name,
                aws_resource_id=security_group_created.aws_resource_id,
                aws_vpc_id=security_group_created.aws_vpc_id,
                region_cloud_id=security_group_created.region_cloud_id,
                project_id=instance.project_id
            )
            db.add(new_security_group)
            db.commit()
            db.refresh(new_security_group)
            aws_security_group_id = new_security_group.aws_resource_id

            # Security Group Default Rules
            security_group_rule_created = create_security_group_rule(SecurityGroupRuleCreateAwsSchema(
                type="ingress",
                aws_security_group_id=aws_security_group_id,
                port=22,
                protocol="tcp",
                cird_ip="0.0.0.0/0",
                region_cloud_id=instance.region_cloud_id
            ))
            new_security_group_rule = SecurityGroupRuleModel(
                type=security_group_rule_created.type,
                aws_resource_id=security_group_rule_created.aws_resource_id,
                aws_security_group_id=security_group_rule_created.aws_security_group_id,
                port=security_group_rule_created.port,
                protocol=security_group_rule_created.protocol,
                cird_ip=security_group_rule_created.cird_ip,
                region_cloud_id=security_group_rule_created.region_cloud_id,
                project_id=instance.project_id
            )
            db.add(new_security_group_rule)
            db.commit()
            db.refresh(new_security_group_rule)

            # Instance
            instance_created = create_instance(InstanceCreateAwsSchema(
                name=f"{instance.name}",
                disk_size=instance.disk_size,
                key_pair_name=key_pair_name,
                instance_type_cloud_id=instance.instance_type_cloud_id,
                aws_ami_id=instance.aws_ami_id,
                aws_subnet_id=aws_subnet_id,
                aws_security_group_id=aws_security_group_id,
                region_cloud_id=instance.region_cloud_id
            ))
            new_instance = InstanceModel(
                name=instance_created.name,
                aws_resource_id=instance_created.aws_resource_id,
                disk_size=instance_created.disk_size,
                public_ip=instance_created.public_ip,
                private_ip=instance_created.private_ip,
                key_pair_name=instance_created.key_pair_name,
                instance_type_cloud_id=instance_created.instance_type_cloud_id,
                aws_ami_id=instance_created.aws_ami_id,
                aws_subnet_id=aws_subnet_id,
                aws_security_group_id=aws_security_group_id,
                region_cloud_id=instance_created.region_cloud_id,
                project_id=instance.project_id
            )
            db.add(new_instance)
            db.commit()
            db.refresh(new_instance)
            return CreatedInstanceSchema(
                name=new_instance.name,
                public_ip=new_instance.public_ip,
                private_ip=new_instance.private_ip,
                aws_security_group_id=new_instance.aws_security_group_id,
                aws_instance_id=new_instance.aws_resource_id,
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating resource on DB: {e}")
    else:
        # TODO: Get Key Pair
        # TODO: Get Subnet
        # TODO: Create Security Group
        # TODO: Create Instance
        pass
