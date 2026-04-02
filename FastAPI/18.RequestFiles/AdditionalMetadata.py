from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File(description="A file read as bytes")]
):
    """
    Upload a file and read it بالكامل into memory as bytes.

    Args:
        file (bytes): File content received via multipart/form-data.

    Returns:
        dict: Size of the uploaded file in bytes.

    Note:
        - The `description` in File() appears in Swagger UI
        - Entire file is loaded into memory (use for small files)
    """
    return {"file_size": len(file)}  # Return size of file


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[
        UploadFile,
        File(description="A file read as UploadFile")
    ],
):
    """
    Upload a file using UploadFile (streaming interface).

    Args:
        file (UploadFile): Uploaded file object with metadata.

    Returns:
        dict: Name of the uploaded file.

    Note:
        - `description` improves API documentation (Swagger UI)
        - UploadFile is efficient for handling large files
    """
    return {"filename": file.filename}  # Return file name