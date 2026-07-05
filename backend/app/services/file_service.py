import hashlib
import magic
from pathlib import Path


def get_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_info(file_path: Path):
    return {
        "filename": file_path.name,
        "extension": file_path.suffix,
        "size": file_path.stat().st_size,
        "mime_type": magic.from_file(str(file_path), mime=True),
        "sha256": get_sha256(file_path),
    }