from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from utils.logs import logger
#from auth.jwt import verify_token
from models import ProjectModel
#from models.auth.user_project import UserProjectModel
from schemas.core.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema


project_router = APIRouter()


@project_router.get(
    "/core/project",
    tags=["core", "project"],
    summary="Get Projects",
    description="Get All Projects",
    response_model=List[ProjectSchema]
)
def get_all_projects(db: Session = Depends(get_db)):
    logger.info("Getting all projects")
    project_query = db.query(ProjectModel).all()
    if not project_query:
        logger.warning(f"Projects not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Projects not found")
    project_list = [project.to_dict() for project in project_query]
    return JSONResponse(project_list)


@project_router.get(
    "/core/project/{id}",
    tags=["core", "project"],
    summary="Get Project",
    description="Get Project by ID",
    response_model=ProjectSchema,
    #dependencies=[Depends(verify_token)]
)
def get_project_by_id(
    id: int = Path(..., description="The id of the project"),
    db: Session = Depends(get_db)
):
    logger.info(f"Getting project with id {id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        logger.warning(f"Project with id {id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    return project


@project_router.post(
    "/core/project",
    tags=["core", "project"],
    summary="Create Project",
    description="Create One Project",
    response_model=ProjectSchema
)
def create_project(
    project: ProjectCreateSchema,
    db: Session = Depends(get_db),
    #user: dict = Depends(verify_token)
):
    logger.info(f"Creating project with name {project.name}")
    if not project.name:
        logger.warning(f"Project name {project.name} is not valid")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Project Data or Project Name already exists")
    new_project = ProjectModel(
        name=project.name,
    )
    try:
        logger.info(f"Adding project with name {new_project.name} to database")
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        # project_user = UserProjectModel(
        #     sub=user.get('sub'),
        #     project_id=new_project.id
        # )
        # db.add(project_user)
        # db.commit()
        return JSONResponse(content=new_project.to_dict(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        logger.error(f"Project ID does not exist in project table")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Project ID does not exist in project table")


@project_router.put(
    "/core/project/{id}",
    tags=["core", "project"],
    summary="Update Project",
    description="Update Project by id",
    response_model=ProjectSchema
)
def update_project_by_id(
    project_update: ProjectUpdateSchema,
    id: int = Path(..., description="The id of the project"),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating project with id {id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        logger.warning(f"Project with id {id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    for key, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    logger.info(f"Project with id {id} updated")
    return ProjectSchema.model_validate(project.__dict__)


@project_router.delete(
    "/core/project/{id}",
    tags=["core", "project"],
    summary="Delete Project",
    description="Delete Project by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_project_by_id(
    id: int = Path(..., description="The id of the project"),
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting project with id {id}")
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        logger.warning(f"Project with id {id} not found")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    db.delete(project)
    db.commit()
    logger.info(f"Project with id {id} deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
