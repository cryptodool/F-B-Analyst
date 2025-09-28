import os

class Settings:
    API_KEY = os.getenv("INGESTION_API_KEY", "")
    STORAGE_PATH = os.getenv("STORAGE_PATH", "/data/uploads")

    CHROMA_API_KEY = os.getenv("CHROMA_API_KEY", "")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT", "")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "")

    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    MAX_FILE_SIZE_MB = float(os.getenv("MAX_FILE_SIZE_MB", 25))

settings = Settings()
