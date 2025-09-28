from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import upload, files, search, query

app = FastAPI(title="Ingestion Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(files.router)
app.include_router(search.router)
app.include_router(query.router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
