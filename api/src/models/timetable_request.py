from pydantic import BaseModel, Field
from typing import List, Optional


class TimetableRequestData(BaseModel):
    content: dict = Field(..., description="The data to be processed by the model.")