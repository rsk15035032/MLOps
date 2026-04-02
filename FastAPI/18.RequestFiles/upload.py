from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    """
    Upload a file and read it بالكامل into memory as bytes.

    Args:
        file (bytes): File content received via multipart/form-data.

    Returns:
        dict: Size of the uploaded file in bytes.

    Note:
        - Entire file is loaded into memory
        - Suitable for small files only
    """
    return {"file_size": len(file)}  # Length of file content


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    """
    Upload a file using UploadFile (streaming interface).

    Args:
        file (UploadFile): Uploaded file object with metadata.

    Returns:
        dict: Name of the uploaded file.

    Note:
        - Uses a file-like object (SpooledTemporaryFile)
        - More efficient for large files
        - Supports async read/write operations
    """
    return {"filename": file.filename}  # Access file metadata