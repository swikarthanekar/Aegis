from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.engines.analyzers.factory import get_analyzer
from app.services.file_service import get_file_info

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    destination = UPLOAD_DIR / file.filename

    with open(destination, "wb") as buffer:
        buffer.write(await file.read())

    metadata = get_file_info(destination)

    analyzer = get_analyzer(destination)

    analysis = (
        analyzer.analyze(destination)
        if analyzer
        else {"status": "No analyzer available"}
    )

    return {
        "metadata": metadata,
        "analysis": analysis,
    }