import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.aws.ami import aws_ami


puyu_frontend = os.getenv('PUYU_FRONTEND')

app = FastAPI(
    title="Puyu API",
    description="Puyu API",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "AWS",
            "description": "AWS Services"
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

app.include_router(aws_ami)
