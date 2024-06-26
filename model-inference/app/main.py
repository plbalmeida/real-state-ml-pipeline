from fastapi import FastAPI, HTTPException, Header, Request
import pandas as pd
import joblib
import os
import logging
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

app = FastAPI()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa 401
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


@app.get("/")
def read_root():
    """Root endpoint of the API.

    Returns:
        dict: A message indicating that the inference API is running.
    """
    return {"message": "Model inference API"}


@app.post("/predict")
async def predict(request: Request, data: dict, api_key: str = Header(None, alias='X-API-Key')):  # noqa 401
    """Make predictions using the trained model.

    Args:
        request (Request): The incoming request object.
        data (dict): The input data for prediction.
        api_key (str): The API key from the request header.

    Returns:
        dict: The prediction results or an error message if the model is not loaded.
    """  # noqa 401
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

    input_df = pd.DataFrame([data])
    logger.info(f"Input Data: {data}")

    try:
        prediction = model_pipeline.predict(input_df)
        logger.info(f"Prediction: {prediction.tolist()}")
        return {"prediction": prediction.tolist()}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")
