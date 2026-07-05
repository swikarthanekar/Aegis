from pydantic import BaseModel


class FileInfo(BaseModel):
    filename: str
    extension: str
    size: int
    mime_type: str
    sha256: str