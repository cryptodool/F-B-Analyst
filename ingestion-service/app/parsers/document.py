from pathlib import Path
  from io import BytesIO

  from .base import chunk_text

  def parse_text_file(path: Path) -> list[str]:
      text = path.read_text(errors="ignore")
      return chunk_text(text)

  def parse_docx(path: Path) -> list[str]:
      import docx
      doc = docx.Document(str(path))
      paragraphs = "\n".join(p.text for p in doc.paragraphs)
      return chunk_text(paragraphs)

  def parse_pdf(path: Path) -> list[str]:
      from pdfminer.high_level import extract_text
      text = extract_text(str(path))
      return chunk_text(text)

  def parse_document(path: Path) -> list[str]:
      suffix = path.suffix.lower()
      if suffix in {".txt", ".md"}:
          return parse_text_file(path)
      if suffix == ".docx":
          return parse_docx(path)
      if suffix == ".pdf":
          return parse_pdf(path)
      return []

