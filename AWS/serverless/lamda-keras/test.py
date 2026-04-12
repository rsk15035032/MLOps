"""
Lambda Inference Client (Production-Grade)
-----------------------------------------

Purpose:
- Send HTTP request to local AWS Lambda runtime
- Handle failures gracefully
- Provide observability (logs + timing)

Why this matters:
- In real systems, network calls fail frequently
- You must design for retries, timeouts, and debugging
"""

from typing import Dict, Any
import requests
import logging
import time


# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Constants (centralized config)
# ------------------------------------------------------------------------------
LAMBDA_URL: str = "http://localhost:8080/2015-03-31/functions/function/invocations"

# Timeout settings (important to avoid hanging requests)
TIMEOUT_SECONDS: int = 5

# Retry configuration
MAX_RETRIES: int = 3
RETRY_BACKOFF: float = 1.5  # exponential backoff multiplier


# ------------------------------------------------------------------------------
# HTTP Client Function
# ------------------------------------------------------------------------------
def invoke_lambda(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke local Lambda function via HTTP.

    Features:
    - Retries with exponential backoff
    - Timeout protection
    - Structured error handling

    Args:
        payload (dict): Request payload

    Returns:
        dict: Response JSON
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt}: Sending request to Lambda")

            start_time = time.time()

            response = requests.post(
                LAMBDA_URL,
                json=payload,
                timeout=TIMEOUT_SECONDS
            )

            latency = time.time() - start_time
            logger.info(f"Response received in {latency:.3f}s")

            # Raise exception for HTTP errors (4xx, 5xx)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt}")

        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error on attempt {attempt}")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            raise

        # Exponential backoff before retry
        sleep_time = RETRY_BACKOFF ** attempt
        logger.info(f"Retrying in {sleep_time:.2f}s...")
        time.sleep(sleep_time)

    raise RuntimeError("All retry attempts failed")


# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    request_payload = {
        "url": "http://bit.ly/mlbookcamp-pants"
    }

    try:
        result = invoke_lambda(request_payload)

        logger.info("Prediction successful")
        print(result)

    except Exception as e:
        logger.error(f"Request failed: {str(e)}")