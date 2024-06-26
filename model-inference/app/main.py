import os
import logging
from datetime import datetime
from typing import List

import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Model Inference API",
    description="API for making predictions using a pre-trained model.",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa401
logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join('/models', 'trained_model.joblib')
API_KEY = os.getenv('API_KEY')

logger.info(f"Checking if model exists at {MODEL_PATH}")
if os.path.exists(MODEL_PATH):
    logger.info("Model found. Loading the model.")
    model_pipeline = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
else:
    logger.error(f"Model not found at {MODEL_PATH}")
    model_pipeline = None


class PredictionRequest(BaseModel):
    type: str = Field(..., example="house", description="The type of the property.")  # noqa401
    sector: str = Field(..., example="urban", description="The sector where the property is located.")  # noqa401
    net_usable_area: float = Field(..., example=120.0, description="Net usable area of the property.")  # noqa401
    net_area: float = Field(..., example=150.0, description="Total net area of the property.")  # noqa401
    n_rooms: int = Field(..., example=3, description="Number of rooms in the property.")  # noqa401
    n_bathroom: int = Field(..., example=2, description="Number of bathrooms in the property.")  # noqa401
    latitude: float = Field(..., example=40.7128, description="Latitude coordinate of the property.")  # noqa401
    longitude: float = Field(..., example=-74.0060, description="Longitude coordinate of the property.")  # noqa401


class PredictionResponse(BaseModel):
    prediction: List[float] = Field(..., example=[10450.683126723623], description="The predicted value(s).")  # noqa401


@app.get("/", summary="Root Endpoint", description="Returns a message indicating that the inference API is running.", tags=["Root"])  # noqa401
def read_root():
    """Root endpoint of the API.

    Returns:
        dict: A message indicating that the inference API is running.
    """
    return {"message": "Model inference API"}


@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Make Prediction",
    description="Make predictions using the trained model. You must provide a valid API key in the `X-API-Key` header.",  # noqa401
    tags=["Prediction"],
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "net_area"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        403: {
            "description": "Invalid API Key",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid API Key"}
                }
            }
        },
        500: {
            "description": "Prediction error",
            "content": {
                "application/json": {
                    "example": {"detail": "Prediction error"}
                }
            }
        }
    }
)
async def predict(request: Request, data: PredictionRequest, api_key: str = Header(None, alias='X-API-Key')):  # noqa401
    """Make predictions using the trained model.

    This endpoint receives the data of a property and returns the predicted value(s).

    Args:
        request (Request): The incoming request object.
        data (PredictionRequest): The input data for prediction.
        api_key (str): The API key from the request header.

    Returns:
        PredictionResponse: The prediction results or an error message if the model is not loaded.

    Raises:
        HTTPException: If the API key is invalid or if there is an error during prediction.
    """  # noqa401
    request_time = datetime.utcnow().isoformat()
    logger.info(f"Received API Key: {api_key}")
    logger.info(f"Expected API Key: {API_KEY}")
    logger.info(f"Request Time: {request_time}")
    logger.info(f"Request Client: {request.client.host}")

    if api_key != API_KEY:
        logger.error("Invalid API Key")
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if model_pipeline is None:
        logger.error("Model is not loaded")
        return {"message": "Model is not loaded"}

    input_df = pd.DataFrame([data.dict()])
    logger.info(f"Input Data: {data.dict()}")

    try:
        prediction = model_pipeline.predict(input_df)
        logger.info(f"Prediction: {prediction.tolist()}")
        return {"prediction": prediction.tolist()}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")
