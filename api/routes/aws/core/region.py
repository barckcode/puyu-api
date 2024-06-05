from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.aws.core.region import RegionModel
from models.core.cloud import CloudModel
from models.aws.core.ami import AmiModel
from schemas.aws.core.region import RegionSchema, RegionCreateSchema, RegionUpdateSchema
from schemas.aws.core.ami import AmiSchema


aws_region = APIRouter()


@aws_region.get(
    "/aws/region",
    tags=["AWS Core"],
    summary="Get Regions",
    description="Get All Regions",
    response_model=List[RegionSchema],
    #dependencies=[Depends(verify_token)]
)
async def get_all_regions(db: Session = Depends(get_db)):
    region_query = db.query(RegionModel).all()
    region_list = [region.to_dict() for region in region_query]
    return JSONResponse(region_list)


@aws_region.get(
    "/aws/region/{id}",
    tags=["AWS Core"],
    summary="Get Region",
    description="Get Region by ID",
    response_model=RegionSchema
)
def get_region_by_id(id: int, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == id).first()
    if region is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    return region


@aws_region.get(
    "/aws/region/{id}/amis",
    tags=["AWS Core"],
    summary="Get AMIs by Region ID",
    description="Get AMIs by Region ID",
    response_model=List[AmiSchema],
    #dependencies=[Depends(verify_token)]
)
async def get_all_amis_by_region_id(id: int, db: Session = Depends(get_db)):
    ami_query = db.query(AmiModel).filter(AmiModel.region_id == id).all()
    ami_list = [ami.to_dict() for ami in ami_query]
    return JSONResponse(ami_list)


@aws_region.post(
    "/aws/region",
    tags=["AWS Core"],
    summary="Create Region",
    description="Create One Region",
    response_model=RegionSchema
)
def create_region(region: RegionCreateSchema, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == region.cloud_id).first()
    if not cloud:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    if not region.name or not region.region_aws_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Region Data or Region Name already exists")
    new_region = RegionModel(
        name=region.name,
        region_aws_id=region.region_aws_id,
        cloud_id=region.cloud_id
    )
    try:
        db.add(new_region)
        db.commit()
        db.refresh(new_region)
        return new_region
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Region ID does not exist in region table")


@aws_region.put(
    "/aws/region/{id}",
    tags=["AWS Core"],
    summary="Update Region",
    description="Update Region by id",
    response_model=RegionSchema
)
def update_region_by_id(id: int, region_update: RegionUpdateSchema, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == id).first()
    if region is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    for key, value in region_update.model_dump(exclude_unset=True).items():
        setattr(region, key, value)
    db.commit()
    db.refresh(region)
    return RegionSchema.model_validate(region.__dict__)


@aws_region.delete(
    "/aws/region/{id}",
    tags=["AWS Core"],
    summary="Delete Region",
    description="Delete Region by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_region_by_id(id: int, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == id).first()
    if region is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    db.delete(region)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
