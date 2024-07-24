from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
from models import RegionModel
from schemas.core.region import RegionFilterParams, RegionSchema, RegionCreateSchema, RegionUpdateSchema


region_router = APIRouter()


@region_router.get(
    "/core/region",
    tags=["core", "region"],
    summary="Get all regions with optional filters",
    response_model=List[RegionSchema],
)
def get_all_regions(
    db: Session = Depends(get_db),
    filters: RegionFilterParams = Depends(RegionFilterParams),
):
    logger.info(f"Getting regions")
    query = db.query(RegionModel)
    if filters.id is not None:
        logger.info(f"Filtering by id: {filters.id}")
        query = query.filter(RegionModel.id == filters.id)
    if filters.name is not None:
        logger.info(f"Filtering by name: {filters.name}")
        query = query.filter(RegionModel.name.ilike(f"%{filters.name}%"))
    if filters.available is not None:
        logger.info(f"Filtering by available: {filters.available}")
        query = query.filter(RegionModel.available == filters.available)
    regions = query.all()
    if not regions:
        logger.warning(f"No regions found with the given filters")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    regions_list = [region.to_dict() for region in regions]
    return JSONResponse(content=regions_list, status_code=status.HTTP_200_OK)


@region_router.post(
    "/core/region",
    tags=["core", "region"],
    summary="Create a region",
    response_model=RegionSchema,
)
def create_region(region: RegionCreateSchema, db: Session = Depends(get_db)):
    logger.info(f"Creating region")
    region = RegionModel(**region.dict())
    try:
        logger.info(f"Adding region to database")
        db.add(region)
        db.commit()
    except IntegrityError:
        logger.warning(f"Region already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Region already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating region: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating region")
    return JSONResponse(content=region.to_dict(), status_code=status.HTTP_201_CREATED)


@region_router.put(
    "/core/region/{region_id}",
    tags=["core", "region"],
    summary="Update a region",
    response_model=RegionSchema,
)
def update_region(region_id: int, region_update: RegionUpdateSchema, db: Session = Depends(get_db)):
    logger.info(f"Updating region with id {region_id}")
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
    if not region:
        logger.warning(f"Region with id {region_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    for key, value in region_update.model_dump(exclude_unset=True).items():
        setattr(region, key, value)
    db.commit()
    db.refresh(region)
    logger.info(f"Region with id {region_id} updated")
    return JSONResponse(content=region.to_dict(), status_code=status.HTTP_200_OK)


@region_router.delete(
    "/core/region/{region_id}",
    tags=["core", "region"],
    summary="Delete a region",
)
def delete_region(region_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting region with id {region_id}")
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
    if not region:
        logger.warning(f"Region with id {region_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Region not found")
    db.delete(region)
    db.commit()
    logger.info(f"Region with id {region_id} deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
