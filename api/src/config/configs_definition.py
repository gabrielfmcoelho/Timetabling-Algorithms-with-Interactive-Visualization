from dataclasses import dataclass
from typing import List, Dict
from icecream import ic


@dataclass
class AppConfigsDefinition:
    # [TODO: DEBUG WHY THE __slots__ IS version was conflicting with the version attribute]
    title: str
    description: str
    version: str = '0.1.0'
    openapi_url: str = '/openapi.json'
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    swagger_ui_oauth2_redirect_url: str = '/docs/oauth2-redirect'
    swagger_ui_init_oauth: str|None = None 
    openapi_tags: List[dict]|None = None

    def __init__(self, mode: str, title: str, version: str|None = None, description: str|None = None, openapi_tags: List[dict]|None = None):
        mod = '' if mode == 'prod' else f'-{mode}'.upper()
        self.title = f"{title.capitalize()}{mod}"
        self.version = version if version else self.version
        self.description = description if description else f"{title.capitalize()}, it's goal is to provide a RESTful API with the necessary endpoints to implement a interface operations."
        default_openapi_tags = [{'name': 'default', 'description': 'Operations to validate the API well functioning'}] # [TODO: CREATE A DEFAULT FACTORY FUNCTION]
        self.openapi_tags = default_openapi_tags + openapi_tags if openapi_tags else default_openapi_tags
        
@dataclass
class CorsConfigsDefinition:
    __slots__ = ['allow_origins', 'allow_credentials', 'allow_methods', 'allow_headers']
    allow_origins: List[str]
    allow_credentials: bool
    allow_methods: List[str]
    allow_headers: List[str]