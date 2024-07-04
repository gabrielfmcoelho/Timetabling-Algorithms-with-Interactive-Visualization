from dotenv import load_dotenv
import os

from config.configs_definition import AppConfigsDefinition, CorsConfigsDefinition


load_dotenv()


if not os.environ.get("MODE") or os.environ.get("MODE") not in ['dev', 'prod']:
    raise ValueError("MODE not found in .env or it's value is not 'dev' or 'prod'")
if not os.environ.get("PROJECT_NAME"):
    raise ValueError("Main env var PROJECT_NAME not found in .env")

APP_CONFIGS = AppConfigsDefinition(
    mode=os.environ.get("MODE"),
    title=os.environ.get("PROJECT_NAME"),
    version=os.environ.get("VERSION"),
    description=f"{os.environ.get('PROJECT_NAME')}, it's goal is to provide a RESTful API with the necessary endpoints to implement a interface operations for the {os.environ.get('PROJECT_NAME')} project."
)


if not os.environ.get("CORS_ALLOW_ORIGINS") or not os.environ.get("CORS_ALLOW_CREDENTIALS") or not os.environ.get("CORS_ALLOW_METHODS") or not os.environ.get("CORS_ALLOW_HEADERS"):
    raise ValueError("CORS env vars not found in .env")

CORS_CONFIGS = CorsConfigsDefinition(
    allow_origins=os.environ.get("CORS_ALLOW_ORIGINS").split(','),
    allow_credentials=os.environ.get("CORS_ALLOW_CREDENTIALS"),
    allow_methods=os.environ.get("CORS_ALLOW_METHODS").split(','),
    allow_headers=os.environ.get("CORS_ALLOW_HEADERS").split(',')
)