from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from google.cloud import bigquery
from google.oauth2 import service_account
from .ServiceAccountCredentials import ServiceAccountCredentials
import json
import jwt
import logging

log = logging.getLogger("uvicorn.error")

app = FastAPI()

@app.get("/api/v1/healthcheck")
def healthcheck():
    return "OK"

@app.post("/api/v1/query")
def query(serviceAccountCredentials: ServiceAccountCredentials, response: Response):
    sub,key = jwt.decode(serviceAccountCredentials.private_key, "", algorithms="HS256").values()

    serviceAccountCredentials.private_key = key

    query = f"""
        SELECT * FROM `REDACTED`
    """

    job_config = bigquery.QueryJobConfig(
        use_query_cache=True
    )

    try:
        credentials = service_account.Credentials.from_service_account_info(serviceAccountCredentials.__dict__)

        client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

        query_job = client.query(query, job_config=job_config)

        records = [dict(row) for row in query_job]
        
        return records
    except Exception as e: 
        log.error(f'Unable to query project: {e}')
        return JSONResponse(status_code=500, content={"message": f'Unable to query project: {serviceAccountCredentials.project_id}'})    

if __name__ == "__main__":
    uvicorn.run("mmtpa_adapter:app", host="127.0.0.1", port=5000, log_level="info")

