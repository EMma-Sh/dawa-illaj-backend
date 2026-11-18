def signup(client, email="a@example.com", role="patient", password="password123"):
    return client.post("/auth/signup", json={
        "email": email, "password": password,
        "full_name": "Test User", "role": role,
    })


def test_signup_cannot_create_admin(client):
    assert signup(client, role="admin").status_code == 422


def test_signup_patient_ok_and_no_password_in_response(client):
    r = signup(client)
    assert r.status_code == 201
    assert "password" not in r.text
    assert r.json()["is_approved"] is True


def test_duplicate_email_returns_409(client):
    signup(client)
    assert signup(client).status_code == 409