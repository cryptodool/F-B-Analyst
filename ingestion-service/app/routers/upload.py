from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from uuid import uuid4
from pathlib import Path

from ..auth import verify_api_key
from ..config import settings
from ..storage import base_path
from ..parsers import parse_file
from ..embedding import upsert_embedding

router = APIRouter(prefix="/upload", dependencies=[Depends(verify_api_key)])

MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid4())
    suffix = Path(file.filename).suffix.lower() or ".dat"
    stored_path = base_path / f"{doc_id}{suffix}"

    size = 0
    chunk_size = 1024 * 1024  # 1MB

    with stored_path.open("wb") as out:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_BYTES:
                stored_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File too large",
                )
            out.write(chunk)

    chunks = parse_file(stored_path)
    metadata = {
        "doc_id": doc_id,
        "filename": file.filename,
        "extension": suffix,
    }
    upsert_embedding(doc_id, chunks, metadata)

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "chunks": len(chunks),
    }
