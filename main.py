from fastapi import FastAPI
from apis.upload_sa import router as upload_router

print("✅ main.py is being executed...")  # 👈 debug log

app = FastAPI(title="GCP Secret Manager API")

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(upload_router, prefix="/api/upload", tags=["Upload SA"])
