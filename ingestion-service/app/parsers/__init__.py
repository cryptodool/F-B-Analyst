from pathlib import Path
  from . import tabular, document, image, archive

  def parse_file(path: Path) -> list[str]:
      suffix = path.suffix.lower()
      if suffix in [".csv", ".xls", ".xlsx"]:
          return tabular.parse_tabular(path)
      if suffix in [".txt", ".md", ".docx", ".pdf"]:
          return document.parse_document(path)
      if suffix in [".png", ".jpg", ".jpeg"]:
          return image.parse_image(path)
      if suffix == ".zip":
          return archive.parse_archive(path)
      return []

