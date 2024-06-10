from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.aws.core.ami import AmiModel
from models.core.region import RegionModel
from schemas.aws.core.ami import AmiSchema, AmiCreateSchema, AmiUpdateSchema


aws_ami = APIRouter()


@aws_ami.get(
    "/aws/ami",
    tags=["AWS Core"],
    summary="Get AMIs",
    description="Get All AMIs",
    response_model=List[AmiSchema],
    #dependencies=[Depends(verify_token)]
)
async def get_all_amis(db: Session = Depends(get_db)):
    ami_query = db.query(AmiModel).all()
    ami_list = [ami.to_dict() for ami in ami_query]
    return JSONResponse(ami_list)


@aws_ami.get(
    "/aws/ami/{id}",
    tags=["AWS Core"],
    summary="Get AMI",
    description="Get AMI by ID",
    response_model=AmiSchema
)
def get_ami_by_id(id: int, db: Session = Depends(get_db)):
    ami = db.query(AmiModel).filter(AmiModel.id == id).first()
    if ami is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="AMI not found")
    return ami


@aws_ami.post(
    "/aws/ami",
    tags=["AWS Core"],
    summary="Create AMI",
    description="Create One AMI",
    response_model=AmiSchema
)
def create_ami(ami: AmiCreateSchema, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == ami.region_id).first()
    if not region:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    if not ami.distribution or not ami.version or not ami.ami_aws_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect AMI Data or AMI Name already exists")
    new_ami = AmiModel(
        distribution=ami.distribution,
        version=ami.version,
        ami_aws_id=ami.ami_aws_id,
        region_id=ami.region_id
    )
    try:
        db.add(new_ami)
        db.commit()
        db.refresh(new_ami)
        return new_ami
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AMI ID does not exist in ami table")


@aws_ami.put(
    "/aws/ami/{id}",
    tags=["AWS Core"],
    summary="Update AMI",
    description="Update AMI by id",
    response_model=AmiSchema
)
def update_ami_by_id(id: int, ami_update: AmiUpdateSchema, db: Session = Depends(get_db)):
    ami = db.query(AmiModel).filter(AmiModel.id == id).first()
    if ami is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="AMI not found")
    for key, value in ami_update.model_dump(exclude_unset=True).items():
        setattr(ami, key, value)
    db.commit()
    db.refresh(ami)
    return AmiSchema.model_validate(ami.__dict__)


@aws_ami.delete(
    "/aws/ami/{id}",
    tags=["AWS Core"],
    summary="Delete AMI",
    description="Delete AMI by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ami_by_id(id: int, db: Session = Depends(get_db)):
    ami = db.query(AmiModel).filter(AmiModel.id == id).first()
    if ami is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="AMI not found")
    db.delete(ami)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
