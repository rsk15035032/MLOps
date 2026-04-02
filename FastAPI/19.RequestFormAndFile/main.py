from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    """
    Upload files along with form data.

    Args:
        file (bytes): File read بالكامل into memory as raw bytes.
        fileb (UploadFile): File handled as a streaming UploadFile object.
        token (str): Form field (e.g., authentication token).

    Returns:
        dict:
            - file_size: Size of the first file (bytes)
            - token: Submitted form token
            - fileb_content_type: MIME type of the second file

    Note:
        - Combines File() and Form() in a single request
        - Request must use 'multipart/form-data'
        - `file` → loads entire file into memory
        - `fileb` → efficient streaming interface
    """
    return {
        "file_size": len(file),  # Size of first file
        "token": token,  # Form field value
        "fileb_content_type": fileb.content_type,  # Metadata of second file
    }