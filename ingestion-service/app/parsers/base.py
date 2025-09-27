from pathlib import Path
  from typing import Iterable, List

  CHUNK_SIZE = 800  # adjust token/character length as needed

  def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
      """Split text into overlapping chunks."""
      text = text.strip()
      if not text:
          return []
      chunks = []
      start = 0
      while start < len(text):
          end = start + chunk_size
          chunks.append(text[start:end])
          start += chunk_size
      return chunks

  def detect_category(path: Path) -> str:
      return path.suffix.lower()

