from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from models.core.project import ProjectModel
from schemas.core.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema


project = APIRouter()


@project.get(
    "/project",
    tags=["Core"],
    summary="Get Projects",
    description="Get All Projects",
    response_model=List[ProjectSchema]
)
def get_all_projects(db: Session = Depends(get_db)):
    project_query = db.query(ProjectModel).all()
    project_list = [project.to_dict() for project in project_query]
    return JSONResponse(project_list)


@project.get(
    "/project/{id}",
    tags=["Core"],
    summary="Get Project",
    description="Get Project by ID",
    response_model=ProjectSchema
)
def get_project_by_id(id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    return project


@project.post(
    "/project",
    tags=["Core"],
    summary="Create Project",
    description="Create One Project",
    response_model=ProjectSchema
)
def create_project(project: ProjectCreateSchema, db: Session = Depends(get_db)):
    if not project.name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Project Data or Project Name already exists")
    new_project = ProjectModel(
        name=project.name,
    )
    try:
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Project ID does not exist in project table")


@project.put(
    "/project/{id}",
    tags=["Core"],
    summary="Update Project",
    description="Update Project by id",
    response_model=ProjectSchema
)
def update_project_by_id(id: int, project_update: ProjectUpdateSchema, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    for key, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return ProjectSchema.model_validate(project.__dict__)


@project.delete(
    "/project/{id}",
    tags=["Core"],
    summary="Delete Project",
    description="Delete Project by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_project_by_id(id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == id).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project not found")
    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
