from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.core.storage import StorageModel
from models.core.cloud import CloudModel
from schemas.core.storage import StorageSchema, StorageCreateSchema, StorageUpdateSchema


storage = APIRouter()


@storage.get(
    "/storage",
    tags=["Core"],
    summary="Get Storages",
    description="Get All Storages",
    response_model=List[StorageSchema],
    #dependencies=[Depends(verify_token)]
)
async def get_all_storages(db: Session = Depends(get_db)):
    storage_query = db.query(StorageModel).all()
    storage_list = [storage.to_dict() for storage in storage_query]
    return JSONResponse(storage_list)


@storage.get(
    "/storage/{id}",
    tags=["Core"],
    summary="Get Storage",
    description="Get Storage by ID",
    response_model=StorageSchema
)
def get_storage_by_id(id: int, db: Session = Depends(get_db)):
    storage = db.query(StorageModel).filter(StorageModel.id == id).first()
    if storage is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Storage not found")
    return storage


@storage.post(
    "/storage",
    tags=["Core"],
    summary="Create Storage",
    description="Create One Storage",
    response_model=StorageSchema
)
def create_storage(storage: StorageCreateSchema, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == storage.cloud_id).first()
    if not cloud:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Cloud not found")
    if not storage.size or not storage.type:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Storage Data")
    new_storage = StorageModel(
        size=storage.size,
        type=storage.type,
        cloud_id=storage.cloud_id
    )
    try:
        db.add(new_storage)
        db.commit()
        db.refresh(new_storage)
        return new_storage
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cloud ID does not exist in cloud table")


@storage.put(
    "/storage/{id}",
    tags=["Core"],
    summary="Update Storage",
    description="Update Storage by id",
    response_model=StorageSchema
)
def update_storage_by_id(id: int, storage_update: StorageUpdateSchema, db: Session = Depends(get_db)):
    storage = db.query(StorageModel).filter(StorageModel.id == id).first()
    if storage is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Storage not found")
    for key, value in storage_update.model_dump(exclude_unset=True).items():
        setattr(storage, key, value)
    db.commit()
    db.refresh(storage)
    return StorageSchema.model_validate(storage.__dict__)


@storage.delete(
    "/storage/{id}",
    tags=["Core"],
    summary="Delete Storage",
    description="Delete Storage by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_storage_by_id(id: int, db: Session = Depends(get_db)):
    storage = db.query(StorageModel).filter(StorageModel.id == id).first()
    if storage is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Storage not found")
    db.delete(storage)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
