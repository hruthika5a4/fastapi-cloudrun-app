from fastapi import FastAPI
from apis.upload_sa import router as upload_router

app = FastAPI(title="GCP Secret Manager API")

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(upload_router, prefix="/api/upload", tags=["Upload SA"])
