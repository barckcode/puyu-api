from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
from models import ProxNodeModel, RegionModel
from schemas.servers.node import ProxNodeSchema, ProxNodeCreateSchema, ProxNodeUpdateSchema


prox_node_router = APIRouter()


@prox_node_router.get(
    "/server/nodes",
    tags=["servers", "nodes"],
    summary="Get all nodes with optional filters",
    response_model=List[ProxNodeSchema]
)
def get_all_nodes(
    db: Session = Depends(get_db),
    region_id: int | None = Query(default=None, description="The ID of the region to filter by")
):
    logger.info(f"Getting nodes")
    if region_id:
        region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
        if not region:
            logger.warning(f"Region not found: {region_id}")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        nodes = db.query(ProxNodeModel).filter(ProxNodeModel.region_id == region_id).all()
    else:
        nodes = db.query(ProxNodeModel).all()
    nodes_list = [node.to_dict() for node in nodes]
    return JSONResponse(content=nodes_list, status_code=status.HTTP_200_OK)


@prox_node_router.post(
    "/server/nodes",
    tags=["servers", "nodes"],
    summary="Create a new node",
    response_model=ProxNodeSchema
)
def create_node(
    node: ProxNodeCreateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Creating node")
    region = db.query(RegionModel).filter(RegionModel.id == node.region_id).first()
    if not region:
        logger.warning(f"Region not found: {node.region_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    node_model = ProxNodeModel(**node.dict())
    try:
        db.add(node_model)
        db.commit()
        db.refresh(node_model)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating node: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating node")
    return JSONResponse(content=node_model.to_dict(), status_code=status.HTTP_201_CREATED)


@prox_node_router.put(
    "/server/nodes/{node_id}",
    tags=["servers", "nodes"],
    summary="Update a node",
    response_model=ProxNodeSchema
)
def update_node(
    node_id: int,
    node_update: ProxNodeUpdateSchema,
    db: Session = Depends(get_db)
):
    logger.info(f"Updating node: {node_id}")
    node = db.query(ProxNodeModel).filter(ProxNodeModel.id == node_id).first()
    if not node:
        logger.warning(f"Node not found: {node_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    if node_update.region_id:
        region = db.query(RegionModel).filter(RegionModel.id == node_update.region_id).first()
        if not region:
            logger.warning(f"Region not found: {node_update.region_id}")
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    for key, value in node_update.model_dump(exclude_unset=True).items():
        setattr(node, key, value)
    db.commit()
    db.refresh(node)
    logger.info(f"Node updated: {node_id}")
    return JSONResponse(content=node.to_dict(), status_code=status.HTTP_200_OK)


@prox_node_router.delete(
    "/server/nodes/{node_id}",
    tags=["servers", "nodes"],
    summary="Delete a node",
    response_model=ProxNodeSchema
)
def delete_node(
    node_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting node: {node_id}")
    node = db.query(ProxNodeModel).filter(ProxNodeModel.id == node_id).first()
    if not node:
        logger.warning(f"Node not found: {node_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    db.delete(node)
    db.commit()
    logger.info(f"Node deleted: {node_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
