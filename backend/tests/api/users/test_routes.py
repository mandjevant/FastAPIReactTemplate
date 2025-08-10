"""Test user routes."""

import pytest
import uuid


def test_read_user_me(client, test_user_headers):
    """Test reading the current user's details."""
    response = client.get("/api/v1/users/me", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "full_name" in data


def test_update_user_me(client, test_user_headers):
    """Test updating the current user's details."""
    update_data = {
        "full_name": "Updated User",
        "email": "updatedemail@hotmail.com",
    }
    response = client.patch(
        "/api/v1/users/me", headers=test_user_headers, json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == update_data["email"]


def test_delete_user_me(client, test_user_headers):
    """Test deleting the current user."""
    response = client.delete("/api/v1/users/me", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"


def test_delete_user_me_not_allowed(client, test_admin_headers):
    """Test deleting the current user when not allowed."""
    response = client.delete("/api/v1/users/me", headers=test_admin_headers)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Super users are not allowed to delete themselves"


def test_update_password(client, test_user_headers):
    """Test updating the current user's password."""
    update_data = {
        "current_password": "password",  # pragma: allowlist secret
        "new_password": "newpassword123",  # pragma: allowlist secret
    }
    response = client.post(
        "/api/v1/users/me/password", headers=test_user_headers, json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password updated successfully"


def test_read_user(client, test_user_headers):
    """Test reading a specific user."""
    response = client.get("/api/v1/users/me", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]

    response = client.get(f"/api/v1/users/{user_id}", headers=test_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user_id)


def test_read_user_not_found(client, test_user_headers):
    """Test reading a user that does not exist."""
    user_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{user_id}", headers=test_user_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


def test_list_users(client, test_admin_headers):
    """Test listing users."""
    response = client.get("/api/v1/users/", headers=test_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)
    assert data["count"] == len(data["data"])
    assert data["count"] > 0


def test_list_users_not_allowed(client, test_user_headers):
    """Test listing users when not allowed."""
    response = client.get("/api/v1/users/", headers=test_user_headers)
    assert response.status_code == 403


def test_register_user(client):
    """Test user registration."""
    registration_data = {
        "email": "testingemail@example.com",
        "password": "testpassword123",  # pragma: allowlist secret
        "full_name": "Test User",
    }
    response = client.post("/api/v1/users/signup", json=registration_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == registration_data["email"]


def test_update_user(client, test_admin_headers):
    """Test updating a user."""
    registration_data = {
        "email": "testingemail@example.com",
        "password": "testpassword123",  # pragma: allowlist secret
        "full_name": "Test User",
    }
    response = client.post("/api/v1/users/signup", json=registration_data)
    assert response.status_code == 200

    user_id = response.json()["id"]
    update_data = {
        "email": "updated@example.com",
        "full_name": "Updated User",
    }
    response = client.patch(
        f"/api/v1/users/{user_id}", headers=test_admin_headers, json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == update_data["email"]
    assert data["full_name"] == update_data["full_name"]


def test_update_user_not_allowed(client, test_user_headers):
    """Test updating a user when not allowed."""
    user_id = uuid.uuid4()
    update_data = {
        "email": "updated@example.com",
        "full_name": "Updated User",
    }
    response = client.patch(
        f"/api/v1/users/{user_id}", headers=test_user_headers, json=update_data
    )
    assert response.status_code == 403


def test_delete_user(client, test_admin_headers):
    """Test deleting a user."""
    registration_data = {
        "email": "testingemail@example.com",
        "password": "testpassword123",  # pragma: allowlist secret
        "full_name": "Test User",
    }
    response = client.post("/api/v1/users/signup", json=registration_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.delete(f"/api/v1/users/{user_id}", headers=test_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"


def test_delete_user_not_allowed(client, test_user_headers):
    """Test deleting a user when not allowed."""
    user_id = uuid.uuid4()
    response = client.delete(f"/api/v1/users/{user_id}", headers=test_user_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


def test_delete_user_not_allowed_admin(client, test_admin_headers):
    """Test deleting an admin."""
    response = client.get("/api/v1/users/me", headers=test_admin_headers)
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    response = client.delete(f"/api/v1/users/{user_id}", headers=test_admin_headers)
    assert response.status_code == 403


def test_delete_user_not_found(client, test_admin_headers):
    """Test deleting a user that does not exist."""
    user_id = uuid.uuid4()
    response = client.delete(f"/api/v1/users/{user_id}", headers=test_admin_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
