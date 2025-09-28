# ingestion-service/app/main.py
from fastapi import FastAPI
from .auth import AuthDependency
from .routers import upload, files, search, query

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Protect all routers with the API key dependency
app.include_router(upload.router, dependencies=[AuthDependency])
app.include_router(files.router,  dependencies=[AuthDependency])
app.include_router(search.router, dependencies=[AuthDependency])
app.include_router(query.router,  dependencies=[AuthDependency])
