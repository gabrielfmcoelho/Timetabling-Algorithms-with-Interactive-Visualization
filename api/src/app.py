from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict
from icecream import ic

import os

from config.configs import APP_CONFIGS, CORS_CONFIGS
from logs.logger import Logger


logger = Logger(log_dir="logs/history").get_logger()

app = FastAPI(**asdict(APP_CONFIGS))

app.add_middleware(
    CORSMiddleware,
    **asdict(CORS_CONFIGS)
)


@app.get('/')
async def root():
    return {'message': f'Welcome to the {APP_CONFIGS.title} API, check the documentation at {APP_CONFIGS.docs_url} or {APP_CONFIGS.redoc_url} endpoints.'}

@app.post('/ping')
async def ping():
    return {'message': 'pong'}


from routes.ai import router as ai_router

app.include_router(ai_router)