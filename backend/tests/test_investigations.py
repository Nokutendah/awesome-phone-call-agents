from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_investigation():
    # 1. Create investigation
    mission_text = "Call ABC Bakery and ask if they make gluten-free wedding cakes."
    response = client.post("/api/investigations", json={"mission": mission_text})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["mission"] == mission_text
    assert data["status"] in ["draft", "ready", "needs_user_input"]
    investigation_id = data["id"]

    # 2. Fetch created investigation by ID
    get_res = client.get(f"/api/investigations/{investigation_id}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["id"] == investigation_id
    assert get_data["mission"] == mission_text

    # 3. Start investigation
    start_res = client.post(
        f"/api/investigations/{investigation_id}/start",
        json={"phone_number": "(555) 019-2834", "target_name": "ABC Bakery"}
    )
    assert start_res.status_code == 200
    start_data = start_res.json()
    assert start_data["status"] == "dialing"
    assert start_data["phone_number"] == "(555) 019-2834"
    assert start_data["target_name"] == "ABC Bakery"

    # 4. List all investigations
    list_res = client.get("/api/investigations")
    assert list_res.status_code == 200
    all_items = list_res.json()
    assert len(all_items) >= 1
    assert any(item["id"] == investigation_id for item in all_items)
