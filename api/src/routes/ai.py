from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Annotated

from logs.logger import Logger
from machine_learning.models_interface import ModelsInterface
from models.ai import RequestAiData


router = APIRouter(
    prefix='/service',
    tags=['Service'],
)

logger = Logger().get_logger()


@router.post(
    "/ai/{model_id}",
    description="This endpoint receives a data to be processed by a machine learning model, the model_id is used to select the model to be used.",
)
async def ocr_essay_image(
    request_data: RequestAiData,
    model_id: Annotated[str, "The model id to be used. 'model_a'."] = "model_a",
):
    """
    This endpoint receives receives a data to be processed by a machine learning model, the model_id is used to select the model to be used.
    """
    logger.info(f"Route /service/ai/{model_id} called by user.")
    try:
        response = ModelsInterface.run(model_id, request_data.content)
        return {"ocr_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    