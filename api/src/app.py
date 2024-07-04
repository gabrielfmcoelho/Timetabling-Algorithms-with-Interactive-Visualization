from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.app_config import APP_CONFIGS, CORS_CONFIGS

from src.routes.ai import router as service_router
from src.logging.logger import Logger


app_logger = Logger(log_dir="src/logging/logs").get_logger()

app = FastAPI(**APP_CONFIGS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIGS["allow_origins"],
    allow_credentials=CORS_CONFIGS["allow_credentials"],
    allow_methods=CORS_CONFIGS["allow_methods"],
    allow_headers=CORS_CONFIGS["allow_headers"],
)


@app.get('/')
async def root():
    return {'message': f'Welcome to the {APP_CONFIGS["title"]}'}

@app.post('/ping')
async def ping():
    return {'message': 'pong'}


app.include_router(service_router)