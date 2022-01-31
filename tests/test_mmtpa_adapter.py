from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/api/v1/healthcheck")
async def read_main():
    return "OK"

@app.post("/api/v1/query")
async def query():
    return [{"event_date": "20210105"}]


client = TestClient(app)


def test_read_main():
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == "OK"

def test_query():
    response = client.post(
        "/api/v1/query",
        json={
            "type": "service_account",
            "date": "20210105",
            "projet_id": "test-project",
            "private_key_id": "test",
            "private_key": "testkey",
            "client_email": "test@test.com",
            "client_id": "test",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "ttps://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "test",
            "client_x509_cert_url": "test"
        }
    )
    assert response.status_code == 200
    assert response.json() == [{"event_date": "20210105"}]