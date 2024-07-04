from pydantic import BaseModel, Field
from typing import List, Optional


class RequestAiData(BaseModel):
    content: dict = Field(..., description="The data to be processed by the model.")