from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import os
import joblib
from src.model_pipeline import ModelPipeline


app = FastAPI()


DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'mysql'
DB_NAME = 'db01'

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


@app.get("/")
def read_root():
    """Root endpoint of the API.

    Returns:
        dict: A message indicating that the API is running.
    """
    return {"message": "Model training API"}


@app.get("/train")
def train_model():
    """Train the model using data from the MySQL database.

    This endpoint fetches data from the MySQL database, trains a model using the 
    data, and saves the trained model to the specified path on the host machine.

    Returns:
        dict: A message indicating that the model was trained and saved successfully,
              or indicating that no data was available for training.
    """  # noqa 401
    query = text("SELECT * FROM tb01")

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    if df.empty:
        return {"message": "No data available for training"}

    X = df.drop(columns=["price"])
    y = df["price"]

    categorical_cols = ["type", "sector"]
    target = "price"

    model_pipeline = ModelPipeline(categorical_cols, target)
    model_pipeline.fit(X, y)

    model_path = "/models/trained_model.joblib"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model_pipeline, model_path)

    return {"message": "Model trained and saved successfully"}
