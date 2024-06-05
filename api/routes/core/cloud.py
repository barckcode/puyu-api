from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.core.cloud import CloudModel
from models.aws.core.region import RegionModel
from schemas.core.cloud import CloudSchema, CloudCreateSchema, CloudUpdateSchema
from schemas.aws.core.region import RegionSchema


cloud = APIRouter()


@cloud.get(
    "/cloud",
    tags=["Core"],
    summary="Get Clouds",
    description="Get All Clouds",
    response_model=List[CloudSchema],
    dependencies=[Depends(verify_token)]
)
async def get_all_clouds(db: Session = Depends(get_db)):
    cloud_query = db.query(CloudModel).all()
    cloud_list = [cloud.to_dict() for cloud in cloud_query]
    return JSONResponse(cloud_list)


@cloud.get(
    "/cloud/{id}",
    tags=["Core"],
    summary="Get Cloud",
    description="Get Cloud by ID",
    response_model=CloudSchema
)
def get_cloud_by_id(id: int, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == id).first()
    if cloud is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    return cloud


@cloud.get(
    "/cloud/{id}/regions",
    tags=["Core"],
    summary="Get Regions by Cloud ID",
    description="Get Regions by Cloud ID",
    response_model=List[RegionSchema],
    dependencies=[Depends(verify_token)]
)
def get_region_by_cloud_id(id: int, db: Session = Depends(get_db)):
    region_query = db.query(RegionModel).filter(RegionModel.cloud_id == id).all()
    if region_query is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud ID dont have regions")
    region_list = [region.to_dict() for region in region_query]
    return JSONResponse(region_list)


@cloud.post(
    "/cloud",
    tags=["Core"],
    summary="Create Cloud",
    description="Create One Cloud",
    response_model=CloudSchema
)
def create_cloud(cloud: CloudCreateSchema, db: Session = Depends(get_db)):
    if not cloud.name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Cloud Data or Cloud Name already exists")
    new_cloud = CloudModel(
        name=cloud.name,
    )
    try:
        db.add(new_cloud)
        db.commit()
        db.refresh(new_cloud)
        return new_cloud
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cloud ID does not exist in cloud table")


@cloud.put(
    "/cloud/{id}",
    tags=["Core"],
    summary="Update Cloud",
    description="Update Cloud by id",
    response_model=CloudSchema
)
def update_cloud_by_id(id: int, cloud_update: CloudUpdateSchema, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == id).first()
    if cloud is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    for key, value in cloud_update.model_dump(exclude_unset=True).items():
        setattr(cloud, key, value)
    db.commit()
    db.refresh(cloud)
    return CloudSchema.model_validate(cloud.__dict__)


@cloud.delete(
    "/cloud/{id}",
    tags=["Core"],
    summary="Delete Cloud",
    description="Delete Cloud by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_cloud_by_id(id: int, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == id).first()
    if cloud is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    db.delete(cloud)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
