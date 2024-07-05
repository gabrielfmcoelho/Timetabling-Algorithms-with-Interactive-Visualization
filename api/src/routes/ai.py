from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from fastapi.responses import FileResponse
from typing import Annotated

import os

from logs.logger import Logger
from machine_learning.models_interface import ModelsInterface
from models.timetable_request import TimetableRequestData


router = APIRouter(
    prefix='/service',
    tags=['Service'],
)

logger = Logger().get_logger()


env_mode = os.getenv("MODE", "dev")


@router.post(
    "/ai/{model_id}",
    description="This endpoint receives a data to be processed by a machine learning model, the model_id is used to select the model to be used.",
    status_code=status.HTTP_200_OK
)
async def ocr_essay_image(
    request_data: TimetableRequestData,
    model_id: Annotated[str, "The model id to be used. 'model_a'."] = "model_a",
):
    """
    This endpoint receives receives a data to be processed by a machine learning model, the model_id is used to select the model to be used.
    """
    logger.info(f"Route /service/ai/{model_id} called by user.")
    try:
        if env_mode == "prod":
            response = ModelsInterface.run(model_id, "timetabling", request_data.model_dump())
        else:
            response = {"timetable": "not implemented yet"}
        return {"data": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    