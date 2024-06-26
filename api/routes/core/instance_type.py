from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.core.instance_type import InstanceTypeModel
from models.core.cloud import CloudModel
from schemas.core.instance_type import InstanceTypeSchema, InstanceTypeCreateSchema, InstanceTypeUpdateSchema


instance_type = APIRouter()


@instance_type.get(
    "/instance-type",
    tags=["Core"],
    summary="Get Instance Types",
    description="Get All Instance Types",
    response_model=List[InstanceTypeSchema],
    #dependencies=[Depends(verify_token)]
)
async def get_all_instance_types(db: Session = Depends(get_db)):
    instance_type_query = db.query(InstanceTypeModel).all()
    instance_type_list = [instance_type.to_dict() for instance_type in instance_type_query]
    return JSONResponse(instance_type_list)


@instance_type.get(
    "/instance-type/{id}",
    tags=["Core"],
    summary="Get Instance Type",
    description="Get Instance Type by ID",
    response_model=InstanceTypeSchema
)
def get_instance_type_by_id(id: int, db: Session = Depends(get_db)):
    instance_type = db.query(InstanceTypeModel).filter(InstanceTypeModel.id == id).first()
    if instance_type is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Instance Type not found")
    return instance_type


@instance_type.post(
    "/instance-type",
    tags=["Core"],
    summary="Create Instance Type",
    description="Create One Instance Type",
    response_model=InstanceTypeSchema
)
def create_instance_type(instance_type: InstanceTypeCreateSchema, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == instance_type.cloud_id).first()
    if not cloud:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    if not instance_type.cpu or not instance_type.memory or not instance_type.instance_type_cloud_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Instance Type Data or Instance Type Name already exists")
    new_instance_type = InstanceTypeModel(
        cpu=instance_type.cpu,
        memory=instance_type.memory,
        instance_type_cloud_id=instance_type.instance_type_cloud_id,
        cloud_id=instance_type.cloud_id
    )
    try:
        db.add(new_instance_type)
        db.commit()
        db.refresh(new_instance_type)
        return new_instance_type
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Instance Type ID does not exist in instance type table")


@instance_type.put(
    "/instance-type/{id}",
    tags=["Core"],
    summary="Update Instance Type",
    description="Update Instance Type by id",
    response_model=InstanceTypeSchema
)
def update_instance_type_by_id(id: int, instance_type_update: InstanceTypeUpdateSchema, db: Session = Depends(get_db)):
    instance_type = db.query(InstanceTypeModel).filter(InstanceTypeModel.id == id).first()
    if instance_type is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Instance Type not found")
    for key, value in instance_type_update.model_dump(exclude_unset=True).items():
        setattr(instance_type, key, value)
    db.commit()
    db.refresh(instance_type)
    return InstanceTypeSchema.model_validate(instance_type.__dict__)


@instance_type.delete(
    "/instance-type/{id}",
    tags=["Core"],
    summary="Delete Instance Type",
    description="Delete Instance Type by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_instance_type_by_id(id: int, db: Session = Depends(get_db)):
    instance_type = db.query(InstanceTypeModel).filter(InstanceTypeModel.id == id).first()
    if instance_type is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Instance Type not found")
    db.delete(instance_type)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
