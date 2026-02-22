import json
import pytest
from fastapi.testclient import TestClient
from Patterns.Singelton.Fapp import app
from pathlib import Path

client = TestClient(app)

payload_file = Path(__file__).parent.parent / "Impl" / "payloads.json"
with open(payload_file) as f:
    test_cases = json.load(f)

@pytest.mark.parametrize("case", test_cases)
def test_operations(case):
    operation = case["operation"]
    payload = case["payload"]
    response = client.post(f"/{operation}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data