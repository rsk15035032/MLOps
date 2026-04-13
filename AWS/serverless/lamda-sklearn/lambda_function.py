import pickle
import logging
from typing import Dict, Any

# ----------------------------------------
# Logging Configuration
# ----------------------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ----------------------------------------
# Constants
# ----------------------------------------
MODEL_PATH = "model.bin"
THRESHOLD = 0.5
MODEL_VERSION = "v1.0"

# ----------------------------------------
# Load Model (Executed Once - Cold Start)
# ----------------------------------------
try:
    with open(MODEL_PATH, "rb") as f:
        pipeline = pickle.load(f)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    pipeline = None


# ----------------------------------------
# Prediction Logic
# ----------------------------------------
def predict_single(customer: Dict[str, Any]) -> float:
    """
    Predict churn probability for a single customer.
    """
    prob = pipeline.predict_proba(customer)[0, 1]
    return float(prob)


# ----------------------------------------
# Lambda Handler
# ----------------------------------------
def lambda_handler(event, context):
    """
    AWS Lambda entrypoint.
    """

    try:
        logger.info(f"Received event: {event}")

        customer = event.get("customer")

        if not customer:
            return {
                "statusCode": 400,
                "error": "Missing 'customer' field in request"
            }

        prob = predict_single(customer)

        response = {
            "churn_probability": prob,
            "churn": prob >= THRESHOLD,
            "model_version": MODEL_VERSION
        }

        logger.info(f"Prediction result: {response}")

        return {
            "statusCode": 200,
            "body": response
        }

    except Exception as e:
        logger.error(f"Error during prediction: {e}")

        return {
            "statusCode": 500,
            "error": str(e)
        }