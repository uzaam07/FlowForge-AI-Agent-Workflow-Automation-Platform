def register(client, email="one@example.com"):
    return client.post("/api/auth/register", json={"email":email,"password":"a-strong-password-123"})

def headers(token): return {"Authorization":f"Bearer {token}"}

def test_register_and_login(client):
    response = register(client)
    assert response.status_code == 201
    assert "password_hash" not in str(response.json())
    login = client.post("/api/auth/login", json={"email":"one@example.com","password":"a-strong-password-123"})
    assert login.status_code == 200 and login.json()["access_token"]

def test_weak_password_rejected(client):
    assert client.post("/api/auth/register", json={"email":"x@example.com","password":"short"}).status_code == 422

def test_owner_isolation(client):
    a = register(client, "a@example.com").json()["access_token"]
    b = register(client, "b@example.com").json()["access_token"]
    definition = {"nodes":[{"id":"start","type":"trigger","label":"Start","config":{}},{"id":"end","type":"output","label":"End","config":{}}],"edges":[{"source":"start","target":"end"}]}
    created = client.post("/api/workflows", headers=headers(a), json={"name":"Private","description":"","definition":definition})
    assert created.status_code == 201
    wid = created.json()["id"]
    assert client.get(f"/api/workflows/{wid}", headers=headers(b)).status_code == 404
    assert client.post(f"/api/workflows/{wid}/runs", headers=headers(b), json={"input_data":{}}).status_code == 404
    assert client.get("/api/workflows", headers=headers(b)).json() == []

def test_admin_route_denies_regular_user(client):
    token = register(client).json()["access_token"]
    assert client.get("/api/admin/overview", headers=headers(token)).status_code == 403

def test_bad_token_rejected(client):
    assert client.get("/api/me", headers=headers("invalid")).status_code == 401

def test_cycle_rejected(client):
    token = register(client).json()["access_token"]
    d = {"nodes":[{"id":"a","type":"trigger","label":"A","config":{}},{"id":"b","type":"output","label":"B","config":{}}],"edges":[{"source":"a","target":"b"},{"source":"b","target":"a"}]}
    assert client.post("/api/workflows", headers=headers(token), json={"name":"Cycle","description":"","definition":d}).status_code == 422
