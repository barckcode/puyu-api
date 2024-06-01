from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from models.core.service import ServiceModel
from models.core.cloud import CloudModel
from schemas.core.service import ServiceSchema, ServiceCreateSchema, ServiceUpdateSchema


service = APIRouter()


@service.get(
    "/service",
    tags=["Core"],
    summary="Get Services",
    description="Get All Services",
    response_model=List[ServiceSchema]
)
def get_all_services(db: Session = Depends(get_db)):
    service_query = db.query(ServiceModel).all()
    service_list = [service.to_dict() for service in service_query]
    return JSONResponse(service_list)


@service.get(
    "/service/{id}",
    tags=["Core"],
    summary="Get Service",
    description="Get Service by ID",
    response_model=ServiceSchema
)
def get_service_by_id(id: int, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    return service


@service.post(
    "/service",
    tags=["Core"],
    summary="Create Service",
    description="Create One Service",
    response_model=ServiceSchema
)
def create_service(service: ServiceCreateSchema, db: Session = Depends(get_db)):
    cloud = db.query(CloudModel).filter(CloudModel.id == service.cloud_id).first()
    if not cloud:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cloud ID does not exist in cloud table")
    if not service.name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Service Data or Service Name already exists")
    new_service = ServiceModel(
        name=service.name,
        cloud_id=service.cloud_id
    )
    try:
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return new_service
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Service ID does not exist in service table")


@service.put(
    "/service/{id}",
    tags=["Core"],
    summary="Update Service",
    description="Update Service by id",
    response_model=ServiceSchema
)
def update_service_by_id(id: int, service_update: ServiceUpdateSchema, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    if service_update.cloud_id is not None:
        cloud = db.query(CloudModel).filter(CloudModel.id == service_update.cloud_id).first()
        if not cloud:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cloud ID does not exist in cloud table")
    for key, value in service_update.model_dump(exclude_unset=True).items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return ServiceSchema.model_validate(service.__dict__)


@service.delete(
    "/service/{id}",
    tags=["Core"],
    summary="Delete Service",
    description="Delete Service by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_service_by_id(id: int, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.id == id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    db.delete(service)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
