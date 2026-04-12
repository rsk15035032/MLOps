"""
ONNX Image Classification Inference Pipeline (Production-Ready)
--------------------------------------------------------------

Key Features:
- Clean separation of concerns (preprocessing, inference, handler)
- Type safety with hints
- Robust error handling
- Optimized ONNX runtime usage
- Fully documented for maintainability (FAANG-level standard)

Assumptions:
- Model expects input in PyTorch format (NCHW, normalized)
- Input image is fetched via URL
"""

from typing import Dict, List, Any
import logging

import numpy as np
import onnxruntime as ort
from keras_image_helper import create_preprocessor


# ------------------------------------------------------------------------------
# Logging Configuration (critical for production debugging)
# ------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Constants (centralized config improves maintainability)
# ------------------------------------------------------------------------------
MODEL_PATH: str = "clothing-model-new.onnx"

# Standard ImageNet normalization values (used by most pretrained PyTorch models)
IMAGENET_MEAN: np.ndarray = np.array([0.485, 0.456, 0.406])
IMAGENET_STD: np.ndarray = np.array([0.229, 0.224, 0.225])

# Model input size
TARGET_SIZE = (224, 224)

# Class labels (order MUST match model output)
CLASSES: List[str] = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt",
]


# ------------------------------------------------------------------------------
# Preprocessing Function
# ------------------------------------------------------------------------------
def preprocess_pytorch(x: np.ndarray) -> np.ndarray:
    """
    Preprocess input image tensor for PyTorch-based ONNX model.

    Steps:
    1. Scale pixel values from [0, 255] → [0, 1]
    2. Convert layout NHWC → NCHW (required by PyTorch models)
    3. Normalize using ImageNet statistics

    Args:
        x (np.ndarray):
            Input image array
            Shape: (batch, height, width, channels)
            dtype: float32 or uint8

    Returns:
        np.ndarray:
            Preprocessed tensor
            Shape: (batch, channels, height, width)
            dtype: float32
    """

    # Ensure float32 for numerical stability
    x = x.astype(np.float32)

    # Step 1: Normalize pixel range
    x /= 255.0

    # Step 2: Convert NHWC → NCHW
    x = np.transpose(x, (0, 3, 1, 2))

    # Step 3: Normalize using broadcasting
    # Reshape mean/std to match NCHW format
    mean = IMAGENET_MEAN.reshape(1, 3, 1, 1)
    std = IMAGENET_STD.reshape(1, 3, 1, 1)

    x = (x - mean) / std

    return x


# ------------------------------------------------------------------------------
# Preprocessor Initialization (reused across requests)
# ------------------------------------------------------------------------------
preprocessor = create_preprocessor(
    preprocess_pytorch,
    target_size=TARGET_SIZE
)


# ------------------------------------------------------------------------------
# ONNX Runtime Session Initialization (IMPORTANT: done once)
# ------------------------------------------------------------------------------
def create_session(model_path: str) -> ort.InferenceSession:
    """
    Create ONNX Runtime session with optimized settings.

    Why this matters:
    - Session creation is expensive → reuse across invocations
    - Enables performance optimizations

    Args:
        model_path (str): Path to ONNX model

    Returns:
        ort.InferenceSession
    """

    # Session options for performance tuning
    session_options = ort.SessionOptions()

    # Graph optimization (important for latency)
    session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    # Create session
    session = ort.InferenceSession(
        model_path,
        sess_options=session_options,
        providers=["CPUExecutionProvider"],  # Change to CUDA if GPU available
    )

    logger.info("ONNX session created successfully")

    return session


# Initialize session once (cold start optimization)
session = create_session(MODEL_PATH)

# Cache input/output names (avoids repeated lookup overhead)
INPUT_NAME: str = session.get_inputs()[0].name
OUTPUT_NAME: str = session.get_outputs()[0].name


# ------------------------------------------------------------------------------
# Prediction Function
# ------------------------------------------------------------------------------
def predict(image_url: str) -> Dict[str, float]:
    """
    Perform inference on an image URL.

    Pipeline:
    URL → Image → Preprocess → ONNX Inference → Postprocess

    Args:
        image_url (str): Public image URL

    Returns:
        Dict[str, float]: Class probabilities
    """

    try:
        # Step 1: Load and preprocess image
        x = preprocessor.from_url(image_url)

        # Step 2: Run inference
        outputs = session.run(
            [OUTPUT_NAME],
            {INPUT_NAME: x}
        )

        # Step 3: Extract predictions
        predictions = outputs[0][0]  # shape: (num_classes,)

        # Convert to Python list for serialization
        predictions = predictions.tolist()

        # Step 4: Map class labels to probabilities
        result = dict(zip(CLASSES, predictions))

        return result

    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise RuntimeError("Prediction failed") from e


# ------------------------------------------------------------------------------
# AWS Lambda Handler (Entry Point)
# ------------------------------------------------------------------------------
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda entry point.

    Expected event format:
    {
        "url": "https://example.com/image.jpg"
    }

    Args:
        event (dict): Lambda event payload
        context: Lambda runtime context

    Returns:
        dict: Prediction result or error response
    """

    try:
        # Validate input
        if "url" not in event:
            raise ValueError("Missing 'url' in request")

        image_url: str = event["url"]

        # Run prediction
        result = predict(image_url)

        return {
            "statusCode": 200,
            "body": result
        }

    except Exception as e:
        logger.exception("Lambda execution failed")

        return {
            "statusCode": 500,
            "error": str(e)
        }