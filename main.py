import os
import sys
import time

print("🚀 Starting container...")
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("Listing current directory:", os.listdir("."))
time.sleep(2)

try:
    from fastapi import FastAPI
    from apis.upload_sa import router as upload_router
except Exception as e:
    print("❌ Import failed:", e)
    time.sleep(30)  # keep alive long enough to see logs
    raise e

print("✅ Imports successful")

app = FastAPI(title="GCP Secret Manager API")

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(upload_router, prefix="/api/upload", tags=["Upload SA"])
print("✅ FastAPI app loaded")

time.sleep(2)
