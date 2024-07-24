from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
from models.core.service import ServiceModel
from schemas.core.service import ServiceFilterParams, ServiceSchema, ServiceCreateSchema, ServiceUpdateSchema


service_router = APIRouter()


@service_router.get(
    "/core/service",
    tags=["core", "service"],
    summary="Get all services with optional filters",
    response_model=List[ServiceSchema],
)
def get_all_services(
    db: Session = Depends(get_db),
    filters: ServiceFilterParams = Depends(ServiceFilterParams),
):
    logger.info(f"Getting services")
    query = db.query(ServiceModel)
    if filters.id is not None:
        logger.info(f"Filtering by id: {filters.id}")
        query = query.filter(ServiceModel.id == filters.id)
    if filters.name is not None:
        logger.info(f"Filtering by name: {filters.name}")
        query = query.filter(ServiceModel.name.ilike(f"%{filters.name}%"))
    if filters.available is not None:
        logger.info(f"Filtering by available: {filters.available}")
        query = query.filter(ServiceModel.available == filters.available)
    services = query.all()
    if not services:
        logger.warning(f"No services found with the given filters")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    services_list = [service.to_dict() for service in services]
    return JSONResponse(content=services_list, status_code=status.HTTP_200_OK)


@service_router.post(
    "/core/service",
    tags=["core", "service"],
    summary="Create a service",
    response_model=ServiceSchema,
)
def create_service(service: ServiceCreateSchema, db: Session = Depends(get_db)):
    logger.info(f"Creating service")
    service = ServiceModel(**service.dict())
    try:
        logger.info(f"Adding service to database")
        db.add(service)
        db.commit()
    except IntegrityError:
        logger.warning(f"Service already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service already exists")
    return JSONResponse(content=service.to_dict(), status_code=status.HTTP_201_CREATED)


@service_router.put(
    "/core/service/{service_id}",
    tags=["core", "service"],
    summary="Update a service",
    response_model=ServiceSchema,
)
def update_service(service_id: int, service_update: ServiceUpdateSchema, db: Session = Depends(get_db)):
    logger.info(f"Updating service with id {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"Service with id {service_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    for key, value in service_update.model_dump(exclude_unset=True).items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    logger.info(f"Service with id {service_id} updated")
    return JSONResponse(content=service.to_dict(), status_code=status.HTTP_200_OK)


@service_router.delete(
    "/core/service/{service_id}",
    tags=["core", "service"],
    summary="Delete a service",
)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting service with id {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"Service with id {service_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    db.delete(service)
    db.commit()
    logger.info(f"Service with id {service_id} deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
