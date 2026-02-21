# test_execute.py
import pytest
from fastapi.testclient import TestClient
from Models.models import ActionRequest
from Patterns.Singelton.Fapp import app
from Patterns.Factory.CommandFactory import CommandFactory
from Patterns.Template.ErrorTemplate import AppErrors

client = TestClient(app)

@pytest.mark.parametrize(
    "operation, payload, expected_status",
    [
        ("math", {"type": "solve", "message": ["2*x + 1 = 10"]}, 200),
        ("math", {"type": "expression", "message": ["x + 5"]}, 200),
        ("math", {"type": "matrix_det", "message": [[ [1,2],[3,4] ]]}, 200),
        ("math", {"type": "motion", "message": ["v0=0", "a=2", "t=3"]}, 200),
        ("unknown_op", {"type": "solve", "message": ["2*x + 1 = 10"]}, 404),
        ("math", {"type": "solve", "message": []}, 400),
    ]
)
def test_execute(operation, payload, expected_status):
    req = ActionRequest(**payload)
    response = client.post(f"/{operation}", json=req.dict())
    assert response.status_code == expected_status