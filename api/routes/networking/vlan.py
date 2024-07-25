from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from utils.logs import logger
from models import ProxNodeModel, ProxVlanModel
from schemas.networking.vlan import ProxVlanSchema, ProxVlanCreateSchema, ProxVlanUpdateSchema


prox_vlan_router = APIRouter()


@prox_vlan_router.get(
    "/networking/vlans",
    tags=["networking", "vlans"],
    summary="Get all vlans with optional filters",
    response_model=List[ProxVlanSchema]
)
def get_all_vlans(
    db: Session = Depends(get_db),
    prox_node_id: int | None = Query(default=None, description="The ID of the prox node to filter by"),
    vlan_id: int | None = Query(default=None, description="The ID of the vlan to filter by")
):
    logger.info(f"Getting vlans")
    if prox_node_id:
        prox_node = db.query(ProxNodeModel).filter(ProxNodeModel.id == prox_node_id).first()
        if not prox_node:
            logger.warning(f"Prox node not found: {prox_node_id}")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        vlans = db.query(ProxVlanModel).filter(ProxVlanModel.prox_node_id == prox_node_id).all()
    elif vlan_id:
        vlans = db.query(ProxVlanModel).filter(ProxVlanModel.id == vlan_id).first()
    else:
        vlans = db.query(ProxVlanModel).all()
    vlans_list = [vlan.to_dict() for vlan in vlans]
    return JSONResponse(content=vlans_list, status_code=status.HTTP_200_OK)


@prox_vlan_router.post(
    "/networking/vlans",
    tags=["networking", "vlans"],
    summary="Create a new vlan",
    response_model=ProxVlanSchema
)
def create_vlan(
    vlan: ProxVlanCreateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Creating node")
    prox_node = db.query(ProxNodeModel).filter(ProxNodeModel.id == vlan.prox_node_id).first()
    if not prox_node:
        logger.warning(f"Prox node not found: {vlan.prox_node_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    vlan_model = ProxVlanModel(**vlan.dict())
    try:
        db.add(vlan_model)
        db.commit()
        db.refresh(vlan_model)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating node: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating node")
    return JSONResponse(content=vlan_model.to_dict(), status_code=status.HTTP_201_CREATED)


@prox_vlan_router.put(
    "/networking/vlans/{vlan_id}",
    tags=["networking", "vlans"],
    summary="Update a vlan",
    response_model=ProxVlanSchema
)
def update_vlan(
    vlan_id: int,
    vlan_update: ProxVlanUpdateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Updating vlan: {vlan_id}")
    vlan = db.query(ProxVlanModel).filter(ProxVlanModel.id == vlan_id).first()
    if not vlan:
        logger.warning(f"Vlan not found: {vlan_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    if vlan_update.prox_node_id:
        prox_node = db.query(ProxNodeModel).filter(ProxNodeModel.id == vlan_update.prox_node_id).first()
        if not prox_node:
            logger.warning(f"Prox node not found: {vlan_update.prox_node_id}")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    for key, value in vlan_update.model_dump(exclude_unset=True).items():
        setattr(vlan, key, value)
    db.commit()
    db.refresh(vlan)
    logger.info(f"Vlan updated: {vlan_id}")
    return JSONResponse(content=vlan.to_dict(), status_code=status.HTTP_200_OK)


@prox_vlan_router.delete(
    "/networking/vlans/{vlan_id}",
    tags=["networking", "vlans"],
    summary="Delete a vlan",
    response_model=ProxVlanSchema
)
def delete_vlan(
    vlan_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting vlan: {vlan_id}")
    vlan = db.query(ProxVlanModel).filter(ProxVlanModel.id == vlan_id).first()
    if not vlan:
        logger.warning(f"Vlan not found: {vlan_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    db.delete(vlan)
    db.commit()
    logger.info(f"Vlan deleted: {vlan_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
