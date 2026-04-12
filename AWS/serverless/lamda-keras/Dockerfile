# ------------------------------------------------------------------------------
# Base Image (AWS Lambda Python Runtime)
# ------------------------------------------------------------------------------
FROM public.ecr.aws/lambda/python:3.13

# ------------------------------------------------------------------------------
# Environment Variables (improves Python performance & logging)
# ------------------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# ------------------------------------------------------------------------------
# Install Dependencies (layer caching optimization)
# ------------------------------------------------------------------------------
# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ------------------------------------------------------------------------------
# Copy Model & Application Code
# ------------------------------------------------------------------------------
# Place model in /var/task (Lambda working directory)
COPY clothing-model-new.onnx /var/task/
COPY lambda_function.py /var/task/

# ------------------------------------------------------------------------------
# Lambda Handler Entry Point
# ------------------------------------------------------------------------------
CMD ["lambda_function.lambda_handler"]