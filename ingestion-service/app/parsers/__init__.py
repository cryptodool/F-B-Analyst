# ingestion-service/app/parsers/__init__.py
from typing import Union, Tuple, List, Dict
from pathlib import Path

def parse_file(src: Union[str, Path, object]) -> Tuple[List[str], Dict]:
    """
    Minimal placeholder parser to let the service boot.
    Returns no chunks and basic metadata. Safe to call even if `src` is an UploadFile.
    """
    # Try to get a filename if this is an UploadFile-like object
    name = getattr(src, "filename", None)
    if not name:
        try:
            name = str(src)
        except Exception:
            name = "unknown"

    p = Path(name)
    # Return empty chunks; downstream `upsert_embedding` will no-op on empty lists
    return [], {"name": p.name, "suffix": p.suffix.lower()}
