import importlib.util
from pathlib import Path

app_file = Path(__file__).resolve().parents[1] / "app.py"
spec = importlib.util.spec_from_file_location("incident_api", app_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

client = module.app.test_client()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_missing_required_fields():
    response = client.post("/incidents", json={})
    assert response.status_code == 400


def test_create_and_list_incidents():
    response = client.post(
        "/incidents",
        json={"title": "CI test", "status": "open"}
    )
    assert response.status_code == 201

    response = client.get("/incidents")
    assert response.status_code == 200
    assert any(row["title"] == "CI test" for row in response.get_json())
