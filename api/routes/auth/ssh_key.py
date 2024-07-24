from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
from models.auth.ssh_key import SshKeyModel
from models.core.project import ProjectModel
from schemas.auth.ssh_key import SshKeySchema, SshKeyCreateSchema, SshKeyUpdateSchema


ssh_key_router = APIRouter()


@ssh_key_router.get(
    "/core/ssh_keys",
    tags=["core", "ssh_keys"],
    summary="Get ssh keys for a project",
    response_model=List[SshKeySchema],
)
def get_ssh_keys_for_project(project_id: int, db: Session = Depends(get_db)):
    logger.info(f"Getting ssh keys for project with id {project_id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        logger.warning(f"Project with id {project_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    ssh_keys = db.query(SshKeyModel).filter(SshKeyModel.project_id == project_id).all()
    if not ssh_keys:
        logger.warning(f"Ssh keys not found for project with id {project_id}")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ssh keys not found")
    ssh_keys_list = [ssh_key.to_dict() for ssh_key in ssh_keys]
    return JSONResponse(content=ssh_keys_list, status_code=status.HTTP_200_OK)


@ssh_key_router.post(
    "/core/ssh_keys",
    tags=["core", "ssh_keys"],
    summary="Create a ssh key",
    response_model=SshKeySchema,
)
def create_ssh_key(ssh_key: SshKeyCreateSchema, db: Session = Depends(get_db)):
    logger.info(f"Creating ssh key for project with id {ssh_key.project_id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == ssh_key.project_id).first()
    if not project:
        logger.warning(f"Project with id {ssh_key.project_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    ssh_key = SshKeyModel(**ssh_key.dict())
    try:
        logger.info(f"Adding ssh key to database")
        db.add(ssh_key)
        db.commit()
    except IntegrityError:
        logger.warning(f"Ssh key already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ssh key already exists")
    return JSONResponse(content=ssh_key.to_dict(), status_code=status.HTTP_201_CREATED)


@ssh_key_router.put(
    "/core/ssh_keys/{ssh_key_id}",
    tags=["core", "ssh_keys"],
    summary="Update a ssh key for a project",
    response_model=SshKeySchema,
)
def update_ssh_key(ssh_key_id: int, ssh_update: SshKeyUpdateSchema, db: Session = Depends(get_db)):
    logger.info(f"Updating ssh key with id {ssh_key_id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == ssh_update.project_id).first()
    if not project:
        logger.warning(f"Project with id {ssh_update.project_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    ssh_key = db.query(SshKeyModel).filter(SshKeyModel.id == ssh_key_id).first()
    if not ssh_key:
        logger.warning(f"Ssh key with id {ssh_key_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ssh key not found")
    for key, value in ssh_update.model_dump(exclude_unset=True).items():
        setattr(ssh_key, key, value)
    db.commit()
    db.refresh(ssh_key)
    logger.info(f"Ssh key with id {ssh_key_id} updated")
    return JSONResponse(content=ssh_key.to_dict(), status_code=status.HTTP_200_OK)


@ssh_key_router.delete(
    "/core/ssh_keys/{ssh_key_id}",
    tags=["core", "ssh_keys"],
    summary="Delete a ssh key",
)
def delete_ssh_key(ssh_key_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting ssh key with id {ssh_key_id}")
    ssh_key = db.query(SshKeyModel).filter(SshKeyModel.id == ssh_key_id).first()
    if not ssh_key:
        logger.warning(f"Ssh key with id {ssh_key_id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Ssh key not found")
    db.delete(ssh_key)
    db.commit()
    logger.info(f"Ssh key with id {ssh_key_id} deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
