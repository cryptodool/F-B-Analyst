from pathlib import Path
  import pandas as pd
  from .base import chunk_text

  def parse_tabular(path: Path) -> list[str]:
      try:
          if path.suffix.lower() == ".csv":
              df = pd.read_csv(path)
          else:
              df = pd.read_excel(path)
      except Exception as exc:
          return [f"Failed to parse table: {exc}"]

      df = df.fillna("")
      text_rows = []
      for _, row in df.iterrows():
          row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
          text_rows.append(row_text)
      full_text = "\n".join(text_rows)
      return chunk_text(full_text)
