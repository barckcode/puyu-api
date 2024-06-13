from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
#from routes.aws.config import aws_access_key_id, aws_secret_access_key
from models.core.project import ProjectModel
from models.aws.services.network import VpcModel, SubnetModel
from models.aws.services.ec2 import KeyPairModel
from schemas.aws.services.instance import InstanceCreateSchema
from schemas.aws.services.network import VpcCreateAwsSchema, SubnetCreateAwsSchema
from schemas.aws.services.ec2 import KeyPairCreateSchema
from services.aws.network import create_vpc, create_subnet
from services.aws.ec2 import create_key_pair


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
    #response_model=InstanceCreateSchema
)
def create_instance(instance: InstanceCreateSchema, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.project_id == instance.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")

    # Validate Initial Setup
    # VPC
    vpc = db.query(VpcModel).filter(VpcModel.project_id == instance.project_id).first()
    if not vpc:
        vpc_created = create_vpc(VpcCreateAwsSchema(
            name=instance.name,
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
            try:
                db.add(new_subnet)
                db.commit()
                db.refresh(new_subnet)
                aws_subnet_id = new_subnet.aws_resource_id # TODO: Need for create Instance

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
                try:
                    db.add(new_key_pair)
                    db.commit()
                    db.refresh(new_key_pair)
                    key_pair_name = new_key_pair.name # TODO: Need for create Instance
                except Exception as e:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating Key Pair on DB: {e}")

                # Security Group
                # TODO: Create Security Group
                # TODO: Create Instance
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating Subnet on DB: {e}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating VPC on DB: {e}")
    else:
        # TODO: Get Key Pair
        # TODO: Get Subnet
        # TODO: Create Security Group
        # TODO: Create Instance
        pass
