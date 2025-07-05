# app/main.py
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import os

# Initialize FastAPI app
app = FastAPI(title="ACME Job Success Predictor API")

# Define the path to the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')

# Load the trained model pipeline from the .pkl file
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    # This is a fallback for environments where the model isn't found
    model = None
    print(f"Warning: Model file not found at {MODEL_PATH}")


# Define the input data structure using Pydantic for validation
class JobFeatures(BaseModel):
    job_type: str
    job_priority: str
    engineer_skill_level: int
    engineer_experience_years: int
    distance_km: float

    class Config:
        schema_extra = {
            "example": {
                "job_type": "Plumbing",
                "job_priority": "High",
                "engineer_skill_level": 3,
                "engineer_experience_years": 5,
                "distance_km": 15.5
            }
        }

# Root endpoint for health check
@app.get("/")
def read_root():
    """ A simple health check endpoint. """
    return {"status": "ok", "message": "Welcome to the ACME Prediction API!"}

# Prediction endpoint
@app.post("/predict")
def predict(features: JobFeatures):
    """
    Predicts the success of a job based on input features.
    """
    if model is None:
        return {"error": "Model is not loaded. Cannot make predictions."}, 503

    # Convert input data to a pandas DataFrame
    # The model pipeline expects a DataFrame as input
    input_df = pd.DataFrame([features.dict()])

    # Make a prediction
    # The result is an array, so we get the first element
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]

    # Return the result as JSON
    return {
        "prediction": int(prediction),
        "prediction_label": "Success" if int(prediction) == 1 else "Failure",
        "probability_success": float(prediction_proba[1]),
        "probability_failure": float(prediction_proba[0])
    }