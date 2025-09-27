from pathlib import Path
  from .base import chunk_text

  def parse_image(path: Path) -> list[str]:
      try:
          from PIL import Image
          import pytesseract
          image = Image.open(str(path))
          text = pytesseract.image_to_string(image)
          return chunk_text(text)
      except Exception as exc:
          return [f"OCR failed: {exc}"]
