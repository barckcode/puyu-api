from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from db.session import get_db
from auth.jwt import verify_token
from models.auth.project_user import ProjectUserModel
from models.core.project import ProjectModel
from schemas.auth.project_user import ProjectUserSchema


project_user = APIRouter()


@project_user.get(
    "/projects/users/all",
    tags=["Auth"],
    summary="Get Projects & Users",
    description="Get All Projects & Users",
    response_model=List[ProjectUserSchema]
)
def get_all_projects_and_users(db: Session = Depends(get_db)):
    project_user_query = db.query(ProjectUserModel).all()
    project_user_list = [project_user.to_dict() for project_user in project_user_query]
    return JSONResponse(project_user_list)


@project_user.get(
    "/projects/user",
    tags=["Auth"],
    summary="Get user projects",
    description="Get All user projects by user",
    response_model=List[ProjectUserSchema]
)
def get_all_projects_by_user(sub: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    print("user:", user)
    project_user_query = db.query(ProjectUserModel).filter(ProjectUserModel.sub == sub).all()
    project_user_list = [project_user.to_dict() for project_user in project_user_query]
    return JSONResponse(project_user_list)


@project_user.get(
    "/project/{project_id}/users",
    tags=["Auth"],
    summary="Get project users",
    description="Get All project users by project",
    response_model=List[ProjectUserSchema]
)
def get_all_project_users(project_id: int, db: Session = Depends(get_db)):
    project_user_query = db.query(ProjectUserModel).filter(ProjectUserModel.project_id == project_id).all()
    project_user_list = [project_user.to_dict() for project_user in project_user_query]
    return JSONResponse(project_user_list)


@project_user.post(
    "/project/{project_id}/user",
    tags=["Auth"],
    summary="Associate users with projects",
    description="Associate users with projects",
    response_model=ProjectUserSchema
)
def create_project_user(project_id: int, sub: str, db: Session = Depends(get_db)):
    if not project_id or not sub:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect Project User Data")
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project ID does not exist in project table")
    new_project_user = ProjectUserModel(
        project_id=project_id,
        sub=sub
    )
    try:
        db.add(new_project_user)
        db.commit()
        db.refresh(new_project_user)
        return new_project_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User is already associated with the project")


@project_user.delete(
    "/project/{project_id}/user",
    tags=["Auth"],
    summary="Delete user from project",
    description="Delete user from project",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_from_project(project_id: int, sub: str, db: Session = Depends(get_db)):
    project_user = db.query(ProjectUserModel).filter(ProjectUserModel.project_id == project_id, ProjectUserModel.sub == sub).first()
    if project_user is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Project User not found")
    db.delete(project_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
