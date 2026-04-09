"""
ONNX Image Classification Inference Pipeline
--------------------------------------------

- Framework: ONNX Runtime
- Preprocessing: Custom PyTorch-style normalization
- Input: Image URL
- Output: Class probabilities

Designed for:
- AWS Lambda deployment
- Scalable inference APIs
"""

import numpy as np
import onnxruntime as ort
from keras_image_helper import create_preprocessor


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MODEL_PATH = "clothing-model-new.onnx"

# Standard ImageNet normalization values (used in PyTorch models)
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406])
IMAGENET_STD = np.array([0.229, 0.224, 0.225])

# Class labels for prediction mapping
CLASSES = [
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


# -------------------------------------------------------------------
# Preprocessing Function
# -------------------------------------------------------------------

def preprocess_image(
    X: np.ndarray,
    mean: np.ndarray = IMAGENET_MEAN,
    std: np.ndarray = IMAGENET_STD,
) -> np.ndarray:
    """
    Preprocess input image for ONNX model (PyTorch-style).

    Steps:
    1. Scale pixel values to [0, 1]
    2. Convert NHWC → NCHW format
    3. Normalize using mean and std

    Args:
        X (np.ndarray): Input image array of shape (B, H, W, C)

    Returns:
        np.ndarray: Preprocessed tensor of shape (B, C, H, W)
    """

    # Normalize pixel values from [0, 255] → [0, 1]
    X = X / 255.0

    # Convert layout: NHWC → NCHW (required for PyTorch models)
    X = X.transpose(0, 3, 1, 2)

    # Reshape mean and std for broadcasting
    mean = mean.reshape(1, 3, 1, 1)
    std = std.reshape(1, 3, 1, 1)

    # Apply normalization
    X = (X - mean) / std

    return X.astype(np.float32)


# -------------------------------------------------------------------
# Model Loader
# -------------------------------------------------------------------

def load_model(model_path: str = MODEL_PATH):
    """
    Load ONNX model and return session with input/output names.
    """

    session = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"]  # Change to CUDA if needed
    )

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    return session, input_name, output_name


# -------------------------------------------------------------------
# Prediction Pipeline
# -------------------------------------------------------------------

class ImageClassifier:
    """
    Encapsulates preprocessing + inference logic.
    """

    def __init__(self, model_path: str = MODEL_PATH, classes: list = CLASSES):
        self.session, self.input_name, self.output_name = load_model(model_path)
        self.classes = classes

        # Create reusable preprocessor
        self.preprocessor = create_preprocessor(
            preprocess_image,
            target_size=(224, 224)
        )

    def predict_from_url(self, url: str) -> dict:
        """
        Run inference on an image URL.

        Args:
            url (str): Image URL

        Returns:
            dict: Class → probability mapping
        """

        # Load and preprocess image
        X = self.preprocessor.from_url(url)

        # Run inference
        outputs = self.session.run(
            [self.output_name],
            {self.input_name: X}
        )

        # Convert output to Python list
        predictions = outputs[0][0].tolist()

        # Map predictions to class labels
        return dict(zip(self.classes, predictions))


# -------------------------------------------------------------------
# AWS Lambda Entry Point
# -------------------------------------------------------------------

# Initialize model globally (warm start optimization)
classifier = ImageClassifier()


def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda handler.

    Expected event:
    {
        "url": "https://example.com/image.jpg"
    }
    """

    # Extract input
    url = event.get("url")

    if not url:
        return {"error": "Missing 'url' in request"}

    # Run prediction
    result = classifier.predict_from_url(url)

    return result