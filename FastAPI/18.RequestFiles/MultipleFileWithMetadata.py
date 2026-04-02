from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    """
    Upload multiple files and read them as raw bytes.

    Args:
        files (list[bytes]): List of file contents.

    Returns:
        dict: Sizes of all uploaded files.

    Note:
        - All files are loaded بالكامل into memory
        - Suitable only for small files
    """
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    """
    Upload multiple files using UploadFile.

    Args:
        files (list[UploadFile]): List of uploaded file objects.

    Returns:
        dict: Filenames of uploaded files.

    Note:
        - More memory efficient (streaming)
        - Recommended for large files
    """
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    """
    Serve a simple HTML page with file upload forms.

    Returns:
        HTMLResponse: HTML content with two forms:
            - Upload multiple files as bytes
            - Upload multiple files as UploadFile

    Note:
        - `multiple` attribute allows selecting multiple files
        - `enctype="multipart/form-data"` is required for file uploads
    """
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)