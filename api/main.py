import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.core.cloud import cloud
from routes.core.service import service
from routes.core.project import project
from routes.auth.project_user import project_user


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
