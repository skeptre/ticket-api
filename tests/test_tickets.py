def test_get_tickets_empty(client, auth_headers):
    """Test getting tickets when none exist."""
    response = client.get("/tickets/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_create_ticket(client, auth_headers):
    """Test creating a new ticket."""
    response = client.post(
        "/tickets/",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "priority": "high",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["description"] == "This is a test ticket"
    assert data["priority"] == "high"
    assert data["status"] == "open"


def test_create_ticket_unauthorized(client):
    """Test creating ticket without auth fails."""
    response = client.post(
        "/tickets/",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "priority": "high",
        },
    )
    assert response.status_code == 401


def test_get_ticket_by_id(client, auth_headers):
    """Test getting a specific ticket by ID."""
    # First create a ticket
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "priority": "medium",
        },
        headers=auth_headers,
    )
    ticket_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/tickets/{ticket_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == "Test Ticket"


def test_get_ticket_not_found(client, auth_headers):
    """Test getting nonexistent ticket returns 404."""
    response = client.get("/tickets/999", headers=auth_headers)
    assert response.status_code == 404


def test_update_ticket(client, auth_headers):
    """Test updating a ticket."""
    # Create a ticket
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Original Title",
            "description": "Original description",
            "priority": "low",
        },
        headers=auth_headers,
    )
    ticket_id = create_response.json()["id"]

    # Update the ticket
    response = client.put(
        f"/tickets/{ticket_id}",
        json={"title": "Updated Title", "status": "in_progress"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"


def test_delete_ticket(client, auth_headers):
    """Test deleting a ticket."""
    # Create a ticket
    create_response = client.post(
        "/tickets/",
        json={
            "title": "To Delete",
            "description": "This will be deleted",
            "priority": "low",
        },
        headers=auth_headers,
    )
    ticket_id = create_response.json()["id"]

    # Delete the ticket
    response = client.delete(f"/tickets/{ticket_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/tickets/{ticket_id}", headers=auth_headers)
    assert get_response.status_code == 404
