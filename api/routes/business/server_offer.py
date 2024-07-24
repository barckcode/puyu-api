from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from db.session import get_db
from utils.logs import logger
from models import ServerOfferModel, ServiceModel
from schemas.business.server_offer import ServerOfferSchema, ServerOfferCreateSchema, ServerOfferUpdateSchema


server_offer_router = APIRouter()


@server_offer_router.get(
    "/business/server-offer",
    tags=["business", "server_offer"],
    summary="Get all server offers",
    response_model=ServerOfferSchema,
)
def get_server_offers(
    db: Session = Depends(get_db)
):
    logger.info("Getting all server offers")
    server_offers = db.query(ServerOfferModel).all()
    if not server_offers:
        logger.warning("No server offers found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_offer_list = [server_offer.to_dict() for server_offer in server_offers]
    return JSONResponse(server_offer_list)


@server_offer_router.get(
    "/business/server-offer/{service_id}",
    tags=["business", "server_offer"],
    summary="Get a server offers by service ID",
    response_model=ServerOfferSchema,
)
def get_server_offers_by_service_id(
    service_id: int = Path(..., description="The ID of the service"),
    db: Session = Depends(get_db)
):
    logger.info(f"Getting server offers for service ID: {service_id}")
    service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    if not service:
        logger.warning(f"No service found for ID: {service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_offers = db.query(ServerOfferModel).filter(ServerOfferModel.service_id == service_id).all()
    if not server_offers:
        logger.warning(f"No server offers found for service ID: {service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    server_offer_list = [server_offer.to_dict() for server_offer in server_offers]
    return JSONResponse(server_offer_list)


@server_offer_router.post(
    "/business/server-offer",
    tags=["business", "server_offer"],
    summary="Create a server offer",
    response_model=ServerOfferSchema,
)
def create_server_offer(
    server_offer: ServerOfferCreateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Creating server offer: {server_offer}")
    service = db.query(ServiceModel).filter(ServiceModel.id == server_offer.service_id).first()
    if not service:
        logger.warning(f"No service found for ID: {server_offer.service_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    new_server_offer = ServerOfferModel(**server_offer.dict())
    try:
        db.add(new_server_offer)
        db.commit()
        db.refresh(new_server_offer)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating server offer: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating server offer")
    return JSONResponse(new_server_offer.to_dict(), status_code=status.HTTP_201_CREATED)


@server_offer_router.put(
    "/business/server-offer/{server_offer_id}",
    tags=["business", "server_offer"],
    summary="Update a server offer",
    response_model=ServerOfferSchema,
)
def update_server_offer(
    server_offer: ServerOfferUpdateSchema,
    server_offer_id: int = Path(..., description="The ID of the server offer"),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating server offer ID: {server_offer_id}")
    server_offer_to_update = db.query(ServerOfferModel).filter(ServerOfferModel.id == server_offer_id).first()
    if not server_offer_to_update:
        logger.warning(f"No server offer found for ID: {server_offer_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    for key, value in server_offer.model_dump(exclude_unset=True).items():
        setattr(server_offer_to_update, key, value)
    db.commit()
    db.refresh(server_offer_to_update)
    logger.info(f"Server offer with ID: {server_offer_id} updated successfully")
    return ServerOfferSchema.model_validate(server_offer_to_update.__dict__)


@server_offer_router.delete(
    "/business/server-offer/{server_offer_id}",
    tags=["business", "server_offer"],
    summary="Delete a server offer",
    response_model=ServerOfferSchema,
)
def delete_server_offer(
    server_offer_id: int = Path(..., description="The ID of the server offer"),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting server offer with ID: {server_offer_id}")
    server_offer_to_delete = db.query(ServerOfferModel).filter(ServerOfferModel.id == server_offer_id).first()
    if not server_offer_to_delete:
        logger.warning(f"No server offer found for ID: {server_offer_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    db.delete(server_offer_to_delete)
    db.commit()
    logger.info(f"Server offer with ID: {server_offer_id} deleted successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
