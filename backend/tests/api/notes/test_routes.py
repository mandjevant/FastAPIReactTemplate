def test_create_note(client, test_user_headers):
    response = client.post(
        "/api/v1/notes/",
        json={"title": "Test Note", "content": "Test Content"},
        headers=test_user_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"
    assert "id" in data


def test_read_notes(client, test_user_headers):
    # Create a note first
    client.post(
        "/api/v1/notes/",
        json={"title": "Note 1", "content": "Content 1"},
        headers=test_user_headers,
    )
    response = client.get("/api/v1/notes/", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_note(client, test_user_headers):
    # Create a note first
    create_resp = client.post(
        "/api/v1/notes/",
        json={"title": "Note 2", "content": "Content 2"},
        headers=test_user_headers,
    )
    note_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/notes/{note_id}", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Note 2"


def test_read_note_not_found(client, test_user_headers):
    response = client.get("/api/v1/notes/9999", headers=test_user_headers)
    assert response.status_code == 404


def test_delete_note(client, test_user_headers):
    # Create a note first
    create_resp = client.post(
        "/api/v1/notes/",
        json={"title": "Note 3", "content": "Content 3"},
        headers=test_user_headers,
    )
    note_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/notes/{note_id}", headers=test_user_headers)
    assert response.status_code == 204


def test_delete_note_not_found(client, test_user_headers):
    response = client.delete("/api/v1/notes/9999", headers=test_user_headers)
    assert response.status_code == 404
