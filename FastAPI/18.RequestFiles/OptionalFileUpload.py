from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    """
    Upload a file as raw bytes (optional).

    Args:
        file (bytes | None): File content received via multipart/form-data.
                             Can be None if no file is sent.

    Returns:
        dict:
            - If file is provided → returns file size
            - If no file → returns message
    """
    if not file:
        return {"message": "No file sent"}  # No file provided
    else:
        return {"file_size": len(file)}  # Size of uploaded file


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    """
    Upload a file using UploadFile (optional).

    Args:
        file (UploadFile | None): Uploaded file object.
                                 Can be None if no file is sent.

    Returns:
        dict:
            - If file is provided → returns filename
            - If no file → returns message

    Note:
        UploadFile is more efficient for large files.
    """
    if not file:
        return {"message": "No upload file sent"}  # No file provided
    else:
        return {"filename": file.filename}  # Return file name