import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.core.cloud import cloud
from routes.core.service import service
from routes.core.project import project
from routes.auth.project_user import project_user
from routes.core.instance_type import instance_type
from routes.core.storage import storage
from routes.core.region import region
from routes.aws.core.ami import aws_ami
from routes.aws.services.instance import aws_instance


puyu_frontend = os.getenv('PUYU_FRONTEND_URL')

app = FastAPI(
    title="Puyu API",
    description="Puyu API",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "Core",
            "description": "Core Stack"
        },
        {
            "name": "Auth",
            "description": "Authorization and authentication endpoints"
        }
    ]
)

origins = [
    puyu_frontend,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cloud)
app.include_router(service)
app.include_router(project)
app.include_router(project_user)
app.include_router(instance_type)
app.include_router(storage)
app.include_router(region)
app.include_router(aws_ami)
app.include_router(aws_instance)
