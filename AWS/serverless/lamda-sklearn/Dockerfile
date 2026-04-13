FROM public.ecr.aws/lambda/python:3.13

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Export and install dependencies
RUN uv export --format requirements-txt > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY lambda_function.py model.bin ./

# Lambda entrypoint
CMD ["lambda_function.lambda_handler"]