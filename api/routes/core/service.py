from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
from models import ServiceModel, RegionModel, RegionServiceModel
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
    new_service = ServiceModel(
        name=service.name,
        description=service.description,
        available=service.available
    )
    try:
        logger.info(f"Adding service to database")
        db.add(new_service)
        db.flush()
        for region_id in service.region_ids:
            region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
            if not region:
                logger.warning(f"Region with id {region_id} not found")
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            region_service = RegionServiceModel(region_id=region_id, service_id=new_service.id)
            db.add(region_service)
        db.commit()
        db.refresh(new_service)
    except IntegrityError:
        logger.warning(f"Service already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating service: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating service")
    response_data = new_service.to_dict()
    response_data["regions"] = service.region_ids
    return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@service_router.post(
    "/core/service/{service_id}/regions",
    tags=["core", "service"],
    summary="Add regions to an existing service",
    response_model=ServiceSchema,
)
def add_regions_to_service(
    service_id: int = Path(..., description="The ID of the service to add regions to"),
    region_ids: List[int] = Body(..., description="The IDs of the regions to add to the service"),
    db: Session = Depends(get_db)
):
    logger.info(f"Adding regions to service {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"Service with id {service_id} not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    existing_regions = set(rs.region_id for rs in service.regions)
    try:
        for region_id in region_ids:
            if region_id not in existing_regions:
                region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
                if not region:
                    logger.warning(f"Region with id {region_id} not found")
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
                region_service = RegionServiceModel(region_id=region_id, service_id=service_id)
                db.add(region_service)
        db.commit()
        db.refresh(service)
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding regions to service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error adding regions to service")
    return JSONResponse(content=service.to_dict(), status_code=status.HTTP_200_OK)


@service_router.delete(
    "/core/service/{service_id}/regions",
    tags=["core", "service"],
    summary="Remove regions from an existing service",
    response_model=ServiceSchema,
)
def remove_regions_from_service(
    service_id: int = Path(..., description="The ID of the service to remove regions from"),
    region_ids: List[int] = Body(..., description="The IDs of the regions to remove from the service"),
    db: Session = Depends(get_db)
):
    logger.info(f"Removing regions from service {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"Service with id {service_id} not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    try:
        db.query(RegionServiceModel).filter(
            RegionServiceModel.service_id == service_id,
            RegionServiceModel.region_id.in_(region_ids)
        ).delete(synchronize_session=False)
        db.commit()
        db.refresh(service)
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing regions from service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error removing regions from service")
    return JSONResponse(content=service.to_dict(), status_code=status.HTTP_200_OK)


@service_router.put(
    "/core/service/{service_id}",
    tags=["core", "service"],
    summary="Update a service",
    response_model=ServiceSchema,
)
def update_service(
    service_update: ServiceUpdateSchema,
    service_id: int = Path(..., description="The ID of the service to update"),
    db: Session = Depends(get_db)
):
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
def delete_service(
    service_id: int = Path(..., description="The ID of the service to delete"),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting service with id {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"Service with id {service_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Service not found")
    db.delete(service)
    db.commit()
    logger.info(f"Service with id {service_id} deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
