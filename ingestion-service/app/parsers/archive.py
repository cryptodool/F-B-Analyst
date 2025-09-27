from pathlib import Path
  import tempfile
  import zipfile

  from . import tabular, document, image

  def parse_archive(path: Path) -> list[str]:
      chunks = []
      with tempfile.TemporaryDirectory() as tmpdir:
          with zipfile.ZipFile(str(path), "r") as zf:
              zf.extractall(tmpdir)
          for extracted in Path(tmpdir).rglob("*"):
              if extracted.is_dir():
                  continue
              chunks.extend(parse_by_extension(extracted))
      return chunks

  # helper to reuse logic
  def parse_by_extension(path: Path) -> list[str]:
      suffix = path.suffix.lower()
      if suffix in [".csv", ".xls", ".xlsx"]:
          return tabular.parse_tabular(path)
      if suffix in [".txt", ".md", ".docx", ".pdf"]:
          return document.parse_document(path)
      if suffix in [".png", ".jpg", ".jpeg"]:
          return image.parse_image(path)
      return []

