from fastapi import APIRouter, UploadFile, File, HTTPException
from google.cloud import secretmanager
import json
import os

router = APIRouter()

@router.post("/sa-file")
async def upload_sa_file(file: UploadFile = File(...)):
    """
    Upload a service account file and save it in Secret Manager.
    """
    try:
        # read uploaded file
        contents = await file.read()
        data = json.loads(contents)

        secret_id = os.path.splitext(file.filename)[0]
        project_id = os.environ.get("PROJECT_ID")

        if not project_id:
            raise HTTPException(status_code=400, detail="PROJECT_ID not set in environment variables.")

        client = secretmanager.SecretManagerServiceClient()
        parent = f"projects/{project_id}"

        # Create a new secret (if not exists)
        try:
            client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
        except Exception:
            # Secret might already exist
            pass

        # Add secret version
        client.add_secret_version(
            request={
                "parent": f"{parent}/secrets/{secret_id}",
                "payload": {"data": contents},
            }
        )

        return {"message": f"Service account saved to Secret Manager as '{secret_id}'."}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
