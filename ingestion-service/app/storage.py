# ingestion-service/app/storage.py
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from .config import settings

# Root of all persisted files (defaults to /data/uploads)
base_path = Path(settings.STORAGE_PATH).resolve()
base_path.mkdir(parents=True, exist_ok=True)

def file_path(name: str) -> Path:
    """Return absolute path for a file under base_path and ensure parent dirs exist."""
    p = base_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

async def save_uploadfile(upload: UploadFile, dest_name: Optional[str] = None) -> str:
    """Save a FastAPI UploadFile to storage; returns stored relative name."""
    name = dest_name or (upload.filename or "uploaded_file")
    dest = file_path(name)
    content = await upload.read()
    dest.write_bytes(content)
    return name

def save_bytes(name: str, data: bytes) -> str:
    """Save raw bytes to storage; returns stored relative name."""
    file_path(name).write_bytes(data)
    return name

def read_bytes(name: str) -> bytes:
    """Read a stored file as bytes."""
    return file_path(name).read_bytes()

def list_files() -> list[dict]:
    """List stored files with basic metadata."""
    items: list[dict] = []
    for p in base_path.rglob("*"):
        if p.is_file():
            st = p.stat()
            items.append({
                "name": str(p.relative_to(base_path)),
                "size": st.st_size,
                "modified": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            })
    return items

