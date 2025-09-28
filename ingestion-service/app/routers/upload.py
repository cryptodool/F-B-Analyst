from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
  from uuid import uuid4
  from pathlib import Path
  import shutil

  from ..auth import verify_api_key
  from ..config import settings
  from ..storage import base_path
  from ..parsers import parse_file
  from ..embedding import upsert_embedding

  router = APIRouter(prefix="/upload", dependencies=[Depends(verify_api_key)])

  @router.post("")
  async def upload_file(file: UploadFile = File(...)):
      if file.size and file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
          raise HTTPException(
              status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
              detail="File too large",
          )

      doc_id = str(uuid4())
      suffix = Path(file.filename).suffix.lower() or ".dat"

      stored_path = base_path / f"{doc_id}{suffix}"
      with stored_path.open("wb") as out:
          shutil.copyfileobj(file.file, out)

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
