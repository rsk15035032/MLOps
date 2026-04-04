from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins (domains that can access this API)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allowed domains
    allow_credentials=True,       # Allow cookies/auth headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)


@app.get("/")
async def main():
    """
    Root endpoint to verify API is running.

    Returns:
        dict: A simple welcome message.

    Purpose:
        - Health check endpoint
        - Basic connectivity test for frontend-backend integration

    Example:
        Request:
            GET /

        Response:
            {
                "message": "Hello World"
            }
    """
    return {"message": "Hello World"}