from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from utils.logs import logger
from models import ServerImageModel, ServiceModel
from schemas.servers.image import ServerImageSchema, ServerImageCreateSchema, ServerImageUpdateSchema


server_image_router = APIRouter()


@server_image_router.get(
    "/server/image",
    tags=["servers", "images"],
    summary="Get all server images",
    response_model=ServerImageSchema,
)
def get_server_images(
    db: Session = Depends(get_db)
):
    logger.info("Getting all server images")
    server_images = db.query(ServerImageModel).all()
    if not server_images:
        logger.warning("No server images found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_image_list = [server_image.to_dict() for server_image in server_images]
    return JSONResponse(server_image_list)


@server_image_router.get(
    "/server/image/{service_id}",
    tags=["servers", "images"],
    summary="Get a server image by Service ID",
    response_model=ServerImageSchema,
)
def get_server_image_by_service_id(
    service_id: int = Path(..., description="The ID of the service"),
    db: Session = Depends(get_db)
):
    logger.info(f"Getting server image for service ID: {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"No service found for ID: {service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_images = db.query(ServerImageModel).filter(ServerImageModel.service_id == service_id).all()
    if not server_images:
        logger.warning(f"No server image found for service ID: {service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_images_list = [server_image.to_dict() for server_image in server_images]
    return JSONResponse(content=server_images_list)


@server_image_router.post(
    "/server/image",
    tags=["servers", "images"],
    summary="Create a server image",
    response_model=ServerImageSchema,
)
def create_server_image(
    server_image: ServerImageCreateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Creating server image: {server_image}")
    service = db.query(ServiceModel).filter(ServiceModel.id == server_image.service_id).first()
    if not service:
        logger.warning(f"No service found for ID: {server_image.service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    new_server_image = ServerImageModel(**server_image.dict())
    try:
        db.add(new_server_image)
        db.commit()
        db.refresh(new_server_image)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating server image: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating server image")
    return JSONResponse(new_server_image.to_dict(), status_code=status.HTTP_201_CREATED)


@server_image_router.put(
    "/server/image/{server_image_id}",
    tags=["servers", "images"],
    summary="Update a server image",
    response_model=ServerImageSchema,
)
def update_server_image(
    server_image: ServerImageUpdateSchema,
    server_image_id: int = Path(..., description="The ID of the server image"),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating server image ID: {server_image_id}")
    server_image_to_update = db.query(ServerImageModel).filter(ServerImageModel.id == server_image_id).first()
    if not server_image_to_update:
        logger.warning(f"No server image found for ID: {server_image_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    for key, value in server_image.model_dump(exclude_unset=True).items():
        setattr(server_image_to_update, key, value)
    db.commit()
    db.refresh(server_image_to_update)
    logger.info(f"Server image with ID: {server_image_id} updated successfully")
    return ServerImageSchema.model_validate(server_image_to_update.__dict__)


@server_image_router.delete(
    "/server/image/{server_image_id}",
    tags=["servers", "images"],
    summary="Delete a server image",
    response_model=ServerImageSchema,
)
def delete_server_image(
    server_image_id: int = Path(..., description="The ID of the server image"),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting server image with ID: {server_image_id}")
    server_image_to_delete = db.query(ServerImageModel).filter(ServerImageModel.id == server_image_id).first()
    if not server_image_to_delete:
        logger.warning(f"No server image found for ID: {server_image_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    db.delete(server_image_to_delete)
    db.commit()
    logger.info(f"Server image with ID: {server_image_id} deleted successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
