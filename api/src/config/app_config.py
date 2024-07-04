from dotenv import load_dotenv
import os

load_dotenv()
if not os.environ.get("MODE") or os.environ.get("MODE") not in ['dev', 'prod']:
    raise ValueError("MODE not found in .env or it's value is not 'dev' or 'prod'")
if not os.environ.get("PROJECT_NAME"):
    raise ValueError("Main env var PROJECT_NAME not found in .env")

PROJECT_NAME = os.environ.get("PROJECT_NAME")

APP_CONFIGS = {
    'title': PROJECT_NAME,
    'description': f"{PROJECT_NAME}, it's goal is to provide a RESTful API with the necessary endpoints to implement a inteface for a machine learning models and operations.",
    'version': '0.1.0',
    'openapi_url': '/openapi.json' if os.environ.get("MODE") == 'dev' else None,
    'docs_url': '/docs',
    'redoc_url': '/redoc',
    'swagger_ui_oauth2_redirect_url': '/docs/oauth2-redirect',
    'swagger_ui_init_oauth': None,
    'openapi_tags': [
        {
            'name': 'default',
            'description': 'Operations to validate the API well functioning'
        },
    ]
}

CORS_CONFIGS = {
    "allow_origins": [
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}